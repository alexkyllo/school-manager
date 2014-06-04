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
            ('name', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('frequency', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('params', self.gf('django.db.models.fields.BinaryField')(blank=True)),
        ))
        db.send_create_signal('school_calendar', ['RecurrenceRule'])


    def backwards(self, orm):
        # Deleting model 'RecurrenceRule'
        db.delete_table('school_calendar_recurrencerule')


    models = {
        'school_calendar.recurrencerule': {
            'Meta': {'object_name': 'RecurrenceRule'},
            'frequency': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'params': ('django.db.models.fields.BinaryField', [], {'blank': 'True'})
        }
    }

    complete_apps = ['school_calendar']