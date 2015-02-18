# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='StatsyEvent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30, verbose_name=b'name')),
                ('is_active', models.BooleanField(default=True, verbose_name=b'is active')),
            ],
            options={
                'verbose_name': 'Statsy Event',
                'verbose_name_plural': 'Statsy Events',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='StatsyGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30, verbose_name=b'name')),
                ('is_active', models.BooleanField(default=True, verbose_name=b'is active')),
            ],
            options={
                'verbose_name': 'Statsy Group',
                'verbose_name_plural': 'Statsy Groups',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='StatsyObject',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('label', models.CharField(max_length=255, null=True, verbose_name=b'label', blank=True)),
                ('object_id', models.PositiveIntegerField(null=True, blank=True)),
                ('created_at', models.DateTimeField(db_index=True, null=True, verbose_name=b'created at', blank=True)),
                ('float_value', models.FloatField(null=True, verbose_name=b'float value', blank=True)),
                ('text_value', models.CharField(max_length=255, null=True, verbose_name=b'text value', blank=True)),
                ('url', models.URLField(null=True, verbose_name=b'url', blank=True)),
                ('duration', models.IntegerField(null=True, verbose_name=b'duration', blank=True)),
                ('extra', jsonfield.fields.JSONField(max_length=1024, null=True, verbose_name=b'extra', blank=True)),
                ('content_type', models.ForeignKey(blank=True, to='contenttypes.ContentType', null=True)),
                ('event', models.ForeignKey(related_name='statsy_object_list', verbose_name=b'event', blank=True, to='statsy.StatsyEvent', null=True)),
                ('group', models.ForeignKey(related_name='statsy_object_list', verbose_name=b'group', blank=True, to='statsy.StatsyGroup', null=True)),
                ('user', models.ForeignKey(related_name='statsy_object_list', verbose_name=b'user', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': 'Statsy Object',
                'verbose_name_plural': 'Statsy Objects',
                'permissions': (('stats_view', 'Can view stats'),),
            },
            bases=(models.Model,),
        ),
    ]
