# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('main_site', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='prescription',
            name='description',
            field=models.CharField(null=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='record',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 7, 16, 1, 32, 57319)),
        ),
    ]
