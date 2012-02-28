from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from urllib import quote_plus
from datetime import datetime
from datetime import timedelta
import base64
import hmac
import hashlib
import os

from base import BaseUploadifyBackend, _set_default_if_none, json

# AWS Options
ACCESS_KEY_ID       = getattr(settings, 'AWS_ACCESS_KEY_ID', None)
SECRET_ACCESS_KEY   = getattr(settings, 'AWS_SECRET_ACCESS_KEY', None)
BUCKET_NAME         = getattr(settings, 'AWS_BUCKET_NAME', None)
SECURE_URLS         = getattr(settings, 'AWS_S3_SECURE_URLS', False)
BUCKET_URL          = getattr(settings, 'AWS_BUCKET_URL', ('https://' if SECURE_URLS else 'http://') + BUCKET_NAME + '.s3.amazonaws.com')
DEFAULT_ACL         = getattr(settings, 'AWS_DEFAULT_ACL', 'public-read')
DEFAULT_KEY_PATTERN = getattr(settings, 'AWS_DEFAULT_KEY_PATTERN', '${targetname}')
DEFAULT_FORM_TIME   = getattr(settings, 'AWS_DEFAULT_FORM_LIFETIME', 36000) # 10 HOURS


class S3UploadifyBackend(BaseUploadifyBackend):
    """Uploadify for Amazon S3"""
    
    def __init__(self, request, uploadify_options={}, post_data={}, conditions={}):
        self.conditions = conditions
        super(S3UploadifyBackend, self).__init__(request, uploadify_options, post_data)
    
    def get_uploader(self):
        return BUCKET_URL
    
    def build_post_data(self):
        self.options['fileObjName'] = 'file' #S3 requires this be the field name
        
        if 'folder' in self.options:
            key = os.path.join(self.options['folder'], DEFAULT_KEY_PATTERN)
        else:
            key = DEFAULT_KEY_PATTERN
        #_set_default_if_none(self.post_data, 'key', key) #this is set by update_post_params
        _set_default_if_none(self.post_data, 'acl', DEFAULT_ACL)
        
        try:
            _set_default_if_none(self.post_data, 'bucket', BUCKET_NAME)
        except ValueError:
            raise ImproperlyConfigured("Bucket name is a required property.")
 
        try:
            _set_default_if_none(self.post_data, 'AWSAccessKeyId', ACCESS_KEY_ID)
        except ValueError:
            raise ImproperlyConfigured("AWS Access Key ID is a required property.")

        self.conditions = self.build_conditions()

        if not SECRET_ACCESS_KEY:
            raise ImproperlyConfigured("AWS Secret Access Key is a required property.")
        
        expiration_time = datetime.utcnow() + timedelta(seconds=DEFAULT_FORM_TIME)
        self.policy_string = self.build_post_policy(expiration_time)
        self.policy = base64.b64encode(self.policy_string)
         
        self.signature = base64.encodestring(hmac.new(SECRET_ACCESS_KEY, self.policy, hashlib.sha1).digest()).strip()
        
        self.post_data['policy'] = self.policy
        self.post_data['signature'] = self.signature
    
    def build_conditions(self):
        conditions = list()
        
        #make s3 happy with uploadify
        #conditions.append(['starts-with', '$folder', '']) #no longer passed by uploadify
        conditions.append(['starts-with', '$filename', ''])
        conditions.append(['starts-with', '$targetname', '']) #variable introduced by this package
        conditions.append(['starts-with', '$targetpath', self.options['folder']])
        #conditions.append({'success_action_status': '200'})
        
        #real conditions
        conditions.append(['starts-with', '$key', self.options['folder']])
        conditions.append({'bucket': self.post_data['bucket']})
        conditions.append({'acl': self.post_data['acl']})
        return conditions
    
    def build_post_policy(self, expiration_time):
        policy = {'expiration': expiration_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
                  'conditions': self.conditions,}
        return json.dumps(policy)
    
    def update_post_params(self, params):
        #instruct s3 that our key is the targetpath
        params['key'] = params['targetpath']

def _uri_encode(str):
    try:
        # The Uploadify flash component apparently decodes the scriptData once, so we need to encode twice here.
        return quote_plus(quote_plus(str, safe='~'), safe='~')
    except:
        raise ValueError

