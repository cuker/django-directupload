from django.forms.widgets import FileInput, ClearableFileInput
from django.core.files.storage import default_storage
from django.db.models.fields.files import FileField
from django.conf import settings

class UploadifyInputMixin(object):
    db_field = None
    
    class Media: #this does not work for the admin as django ignores it [WTF]
        css = {'all': ('uploadify/uploadify.css',)}
        if settings.DEBUG:
            js = ('uploadify/jquery.uploadify.js', 'uploadify/widget.js')
        else:
            js = ('uploadify/jquery.uploadify.min.js', 'uploadify/widget.js')
    
    def get_file_field(self):
        if self.db_field:
            return self.db_field
        return FileField(upload_to='', storage=default_storage)
    
    def value_from_datadict(self, data, files, name):
        "File widgets take data from FILES, not POST"
        if name in data:
            file_path = data[name]
            file_field = self.get_file_field()
            file_obj = file_field.storage.open(file_path)
            file_copy = file_field.attr_class(None, file_field, file_path)
            file_copy.file = file_obj
            file_copy._committed = True
            return file_copy
        return None
    
    def prepare_attrs(self, attrs):
        attrs = attrs or {}
        file_field = self.get_file_field()
        attrs['class'] = 'uploadifyinput'
        attrs['data-upload-to'] = file_field.upload_to
        return attrs

class UploadifyFileInput(UploadifyInputMixin, FileInput):
    def __init__(self, *args, **kwargs):
        self.db_field = kwargs.pop('db_field', None)
        FileInput.__init__(self, *args, **kwargs)
    
    def value_from_datadict(self, data, files, name):
        file_obj = UploadifyInputMixin.value_from_datadict(self, data, files, name)
        if file_obj:
            return file_obj
        return super(UploadifyFileInput, self).value_from_datadict(data, files, name)
    
    def render(self, name, value, attrs=None):
        attrs = self.prepare_attrs(attrs)
        return super(UploadifyFileInput, self).render(name, value, attrs)

class UploadifyClearableFileInput(UploadifyInputMixin, ClearableFileInput):
    def __init__(self, *args, **kwargs):
        self.db_field = kwargs.pop('db_field', None)
        ClearableFileInput.__init__(self, *args, **kwargs)
    
    def value_from_datadict(self, data, files, name):
        file_obj = UploadifyInputMixin.value_from_datadict(self, data, files, name)
        if file_obj:
            return file_obj
        return super(UploadifyClearableFileInput, self).value_from_datadict(data, files, name)
    
    def render(self, name, value, attrs=None):
        attrs = self.prepare_attrs(attrs)
        return super(UploadifyClearableFileInput, self).render(name, value, attrs)

