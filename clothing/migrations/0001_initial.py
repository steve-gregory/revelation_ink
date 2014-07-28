# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Size'
        db.create_table('clothing_size', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
        ))
        db.send_create_signal('clothing', ['Size'])

        # Adding model 'Category'
        db.create_table('clothing_category', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['clothing.Category'], null=True, blank=True)),
        ))
        db.send_create_signal('clothing', ['Category'])

        # Adding model 'Item'
        db.create_table('clothing_item', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['clothing.Category'])),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('sku', self.gf('django.db.models.fields.CharField')(default='', max_length=255)),
            ('price', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=5, decimal_places=2)),
            ('markdownPrice', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=5, decimal_places=2)),
            ('featured', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('shown', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('featured_image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('front', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('back', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal('clothing', ['Item'])

        # Adding model 'Stock'
        db.create_table('clothing_stock', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('item', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['clothing.Item'])),
            ('size', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['clothing.Size'])),
            ('quantity', self.gf('django.db.models.fields.IntegerField')(default=-1)),
        ))
        db.send_create_signal('clothing', ['Stock'])

        # Adding model 'StockSold'
        db.create_table('clothing_stocksold', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('item', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['clothing.Item'])),
            ('size', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['clothing.Size'])),
            ('count', self.gf('django.db.models.fields.IntegerField')(default=1)),
        ))
        db.send_create_signal('clothing', ['StockSold'])

        # Adding model 'Transaction'
        db.create_table('clothing_transaction', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('full_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('email', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('shipping_info', self.gf('django.db.models.fields.TextField')()),
            ('billing_info', self.gf('django.db.models.fields.TextField')()),
            ('confirmation_id', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('shipped', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('clothing', ['Transaction'])

        # Adding M2M table for field items_sold on 'Transaction'
        m2m_table_name = db.shorten_name('clothing_transaction_items_sold')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('transaction', models.ForeignKey(orm['clothing.transaction'], null=False)),
            ('stocksold', models.ForeignKey(orm['clothing.stocksold'], null=False))
        ))
        db.create_unique(m2m_table_name, ['transaction_id', 'stocksold_id'])


    def backwards(self, orm):
        # Deleting model 'Size'
        db.delete_table('clothing_size')

        # Deleting model 'Category'
        db.delete_table('clothing_category')

        # Deleting model 'Item'
        db.delete_table('clothing_item')

        # Deleting model 'Stock'
        db.delete_table('clothing_stock')

        # Deleting model 'StockSold'
        db.delete_table('clothing_stocksold')

        # Deleting model 'Transaction'
        db.delete_table('clothing_transaction')

        # Removing M2M table for field items_sold on 'Transaction'
        db.delete_table(db.shorten_name('clothing_transaction_items_sold'))


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
            'markdownPrice': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '5', 'decimal_places': '2'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'price': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '5', 'decimal_places': '2'}),
            'quantity': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['clothing.Size']", 'through': "orm['clothing.Stock']", 'symmetrical': 'False'}),
            'shown': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'sku': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'})
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