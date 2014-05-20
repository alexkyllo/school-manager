# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding M2M table for field students on 'School'
        m2m_table_name = db.shorten_name('schools_school_students')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('school', models.ForeignKey(orm['schools.school'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['school_id', 'user_id'])

        # Adding M2M table for field instructors on 'School'
        m2m_table_name = db.shorten_name('schools_school_instructors')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('school', models.ForeignKey(orm['schools.school'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['school_id', 'user_id'])

        # Adding field 'Session.school'
        db.add_column('schools_session', 'school',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=2, to=orm['schools.School']),
                      keep_default=False)

        # Adding field 'Course.school'
        db.add_column('schools_course', 'school',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=2, to=orm['schools.School']),
                      keep_default=False)


    def backwards(self, orm):
        # Removing M2M table for field students on 'School'
        db.delete_table(db.shorten_name('schools_school_students'))

        # Removing M2M table for field instructors on 'School'
        db.delete_table(db.shorten_name('schools_school_instructors'))

        # Deleting field 'Session.school'
        db.delete_column('schools_session', 'school_id')

        # Deleting field 'Course.school'
        db.delete_column('schools_course', 'school_id')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'unique': 'True'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['auth.Permission']", 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'user_set'", 'symmetrical': 'False', 'to': "orm['auth.Group']", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'user_set'", 'symmetrical': 'False', 'to': "orm['auth.Permission']", 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '30', 'unique': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'schools.course': {
            'Meta': {'object_name': 'Course'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instructors': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'course_instructors'", 'symmetrical': 'False', 'to': "orm['auth.User']"}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'courses'", 'to': "orm['schools.Location']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'school': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['schools.School']"}),
            'students': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'course_students'", 'symmetrical': 'False', 'to': "orm['auth.User']"})
        },
        'schools.location': {
            'Meta': {'object_name': 'Location'},
            'address_1': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'address_2': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'managers': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['auth.User']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'school': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'locations'", 'to': "orm['schools.School']"}),
            'state_province': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'zip_postal_code': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        'schools.school': {
            'Meta': {'object_name': 'School'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instructors': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'school_instructors'", 'symmetrical': 'False', 'to': "orm['auth.User']"}),
            'manager': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'manager'", 'to': "orm['auth.User']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'students': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'school_students'", 'symmetrical': 'False', 'to': "orm['auth.User']"})
        },
        'schools.session': {
            'Meta': {'object_name': 'Session'},
            'course': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['schools.Course']"}),
            'enddatetime': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'school': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['schools.School']"}),
            'startdatetime': ('django.db.models.fields.DateTimeField', [], {}),
            'students': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['auth.User']"})
        }
    }

    complete_apps = ['schools']