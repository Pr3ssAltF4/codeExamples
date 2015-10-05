# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_site', '0002_auto_20151003_1505'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hospitaladmin',
            name='listOfUsers',
        ),
        migrations.AddField(
            model_name='hospitaladmin',
            name='listOfDoctors',
            field=models.ManyToManyField(related_name='subordinates', to='main_site.Doctor'),
        ),
        migrations.AddField(
            model_name='hospitaladmin',
            name='listOfNurses',
            field=models.ManyToManyField(related_name='employees', to='main_site.Nurse'),
        ),
        migrations.AddField(
            model_name='hospitaladmin',
            name='listOfPatients',
            field=models.ManyToManyField(related_name='customers', to='main_site.Patient'),
        ),
        migrations.AlterField(
            model_name='doctor',
            name='listOfPatients',
            field=models.ManyToManyField(related_name='patients', to='main_site.Patient'),
        ),
        migrations.AlterField(
            model_name='nurse',
            name='listOfDoctors',
            field=models.ManyToManyField(related_name='doctors', to='main_site.Doctor'),
        ),
        migrations.AlterField(
            model_name='nurse',
            name='listOfPatients',
            field=models.ManyToManyField(related_name='patient', to='main_site.Patient'),
        ),
    ]
