# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'MemberCtg'
        db.create_table(u'newsletter_memberctg', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'newsletter', ['MemberCtg'])

        # Adding model 'Member'
        db.create_table(u'newsletter_member', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('firstname', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('lastname', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('cap', self.gf('django.db.models.fields.CharField')(max_length=5, null=True, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=128)),
            ('notes', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'newsletter', ['Member'])

        # Adding M2M table for field categories on 'Member'
        m2m_table_name = db.shorten_name(u'newsletter_member_categories')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('member', models.ForeignKey(orm[u'newsletter.member'], null=False)),
            ('memberctg', models.ForeignKey(orm[u'newsletter.memberctg'], null=False))
        ))
        db.create_unique(m2m_table_name, ['member_id', 'memberctg_id'])

        # Adding model 'Settings'
        db.create_table(u'newsletter_settings', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('site', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['sites.Site'], unique=True)),
            ('from_name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('from_email', self.gf('django.db.models.fields.EmailField')(max_length=128)),
            ('to_name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('to_email', self.gf('django.db.models.fields.EmailField')(max_length=128)),
            ('return_path', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('test_email', self.gf('django.db.models.fields.EmailField')(max_length=128)),
        ))
        db.send_create_signal(u'newsletter', ['Settings'])

        # Adding model 'Item'
        db.create_table(u'newsletter_item', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('creation_date', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('last_edit_date', self.gf('django.db.models.fields.DateField')(auto_now=True, auto_now_add=True, blank=True)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('public', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'newsletter', ['Item'])

        # Adding model 'Log'
        db.create_table(u'newsletter_log', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('item', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['newsletter.Item'])),
            ('success', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'newsletter', ['Log'])

        # Adding M2M table for field categories on 'Log'
        m2m_table_name = db.shorten_name(u'newsletter_log_categories')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('log', models.ForeignKey(orm[u'newsletter.log'], null=False)),
            ('memberctg', models.ForeignKey(orm[u'newsletter.memberctg'], null=False))
        ))
        db.create_unique(m2m_table_name, ['log_id', 'memberctg_id'])

        # Adding model 'LogError'
        db.create_table(u'newsletter_logerror', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('log', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['newsletter.Log'])),
            ('emails', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'newsletter', ['LogError'])


    def backwards(self, orm):
        # Deleting model 'MemberCtg'
        db.delete_table(u'newsletter_memberctg')

        # Deleting model 'Member'
        db.delete_table(u'newsletter_member')

        # Removing M2M table for field categories on 'Member'
        db.delete_table(db.shorten_name(u'newsletter_member_categories'))

        # Deleting model 'Settings'
        db.delete_table(u'newsletter_settings')

        # Deleting model 'Item'
        db.delete_table(u'newsletter_item')

        # Deleting model 'Log'
        db.delete_table(u'newsletter_log')

        # Removing M2M table for field categories on 'Log'
        db.delete_table(db.shorten_name(u'newsletter_log_categories'))

        # Deleting model 'LogError'
        db.delete_table(u'newsletter_logerror')


    models = {
        u'newsletter.item': {
            'Meta': {'object_name': 'Item'},
            'creation_date': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_edit_date': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'text': ('django.db.models.fields.TextField', [], {})
        },
        u'newsletter.log': {
            'Meta': {'object_name': 'Log'},
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['newsletter.MemberCtg']", 'null': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['newsletter.Item']"}),
            'success': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'newsletter.logerror': {
            'Meta': {'object_name': 'LogError'},
            'emails': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'log': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['newsletter.Log']"})
        },
        u'newsletter.member': {
            'Meta': {'object_name': 'Member'},
            'cap': ('django.db.models.fields.CharField', [], {'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['newsletter.MemberCtg']", 'null': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '128'}),
            'firstname': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lastname': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        u'newsletter.memberctg': {
            'Meta': {'object_name': 'MemberCtg'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        u'newsletter.settings': {
            'Meta': {'object_name': 'Settings'},
            'from_email': ('django.db.models.fields.EmailField', [], {'max_length': '128'}),
            'from_name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'return_path': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'site': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['sites.Site']", 'unique': 'True'}),
            'test_email': ('django.db.models.fields.EmailField', [], {'max_length': '128'}),
            'to_email': ('django.db.models.fields.EmailField', [], {'max_length': '128'}),
            'to_name': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        u'sites.site': {
            'Meta': {'ordering': "('domain',)", 'object_name': 'Site', 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['newsletter']