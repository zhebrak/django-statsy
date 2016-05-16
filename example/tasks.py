# coding: utf-8

import statsy

from example.celery_app import app


@app.task
def sample_callback_task(_):
    statsy.send(
        extra='I\'m the task callback'
    )

