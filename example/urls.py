# coding: utf-8

from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

import example.views as views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^post/(?P<post_id>\d+)/$', views.get_post, name='get_post'),
    url(r'^about/$', views.AboutView.as_view(), name='about'),

    url(r'^stats/', include('statsy.urls')),
    url(r'^tests/', include('tests.urls')),

    url(r'^admin/', include(admin.site.urls)),
]

urlpatterns += staticfiles_urlpatterns()


if settings.DEBUG:
    try:
        import debug_toolbar
        urlpatterns.append(
            url(r'^__debug__/', include(debug_toolbar.urls)),
        )
    except ImportError:
        pass
