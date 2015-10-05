# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main_site', '0017_auto_20151004_1931'),
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('title', models.CharField(max_length=20)),
                ('description', models.CharField(max_length=140)),
                ('date', models.DateField()),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('doctor', models.ForeignKey(blank=True, null=True, to=settings.AUTH_USER_MODEL, default=None, related_name='caretakers')),
                ('location', models.ForeignKey(blank=True, default=None, to='main_site.Hospital', related_name='locs')),
                ('patient', models.ForeignKey(blank=True, null=True, to=settings.AUTH_USER_MODEL, default=None, related_name='customers')),
            ],
        ),
    ]
