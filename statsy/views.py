# coding: utf-8

from django.db.models import Count

from statsy import statsy


def dashboard(request):
    today_group_stats = statsy.objects.today().select_related('group')\
        .extra({"hour": "strftime('%H:%M', created_at)"})\
        .values('group__name', 'hour').annotate(count=Count('group_id'))

    today_event_stats = statsy.objects.today().select_related('event')\
        .extra({"hour": "strftime('%H:%M', created_at)"})\
        .values('event__name', 'hour').annotate(count=Count('event_id'))

    print today_event_stats
    print today_group_stats


def user(request):
    pass


def group(request):
    pass


def event(request):
    pass


def tracking(request):
    pass

