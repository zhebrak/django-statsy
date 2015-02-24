# coding: utf-8

import json

from datetime import datetime, timedelta

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
    return statsy.objects.select_related('group', 'event')[:limit]


def get_today_category_stats(request, category):
    now = datetime.today()
    start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    aggregation_period = 15  # 15 minutes

    stats = get_aggregated_stats_for_the_period(
        category=category, start=start, aggregation_period=aggregation_period
    )

    return HttpResponse(json.dumps(stats), content_type='application/json')


def get_week_category_stats(request, category):
    now = datetime.today()
    monday = now - timedelta(days=now.weekday())
    start = monday.replace(hour=0, minute=0, second=0, microsecond=0)
    aggregation_period = 90  # 90 minutes

    stats = get_aggregated_stats_for_the_period(
        category=category, start=start, aggregation_period=aggregation_period
    )

    return HttpResponse(json.dumps(stats), content_type='application/json')


def get_month_category_stats(request, category):
    now = datetime.today()
    start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    aggregation_period = 6 * 60  # 6 hours

    stats = get_aggregated_stats_for_the_period(
        category=category, start=start, aggregation_period=aggregation_period
    )

    return HttpResponse(json.dumps(stats), content_type='application/json')


def get_aggregated_stats_for_the_period(category, start, end=None, aggregation_period=15, average_by=15):
    time_extract_sqlite = "strftime('%d:%H:%M', created_at)"
    time_extract_mysql = "DATE_FORMAT(created_at, '%%e:%%H:%%i')"

    time_extract = time_extract_mysql
    if settings.DATABASES['default']['ENGINE'] == 'django.db.backends.sqlite3':
        time_extract = time_extract_sqlite

    stats = statsy.objects.by_time(start=start, end=end).select_related(category)\
        .extra({"time": time_extract})\
        .values(category + '__name', 'time').annotate(count=Count(category + '_id'))

    aggregated_stats = dict()
    for data in stats:
        name = data[category + '__name']
        if name not in aggregated_stats:
            aggregated_stats[name] = dict()

        aggregated_time = get_aggregated_time(data['time'], aggregation_period)

        if aggregated_time not in aggregated_stats[name]:
            aggregated_stats[name][aggregated_time] = 0

        aggregated_stats[name][aggregated_time] += data['count']

    now = datetime.now()

    aggregated_periods = [
        get_aggregated_time(
            '{0}:{1}:{2}'.format(day, minute / 60, minute % 60),
            aggregation_period
        )
        for day in range(start.day, now.day + 1)
        for minute in range(0, 60 * 24, aggregation_period)
    ]

    last_period = get_aggregated_time(
        '{0}:{1}:{2}'.format(now.day, now.hour, now.minute),
        aggregation_period
    )

    for category, data in aggregated_stats.items():
        consecutive_null_periods = []
        for period in aggregated_periods:
            if period >= last_period:
                data[period] = None

            elif period not in data:
                consecutive_null_periods.append(period)
                if len(consecutive_null_periods) == 10:
                    for null_period in consecutive_null_periods:
                        data[null_period] = None

                    consecutive_null_periods = []

                else:
                    data[period] = 0

            else:
                consecutive_null_periods = []
                data[period] /= float(aggregation_period) / average_by

        aggregated_stats[category] = sorted(data.items())

    return aggregated_stats


def get_aggregated_time(time_string, aggregate_by):
    day, hours, minutes = time_string.split(':')
    aggregated_minutes = int(float(hours) * 60 + float(minutes)) / aggregate_by

    day = ('0' + day)[-2:]
    hours = ('0' + str(aggregated_minutes * aggregate_by / 60))[-2:]
    minutes = ('0' + str((aggregated_minutes * aggregate_by) % 60))[-2:]

    return ':'.join([day, hours, minutes])

