# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_site', '0004_auto_20151003_1553'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctor',
            name='hospital',
            field=models.ForeignKey(default=None, null=True, blank=True, to='main_site.Hospital'),
        ),
        migrations.AlterField(
            model_name='doctor',
            name='office_location',
            field=models.CharField(null=True, blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='doctor',
            name='phone_number',
            field=models.CharField(null=True, blank=True, max_length=15),
        ),
        migrations.AlterField(
            model_name='hospitaladmin',
            name='hospital',
            field=models.ForeignKey(null=True, blank=True, to='main_site.Hospital'),
        ),
        migrations.AlterField(
            model_name='hospitaladmin',
            name='phone_number',
            field=models.CharField(null=True, blank=True, max_length=15),
        ),
        migrations.AlterField(
            model_name='nurse',
            name='hospital',
            field=models.ForeignKey(default=None, null=True, blank=True, to='main_site.Hospital'),
        ),
        migrations.AlterField(
            model_name='nurse',
            name='phone_number',
            field=models.CharField(null=True, blank=True, max_length=15),
        ),
        migrations.AlterField(
            model_name='patient',
            name='address',
            field=models.CharField(null=True, blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='patient',
            name='age',
            field=models.IntegerField(default=0, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='patient',
            name='gender',
            field=models.CharField(null=True, blank=True, max_length=10),
        ),
        migrations.AlterField(
            model_name='patient',
            name='height_in_m',
            field=models.FloatField(default=0, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='patient',
            name='phone_number',
            field=models.CharField(null=True, blank=True, max_length=15),
        ),
        migrations.AlterField(
            model_name='patient',
            name='weight_in_kg',
            field=models.FloatField(default=0, null=True, blank=True),
        ),
    ]
