# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('schools', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=36)),
                ('startdatetime', models.DateTimeField(blank=True, null=True)),
                ('enddatetime', models.DateTimeField(blank=True, null=True)),
                ('allday', models.BooleanField(default=False)),
                ('recurring', models.BooleanField(default=False)),
                ('attendees', models.ManyToManyField(to=settings.AUTH_USER_MODEL, related_name='attendees')),
                ('course', models.ForeignKey(to='schools.Course', null=True)),
                ('creator', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Occurrence',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('event', models.ForeignKey(to='school_calendar.Event')),
            ],
        ),
        migrations.CreateModel(
            name='Rule',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('frequency', models.CharField(choices=[('YEARLY', 'yearly'), ('MONTHLY', 'monthly'), ('WEEKLY', 'weekly'), ('DAILY', 'daily')], max_length=10)),
                ('byweekday', models.CharField(blank=True, max_length=36)),
                ('until', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='event',
            name='rule',
            field=models.ForeignKey(null=True, to='school_calendar.Rule', blank=True),
        ),
        migrations.AddField(
            model_name='event',
            name='school',
            field=models.ForeignKey(to='schools.School'),
        ),
    ]
