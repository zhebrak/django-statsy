# coding: utf-8

import time
from functools import wraps, partial

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.cache import cache

from statsy.models import StatsyObject, StatsyGroup, StatsyEvent
from statsy.tasks import send as send_task


class StatsyException(Exception):
    pass


class StatsyDisabledException(StatsyException):
    pass


class Statsy(object):
    def __init__(self, async=True):
        if settings.STATSY_CELERY and async:
            self.send = self._send_async
        else:
            self.send = self._send

        self.cache = StatsyCache()

    def send(
            self, user=None, group=None, event=None, related_object=None,
            value=None, url=None, duration=None, extra=None
    ):
        """ Determining in __init__ """
        raise NotImplemented

    def watch(self, value=None, group=None, event=None):
        watch_with_params = True
        if callable(value):
            watch_with_params = False

        def decorator(func):

            @wraps(func)
            def inner(request, *inner_args, **inner_kwargs):
                time_start = time.time()
                result = func(request, *inner_args, **inner_kwargs)
                duration = int((time.time() - time_start) * 1000)

                user = request.user if request.user.is_authenticated() else None

                if watch_with_params:
                    self.send(
                        user=user, group=group, event=event, value=value,
                        url=request.path, duration=duration
                    )
                else:
                    self.send(user=user, url=request.path, duration=duration)

                return result

            return inner

        if not watch_with_params:
            return decorator(value)

        return decorator

    def _send(self, **kwargs):
        try:
            statsy_object = StatsyObject(**self._clean_kwargs(kwargs))
            statsy_object.save()
        except StatsyDisabledException:
            pass

    def _send_async(self, **kwargs):
        try:
            kwargs = self._clean_kwargs_async(kwargs)
            send_task.apply_async(kwargs=kwargs)
        except StatsyDisabledException:
            pass

        except StatsyException:
            self._send(**kwargs)

    def _clean_kwargs(self, kwargs, clean_template=None):
        cleaned_kwargs = kwargs.copy()
        for kwarg in kwargs.iterkeys():
            if clean_template:
                clean_kwarg_func = clean_template.format(kwarg) if clean_template else ''
            else:
                clean_kwarg_func = '_clean_{0}'.format(kwarg)

            if hasattr(self, clean_kwarg_func):
                    cleaned_kwargs.update(
                        getattr(self, clean_kwarg_func)(cleaned_kwargs.pop(kwarg) or {})
                    )

        return cleaned_kwargs

    _clean_kwargs_async = partial(_clean_kwargs, clean_template='_clean_{0}_async')

    def _clean_value(self, value):
        if not value:
            return {
                'value': None
            }

        if isinstance(value, int) or (isinstance(value, str) and value.isdigit()):
            return {
                'value': int(value)
            }

        return {
            'text_value': str(value)
        }

    def _clean_user_async(self, user):
        return {
            'user_id': user.id
        }

    def _clean_group(self, group):
        if not group:
            return {}

        cache_key = 'statsy_group_{0}'.format(group)
        group = self.cache.setdefault(
            cache_key,
            lambda: StatsyGroup.objects.get_or_create(name=group)[0]
        )

        if group.is_active:
            return {
                'group_id': group.id
            }

        raise StatsyDisabledException

    def _clean_event(self, event):
        if not event:
            return {}

        cache_key = 'statsy_event_{0}'.format(event)
        event = self.cache.setdefault(
            cache_key,
            lambda: StatsyEvent.objects.get_or_create(name=event)[0]
        )

        if event.is_active:
            return {
                'event_id': event.id
            }

        raise StatsyDisabledException

    def _clean_related_object_async(self, related_object):
        return {
            'related_object_id': related_object.id,
            'related_object_content_type_id': ContentType.objects.get_for_model(related_object.__class__)
        }

    objects = StatsyObject.objects
    groups = StatsyGroup.objects
    events = StatsyEvent.objects


class StatsyCache(object):
    @staticmethod
    def get(key):
        return cache.get(key)

    @staticmethod
    def set(key, value, timeout=settings.STATSY_CACHE_TIMEOUT):
        return cache.set(key, value, timeout)

    def setdefault(self, key, default, timeout=settings.STATSY_CACHE_TIMEOUT):
        value = self.get(key)
        if not value:
            if callable(default):
                default = default()

            self.set(key, default, timeout)
            value = default

        return value
