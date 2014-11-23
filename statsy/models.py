# coding: utf-8

from datetime import datetime

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from jsonfield import JSONField


class StatsyGroup(models.Model):
    name = models.CharField(max_length=30, verbose_name='group name')
    enabled = models.BooleanField(default=1)

    class Meta:
        verbose_name = 'Statsy Group'
        verbose_name_plural = 'Statsy Groups'

    def __unicode__(self):
        return self.name

    @property
    def is_enabled(self):
        return self.enabled


class StatsyAction(models.Model):
    name = models.CharField(max_length=30, verbose_name='action name')
    enabled = models.BooleanField(default=1)

    class Meta:
        verbose_name = 'Statsy Action'
        verbose_name_plural = 'Statsy Actions'

    def __unicode__(self):
        return self.name

    @property
    def is_enabled(self):
        return self.enabled


class StatsyQuerySet(models.QuerySet):
    def by_user(self, user):
        if isinstance(user, get_user_model()):
            return self.filter(user=user)

        if isinstance(user, int):
            return self.filter(user_id=user)

        if isinstance(user, str):
            return self.filter(user__username=user)

    def by_group(self, group):
        if isinstance(group, str):
            return self.filter(group__name=group)

        if isinstance(group, int):
            return self.filter(group_id=group)

        return self.filter(group=group)

    def by_action(self, action):
        if isinstance(action, str):
            return self.filter(action__name=action)

        if isinstance(action, int):
            return self.filter(action_id=action)

        return self.filter(action=action)

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
        return self.by_time(start=datetime.today())


class StatsyObject(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, related_name='statsy_object_list')
    group = models.ForeignKey(StatsyGroup, blank=True, null=True, related_name='statsy_object_list')
    action = models.ForeignKey(StatsyAction, blank=True, null=True, related_name='statsy_object_list')

    action_object_content_type = models.ForeignKey(ContentType, blank=True, null=True)
    action_object_id = models.PositiveIntegerField(blank=True, null=True)
    action_object = GenericForeignKey('action_object_content_type', 'action_object_id')

    created_at = models.DateTimeField(auto_now_add=True)
    value = models.IntegerField(blank=True, null=True)
    text_value = models.CharField(max_length=255, blank=True, null=True)

    url = models.URLField(blank=True, null=True)
    duration = models.IntegerField(blank=True, null=True)
    extra = JSONField(blank=True, null=True)

    objects = models.Manager.from_queryset(StatsyQuerySet)()

    class Meta:
        verbose_name = 'Statsy Object'
        verbose_name_plural = 'Statsy Objects'

    def __unicode__(self):
        return '{0}:{1} {2}'.format(self.group, self.action, self.created_at.strftime('%d/%M/%Y %H:%m'))
