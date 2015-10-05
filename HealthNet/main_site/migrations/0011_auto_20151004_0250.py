# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_site', '0010_auto_20151004_0228'),
    ]

    operations = [
        migrations.AddField(
            model_name='hospital',
            name='listOfDoctors',
            field=models.ManyToManyField(related_name='hospitalDoctors', blank=True, to='main_site.Doctor'),
        ),
        migrations.AddField(
            model_name='hospital',
            name='listOfHospitalAdmins',
            field=models.ManyToManyField(related_name='hospitalAdmins', blank=True, to='main_site.HospitalAdmin'),
        ),
        migrations.AddField(
            model_name='hospital',
            name='listOfNurses',
            field=models.ManyToManyField(related_name='hospitalNurses', blank=True, to='main_site.Nurse'),
        ),
        migrations.AddField(
            model_name='hospital',
            name='listOfPatients',
            field=models.ManyToManyField(related_name='hospitalPatients', blank=True, to='main_site.Patient'),
        ),
    ]
