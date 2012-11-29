from django.contrib import admin
from clothing.models import Category, Item, Size, Stock, StockSold, Transaction
#from clothing.models import ItemSize

class CategoryAdmin(admin.ModelAdmin):
	pass

class SizeAdmin(admin.ModelAdmin):
	pass

class TransactionAdmin(admin.ModelAdmin):
	list_filter = ['full_name','email']
	filter_vertical = ['items_sold',]

class StockInline(admin.TabularInline):
	model = Stock

class ItemAdmin(admin.ModelAdmin):
	list_filter = ['category','markdownPrice','featured','shown']
	inlines = [
	StockInline,
	]



admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Size, SizeAdmin)

#class ItemSizeAdmin(admin.ModelAdmin):
#	pass
#admin.site.register(ItemSize, ItemSizeAdmin)
