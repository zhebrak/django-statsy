# coding: utf-8

import time

from datetime import datetime
from functools import wraps

from django.contrib.contenttypes.models import ContentType

from statsy.cache import cache
from statsy.exceptions import StatsyException, StatsyDisabled
from statsy.helpers import get_correct_value_field
from statsy.models import StatsyObject, StatsyGroup, StatsyEvent
from statsy.settings import ASYNC


try:
    from statsy.tasks import send as send_task, send_callback
except ImportError:
    send_task, send_callback = None, None


class Statsy(object):
    _send_params = [
        'group', 'event', 'label', 'user', 'user_id'
        'content_object', 'object_id', 'content_type_id',
        'value', 'url', 'duration', 'extra', 'callback'
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

    def watch(self, group=None, event=None, value=None, label=None, callback=None):
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
                        value=value, url=request.path, duration=duration,
                        callback=callback
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
            callback = kwargs.get('callback')
            result = StatsyObject.create(**self._clean_kwargs(kwargs))

            if callback:
                return callback(result)

            return result

        except StatsyDisabled:
            pass

    def _send_async(self, **kwargs):
        if not send_task:
            return self._send(**kwargs)

        if 'created_at' not in kwargs:
            kwargs['created_at'] = datetime.now()

        try:
            callback = kwargs.get('callback')
            if callback:
                try:
                    callback = callback.s()
                except AttributeError:
                    path = '.'.join([callback.__module__, callback.__name__])
                    callback = send_callback.s(path)

            return send_task.apply_async(kwargs=self._clean_kwargs_async(kwargs), link=callback)

        except StatsyDisabled:
            pass

        except StatsyException:
            return self._send(**kwargs)

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
                    getattr(self, clean_func)(cleaned_kwargs.pop(kwarg))
                )

        return cleaned_kwargs

    def _clean_kwargs_async(self, kwargs):
        return self._clean_kwargs(kwargs, clean_template='_clean_{0}_async')

    def _clean_callback(self, _):
        return {}

    def _clean_value(self, value):
        _, cleaned_value = get_correct_value_field(value)

        return {
            'value': cleaned_value
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

        group = group[:StatsyGroup.NAME_LENGTH_LIMIT]

        if self.use_cache:
            cache_key = StatsyGroup.cache_key_string.format(group)
            group = cache.setdefault(
                cache_key,
                lambda: self.groups.get_or_create(name=group)[0]
            )
        else:
            group, _ = self.groups.get_or_create(name=group)

        if group.is_active:
            return {
                'group_id': group.id
            }

        raise StatsyDisabled

    def _clean_event(self, event):
        if not event:
            return {}

        event = event[:StatsyEvent.NAME_LENGTH_LIMIT]

        if self.use_cache:
            cache_key = StatsyEvent.cache_key_string.format(event)
            event = cache.setdefault(
                cache_key,
                lambda: self.events.get_or_create(name=event)[0]
            )
        else:
            event, _ = self.events.get_or_create(name=event)

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
