# coding: utf-8

from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import models


class StatsyBaseQuerySet(models.QuerySet):
    def active(self):
        return self.filter(is_active=True)


class StatsyGroupQuerySet(StatsyBaseQuerySet):
    pass


class StatsyEventQuerySet(StatsyBaseQuerySet):
    pass


class StatsyQuerySet(models.QuerySet):
    def by_group(self, group):
        return self.select_related('group').filter(group__name=group)

    def by_event(self, event):
        return self.select_related('event').filter(event__name=event)

    def by_user(self, user):
        if isinstance(user, get_user_model()):
            return self.filter(user_id=user.id)

        if isinstance(user, int):
            return self.filter(user_id=user)

        if isinstance(user, str):
            return self.select_related('user').filter(user__username=user)

    def by_label(self, label):
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
