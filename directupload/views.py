from django.http import HttpResponse, HttpResponseBadRequest
from django.core.files.storage import default_storage
from django.views.decorators.csrf import csrf_exempt
from django.utils import simplejson as json
from django.utils.encoding import force_unicode, smart_str

from directupload.backends import get_directupload_backend

from urlparse import parse_qsl
import os
import datetime

def upload_options_view(request):
    backend = get_directupload_backend()
    data = backend(request=request).get_options_json()
    return HttpResponse(data)

@csrf_exempt
def upload_file(request):
    #this is handled by a different session then the user's browser, hence csrf exempt
    if not request.POST:
        return HttpResponseBadRequest()
    from directupload.backends.djangoview import unsign
    data = dict(parse_qsl(unsign(request.POST['payload'])))
    assert data['request_time'] #TODO respect some expiration
    path = request.POST['targetpath']
    file_path = default_storage.save(path, request.FILES['file']) #TODO how to tell the storage engine not to rename?
    return HttpResponse(file_path)

def determine_name(request):
    if not request.POST:
        return HttpResponseBadRequest()
    
    upload_to = request.POST['upload_to']
    upload_to = os.path.normpath(force_unicode(datetime.datetime.now().strftime(smart_str(upload_to))))
    
    desired_path = os.path.join(upload_to, request.POST['filename'])
    if desired_path.startswith('/'):
        desired_path = desired_path[1:]
    path = default_storage.get_available_name(desired_path)
    folder = os.path.split(desired_path)[0]
    
    data = {'targetpath':path,
            'targetname':os.path.split(path)[-1],}
    backend = get_directupload_backend()
    backend(request=request, options={'folder':folder}).update_post_params(data)
    return HttpResponse(json.dumps(data))

