# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Job.creation_date'
        db.add_column(u'newsletter_job', 'creation_date',
                      self.gf('django.db.models.fields.DateField')(auto_now_add=True, default=datetime.datetime(2013, 6, 11, 0, 0), blank=True),
                      keep_default=False)

        # Adding field 'Job.uncategorized'
        db.add_column(u'newsletter_job', 'uncategorized',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Subscription.code'
        db.add_column(u'newsletter_subscription', 'code',
                      self.gf('django.db.models.fields.CharField')(default='code', max_length=128),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Job.creation_date'
        db.delete_column(u'newsletter_job', 'creation_date')

        # Deleting field 'Job.uncategorized'
        db.delete_column(u'newsletter_job', 'uncategorized')

        # Deleting field 'Subscription.code'
        db.delete_column(u'newsletter_subscription', 'code')


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
            'creation_date': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'newsletter': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['newsletter.Newsletter']"}),
            'settings': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['newsletter.Settings']"}),
            'uncategorized': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
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
            'code': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
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