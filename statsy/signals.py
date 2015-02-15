# coding: utf-8

from django.db.models.signals import post_save, post_delete

from statsy.cache import cache
from statsy.models import StatsyGroup, StatsyEvent


def invalidate_group_cache(sender, *args, **kwargs):
    cache.delete(kwargs['instance'].cache_key)


post_save.connect(invalidate_group_cache, sender=StatsyGroup)
post_delete.connect(invalidate_group_cache, sender=StatsyGroup)


def invalidate_event_cache(sender, *args, **kwargs):
    cache.delete(kwargs['instance'].cache_key)


post_save.connect(invalidate_event_cache, sender=StatsyEvent)
post_delete.connect(invalidate_event_cache, sender=StatsyEvent)
