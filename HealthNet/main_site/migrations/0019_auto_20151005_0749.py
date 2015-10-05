# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_site', '0018_appointment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='date',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='description',
            field=models.CharField(max_length=140, null=True),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='end_time',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='location',
            field=models.ForeignKey(related_name='locs', default=b'', blank=True, to='main_site.Hospital', null=True),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='start_time',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='title',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
