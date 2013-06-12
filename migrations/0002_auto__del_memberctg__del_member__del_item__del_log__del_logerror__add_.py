# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'MemberCtg'
        db.delete_table(u'newsletter_memberctg')

        # Deleting model 'Member'
        db.delete_table(u'newsletter_member')

        # Removing M2M table for field categories on 'Member'
        db.delete_table(db.shorten_name(u'newsletter_member_categories'))

        # Deleting model 'Item'
        db.delete_table(u'newsletter_item')

        # Deleting model 'Log'
        db.delete_table(u'newsletter_log')

        # Removing M2M table for field categories on 'Log'
        db.delete_table(db.shorten_name(u'newsletter_log_categories'))

        # Deleting model 'LogError'
        db.delete_table(u'newsletter_logerror')

        # Adding model 'Job'
        db.create_table(u'newsletter_job', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('newsletter', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['newsletter.Newsletter'])),
            ('settings', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['newsletter.Settings'])),
        ))
        db.send_create_signal(u'newsletter', ['Job'])

        # Adding M2M table for field categories on 'Job'
        m2m_table_name = db.shorten_name(u'newsletter_job_categories')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('job', models.ForeignKey(orm[u'newsletter.job'], null=False)),
            ('subscriptionctg', models.ForeignKey(orm[u'newsletter.subscriptionctg'], null=False))
        ))
        db.create_unique(m2m_table_name, ['job_id', 'subscriptionctg_id'])

        # Adding model 'Dispatch'
        db.create_table(u'newsletter_dispatch', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('job_dispatch', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['newsletter.JobDispatch'])),
            ('subscription', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['newsletter.Subscription'])),
            ('success', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'newsletter', ['Dispatch'])

        # Adding model 'SubscriptionCtg'
        db.create_table(u'newsletter_subscriptionctg', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'newsletter', ['SubscriptionCtg'])

        # Adding model 'Subscription'
        db.create_table(u'newsletter_subscription', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('firstname', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('lastname', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('cap', self.gf('django.db.models.fields.CharField')(max_length=5, null=True, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=128)),
            ('notes', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'newsletter', ['Subscription'])

        # Adding M2M table for field categories on 'Subscription'
        m2m_table_name = db.shorten_name(u'newsletter_subscription_categories')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('subscription', models.ForeignKey(orm[u'newsletter.subscription'], null=False)),
            ('subscriptionctg', models.ForeignKey(orm[u'newsletter.subscriptionctg'], null=False))
        ))
        db.create_unique(m2m_table_name, ['subscription_id', 'subscriptionctg_id'])

        # Adding model 'Newsletter'
        db.create_table(u'newsletter_newsletter', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('creation_date', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('last_edit_date', self.gf('django.db.models.fields.DateField')(auto_now=True, auto_now_add=True, blank=True)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('public', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'newsletter', ['Newsletter'])

        # Adding model 'JobDispatch'
        db.create_table(u'newsletter_jobdispatch', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('job', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['newsletter.Job'])),
        ))
        db.send_create_signal(u'newsletter', ['JobDispatch'])

        # Deleting field 'Settings.site'
        db.delete_column(u'newsletter_settings', 'site_id')

        # Adding field 'Settings.label'
        db.add_column(u'newsletter_settings', 'label',
                      self.gf('django.db.models.fields.CharField')(default='test', max_length=128),
                      keep_default=False)


    def backwards(self, orm):
        # Adding model 'MemberCtg'
        db.create_table(u'newsletter_memberctg', (
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'newsletter', ['MemberCtg'])

        # Adding model 'Member'
        db.create_table(u'newsletter_member', (
            ('firstname', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('date', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('lastname', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('notes', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('cap', self.gf('django.db.models.fields.CharField')(max_length=5, null=True, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=128)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
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

        # Adding model 'Item'
        db.create_table(u'newsletter_item', (
            ('text', self.gf('django.db.models.fields.TextField')()),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('creation_date', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('last_edit_date', self.gf('django.db.models.fields.DateField')(auto_now=True, auto_now_add=True, blank=True)),
            ('public', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'newsletter', ['Item'])

        # Adding model 'Log'
        db.create_table(u'newsletter_log', (
            ('success', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('item', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['newsletter.Item'])),
            ('date', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
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
            ('log', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['newsletter.Log'])),
            ('emails', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'newsletter', ['LogError'])

        # Deleting model 'Job'
        db.delete_table(u'newsletter_job')

        # Removing M2M table for field categories on 'Job'
        db.delete_table(db.shorten_name(u'newsletter_job_categories'))

        # Deleting model 'Dispatch'
        db.delete_table(u'newsletter_dispatch')

        # Deleting model 'SubscriptionCtg'
        db.delete_table(u'newsletter_subscriptionctg')

        # Deleting model 'Subscription'
        db.delete_table(u'newsletter_subscription')

        # Removing M2M table for field categories on 'Subscription'
        db.delete_table(db.shorten_name(u'newsletter_subscription_categories'))

        # Deleting model 'Newsletter'
        db.delete_table(u'newsletter_newsletter')

        # Deleting model 'JobDispatch'
        db.delete_table(u'newsletter_jobdispatch')

        # Adding field 'Settings.site'
        db.add_column(u'newsletter_settings', 'site',
                      self.gf('django.db.models.fields.related.OneToOneField')(default=0, to=orm['sites.Site'], unique=True),
                      keep_default=False)

        # Deleting field 'Settings.label'
        db.delete_column(u'newsletter_settings', 'label')


    models = {
        u'newsletter.dispatch': {
            'Meta': {'object_name': 'Dispatch'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'job_dispatch': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['newsletter.JobDispatch']"}),
            'subscription': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['newsletter.Subscription']"}),
            'success': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'newsletter.job': {
            'Meta': {'object_name': 'Job'},
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['newsletter.SubscriptionCtg']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'newsletter': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['newsletter.Newsletter']"}),
            'settings': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['newsletter.Settings']"})
        },
        u'newsletter.jobdispatch': {
            'Meta': {'object_name': 'JobDispatch'},
            'date': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'job': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['newsletter.Job']"})
        },
        u'newsletter.newsletter': {
            'Meta': {'object_name': 'Newsletter'},
            'creation_date': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_edit_date': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'text': ('django.db.models.fields.TextField', [], {})
        },
        u'newsletter.settings': {
            'Meta': {'object_name': 'Settings'},
            'from_email': ('django.db.models.fields.EmailField', [], {'max_length': '128'}),
            'from_name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'return_path': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'test_email': ('django.db.models.fields.EmailField', [], {'max_length': '128'}),
            'to_email': ('django.db.models.fields.EmailField', [], {'max_length': '128'}),
            'to_name': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        u'newsletter.subscription': {
            'Meta': {'object_name': 'Subscription'},
            'cap': ('django.db.models.fields.CharField', [], {'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['newsletter.SubscriptionCtg']", 'null': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '128'}),
            'firstname': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lastname': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        u'newsletter.subscriptionctg': {
            'Meta': {'object_name': 'SubscriptionCtg'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        }
    }

    complete_apps = ['newsletter']