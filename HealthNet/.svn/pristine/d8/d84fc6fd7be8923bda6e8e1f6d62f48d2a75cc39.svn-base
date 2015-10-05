# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('phone_number', models.CharField(max_length=15)),
                ('office_location', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Hospital',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('location', models.CharField(max_length=50)),
                ('phone_number', models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='HospitalAdmin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('phone_number', models.CharField(max_length=15)),
                ('hospital', models.ForeignKey(to='main_site.Hospital', blank=True, default=None)),
                ('listOfUsers', models.ManyToManyField(to=settings.AUTH_USER_MODEL, related_name='subordinates')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Nurse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('phone_number', models.CharField(max_length=15)),
                ('hospital', models.ForeignKey(to='main_site.Hospital', blank=True, default=None)),
                ('listOfDoctors', models.ManyToManyField(to=settings.AUTH_USER_MODEL, related_name='doctors')),
                ('listOfPatients', models.ManyToManyField(to=settings.AUTH_USER_MODEL, related_name='patients')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=50, null=True)),
                ('address', models.CharField(max_length=50, null=True)),
                ('phone_number', models.CharField(max_length=15, null=True)),
                ('medical_info', models.CharField(max_length=1000, null=True, blank=True)),
                ('gender', models.CharField(max_length=10, null=True)),
                ('height_in_m', models.FloatField(blank=True, default=0)),
                ('weight_in_kg', models.FloatField(blank=True, default=0)),
                ('age', models.IntegerField(blank=True, default=0)),
                ('general_practitioner', models.ForeignKey(blank=True, to='main_site.Doctor', null=True)),
                ('hospital', models.ForeignKey(blank=True, to='main_site.Hospital', null=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='doctor',
            name='hospital',
            field=models.ForeignKey(to='main_site.Hospital', blank=True, default=None),
        ),
        migrations.AddField(
            model_name='doctor',
            name='listOfPatients',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, related_name='customers'),
        ),
        migrations.AddField(
            model_name='doctor',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
        ),
    ]
