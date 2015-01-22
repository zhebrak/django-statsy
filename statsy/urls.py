# coding: utf-8

from django.conf.urls import patterns, include, url


urlpatterns = patterns('statsy.views',
    url(r'^send/$', 'send', name='send'),

    url(r'^$', 'dashboard'),
    url(r'^group/$', 'group'),
    url(r'^event/$', 'event'),
    # url(r'^user/$', 'user'),
    # url(r'^tracking/$', 'tracking'),
)
