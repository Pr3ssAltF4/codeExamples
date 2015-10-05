# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_site', '0011_auto_20151004_0250'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='general_practitioner',
            field=models.ForeignKey(to='main_site.Doctor', null=True),
        ),
        migrations.AlterField(
            model_name='patient',
            name='hospital',
            field=models.ForeignKey(to='main_site.Hospital', null=True),
        ),
    ]
