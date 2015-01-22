# coding: utf-8

from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render_to_response

from statsy import statsy


def send(request):
    kwargs = {arg: request.POST.get(arg) for arg in statsy.get_send_params()}
    statsy.send(**kwargs)

    return HttpResponse()


# Graphs


def dashboard(request):
    result = {
        'groups': statsy.groups.all(),
        'events': statsy.events.all(),

        'today_group_stats': get_aggregated_today_stats('group'),
        'today_event_stats': get_aggregated_today_stats('event')
    }

    return render_to_response('statsy/dashboard.html', result)


def get_aggregated_today_stats(category):
    day_stats_aggregate_by = 10

    today_stats = statsy.objects.today().select_related(category)\
        .extra({"time": "strftime('%H:%M', created_at)"})\
        .values(category + '__name', 'time').annotate(count=Count(category + '_id'))

    aggregated_stats = dict()
    for data in today_stats:
        name = data[category + '__name']
        if name not in aggregated_stats:
            aggregated_stats[name] = dict()

        aggregated_time = get_aggregated_time(data['time'], day_stats_aggregate_by)
        if aggregated_time not in aggregated_stats[name]:
            aggregated_stats[name][aggregated_time] = 0

        aggregated_stats[name][aggregated_time] += data['count']

    return aggregated_stats


def get_aggregated_time(time_string, aggregate_by):
    hours, minutes = time_string.split(':')
    aggregated_minutes = str(int(minutes) - (int(minutes) % aggregate_by))
    aggregated_minutes = (aggregated_minutes + '0')[:2]  # hour:00 fix

    return ':'.join([hours, aggregated_minutes])


def user(request):
    pass


def group(request):
    pass


def event(request):
    pass


def tracking(request):
    pass

