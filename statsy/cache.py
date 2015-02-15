# coding: utf-8

from django.core.cache import cache as django_cache

from statsy.settings import CACHE_TIMEOUT


class StatsyCache(object):
    @staticmethod
    def get(key):
        return django_cache.get(key)

    @staticmethod
    def set(key, value, timeout=CACHE_TIMEOUT):
        return django_cache.set(key, value, timeout)

    def setdefault(self, key, default, timeout=CACHE_TIMEOUT):
        value = self.get(key)
        if not value:
            if callable(default):
                default = default()

            self.set(key, default, timeout)
            value = default

        return value

    @staticmethod
    def delete(key):
        return django_cache.delete(key)


cache = StatsyCache()
