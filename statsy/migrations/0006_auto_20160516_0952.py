# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('statsy', '0005_auto_20151111_0316'),
    ]

    operations = [
        migrations.AlterIndexTogether(
            name='statsyobject',
            index_together=set([('content_type', 'object_id', 'user')]),
        ),
    ]
