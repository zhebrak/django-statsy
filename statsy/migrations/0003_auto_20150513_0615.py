# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('statsy', '0002_auto_20150222_0457'),
    ]

    operations = [
        migrations.AlterIndexTogether(
            name='statsyobject',
            index_together=set([('content_type', 'object_id')]),
        ),
    ]
