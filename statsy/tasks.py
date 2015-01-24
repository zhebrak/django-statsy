# coding: utf-8

from celery import Celery

from statsy.models import StatsyObject


app = Celery('tasks', broker='amqp://guest@localhost//')


@app.task
def send(self, **kwargs):
    statsy_object = StatsyObject.create(**kwargs)
    statsy_object.save()
