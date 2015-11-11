# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('statsy', '0003_auto_20150513_0615'),
    ]

    operations = [
        migrations.AlterField(
            model_name='statsyevent',
            name='name',
            field=models.CharField(unique=True, max_length=30, verbose_name=b'name'),
        ),
        migrations.AlterField(
            model_name='statsygroup',
            name='name',
            field=models.CharField(unique=True, max_length=30, verbose_name=b'name'),
        ),
    ]
