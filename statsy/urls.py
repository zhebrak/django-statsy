# coding: utf-8

from django.conf.urls import patterns, url


urlpatterns = patterns('statsy.views',
    url(r'^send/$', 'send', name='statsy.send'),

    url(r'^$', 'dashboard', name='statsy.dashboard'),
    url(r'^group/$', 'group', name='statsy.group'),
    url(r'^event/$', 'event', name='statsy.event'),
    url(r'^user/$', 'user', name='statsy.user'),
    url(r'^tracking/$', 'tracking', name='statsy.tracking'),

    url(r'^today_group_stats/$', 'get_today_group_stats', name='statsy.today_group_stats'),
    url(r'^today_event_stats/$', 'get_today_event_stats', name='statsy.today_event_stats'),
)
