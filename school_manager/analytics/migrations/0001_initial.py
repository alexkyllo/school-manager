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
            name='Analysis',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('active_users_now', models.IntegerField()),
                ('user', models.ForeignKey(verbose_name='The user who runs the analysis', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Analyses',
            },
        ),
    ]
