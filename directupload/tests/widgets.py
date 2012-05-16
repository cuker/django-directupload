from django.test import TestCase
from django import forms
from django.db import models
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

from directupload import widgets

class TestModel(models.Model):
    char_field = models.CharField(max_length=20)
    file_field = models.FileField(upload_to='folder')

class TestForm(forms.ModelForm):
    class Meta:
        model = TestModel


class DirectUploadWidgetsTestCase(TestCase):
    def setUp(self):
        self.file_path = 'folder/somefile.txt'
        if default_storage.exists(self.file_path):
            default_storage.delete(self.file_path)
        default_storage.save(self.file_path, ContentFile('new content'))
    
    def test_input_mixin_detects_uploaded_file(self):
        widget = widgets.DirectUploadInputMixin()
        data = {'file_field':self.file_path,
                'char_field':'sometext',}
        files = {}
        name = 'file_field'
        file_obj = widget.value_from_datadict(data, files, name)
        self.assertTrue(file_obj is not None)
        self.assertTrue(file_obj.path.endswith(data['file_field']))
    
    def test_input_mixin_prepare_attrs(self):
        widget = widgets.DirectUploadInputMixin()
        attrs = widget.prepare_attrs(attrs=None)
        self.assertEqual(attrs.get('class'), 'directupload')

