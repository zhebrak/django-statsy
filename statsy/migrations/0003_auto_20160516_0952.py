# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('statsy', '0002_auto_20150222_0457'),
    ]

    operations = [
        migrations.AlterField(
            model_name='statsyevent',
            name='name',
            field=models.CharField(unique=True, max_length=100, verbose_name=b'name'),
        ),
        migrations.AlterField(
            model_name='statsygroup',
            name='name',
            field=models.CharField(unique=True, max_length=100, verbose_name=b'name'),
        ),
        migrations.AlterIndexTogether(
            name='statsyobject',
            index_together=set([('content_type', 'object_id', 'user')]),
        ),
    ]
