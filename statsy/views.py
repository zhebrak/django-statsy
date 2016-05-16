# coding: utf-8

import json


from django.http import HttpResponse
from django.shortcuts import render_to_response

import statsy


def dashboard(request):
    result = {
        'groups': statsy.groups.all(),
        'last_stats': get_last_stats(),
        'today_count': statsy.objects.today().count()
    }

    return render_to_response('statsy/dashboard.html', result)


def get_last_stats(limit=10):
    return statsy.objects.select_related('group', 'event')[:limit]


def today(request):
    return HttpResponse(json.dumps(statsy.objects.today().get_stats()), content_type='application/json')


def custom(request):
    result = {
        'url_map': statsy.site.url_map
    }

    return render_to_response('statsy/custom.html', result)
