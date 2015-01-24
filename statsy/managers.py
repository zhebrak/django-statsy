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
        if isinstance(group, str):
            return self.filter(group__name=group)

        if isinstance(group, int):
            return self.filter(group_id=group)

        return self.filter(group=group)

    def by_event(self, event):
        if isinstance(event, str):
            return self.filter(event__name=event)

        if isinstance(event, int):
            return self.filter(event_id=event)

        return self.filter(event=event)

    def by_user(self, user):
        if isinstance(user, get_user_model()):
            return self.filter(user=user)

        if isinstance(user, int):
            return self.filter(user_id=user)

        if isinstance(user, str):
            return self.filter(user__username=user)

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
                'created_at__' + 'lte' if include_end else 'lt': start
            })

        return self.filter(**filter_args) if filter_args else self

    def today(self):
        now = datetime.now()
        start_of_today = datetime(
            year=now.year, month=now.month, day=now.day,
            hour=0, minute=0, second=0, microsecond=0
        )

        return self.by_time(start=start_of_today)
