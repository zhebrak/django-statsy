# coding: utf-8

from datetime import datetime

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from jsonfield import JSONField

from statsy.descriptors import ValueDescriptor
from statsy.managers import StatsyGroupQuerySet, StatsyEventQuerySet, StatsyQuerySet


class StatsyCategory(models.Model):
    """ Abstract base model for Group and Event """

    name = models.CharField(max_length=30, verbose_name='name')
    is_active = models.BooleanField(default=True, verbose_name='is active')

    class Meta:
        abstract = True

    def __unicode__(self):
        return self.name

    @property
    def cache_key(self):
        return self.cache_key_string.format(self.name)

    def activate(self):
        self.is_active = True
        self.save()

    def deactivate(self):
        self.is_active = False
        self.save()


class StatsyGroup(StatsyCategory):
    objects = StatsyGroupQuerySet.as_manager()

    cache_key_string = 'statsy_group_{0}'

    class Meta:
        verbose_name = 'Statsy Group'
        verbose_name_plural = 'Statsy Groups'


class StatsyEvent(StatsyCategory):
    objects = StatsyEventQuerySet.as_manager()

    cache_key_string = 'statsy_event_{0}'

    class Meta:
        verbose_name = 'Statsy Event'
        verbose_name_plural = 'Statsy Events'


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

    content_type = models.ForeignKey(ContentType, blank=True, null=True)
    object_id = models.PositiveIntegerField(blank=True, null=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    created_at = models.DateTimeField(blank=True, null=True, db_index=True, verbose_name='created at')

    value_types = ('float', 'text')
    value = ValueDescriptor(value_types=value_types)

    float_value = models.FloatField(blank=True, null=True, verbose_name='float value')
    text_value = models.CharField(max_length=255, blank=True, null=True, verbose_name='text value')

    url = models.URLField(blank=True, null=True, verbose_name='url')
    duration = models.IntegerField(blank=True, null=True, verbose_name='duration')
    extra = JSONField(blank=True, null=True, max_length=1024, verbose_name='extra')

    objects = StatsyQuerySet.as_manager()

    class Meta:
        verbose_name = 'Statsy Object'
        verbose_name_plural = 'Statsy Objects'
        ordering = ('-created_at',)
        permissions = (
            ('stats_view', 'Can view stats'),
        )

    def __unicode__(self):
        if self.label:
            return '{0}:{1}:{2} {3}'.format(
                self.group, self.event, self.label,
                self.created_at.strftime('%d/%m/%Y %H:%M')
            )

        return '{0}:{1} {2}'.format(self.group, self.event, self.created_at.strftime('%d/%m/%Y %H:%M'))


    @classmethod
    def create(cls, **kwargs):
        value = kwargs.pop('value', None)

        if 'created_at' not in kwargs:
            kwargs['created_at'] = datetime.now()

        new_object = cls(**kwargs)
        new_object.value = value
        new_object.save()

        return new_object
