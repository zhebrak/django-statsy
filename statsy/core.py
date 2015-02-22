# coding: utf-8

import time

from datetime import datetime
from functools import wraps

from django.contrib.contenttypes.models import ContentType

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
        'group', 'event', 'label', 'user', 'user_id'
        'content_object', 'object_id', 'content_type_id',
        'value', 'url', 'duration', 'extra'
    ]

    def __init__(self, async=True, cache=True):
        if ASYNC and async:
            self.send = self._send_async
        else:
            self.send = self._send

        self.use_cache = cache

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
                time_start = time.time()
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

        if 'created_at' not in kwargs:
            kwargs['created_at'] = datetime.now()

        try:
            send_task.delay(**self._clean_kwargs_async(kwargs))

        except StatsyDisabled:
            pass

        except StatsyException:
            self._send(**kwargs)

    def _clean_kwargs(self, kwargs, clean_template=None):
        cleaned_kwargs = kwargs.copy()
        for kwarg in kwargs.keys():

            default_clean_func = '_clean_{0}'.format(kwarg)
            clean_func = default_clean_func

            if clean_template:
                clean_func = clean_template.format(kwarg)
                if not hasattr(self, clean_func):
                    clean_func = default_clean_func

            if hasattr(self, clean_func):
                cleaned_kwargs.update(
                    getattr(self, clean_func)(cleaned_kwargs.pop(kwarg) or None)
                )

        return cleaned_kwargs

    def _clean_kwargs_async(self, kwargs):
        return self._clean_kwargs(kwargs, clean_template='_clean_{0}_async')

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

        if self.use_cache:
            cache_key = StatsyGroup.cache_key_string.format(group)
            group = cache.setdefault(
                cache_key,
                lambda: self.groups.get_or_create(name=group)[0]
            )
        else:
            group = self.groups.get_or_create(name=group)[0]

        if group.is_active:
            return {
                'group_id': group.id
            }

        raise StatsyDisabled

    def _clean_event(self, event):
        if not event:
            return {}

        if self.use_cache:
            cache_key = StatsyEvent.cache_key_string.format(event)
            event = cache.setdefault(
                cache_key,
                lambda: self.events.get_or_create(name=event)[0]
            )
        else:
            event = self.events.get_or_create(name=event)[0]

        if event.is_active:
            return {
                'event_id': event.id
            }

        raise StatsyDisabled

    def _clean_content_object_async(self, content_object):
        return {
            'object_id': content_object.id,
            'content_type_id': ContentType.objects.get_for_model(content_object.__class__).id
        }

    def get_send_params(self):
        return self._send_params

    objects = StatsyObject.objects
    groups = StatsyGroup.objects
    events = StatsyEvent.objects
