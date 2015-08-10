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
            name='Student',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('belt_rank', models.CharField(choices=[('WHITE', 'White Belt'), ('BLUE', 'Blue Belt'), ('PURPLE', 'Purple Belt'), ('BLACK', 'Black Belt'), ('RED', 'Red Belt')], max_length=10, default='WHITE')),
                ('activity_type', models.CharField(choices=[('YOGA', 'Yoga Student'), ('BJJ', 'Brazilian Jiu-Jitsu')], max_length=10, default='BJJ')),
                ('last_competition', models.DateTimeField(verbose_name='last competition')),
                ('notes', models.TextField()),
                ('current_affiliation', models.ForeignKey(verbose_name='The current school affiliation', to='schools.School')),
                ('name', models.ForeignKey(verbose_name='The students user profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Students',
            },
        ),
    ]
