# coding: utf-8

import json

from datetime import datetime, timedelta


from django.http import HttpResponse
from django.shortcuts import render_to_response

import statsy


def dashboard(request):
    result = {
        'groups': statsy.groups.all(),
        'events': statsy.events.all(),

        'last_stats': get_last_stats(),
        'today_count': statsy.objects.today().count()

    }

    return render_to_response('statsy/dashboard.html', result)


def custom(request):
    result = {
        'url_map': statsy.site.url_map
    }

    return render_to_response('statsy/custom.html', result)


def get_last_stats(limit=10):
    return statsy.objects.select_related('group', 'event')[:limit]


def today(request):
    return HttpResponse(json.dumps(statsy.objects.today().get_stats()), content_type='application/json')
#
#
# def get_week_category_stats(request, category):
#     now = datetime.today()
#     monday = now - timedelta(days=now.weekday())
#     start = monday.replace(hour=0, minute=0, second=0, microsecond=0)
#     aggregation_period = 90  # 90 minutes
#
#     stats = get_aggregated_stats_for_the_period(
#         category=category, start=start, aggregation_period=aggregation_period
#     )
#
#     return HttpResponse(json.dumps(stats), content_type='application/json')
#
#
# def get_month_category_stats(request, category):
#     now = datetime.today()
#     start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
#     aggregation_period = 6 * 60  # 6 hours
#
#     stats = get_aggregated_stats_for_the_period(
#         category=category, start=start, aggregation_period=aggregation_period
#     )
#
#     return HttpResponse(json.dumps(stats), content_type='application/json')



