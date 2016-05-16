# coding: utf-8

import importlib

from celery import Celery

from statsy.models import StatsyObject
from statsy.settings import CELERY_APP


if CELERY_APP is None:
    app = Celery()
else:
    module_str, app_str = CELERY_APP.rsplit('.', 1)
    module = importlib.import_module(module_str)

    app = getattr(module, app_str)


@app.task
def send(**kwargs):
    obj = StatsyObject.create(**kwargs)

    return obj.serialize()


@app.task
def send_callback(result, callback_path):
    module, callback = callback_path.rsplit('.', 1)
    module = importlib.import_module(module)
    callback = getattr(module, callback)

    return callback(result)
