# coding: utf-8

from django.core.cache import cache

from statsy.settings import CACHE_TIMEOUT


class StatsyCache(object):
    @staticmethod
    def get(key):
        return cache.get(key)

    @staticmethod
    def set(key, value, timeout=CACHE_TIMEOUT):
        return cache.set(key, value, timeout)

    def setdefault(self, key, default, timeout=CACHE_TIMEOUT):
        value = self.get(key)
        if not value:
            if callable(default):
                default = default()

            self.set(key, default, timeout)
            value = default

        return value
