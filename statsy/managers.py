# coding: utf-8

from datetime import datetime

from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.db import models

import statsy

from statsy.stats import Stats


class StatsyBaseQuerySet(models.QuerySet):
    def active(self):
        return self.filter(is_active=True)


class StatsyGroupQuerySet(StatsyBaseQuerySet):
    pass


class StatsyEventQuerySet(StatsyBaseQuerySet):
    pass


class StatsyQuerySet(models.QuerySet):
    def by_group(self, group):
        if not group:
            return self

        if isinstance(group, str):
            group_id = statsy.groups.get(name=group).id

        elif isinstance(group, int):
            group_id = group

        return self.filter(group_id=group_id)

    def by_event(self, event):
        if not event:
            return self

        if isinstance(event, str):
            event_id = statsy.events.get(name=event).id

        elif isinstance(event, int):
            event_id = event

        return self.filter(event_id=event_id)

    def by_category(self, category_type, category):
        return getattr(self, 'by_{}'.format(category_type))(category)

    def by_user(self, user):
        if isinstance(user, get_user_model()):
            return self.filter(user_id=user.id)

        if isinstance(user, int):
            return self.filter(user_id=user)

        if isinstance(user, str):
            return self.select_related('user').filter(user__username=user)

    def by_label(self, label):
        if not label:
            return self

        return self.filter(label=label)

    def by_time(self, start=None, end=None, include_start=True, include_end=True):
        filter_args = dict()
        if start:
            filter_args.update({
                'created_at__' + 'gte' if include_start else 'gt': start
            })

        if end:
            filter_args.update({
                'created_at__' + 'lte' if include_end else 'lt': end
            })

        return self.filter(**filter_args) if start or end else self

    def today(self):
        start_of_today = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
        return self.by_time(start=start_of_today)

    def active(self):
        return self.select_related('group', 'event').filter(group__is_active=True, event__is_active=True)

    def fetch(self, mask):
        group, event, label = mask.split(':')
        return self.by_group(group).by_event(event).by_label(label)

    def get_stats(self):
        return Stats.get_stats(self)

    def _numbers(self):
        return self.exclude(float_value=None)

    def _action(self):
        return self.filter(float_value=None, text_value=None)

    def _text(self):
        return self.exclude(text_value=None)

    def for_object(self, obj):
        return self.filter(
            object_id=obj.pk,
            content_type_id=ContentType.objects.get_for_model(obj.__class__.__name__)
        )
