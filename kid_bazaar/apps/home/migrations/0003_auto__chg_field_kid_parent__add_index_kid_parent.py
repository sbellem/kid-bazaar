# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Renaming column for 'Kid.parent' to match new field type.
        db.rename_column(u'home_kid', 'parent', 'parent_id')
        # Changing field 'Kid.parent'
        db.alter_column(u'home_kid', 'parent_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['home.KBUser']))
        # Adding index on 'Kid', fields ['parent']
        db.create_index(u'home_kid', ['parent_id'])


    def backwards(self, orm):
        # Removing index on 'Kid', fields ['parent']
        db.delete_index(u'home_kid', ['parent_id'])


        # Renaming column for 'Kid.parent' to match new field type.
        db.rename_column(u'home_kid', 'parent_id', 'parent')
        # Changing field 'Kid.parent'
        db.alter_column(u'home_kid', 'parent', self.gf('django.db.models.fields.IntegerField')())

    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'home.item': {
            'Meta': {'object_name': 'Item'},
            'age_from': ('django.db.models.fields.IntegerField', [], {}),
            'age_to': ('django.db.models.fields.IntegerField', [], {}),
            'category': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.Kid']"}),
            'pic': ('cloudinary.models.CloudinaryField', [], {'max_length': '100'}),
            'price': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '7', 'decimal_places': '2'}),
            'used_till': ('django.db.models.fields.DateField', [], {})
        },
        u'home.itemrequest': {
            'Meta': {'object_name': 'ItemRequest'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.Item']"}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'items_sold'", 'to': u"orm['home.KBUser']"}),
            'requesting_user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'items_wanted'", 'to': u"orm['home.KBUser']"}),
            'status': ('django.db.models.fields.TextField', [], {'default': "'PENDING'"})
        },
        u'home.kbuser': {
            'Meta': {'object_name': 'KBUser'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'merchant_id': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"})
        },
        u'home.kid': {
            'Meta': {'object_name': 'Kid'},
            'birthday': ('django.db.models.fields.DateField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.KBUser']"}),
            'pic': ('cloudinary.models.CloudinaryField', [], {'max_length': '100'}),
            'sex': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        }
    }

    complete_apps = ['home']