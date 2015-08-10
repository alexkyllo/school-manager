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
            name='Course',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=50)),
                ('instructors', models.ManyToManyField(to=settings.AUTH_USER_MODEL, related_name='course_instructors')),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=50)),
                ('address_1', models.CharField(max_length=50)),
                ('address_2', models.CharField(blank=True, max_length=50)),
                ('city', models.CharField(max_length=50)),
                ('state_province', models.CharField(max_length=4)),
                ('zip_postal_code', models.CharField(max_length=10)),
                ('country', models.CharField(max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='School',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=80)),
                ('members', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('startdatetime', models.DateTimeField()),
                ('enddatetime', models.DateTimeField()),
                ('course', models.ForeignKey(to='schools.Course')),
                ('school', models.ForeignKey(to='schools.School')),
                ('students', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='location',
            name='school',
            field=models.ForeignKey(related_name='locations', to='schools.School'),
        ),
        migrations.AddField(
            model_name='course',
            name='location',
            field=models.ForeignKey(related_name='courses', to='schools.Location'),
        ),
        migrations.AddField(
            model_name='course',
            name='school',
            field=models.ForeignKey(to='schools.School'),
        ),
        migrations.AddField(
            model_name='course',
            name='students',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, related_name='course_students'),
        ),
    ]
