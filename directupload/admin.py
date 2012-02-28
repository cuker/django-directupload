from django.db import models
from django.contrib.admin import ModelAdmin

from widgets import UploadifyClearableFileInput

class UploadifyAdminMixin(object):
    def formfield_for_dbfield(self, db_field, **kwargs):
        if isinstance(db_field, models.FileField):
            return self.formfield_for_file_field(db_field, kwargs.pop('request', None), **kwargs)
        return ModelAdmin.formfield_for_dbfield(self, db_field, **kwargs)
    
    def formfield_for_file_field(self, db_field, request=None, **kwargs):
        """
        Get a form Field that is prepared for uploadify
        """
        kwargs['widget'] = UploadifyClearableFileInput(db_field=db_field)
        return db_field.formfield(**kwargs)

def patch_admin():
    from django.contrib.admin.options import FORMFIELD_FOR_DBFIELD_DEFAULTS
    FORMFIELD_FOR_DBFIELD_DEFAULTS[models.ImageField] = {'widget': UploadifyClearableFileInput}
    FORMFIELD_FOR_DBFIELD_DEFAULTS[models.FileField] = {'widget': UploadifyClearableFileInput}

