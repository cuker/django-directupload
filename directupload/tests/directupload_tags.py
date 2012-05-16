from django.test import TestCase
from django import forms

from django.db import models

class TestModel(models.Model):
    char_field = models.CharField(max_length=20)
    file_field = models.FileField(upload_to='folder')

class TestForm(forms.ModelForm):
    class Meta:
        model = TestModel


class DirectUploadTagsTestCase(TestCase):
    def test_is_file_field(self):
        from directupload.templatetags.directupload_tags import is_file_field
        form = TestForm()
        self.assertTrue(is_file_field(form['file_field'], TestModel))
        self.assertFalse(is_file_field(form['char_field'], TestModel))

