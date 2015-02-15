# coding: utf-8

import time
from functools import wraps, partial

from django.contrib.contenttypes.models import ContentType
from django.http import HttpRequest

from statsy.cache import cache
from statsy.exceptions import StatsyException, StatsyDisabled
from statsy.models import StatsyObject, StatsyGroup, StatsyEvent

try:
    from statsy.tasks import send as send_task
except ImportError:
    send_task = None

from statsy.settings import ASYNC
from statsy.helpers import get_correct_value_field


class Statsy(object):
    _send_params = [
        'group', 'event', 'label', 'user', 'user_i'
        'related_object', 'related_object_id', 'related_object_content_type_id',
        'value', 'url', 'duration', 'extra'
    ]

    def __init__(self, async=True):
        if ASYNC and async:
            self.send = self._send_async
        else:
            self.send = self._send

    def send(self, *args, **kwargs):
        """
        Determining in __init__
        @params: self.get_send_params()
        """
        raise NotImplemented

    def watch(self, group=None, event=None, value=None, label=None):
        watch_with_params = True
        if callable(value):
            watch_with_params = False

        def decorator(func):

            @wraps(func)
            def inner(request, *inner_args, **inner_kwargs):
                func_self = None
                if not isinstance(request, HttpRequest):
                    inner_args = list(inner_args)
                    func_self = request
                    request = inner_args.pop(0)

                time_start = time.time()
                if func_self:
                    result = func(func_self, request, *inner_args, **inner_kwargs)
                else:
                    result = func(request, *inner_args, **inner_kwargs)
                duration = int((time.time() - time_start) * 1000)

                user = request.user if request.user.is_authenticated() else None

                if watch_with_params:
                    self.send(
                        group=group, event=event, label=label, user=user,
                        value=value, url=request.path, duration=duration
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
            StatsyObject.create(**self._clean_kwargs(kwargs))
        except StatsyDisabled:
            pass

    def _send_async(self, **kwargs):
        if not send_task:
            return self._send(**kwargs)

        try:
            kwargs = self._clean_kwargs_async(kwargs)
            send_task.apply_async(kwargs=kwargs)
        except StatsyDisabled:
            pass

        except StatsyException:
            self._send(**kwargs)

    def _clean_kwargs(self, kwargs, clean_template=None):
        cleaned_kwargs = kwargs.copy()
        for kwarg in kwargs.keys():
            if clean_template:
                clean_kwarg_func = clean_template.format(kwarg) if clean_template else ''
            else:
                clean_kwarg_func = '_clean_{0}'.format(kwarg)

            if hasattr(self, clean_kwarg_func):
                    cleaned_kwargs.update(
                        getattr(self, clean_kwarg_func)(cleaned_kwargs.pop(kwarg) or None)
                    )

        return cleaned_kwargs

    _clean_kwargs_async = partial(_clean_kwargs, clean_template='_clean_{0}_async')

    def _clean_value(self, value):
        if not value:
            return {
                'value': None
            }

        return {
            'value': get_correct_value_field(value)[1]
        }

    def _clean_user(self, user):
        if isinstance(user, (int, str)):
            return {
                'user_id': user
            }

        return {
            'user': user
        }

    def _clean_user_async(self, user):
        return {
            'user_id': user.id
        }

    def _clean_group(self, group):
        if not group:
            return {}

        cache_key = StatsyGroup.cache_key_string.format(group)
        group = cache.setdefault(
            cache_key,
            lambda: StatsyGroup.objects.get_or_create(name=group)[0]
        )

        if group.is_active:
            return {
                'group_id': group.id
            }

        raise StatsyDisabled

    def _clean_event(self, event):
        if not event:
            return {}

        cache_key = StatsyEvent.cache_key_string.format(event)
        event = cache.setdefault(
            cache_key,
            lambda: StatsyEvent.objects.get_or_create(name=event)[0]
        )

        if event.is_active:
            return {
                'event_id': event.id
            }

        raise StatsyDisabled

    def _clean_related_object_async(self, related_object):
        return {
            'related_object_id': related_object.id,
            'related_object_content_type_id': ContentType.objects.get_for_model(related_object.__class__)
        }

    def get_send_params(self):
        return self._send_params

    objects = StatsyObject.objects
    groups = StatsyGroup.objects
    events = StatsyEvent.objects
