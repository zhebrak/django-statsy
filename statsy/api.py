# coding: utf-8

import json

from django.http import HttpResponse
from django.views.decorators.http import require_POST

import statsy


@require_POST
def send(request):
    send_params = set(statsy.get_send_params())
    kwargs = {
        arg: value
        for arg, value in request.POST.items()
        if arg in send_params
    }

    if 'value' in kwargs and request.POST.get('value_type', 'string') == 'number':
        kwargs['value'] = float(kwargs['value'])

    if 'user' not in kwargs and 'user_id' not in kwargs and request.user.is_authenticated():
        kwargs['user'] = request.user

    statsy.send(**kwargs)
    result = {
        'response': 'OK'
    }

    return HttpResponse(json.dumps(result), content_type='application/json')
