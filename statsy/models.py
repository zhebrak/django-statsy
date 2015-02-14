# coding: utf-8

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from jsonfield import JSONField

from statsy.descriptors import ValueDescriptor
from statsy.managers import StatsyGroupQuerySet, StatsyEventQuerySet, StatsyQuerySet


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

    value_types = ('int', 'text', 'float')
    value = ValueDescriptor(value_types=value_types)

    int_value = models.IntegerField(blank=True, null=True, verbose_name='int value')
    float_value = models.FloatField(blank=True, null=True, verbose_name='float value')
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

    @classmethod
    def create(cls, **kwargs):
        value = kwargs.pop('value', None)

        new_object = cls.objects.create(**kwargs)
        new_object.value = value
        new_object.save()

        return new_object
