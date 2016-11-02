# coding: utf-8

from datetime import datetime, timedelta
import json

from django.http import HttpResponse
from django.shortcuts import render_to_response

import statsy


def dashboard(request):
    result = {
        'groups': statsy.groups.all(),
        'today_count': statsy.objects.today().count()
    }

    return render_to_response('statsy/dashboard.html', result)


def get_stats(request):
    start, end = request.GET.get('start'), request.GET.get('end')
    date_format = '%d/%m/%y'
    start, end = datetime.strptime(start, date_format), datetime.strptime(end, date_format)

    stats = statsy.objects.by_time(start, end + timedelta(days=1))

    category_count = {}
    for category in ['group', 'event']:
        category_list = request.GET.getlist('{}s[]'.format(category))
        category_count[category] = category_list

        if category_list:
            category_id_list = getattr(statsy, category + 's').filter(
                name__in=category_list
            ).values_list('pk', flat=True)
            stats = stats.filter(**{
                '{}_id__in'.format(category): category_id_list
            })

    events = []
    if len(category_count['group']) == len(category_count['event']) == 1:
        stats = [{
            'data': stats.get_stats(),
            'name': '{}:{}'.format(category_count['group'][0], category_count['event'][0])
        }]
        events = [category_count['event'][0]]

    else:
        category_pairs = stats.select_related(
            'group', 'event'
        ).order_by('group').values_list(
            'group_id', 'event_id', 'group__name', 'event__name'
        ).distinct()
        events = [event for _, _, _, event in category_pairs]

        stats = [
            {
                'data': stats.by_group(group_id).by_event(event_id).get_stats(),
                'name': '{}:{}'.format(group_name, event_name)
            }
            for group_id, event_id, group_name, event_name in category_pairs
        ]

    aggregation_period = statsy.stats.get_aggregation_period_for_days((end - start).days)
    result = {
        'stats': stats,
        'events': events,
        'aggregation_period': aggregation_period
    }
    return HttpResponse(json.dumps(result), content_type='application/json')


def today(request):
    result = {
        'stats': [{
            'data': statsy.objects.today().get_stats(),
            'name': 'today',
        }],
        'aggregation_period': statsy.stats.get_aggregation_period_for_days(1)
    }
    return HttpResponse(json.dumps(result), content_type='application/json')


def custom(request):
    result = {
        'url_map': statsy.site.url_map
    }

    return render_to_response('statsy/custom.html', result)
