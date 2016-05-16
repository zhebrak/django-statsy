# coding: utf-8

from django.utils.module_loading import autodiscover_modules

from statsy.log import logger
from statsy.sites import site


default_app_config = 'statsy.apps.StatsyConfig'


__all__ = [
    'send', 'watch', 'get_send_params'
    'objects', 'groups', 'events',
    'site', 'autodiscover', 'logger',
    'stats'
]


def autodiscover():
    autodiscover_modules('stats', register_to=site)


def init_signals():
    import statsy.signals


def init_shortcuts():
    from statsy.core import Statsy
    from statsy.stats import Stats

    _statsy = Statsy()

    globals().update({
        'Statsy': Statsy,

        'objects': Statsy.objects,
        'groups': Statsy.groups,
        'events': Statsy.events,

        '_statsy': _statsy,
    })

    globals().update({
        'send': _statsy.send,
        'watch': _statsy.watch,

        'get_send_params': _statsy.get_send_params
    })
