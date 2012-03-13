from django import template
from django.db import models
from django.db.models.fields import FieldDoesNotExist

import copy

register = template.Library()

from classytags.core import Options
from classytags.helpers import InclusionTag
from classytags.arguments import Argument, KeywordArgument

from directupload.widgets import DirectUploadClearableFileInput

@register.inclusion_tag('directupload/templatetags/head.html')
def directupload_head():
    return {
        'media': DirectUploadClearableFileInput().media,
    }

class RenderDirectUploadField(InclusionTag):
    name = 'render_upload_field'
    template = 'directupload/templatetags/render_file_widget.html'
    options = Options(
        Argument('field', resolve=True),
        KeywordArgument('model', resolve=True, required=False),
        KeywordArgument('model_field', resolve=True, required=False),
    )
    
    def get_context(self, context, field, model, model_field):
        model = model.get('model', None)
        model_field = model_field.get('model_field', None)
        if not model_field and model:
            model_field = model._meta.get_field(field.name)
        if not model_field:
            pass
        widget = DirectUploadClearableFileInput(db_field=model_field)
        field.field = copy.copy(field.field) #looks weird but field is actually a bound field
        field.field.widget = widget
        return {'widget': widget, 'field':field}

register.tag(RenderDirectUploadField)

def is_file_field(field, model):
    #field|is_file_field:line.model_admin.model
    try:
        model_field = model._meta.get_field(field.name)
    except FieldDoesNotExist:
        return False
    return isinstance(model_field, models.FileField) or hasattr(model_field, 'upload_to')

register.filter('is_file_field', is_file_field)

