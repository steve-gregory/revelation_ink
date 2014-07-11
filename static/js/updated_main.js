
$().ready(function() {
  $('#submit-cart').click( function() {
    window.location = '/cart/show/';
  });
});
$().ready(function() {
  $('.dropdown-toggle').dropdown();
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
