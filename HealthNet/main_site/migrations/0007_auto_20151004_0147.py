# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_site', '0006_auto_20151003_2148'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='patient',
            name='medical_info',
        ),
        migrations.AddField(
            model_name='patient',
            name='emergency_contact',
            field=models.ForeignKey(blank=True, null=True, to='main_site.Patient', related_name='emergencyContact'),
        ),
        migrations.AddField(
            model_name='patient',
            name='initial_medical_info',
            field=models.CharField(max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='patient',
            name='insurance',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='doctor',
            name='listOfPatients',
            field=models.ManyToManyField(to='main_site.Patient', blank=True, related_name='patients'),
        ),
        migrations.AlterField(
            model_name='doctor',
            name='office_location',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='doctor',
            name='phone_number',
            field=models.CharField(max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='hospitaladmin',
            name='hospital',
            field=models.ForeignKey(null=True, to='main_site.Hospital'),
        ),
        migrations.AlterField(
            model_name='hospitaladmin',
            name='listOfDoctors',
            field=models.ManyToManyField(to='main_site.Doctor', blank=True, related_name='subordinates'),
        ),
        migrations.AlterField(
            model_name='hospitaladmin',
            name='listOfNurses',
            field=models.ManyToManyField(to='main_site.Nurse', blank=True, related_name='employees'),
        ),
        migrations.AlterField(
            model_name='hospitaladmin',
            name='listOfPatients',
            field=models.ManyToManyField(to='main_site.Patient', blank=True, related_name='customers'),
        ),
        migrations.AlterField(
            model_name='hospitaladmin',
            name='phone_number',
            field=models.CharField(max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='nurse',
            name='hospital',
            field=models.ForeignKey(null=True, to='main_site.Hospital', default=None),
        ),
        migrations.AlterField(
            model_name='nurse',
            name='listOfDoctors',
            field=models.ManyToManyField(to='main_site.Doctor', blank=True, related_name='doctors'),
        ),
        migrations.AlterField(
            model_name='nurse',
            name='listOfPatients',
            field=models.ManyToManyField(to='main_site.Patient', blank=True, related_name='patient'),
        ),
        migrations.AlterField(
            model_name='nurse',
            name='phone_number',
            field=models.CharField(max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='patient',
            name='address',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='patient',
            name='gender',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='patient',
            name='height_in_m',
            field=models.FloatField(null=True, default=0),
        ),
        migrations.AlterField(
            model_name='patient',
            name='phone_number',
            field=models.CharField(max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='patient',
            name='weight_in_kg',
            field=models.FloatField(null=True, default=0),
        ),
    ]
