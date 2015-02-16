# coding: utf-8

import importlib
import os

from celery import Celery

from statsy.models import StatsyObject
from statsy.settings import CELERY_APP


if CELERY_APP is None:
    app = Celery()
elif isinstance(CELERY_APP, str):
    module_str, app_str = CELERY_APP.rsplit('.', 1)

    try:
        module = importlib.import_module(module_str)

    except ImportError:
        settings_path = os.environ.get('DJANGO_SETTINGS_MODULE')
        settings_dir = settings_path.rsplit('.', 1)[0]

        module_str = '.'.join([settings_dir, module_str])
        module = importlib.import_module(module_str, package=settings_dir)

    app = getattr(module, app_str)

else:
    app = CELERY_APP


@app.task
def send(self, **kwargs):
    StatsyObject.create(**kwargs)
