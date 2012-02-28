from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.urlresolvers import reverse

from django.utils import simplejson as json

from common import UPLOADIFY_OPTIONS, UPLOADIFY_METHODS, DEFAULT_CANCELIMG, DEFAULT_UPLOADER, BUTTON_TEXT

class BaseUploadifyBackend(object):
    def __init__(self, request, uploadify_options={}, post_data={}):
        self.request = request
        self.options = getattr(settings, 'UPLOADIFY_DEFAULT_OPTIONS', {})
        self.options.update(uploadify_options)
        
        if any(True for key in self.options if key not in UPLOADIFY_OPTIONS + UPLOADIFY_METHODS):
            raise ImproperlyConfigured("Attempted to initialize with unrecognized option '%s'." % key)
        
        _set_default_if_none(self.options, 'cancelImage', DEFAULT_CANCELIMG)
        _set_default_if_none(self.options, 'swf', DEFAULT_UPLOADER)
        _set_default_if_none(self.options, 'uploader', self.get_uploader())
        _set_default_if_none(self.options, 'buttonText', BUTTON_TEXT)
        _set_default_if_none(self.options, 'checkExisting', self.get_check_existing())
        _set_default_if_none(self.options, 'determineName', self.get_determine_name())
        
        self.post_data = post_data
        self.build_post_data()
    
    def get_check_existing(self):
        return False
    
    def get_determine_name(self):
        return reverse('uploadify-determine-name')
    
    def get_uploader(self):
        pass
    
    def build_post_data(self):
        pass
    
    def update_post_params(self, params):
        pass
    
    def get_options_json(self):
        self.options['postData'] = self.post_data
        subs = []
        for key in self.options:
            if key in UPLOADIFY_METHODS:
                subs.append(('"%%%s%%"' % key, self.options[key]))
                self.options[key] = "%%%s%%" % key
                
        out = json.dumps(self.options)
        
        for search, replace in subs:
            out = out.replace(search, replace)
            
        return out

def _set_default_if_none(dict, key, default=None):
    if key not in dict:
        dict[key] = default

