# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_site', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nurse',
            name='listOfPatients',
            field=models.ManyToManyField(related_name='patients', to='main_site.Patient'),
        ),
    ]
