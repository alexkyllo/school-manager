# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'RecurrenceRule'
        db.create_table('school_calendar_recurrencerule', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=36)),
            ('frequency', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('params', self.gf('django.db.models.fields.BinaryField')(blank=True)),
        ))
        db.send_create_signal('school_calendar', ['RecurrenceRule'])

        # Adding model 'Event'
        db.create_table('school_calendar_event', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=36)),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('rule', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['school_calendar.RecurrenceRule'], blank=True, null=True)),
            ('startdatetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 6, 7, 0, 0))),
            ('enddatetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 6, 8, 0, 0))),
        ))
        db.send_create_signal('school_calendar', ['Event'])

        # Adding model 'Occurrence'
        db.create_table('school_calendar_occurrence', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['school_calendar.Event'])),
        ))
        db.send_create_signal('school_calendar', ['Occurrence'])


    def backwards(self, orm):
        # Deleting model 'RecurrenceRule'
        db.delete_table('school_calendar_recurrencerule')

        # Deleting model 'Event'
        db.delete_table('school_calendar_event')

        # Deleting model 'Occurrence'
        db.delete_table('school_calendar_occurrence')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'unique': 'True'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True', 'symmetrical': 'False'})
        },
        'auth.permission': {
            'Meta': {'object_name': 'Permission', 'unique_together': "(('content_type', 'codename'),)", 'ordering': "('content_type__app_label', 'content_type__model', 'codename')"},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'blank': 'True', 'max_length': '75'}),
            'first_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'blank': 'True', 'symmetrical': 'False', 'related_name': "'user_set'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True', 'symmetrical': 'False', 'related_name': "'user_set'"}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '30', 'unique': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'object_name': 'ContentType', 'db_table': "'django_content_type'", 'unique_together': "(('app_label', 'model'),)", 'ordering': "('name',)"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'school_calendar.event': {
            'Meta': {'object_name': 'Event'},
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'enddatetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 6, 8, 0, 0)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'rule': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['school_calendar.RecurrenceRule']", 'blank': 'True', 'null': 'True'}),
            'startdatetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 6, 7, 0, 0)'})
        },
        'school_calendar.occurrence': {
            'Meta': {'object_name': 'Occurrence'},
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['school_calendar.Event']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'school_calendar.recurrencerule': {
            'Meta': {'object_name': 'RecurrenceRule'},
            'frequency': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'params': ('django.db.models.fields.BinaryField', [], {'blank': 'True'})
        }
    }

    complete_apps = ['school_calendar']