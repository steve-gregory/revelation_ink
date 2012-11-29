window.ShopItem = Backbone.Model.extend();
window.ShopItemCollection = Backbone.Collection.extend({
	model:ShopItem,
	url:"/api/item",
});

