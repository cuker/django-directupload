from django.http import HttpResponse, HttpResponseBadRequest
from django.core.files.storage import default_storage
from django.views.decorators.csrf import csrf_exempt
from django.utils import simplejson as json

from directupload.backends import get_uploadify_backend

from urlparse import parse_qsl
import os

def uploadify_options_view(request):
    if not request.POST:
        return HttpResponseBadRequest()
    uploadify_options = {}
    if 'upload_to' in request.POST:
        uploadify_options['folder'] = request.POST['upload_to']
    backend = get_uploadify_backend()
    data = backend(request=request, 
                   uploadify_options=uploadify_options).get_options_json()
    return HttpResponse(data)

@csrf_exempt
def upload_file(request):
    #this is handled by a different session then the user's browser, hence csrf exempt
    if not request.POST:
        return HttpResponseBadRequest()
    from directupload.backends.djangoview import unsign
    data = dict(parse_qsl(unsign(request.POST['payload'])))
    assert data['request_time'] #TODO respect some expiration
    path = request.POST.get('targetpath', os.path.join(data['upload_to'], request.POST['Filename']))
    file_path = default_storage.save(path, request.FILES['Filedata']) #TODO how to tell the storage engine not to rename?
    return HttpResponse(file_path)

def determine_name(request):
    if not request.POST:
        return HttpResponseBadRequest()
    desired_path = os.path.join(request.POST['upload_to'], request.POST['filename'])
    path = default_storage.get_available_name(desired_path)
    data = {'targetpath':path,
            'targetname':os.path.split(path)[-1],}
    backend = get_uploadify_backend()
    backend(request=request, uploadify_options={'folder':request.POST['upload_to']}).update_post_params(data)
    return HttpResponse(json.dumps(data))

