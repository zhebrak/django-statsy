# coding: utf-8

import json

from datetime import datetime

from django.conf import settings
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render_to_response

import statsy


def dashboard(request):
    result = {
        'groups': statsy.groups.all(),
        'events': statsy.events.all(),
        'last_stats': get_last_stats()
    }

    return render_to_response('statsy/dashboard.html', result)


def custom(request):
    result = {
        'url_map': statsy.site.url_map
    }

    return render_to_response('statsy/custom.html', result)


def get_last_stats(limit=10):
    return statsy.objects.select_related('group', 'event').order_by('-created_at')[:limit]


def get_today_group_stats(request):
    stats = get_aggregated_today_stats('group')
    return HttpResponse(json.dumps(stats), content_type='application/json')


def get_today_event_stats(request):
    stats = get_aggregated_today_stats('event')
    return HttpResponse(json.dumps(stats), content_type='application/json')


def get_aggregated_today_stats(category, aggregation_period=15):
    time_extract_sqlite = "strftime('%H:%M', created_at)"
    time_extract_mysql = "DATE_FORMAT(created_at, '%%H:%%i')"

    time_extract = time_extract_mysql
    if settings.DATABASES['default']['ENGINE'] == 'django.db.backends.sqlite3':
        time_extract = time_extract_sqlite

    today_stats = statsy.objects.today().select_related(category)\
        .extra({"time": time_extract})\
        .values(category + '__name', 'time').annotate(count=Count(category + '_id'))

    aggregated_stats = dict()
    for data in today_stats:
        name = data[category + '__name']
        if name not in aggregated_stats:
            aggregated_stats[name] = dict()

        aggregated_time = get_aggregated_time(data['time'], aggregation_period)
        if aggregated_time not in aggregated_stats[name]:
            aggregated_stats[name][aggregated_time] = 0

        aggregated_stats[name][aggregated_time] += data['count']

    aggregated_periods = [
        get_aggregated_time(
            '{0}:{1}'.format(hour, minute),
            aggregation_period
        )
        for hour in range(0, 24)
        for minute in range(0, 59, aggregation_period)
    ]

    now = datetime.now()
    last_period = get_aggregated_time(
        '{0}:{1}'.format(now.hour, now.minute),
        aggregation_period
    )

    for category, data in aggregated_stats.items():
        for period in aggregated_periods:
            if period > last_period:
                data[period] = None

            elif period not in data:
                data[period] = 0

        aggregated_stats[category] = sorted(data.items())

    return aggregated_stats


def get_aggregated_time(time_string, aggregate_by):
    hours, minutes = time_string.split(':')

    aggregated_minutes = str(int(minutes) - (int(minutes) % aggregate_by))
    aggregated_minutes = (aggregated_minutes + '0')[:2]  # hour:00 fix
    hours = ('0' + hours)[-2:]

    return ':'.join([hours, aggregated_minutes])
