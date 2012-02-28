from base import BaseUploadifyBackend

import datetime
from urllib import urlencode

from django.middleware.csrf import get_token
from django.core.urlresolvers import reverse

from utils import Signer
signer = Signer()

def sign(value):
    return signer.sign(value)

def unsign(value):
    return signer.unsign(value)

class DjangoViewBackend(BaseUploadifyBackend):
    """Uploadify for using the builtin django view"""
    
    def get_uploader(self):
        return reverse('uploadify-upload-file')
    
    def build_post_data(self):
        data = {'upload_to': self.options['folder'],
                'request_time': datetime.datetime.now().isoformat(),
                '_request_id': 'foo',} #TODO salt}
        signed_data = sign(urlencode(data))
        self.post_data['payload'] = signed_data
        self.post_data['csrfmiddlewaretoken'] = get_token(self.request)

