$().ready(function() {
  $('#shopping-cart-refresh').click(function() {
    refresh_cart();
  });
  refresh_cart();//Update on initialization
  $('#cart-modal').modal({'show':false});//Prepare modal dialog
  
});
var shoppingCartArr = [];
var add_to_cart = function(data_dict) {
  $.post('/cart/add/', data_dict, function(resp) {
    console.log(resp);
    refresh_cart();
  });
};

var update_cart = function(data) {
  var csrfSafeMethod = function(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
  };
  $.ajaxSetup({
    crossDomain: false,
    beforeSend: function(xhr, settings) {
      if (!csrfSafeMethod(settings.type)) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
  });
  $.post('/cart/update/', data, function(resp) {
    console.log(resp);
    refresh_cart();
  });
};

var refresh_cart = function() {
  $.getJSON('/cart/', function(cartItems) {
    console.log(cartItems);
    var item_list = [];
    shoppingCartArr = [];
    $.each(cartItems, function(index) {
      var item = cartItems[index];
      var totalprice = (item.price * item.quantity).toFixed(2);
      console.log(item);
      shoppingCartArr.push(item);
      item_list.push
       ('<tr class="cart-item" id="'+index+'">'+
         '<td>'+
           '<div class="input-append">'+
            '<input class="input-small cart-item-quantity" min="0" max="10" step="1" type="number" value="'+item.quantity+'"></input>'+
            '<span class="add-on remove-item"><i class="icon-remove"></i></span>'+
            '<span class="add-on update-item"><i class="icon-ok"></i></span>'+
           '</div>'+
         '</td>'+
         '<td><img class="thumbnail" src="'+item.image_url+'"/></td>'+
         '<td>'+item.name+'<br/>Size:'+item.size+'<br/>'+item.description+'</td>'+
         '<td class="cart-item-price">'+item.price+'</td>'+
         '<td class="cart-item-total">'+totalprice+'</td>'+
       '</tr>');
    });
    $('#shopping-cart-rows').html(item_list.join(''));
    //Initialize the new span classes
    $('.update-item').click(function() {
      var parentRow = $(this).parents().eq(2)[0];
      var itemID = parentRow.id;
      var item = shoppingCartArr[itemID];
      var item_price = $(parentRow.getElementsByClassName('cart-item-price')[0]).html();
      var item_quantity = $(parentRow.getElementsByClassName('cart-item-quantity')[0]).val();
      item.quantity = item_quantity;
      item.csrftoken = csrftoken;
      update_cart(item);
      var newTotal = item_price * item_quantity;
      $(parentRow.getElementsByClassName('cart-item-total')[0]).html(newTotal);
      
      console.log('stop')
    });
    $('.remove-item').click(function() {
      var parentRow = $(this).parents().eq(2)[0];
      var itemID = parentRow.id;
      var item = shoppingCartArr[itemID];
      item.quantity = 0;
      item.csrftoken = csrftoken;
      update_cart(item);
    });
  });
};
var review_transaction = function() {
  $.getJSON('/cart/', function(cartItems) {
    console.log(cartItems);
    var item_list = [];
    shoppingCartArr = [];
    $.each(cartItems, function(index) {
      var item = cartItems[index];
      var totalprice = (item.price * item.quantity).toFixed(2);
      console.log(item);
      shoppingCartArr.push(item);
      item_list.push
       ('<tr class="cart-item" id="'+index+'">'+
         '<td>'+
          '<input readonly="readonly" class="input-small cart-item-quantity" min="0" max="10" step="1" type="number" value="'+item.quantity+'"></input>'+
         '</td>'+
         '<td><img class="thumbnail" src="'+item.image_url+'"/></td>'+
         '<td>'+item.name+'<br/>Size:'+item.size+'<br/>'+item.description+'</td>'+
         '<td class="cart-item-price">'+item.price+'</td>'+
         '<td class="cart-item-total">'+totalprice+'</td>'+
       '</tr>');
    });
    $('#review-transaction-rows').html(item_list.join(''));
  });
};
