# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main_site', '0012_auto_20151004_0422'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('message_subject', models.CharField(max_length=25, verbose_name='Subject')),
                ('message_text', models.TextField(verbose_name='Message')),
                ('message_time_created', models.DateTimeField(auto_now_add=True)),
                ('recipient', models.ForeignKey(default=None, blank=True, related_name='receive', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(default=None, blank=True, related_name='send', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='patient',
            name='hospital',
            field=models.ForeignKey(blank=True, null=True, to='main_site.Hospital'),
        ),
    ]
