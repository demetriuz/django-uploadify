from django.dispatch import Signal
from django.http import Http404
from django.views.decorators.csrf import csrf_exempt

from misc.json_encode import json_response
from misc.utils import user_from_session_key

upload_received = Signal(providing_args=['request', 'data'])

@csrf_exempt
def upload(request, *args, **kwargs):
    if request.method != 'POST':
        raise Http404
    if 'sessionid' not in request.POST:
        raise Http404
    request.user = user_from_session_key(request.POST['sessionid'])
    if not request.user.is_authenticated():
        raise Http404
    sender = request.POST.get('sender', 'uploadify')
    filename = request.POST.get('fileObjName', 'Filename')
    if request.FILES:
        received_list = upload_received.send(sender=sender, request=request,
            data=request.FILES[filename])
        for received, response in received_list:
            if response is not None:
                if isinstance(response, (dict, list)):
                    return json_response(response)
                else:
                    return response
    raise Http404
