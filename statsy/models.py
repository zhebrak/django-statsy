# coding: utf-8

from datetime import datetime

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from jsonfield import JSONField


class StatsyBaseQuerySet(models.QuerySet):
    def active(self):
        return self.filter(is_active=True)


class StatsyGroupQuerySet(StatsyBaseQuerySet):
    pass


class StatsyEventQuerySet(StatsyBaseQuerySet):
    pass


class StatsyGroup(models.Model):
    name = models.CharField(max_length=30, verbose_name='name')
    is_active = models.BooleanField(default=True, verbose_name='is active')

    objects = StatsyGroupQuerySet.as_manager()

    class Meta:
        verbose_name = 'Statsy Group'
        verbose_name_plural = 'Statsy Groups'

    def __unicode__(self):
        return self.name


class StatsyEvent(models.Model):
    name = models.CharField(max_length=30, verbose_name='name')
    is_active = models.BooleanField(default=True, verbose_name='is active')

    objects = StatsyEventQuerySet.as_manager()

    class Meta:
        verbose_name = 'Statsy Event'
        verbose_name_plural = 'Statsy Events'

    def __unicode__(self):
        return self.name


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


class StatsyObject(models.Model):
    group = models.ForeignKey(
        StatsyGroup, blank=True, null=True,
        related_name='statsy_object_list', verbose_name='group'
    )
    event = models.ForeignKey(
        StatsyEvent, blank=True, null=True,
        related_name='statsy_object_list', verbose_name='event'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, blank=True, null=True,
        related_name='statsy_object_list', verbose_name='user'
    )

    label = models.CharField(max_length=255, blank=True, null=True, verbose_name='label')

    related_object_content_type = models.ForeignKey(ContentType, blank=True, null=True)
    related_object_id = models.PositiveIntegerField(blank=True, null=True)
    related_object = GenericForeignKey('related_object_content_type', 'related_object_id')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='created at')
    value = models.IntegerField(blank=True, null=True, verbose_name='value')
    text_value = models.CharField(max_length=255, blank=True, null=True, verbose_name='text value')

    url = models.URLField(blank=True, null=True, verbose_name='url')
    duration = models.IntegerField(blank=True, null=True, verbose_name='duration')
    extra = JSONField(blank=True, null=True, verbose_name='extra')

    objects = StatsyQuerySet.as_manager()

    class Meta:
        verbose_name = 'Statsy Object'
        verbose_name_plural = 'Statsy Objects'

    def __unicode__(self):
        return '{0}:{1} {2}'.format(self.group, self.event, self.created_at.strftime('%d/%m/%Y %H:%M'))
