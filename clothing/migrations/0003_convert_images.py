# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):

    def forwards(self, orm):
        "Write your forwards methods here."
        # Note: Don't use "from appname.models import ModelName". 
        # Use orm.ModelName to refer to models in this application,
        # and orm['appname.ModelName'] for models in other applications.
        for item in orm.Item.objects.all():
            if item.front:
                front_image = orm.ItemImage(image=item.front, name="%s (front)" % item.name)
                front_image.save()
                item.images.add(front_image)
            if item.back:
                rear_image = orm.ItemImage(image=item.back, name="%s (back)" % item.name)
                rear_image.save()
                item.images.add(rear_image)


    def backwards(self, orm):
        "Write your backwards methods here."
        return

    models = {
        'clothing.category': {
            'Meta': {'object_name': 'Category'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['clothing.Category']", 'null': 'True', 'blank': 'True'})
        },
        'clothing.item': {
            'Meta': {'object_name': 'Item'},
            'back': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['clothing.Category']"}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'featured': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'featured_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'front': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'images': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['clothing.ItemImage']", 'symmetrical': 'False'}),
            'markdownPrice': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '5', 'decimal_places': '2'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'price': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '5', 'decimal_places': '2'}),
            'quantity': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['clothing.Size']", 'through': "orm['clothing.Stock']", 'symmetrical': 'False'}),
            'shown': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'sku': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'})
        },
        'clothing.itemimage': {
            'Meta': {'object_name': 'ItemImage'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'clothing.size': {
            'Meta': {'object_name': 'Size'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        'clothing.stock': {
            'Meta': {'object_name': 'Stock'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['clothing.Item']"}),
            'quantity': ('django.db.models.fields.IntegerField', [], {'default': '-1'}),
            'size': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['clothing.Size']"})
        },
        'clothing.stocksold': {
            'Meta': {'object_name': 'StockSold'},
            'count': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['clothing.Item']"}),
            'size': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['clothing.Size']"})
        },
        'clothing.transaction': {
            'Meta': {'object_name': 'Transaction'},
            'billing_info': ('django.db.models.fields.TextField', [], {}),
            'confirmation_id': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'full_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'items_sold': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['clothing.StockSold']", 'null': 'True', 'blank': 'True'}),
            'shipped': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'shipping_info': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['clothing']
    symmetrical = True
