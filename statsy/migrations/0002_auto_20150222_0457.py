# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('statsy', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='statsyobject',
            options={'ordering': ('-created_at',), 'verbose_name': 'Statsy Object', 'verbose_name_plural': 'Statsy Objects', 'permissions': (('stats_view', 'Can view stats'),)},
        ),
    ]
