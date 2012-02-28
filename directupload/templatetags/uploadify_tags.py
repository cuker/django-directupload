from django import template
from django.db import models

import copy

register = template.Library()

from classytags.core import Options
from classytags.helpers import InclusionTag
from classytags.arguments import Argument, KeywordArgument

from directupload.widgets import UploadifyClearableFileInput

@register.inclusion_tag('uploadify/templatetags/head.html')
def uploadify_head():
    return {
        'media': UploadifyClearableFileInput().media,
    }

class RenderUploadifyField(InclusionTag):
    name = 'render_uploadify_field'
    template = 'uploadify/templatetags/render_uploadify_widget.html'
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
        widget = UploadifyClearableFileInput(db_field=model_field)
        field.field = copy.copy(field.field) #looks weird but field is actually a bound field
        field.field.widget = widget
        return {'widget': widget, 'field':field}

register.tag(RenderUploadifyField)

def is_file_field(field, model):
    #field|is_file_field:line.model_admin.model
    model_field = model._meta.get_field(field.name)
    return isinstance(model_field, models.FileField)

register.filter('is_file_field', is_file_field)

