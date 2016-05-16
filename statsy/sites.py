# coding: utf-8

from functools import update_wrapper

from django.contrib.auth.decorators import permission_required
from django.core.exceptions import PermissionDenied
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

    def register(self, view, name=None, category=default_category, permission=None):
        if view in self._registry:
            raise AlreadyRegistered('The view {0} is already registered'.format(view.__name__))

        self._registry[view.__name__] = (view, name, permission)

        if category not in self._category_map:
            self._category_map[category] = []

        self._category_map[category].append(view.__name__)

    @staticmethod
    def has_permission(request):
        return request.user.has_perm(STATS_VIEW_PERMISSION)

    def stats_view(self, view):
        def inner(request, *args, **kwargs):
            if not self.has_permission(request):
                raise PermissionDenied

            return view(request, *args, **kwargs)

        if not getattr(view, 'csrf_exempt', False):
            inner = csrf_protect(inner)

        return update_wrapper(inner, view)

    def get_urls(self):
        from django.conf.urls import url

        urlpatterns = [
            url(r'^send/$', api.send, name='statsy.send'),

            url(r'^$', self.stats_view(views.dashboard), name='statsy.dashboard'),
            url(r'^custom/$', self.stats_view(views.custom), name='statsy.custom'),
            url(r'^today/$', self.stats_view(views.today), name='statsy.today'),
        ]

        url_map = dict()
        for view_name, (view, _, permission) in self._registry.items():
            url_part = self._get_url_part(view_name)
            url_name = 'statsy.{0}'.format(view_name, url_part)

            stats_view = self.stats_view(view)
            if permission:
                stats_view = permission_required(permission)(stats_view)

            urlpatterns.append(
                url(r'^custom/{0}/'.format(url_part), stats_view, name=url_name)
            )

            url_map[view_name] = url_name

        self._build_url_map(url_map)

        return urlpatterns

    def _build_url_map(self, url_map):
        for category, view_list in self._category_map.items():
            category = category if category != self.default_category else ''
            self._url_map[category] = dict()

            for view_name in view_list:
                self._url_map[category].update({
                    self._get_readable_view_name(view_name): url_map[view_name]
                })

    def _get_readable_view_name(self, view_name):
        _, name, __ = self._registry[view_name]
        return name or \
               ''.join([
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
