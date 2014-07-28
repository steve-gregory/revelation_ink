
$().ready(function() {
  $('#submit-cart').click( function() {
    window.location = '/cart/show/';
  });
});
$().ready(function() {
  $('.dropdown-toggle').dropdown();

  $("*[data-ajaxonload]").bind('mouseenter', function() {
    var e=$(this);
    var timeoutObj;
    e.unbind('mouseenter');
    $.get(e.data('ajaxonload'),function(d) {
        e.popover({
          content: d,
          html: true,
          container: 'body',
          placement: 'auto',
          trigger: "manual",
          template: '<div class="popover" onmouseover="$(this).mouseleave(function() {$(this).hide();});"><div class="arrow"></div><div class="popover-inner"><h3 class="popover-title"></h3><div class="popover-content"><p></p></div></div></div>'
          }).mouseenter(function(e) {
          $(this).popover('show');
          }).mouseleave(function(e) {
          var _this = this;
          setTimeout(function() {
          if (!$(".popover:hover").length) {
            $(_this).popover("hide");
           }
          }, 100);
          }).on("shown.bs.popover", function(e) {
            //Update popover form
            $('form').submit(function(){
              var csrf = $('input[name=csrfmiddlewaretoken]').val();
              var id = $(this).find("#item-id").val();
              var name = $(this).find("#item-name").val();
              var quantity = $('#quantity-select').val();
              var size = $('#size-select').val();
              var data_dict = {'id':id, 'name':name, 'quantity':quantity,'size':size, 'csrfmiddlewaretoken':csrf };
              add_to_cart(data_dict);
              $('#cart-modal').modal({'show':true});
              return false;
            });
          }).popover('show');
    });
  });


  //$('#cart-modal').modal('hide');
});
// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');
$(document).ready(function() {
  $('.aCarousel carousel').carousel({
  interval: 10000
  })
    
    $('.aCarousel carousel').on('slid.bs.carousel', function() {
      //alert("slid");
  });
    
    
});
