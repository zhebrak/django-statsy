# coding: utf-8

import json

from django.http import HttpResponse

import statsy


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
