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

    statsy.send(**kwargs)
    result = {
        'response': 'OK'
    }

    return HttpResponse(json.dumps(result), content_type='application/json')
