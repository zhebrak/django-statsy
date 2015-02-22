# coding: utf-8

from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

import example.views as views


urlpatterns = patterns(
    'example.views',

    url(r'^$', 'index', name='index'),
    url(r'^post/(?P<post_id>\d+)/$', 'get_post', name='get_post'),
    url(r'^about/$', views.AboutView.as_view(), name='about'),

    url(r'^stats/', include('statsy.urls')),
    url(r'^tests/', include('tests.urls')),

    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += staticfiles_urlpatterns()


if settings.DEBUG:
    import debug_toolbar
    urlpatterns += patterns('',
        url(r'^__debug__/', include(debug_toolbar.urls)),
    )
