# coding: utf-8

from django.conf.urls import patterns, url


urlpatterns = patterns('statsy.views',
    url(r'^send/$', 'send', name='statsy.send'),

    url(r'^$', 'dashboard', 'statsy.dashboard'),
    url(r'^group/$', 'group', 'statsy.group'),
    url(r'^event/$', 'event', 'statsy.event'),
    # url(r'^user/$', 'user', 'statsy.user'),
    # url(r'^tracking/$', 'tracking', 'statsy.tracking'),
)
