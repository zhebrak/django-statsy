# coding: utf-8

from functools import update_wrapper
from django.http import Http404
from django.views.decorators.csrf import csrf_protect

import statsy.api as api
import statsy.views as views

from statsy.exceptions import AlreadyRegistered
from statsy.settings import STATS_VIEW_PERMISSION


class StatsySite(object):
    default_category = 'default'

    def __init__(self):
        self._registry = {}
        self._url_map = {}
        self._category_map = {}

    def register(self, view, category=default_category):
        if view in self._registry:
            raise AlreadyRegistered('The view %s is already registered' % view.__name__)

        self._registry[view.__name__] = view

        if category not in self._category_map:
            self._category_map[category] = []

        self._category_map[category].append(view.__name__)

    @staticmethod
    def has_permission(request):
        return request.user.has_perm(STATS_VIEW_PERMISSION)

    def stats_view(self, view):
        def inner(request, *args, **kwargs):
            if not self.has_permission(request):
                raise Http404

            return view(request, *args, **kwargs)

        if not getattr(view, 'csrf_exempt', False):
            inner = csrf_protect(inner)

        return update_wrapper(inner, view)

    def get_urls(self):
        from django.conf.urls import patterns, url

        urlpatterns = patterns('',
            url(r'^send/$', api.send, name='statsy.send'),

            url(r'^$', views.dashboard, name='statsy.dashboard'),

            url(r'^group/$', views.group_list, name='statsy.group_list'),
            url(r'^group/(?P<group_name>.+)/$', views.group, name='statsy.group'),

            url(r'^event/$', views.event_list, name='statsy.event_list'),
            url(r'^event/(?P<event_name>.+)/$', views.event, name='statsy.event'),

            url(r'^user/$', views.user, name='statsy.user'),
            url(r'^tracking/$', views.tracking, name='statsy.tracking'),
            url(r'^custom/$', views.custom, name='statsy.custom'),

            url(r'^today_group_stats/$', views.get_today_group_stats, name='statsy.today_group_stats'),
            url(r'^today_event_stats/$', views.get_today_event_stats, name='statsy.today_event_stats'),
        )

        url_map = dict()
        for view_name, view in self._registry.items():
            url_part = self._get_url_part(view_name)
            url_name = 'statsy.{0}'.format(view_name, url_part)

            urlpatterns += patterns('',
                url(r'^custom/{0}/'.format(url_part), self.stats_view(view), name=url_name)
            )

            url_map[view_name] = url_name

        self._build_url_map(url_map)

        return urlpatterns

    def _build_url_map(self, url_map):
        for category, view_list in self._category_map.items():
            for view_name in view_list:
                category = category if category != self.default_category else ''
                self._url_map[category] = dict()
                self._url_map[category].update({
                    self._get_readable_view_name(view_name): url_map[view_name]
                })

    @staticmethod
    def _get_readable_view_name(view_name):
        return ''.join([
            ' ' + letter if letter.isupper() else letter
            for letter in view_name.replace('_', ' ')
        ]).strip().capitalize()

    @staticmethod
    def _get_url_part(view_name):
        return ''.join([
            ' ' + letter if letter.isupper() else letter
            for letter in view_name
        ]).replace(' ', '_').strip(' _').lower()

    @property
    def url_map(self):
        return self._url_map


site = StatsySite()
