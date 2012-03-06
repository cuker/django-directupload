from django.conf import settings
from django.core.urlresolvers import reverse

from django.utils import simplejson as json

class BaseUploadBackend(object):
    def __init__(self, request, options={}, post_data={}):
        self.request = request
        self.options = getattr(settings, 'DEFAULT_DIRECTUPLOAD_OPTIONS', {})
        self.options.update(options)
        
        _set_default_if_none(self.options, 'url', self.get_target_url())
        _set_default_if_none(self.options, 'determineName', self.get_determine_name())
        
        self.build_options()
        self.post_data = post_data
    
    def get_determine_name(self):
        return reverse('directupload-determine-name')
    
    def get_target_url(self):
        pass
    
    def build_options(self):
        pass
    
    def build_post_data(self):
        pass
    
    def get_options_json(self):
        #self.options['postData'] = self.post_data
        subs = []
        out = json.dumps(self.options)
        
        for search, replace in subs:
            out = out.replace(search, replace)
            
        return out
    
    def update_post_params(self, params):
        self.build_post_data()
        params.update(self.post_data)

def _set_default_if_none(dict, key, default=None):
    if key not in dict:
        dict[key] = default

