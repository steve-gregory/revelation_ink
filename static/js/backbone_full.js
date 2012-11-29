
//to Models
window.ShopItem = Backbone.Model.extend({
  urlRoot:'/api/item',
  defaults:{
    'id':null,
    'name':'',
    'description':'',
    'price':'$0.00',
    'markdown_price':'$0.00',
    'gender':'Male',
    'shown':'True',
    'front':'',
});

window.ShopItemCollection = Backbone.Collection.extend({
  model:ShopItem,
  url:"/api/item",
});

//toViews
window.ItemListView = Backbone.View.extend({
  tagName: 'ul',
  initialize:function() {
    this.model.bind("reset", this.render, this);
    var self = this;
    this.model.bind('add', function(item) {
      $(self.el).append(new ItemListItemView({model:item}).render().el);
    });
  },
  render:function (eventName) {
    _.each(this.model.models, function(item) {
      $(this.el).append(new ItemListItemView({model:item}).render().el);
    }, this);
    return this;
    }
  });

window.ItemListItemView = Backbone.View.extend({
  tagName:'li',
  template:_.template($('#tpl-item-list-item').html()),
  initialize: function() {
    this.model.bind('change', this.render, this);
    this.model.bind('destroy', this.render, this);
  },
  render: function (eventName) {
    $(this.el).html(this.template(this.model.toJSON()));
    return this;
  }
  close: function () {
    $(this.el).unbind();
    $(this.el).remove();
  }
});
window.ItemView = Backbone.View.extend({
  template: _.template($('#tpl-item-details').html()),

  initialize: function() {
    this.model.bind('change', this.render, this);
  },
  render: function(eventName) {
    $(this.el).html(this.template(this.model.toJSON()));
    return this;
  }
  events: {
    'change input':'change',
    'click .save':'saveItem',
    'click .delete':'deleteItem'
  },

  change: function(event) {
    var target = event.target;
    console.log('changing ' + target.id + ' from: ' + target.defaultValue + ' to: ' + target.value);
  },
  saveItem: function() {
    this.model.set({
      name:$('#name').val(),
      //TODO: Change this
      grapes:$('#grapes').val(),
      country:$('#country').val(),
      region:$('#region').val(),
      year:$('#year').val(),
      description:$('#description').val()
    });
    if (this.model.isNew()) {
      app.itemList.create(this.model);
    } else {
      this.model.save();
    }
    return false;
  },
  deleteItem: function() {
    this.model.destroy({
      success:function () {
        alert('Item deleted successfully');
        window.history.back();
      }
    });
    return false;
  },
  close:function () {
    $(this.el).unbind();
    $(this.el).empty();
  }
});

window.HeaderView = Backbone.View.extend({
 
    template:_.template($('#tpl-header').html()),
 
    initialize:function () {
        this.render();
    },
 
    render:function (eventName) {
        $(this.el).html(this.template());
        return this;
    },
 
    events:{
        "click .new":"newItem"
    },
 
    newItem:function (event) {
        if (app.itemView) app.itemView.close();
        app.itemView = new ItemView({model:new Item()});
        $('#content').html(app.itemView.render().el);
        return false;
    }
});
//toRouter
var AppRouter = Backbone.Router.extend({
  routes: {
    '':'list',
    'item/:id':'itemDetails'
  },
  initialize:function() {
    $('#header').html(new HeaderView().render().el);
  },
  list:function() {
    this.itemList = new ShopItemCollection();
    this.itemListView = new ItemListView({model:this.itemList});
    this.itemList.fetch();
    $("#sidebar").html(this.itemListView.render().el);
  },
  itemDetails: function(id) {
    this.item = this.itemList.get(id);
    if (app.itemView) app.itemView.close();
    this.itemView = new ItemView({model:this.item});
  }
});

var app = new AppRouter();
Backbone.history.start();
