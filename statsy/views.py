# coding: utf-8

import json

from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404

import statsy


def send(request):
    kwargs = {
        arg: request.POST.get(arg)
        for arg in statsy.get_send_params()
    }

    statsy.send(**kwargs)

    return HttpResponse()


# Graphs


def dashboard(request):
    result = {
        'groups': statsy.groups.all(),
        'events': statsy.events.all(),
    }

    return render_to_response('statsy/dashboard.html', result)


def get_today_group_stats(request):
    stats = get_aggregated_today_stats('group')
    return HttpResponse(json.dumps(stats), content_type='application/json')


def get_today_event_stats(request):
    stats = get_aggregated_today_stats('event')
    return HttpResponse(json.dumps(stats), content_type='application/json')


def get_aggregated_today_stats(category, aggregation_time=15):
    today_stats = statsy.objects.today().select_related(category)\
        .extra({"time": "strftime('%H:%M', created_at)"})\
        .values(category + '__name', 'time').annotate(count=Count(category + '_id'))

    aggregated_stats = dict()
    for data in today_stats:
        name = data[category + '__name']
        if name not in aggregated_stats:
            aggregated_stats[name] = dict()

        aggregated_time = get_aggregated_time(data['time'], aggregation_time)
        if aggregated_time not in aggregated_stats[name]:
            aggregated_stats[name][aggregated_time] = 0

        aggregated_stats[name][aggregated_time] += data['count']

    aggregated_periods = [
        get_aggregated_time('{0}:{1}'.format(hour, minute), aggregation_time)
        for hour in range(0, 24) for minute in range(0, 59, aggregation_time)
    ]
    for category, data in aggregated_stats.items():
        for period in aggregated_periods:
            if period not in data:
                data[period] = 0

        aggregated_stats[category] = sorted(data.items())

    return aggregated_stats


def get_aggregated_time(time_string, aggregate_by):
    hours, minutes = time_string.split(':')

    aggregated_minutes = str(int(minutes) - (int(minutes) % aggregate_by))
    aggregated_minutes = (aggregated_minutes + '0')[:2]  # hour:00 fix
    hours = ('0' + hours)[-2:]

    return u':'.join([hours, aggregated_minutes])


def group_list(request):
    return render_to_response('statsy/group_list.html', {})


def group(request, group_name):
    group_object = get_object_or_404(statsy.groups.all(), name=group_name)
    return render_to_response('statsy/group.html', {'group': group_object})


def event_list(request):
    return render_to_response('statsy/event_list.html', {})


def event(request, event_name):
    event_object = get_object_or_404(statsy.events.all(), name=event_name)
    return render_to_response('statsy/event.html', {'event': event_object})


def user(request):
    return render_to_response('statsy/dashboard.html', {})


def tracking(request):
    return render_to_response('statsy/dashboard.html', {})

