# coding: utf-8

from django.apps import apps
from django.db.models.signals import post_save, post_delete

from statsy.cache import cache


def invalidate_group_cache(sender, *args, **kwargs):
    cache.delete(kwargs['instance'].cache_key)


post_save.connect(invalidate_group_cache, sender=apps.get_model('statsy', 'StatsyGroup'))
post_delete.connect(invalidate_group_cache, sender=apps.get_model('statsy', 'StatsyGroup'))


def invalidate_event_cache(sender, *args, **kwargs):
    cache.delete(kwargs['instance'].cache_key)


post_save.connect(invalidate_event_cache, sender=apps.get_model('statsy', 'StatsyEvent'))
post_delete.connect(invalidate_event_cache, sender=apps.get_model('statsy', 'StatsyEvent'))
