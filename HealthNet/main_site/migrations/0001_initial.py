# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import datetime


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('title', models.CharField(max_length=20, null=True)),
                ('description', models.CharField(max_length=140, null=True)),
                ('date', models.CharField(max_length=8, null=True)),
                ('start_time', models.CharField(max_length=5, null=True)),
                ('end_time', models.CharField(max_length=5, null=True)),
                ('doctor', models.ForeignKey(to=settings.AUTH_USER_MODEL, blank=True, default=None, null=True, related_name='caretakers')),
            ],
        ),
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('phone_number', models.CharField(max_length=15, null=True)),
                ('office_location', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('activity', models.TextField(max_length=500, blank=True)),
                ('time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Hospital',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=50)),
                ('location', models.CharField(max_length=50)),
                ('phone_number', models.CharField(max_length=15)),
                ('listOfDoctors', models.ManyToManyField(blank=True, related_name='hospitalDoctors', to='main_site.Doctor')),
            ],
        ),
        migrations.CreateModel(
            name='HospitalAdmin',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('phone_number', models.CharField(max_length=15, null=True)),
                ('hospital', models.ForeignKey(to='main_site.Hospital', null=True)),
                ('listOfDoctors', models.ManyToManyField(blank=True, related_name='subordinates', to='main_site.Doctor')),
                ('listOfHospitalAdmins', models.ManyToManyField(blank=True, related_name='coworkers', to='main_site.HospitalAdmin')),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('message_subject', models.CharField(verbose_name='Subject', max_length=25)),
                ('message_text', models.TextField(verbose_name='Message')),
                ('message_time_created', models.DateTimeField(auto_now_add=True)),
                ('urgent', models.CharField(max_length=3, choices=[('YES', 'yes'), ('NO', 'no')])),
                ('recipient', models.ForeignKey(default=None, to=settings.AUTH_USER_MODEL, related_name='receive')),
                ('sender', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='send')),
            ],
        ),
        migrations.CreateModel(
            name='Nurse',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('phone_number', models.CharField(max_length=15, null=True)),
                ('hospital', models.ForeignKey(to='main_site.Hospital', default=None, null=True)),
                ('listOfDoctors', models.ManyToManyField(blank=True, related_name='doctors', to='main_site.Doctor')),
            ],
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('address', models.CharField(max_length=50, null=True)),
                ('phone_number', models.CharField(max_length=15, null=True)),
                ('insurance_id', models.CharField(max_length=500, null=True)),
                ('insurance_provider', models.CharField(max_length=500, null=True)),
                ('gender', models.CharField(max_length=10, null=True)),
                ('height', models.FloatField(null=True, default=0)),
                ('weight', models.FloatField(null=True, default=0)),
                ('age', models.IntegerField(null=True, default=0)),
                ('emergency_contact', models.ForeignKey(to='main_site.Patient', blank=True, null=True, related_name='emergencyContact')),
                ('general_practitioner', models.ForeignKey(to='main_site.Doctor', null=True)),
                ('hospital', models.ForeignKey(to='main_site.Hospital', blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Prescription',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('medicine', models.CharField(max_length=30, null=True)),
                ('amount', models.CharField(max_length=50, null=True)),
                ('doctor', models.ForeignKey(to='main_site.Doctor')),
                ('patient', models.ForeignKey(to='main_site.Patient')),
            ],
        ),
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('description', models.CharField(max_length=500, null=True)),
                ('result', models.CharField(max_length=500, null=True)),
                ('viewable', models.BooleanField(default=False)),
                ('time', models.DateTimeField(default=datetime.datetime(2015, 12, 7, 1, 6, 33, 826990))),
                ('doctor', models.ForeignKey(to='main_site.Doctor')),
                ('patient', models.ForeignKey(to='main_site.Patient')),
            ],
        ),
        migrations.AddField(
            model_name='patient',
            name='prescriptions',
            field=models.ManyToManyField(blank=True, related_name='prescriptions', to='main_site.Prescription'),
        ),
        migrations.AddField(
            model_name='patient',
            name='records',
            field=models.ManyToManyField(blank=True, related_name='records', to='main_site.Record'),
        ),
        migrations.AddField(
            model_name='patient',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='nurse',
            name='listOfPatients',
            field=models.ManyToManyField(blank=True, related_name='patient', to='main_site.Patient'),
        ),
        migrations.AddField(
            model_name='nurse',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='hospitaladmin',
            name='listOfNurses',
            field=models.ManyToManyField(blank=True, related_name='employees', to='main_site.Nurse'),
        ),
        migrations.AddField(
            model_name='hospitaladmin',
            name='listOfPatients',
            field=models.ManyToManyField(blank=True, related_name='customers', to='main_site.Patient'),
        ),
        migrations.AddField(
            model_name='hospitaladmin',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='hospital',
            name='listOfHospitalAdmins',
            field=models.ManyToManyField(blank=True, related_name='hospitalAdmins', to='main_site.HospitalAdmin'),
        ),
        migrations.AddField(
            model_name='hospital',
            name='listOfNurses',
            field=models.ManyToManyField(blank=True, related_name='hospitalNurses', to='main_site.Nurse'),
        ),
        migrations.AddField(
            model_name='hospital',
            name='listOfPatients',
            field=models.ManyToManyField(blank=True, related_name='hospitalPatients', to='main_site.Patient'),
        ),
        migrations.AddField(
            model_name='event',
            name='hospitals',
            field=models.ForeignKey(to='main_site.Hospital', default=None, null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='initiated_by',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='initiator'),
        ),
        migrations.AddField(
            model_name='event',
            name='prescriptions',
            field=models.ForeignKey(to='main_site.Prescription', default=None, null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='target_of',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, default=None, null=True, related_name='target'),
        ),
        migrations.AddField(
            model_name='doctor',
            name='hospital',
            field=models.ForeignKey(to='main_site.Hospital', blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='doctor',
            name='listOfPatients',
            field=models.ManyToManyField(blank=True, related_name='patients', to='main_site.Patient'),
        ),
        migrations.AddField(
            model_name='doctor',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='appointment',
            name='location',
            field=models.ForeignKey(to='main_site.Hospital', blank=True, default='', null=True, related_name='locs'),
        ),
        migrations.AddField(
            model_name='appointment',
            name='patient',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, blank=True, default=None, null=True, related_name='customers'),
        ),
    ]
