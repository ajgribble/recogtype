# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ChallengeFocuses'
        db.create_table('recogmatch_challengefocuses', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('first_letters', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('second_letters', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('third_letters', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('ending_letters', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('digraphs', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('trigraphs', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('doubles', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('common_2l_words', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('common_3l_words', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('common_4l_words', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('common_nl_words', self.gf('django.db.models.fields.CharField')(max_length=25)),
        ))
        db.send_create_signal('recogmatch', ['ChallengeFocuses'])

        # Deleting field 'Challenge.cType'
        db.delete_column('recogmatch_challenge', 'cType')

        # Adding field 'Challenge.challenge_type'
        db.add_column('recogmatch_challenge', 'challenge_type',
                      self.gf('django.db.models.fields.CharField')(default='f', max_length=10),
                      keep_default=False)

        # Adding field 'Challenge.challenge_use'
        db.add_column('recogmatch_challenge', 'challenge_use',
                      self.gf('django.db.models.fields.CharField')(default='t', max_length=10),
                      keep_default=False)

        # Adding M2M table for field challenge_focus on 'Challenge'
        db.create_table('recogmatch_challenge_challenge_focus', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('challenge', models.ForeignKey(orm['recogmatch.challenge'], null=False)),
            ('challengefocuses', models.ForeignKey(orm['recogmatch.challengefocuses'], null=False))
        ))
        db.create_unique('recogmatch_challenge_challenge_focus', ['challenge_id', 'challengefocuses_id'])


        # Changing field 'Challenge.title'
        db.alter_column('recogmatch_challenge', 'title', self.gf('django.db.models.fields.CharField')(max_length=50))
    def backwards(self, orm):
        # Deleting model 'ChallengeFocuses'
        db.delete_table('recogmatch_challengefocuses')

        # Adding field 'Challenge.cType'
        db.add_column('recogmatch_challenge', 'cType',
                      self.gf('django.db.models.fields.CharField')(default='f', max_length=10),
                      keep_default=False)

        # Deleting field 'Challenge.challenge_type'
        db.delete_column('recogmatch_challenge', 'challenge_type')

        # Deleting field 'Challenge.challenge_use'
        db.delete_column('recogmatch_challenge', 'challenge_use')

        # Removing M2M table for field challenge_focus on 'Challenge'
        db.delete_table('recogmatch_challenge_challenge_focus')


        # Changing field 'Challenge.title'
        db.alter_column('recogmatch_challenge', 'title', self.gf('django.db.models.fields.CharField')(max_length=30))
    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
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
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'recogmatch.biotemplate': {
            'Meta': {'object_name': 'BioTemplate'},
            'bio_model': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'recogmatch.challenge': {
            'Meta': {'object_name': 'Challenge'},
            'body': ('django.db.models.fields.TextField', [], {}),
            'challenge_focus': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['recogmatch.ChallengeFocuses']", 'symmetrical': 'False'}),
            'challenge_type': ('django.db.models.fields.CharField', [], {'default': "'f'", 'max_length': '10'}),
            'challenge_use': ('django.db.models.fields.CharField', [], {'default': "'t'", 'max_length': '10'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'recogmatch.challengefocuses': {
            'Meta': {'object_name': 'ChallengeFocuses'},
            'common_2l_words': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'common_3l_words': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'common_4l_words': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'common_nl_words': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'digraphs': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'doubles': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'ending_letters': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'first_letters': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'second_letters': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'third_letters': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'trigraphs': ('django.db.models.fields.CharField', [], {'max_length': '25'})
        },
        'recogmatch.rawsample': {
            'Meta': {'object_name': 'RawSample'},
            'challenge_id': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['recogmatch.Challenge']"}),
            'data': ('django.db.models.fields.TextField', [], {}),
            'date_supplied': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        }
    }

    complete_apps = ['recogmatch']