# coding: utf-8

from django.apps import AppConfig


class StatsyConfig(AppConfig):
    name = 'statsy'

    def ready(self):
        self.module.autodiscover()
        self.module.init_signals()
        self.module.init_shortcuts()
