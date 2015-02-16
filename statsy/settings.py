# coding: utf-8

from django.conf import settings


CACHE_TIMEOUT = getattr(settings, 'STATSY_CACHE_TIMEOUT', 60 * 15)

ASYNC = getattr(settings, 'STATSY_ASYNC', False)
CELERY_APP = getattr(settings, 'CELERY_APP', None)

STATS_VIEW_PERMISSION = getattr(settings, 'STATSY_VIEW_PERMISSION', 'statsy.stats_view')
