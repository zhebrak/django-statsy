# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.contrib.auth.hashers import make_password


def create_sample_post_list(apps, schema_editor):
    Post = apps.get_model('example', 'Post')

    first_post = Post(
        title='Statsy is a simple tool for collecting and viewing user statistics',
        content='With Statsy you can...'
    )

    first_post.save()

    second_post = Post(
        title='More information',
        content='More information you can find at github or just ask me in person :)'
    )

    second_post.save()


def create_superuser(apps, schema_editor):
    User = apps.get_model('auth', 'User')

    superuser = User(
        username='statsy',
        password=make_password('statsy'),
        is_superuser=True,
        is_staff=True
    )
    superuser.save()


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
        ('example', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_sample_post_list),
        migrations.RunPython(create_superuser),
    ]
