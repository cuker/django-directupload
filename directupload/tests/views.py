from django.test import TestCase
from django.test.client import RequestFactory
from django.utils import simplejson as json
from django.core.files.base import ContentFile

from directupload import views
from directupload.backends import get_directupload_backend

class UploadViewsTestCase(TestCase):
    #TODO this becomes a backend dependent test case
    def setUp(self):
        self.request_factory = RequestFactory()
    
    def get_backend(self):
        backend = get_directupload_backend()
        return backend
    
    def assertDetermineNameResponse(self, response):
        self.assertEqual(response.status_code, 200)
        json_data = json.loads(response.content)
        self.assertTrue('targetpath' in json_data)
        self.assertTrue('targetname' in json_data)
        return json_data
    
    def assertUploadOptionsResponse(self, response):
        self.assertEqual(response.status_code, 200)
        json_data = json.loads(response.content)
        return json_data
    
    def test_determine_name(self):
        data = {'upload_to':'/images/',
                'filename':'somefile.png',}
        request = self.request_factory.post('/', data)
        response = views.determine_name(request)
        json_data = self.assertDetermineNameResponse(response)
        print json_data
    
    def test_determine_name_handles_date_paths(self):
        data = {'upload_to':'/images/%Y/%m/%d/',
                'filename':'somefile.png',}
        request = self.request_factory.post('/', data)
        response = views.determine_name(request)
        json_data = self.assertDetermineNameResponse(response)
    
    def test_upload_file(self):
        data = {'targetpath':'foo/somefile.png',}
        files = {'file':open(__file__, 'r'),} #This is django being inconsistent, ContentFile should be accepted!
        
        backend = self.get_backend()
        backend(request=self.request_factory.get('/'), options={'folder':'foo'}).update_post_params(data)
        assert 'payload' in data
        
        data.update(files)
        request = self.request_factory.post('/', data=data)#, content_type='multipart/form-data')
        response = views.upload_file(request)
        self.assertEqual(response.status_code, 200)
    
    def test_upload_options_view(self):
        request = self.request_factory.get('/')
        response = views.upload_options_view(request)
        json_data = self.assertUploadOptionsResponse(response)

