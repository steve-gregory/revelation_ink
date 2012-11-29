$().ready(function() {
  var updateTwitterFeed = function(username,count) {
    var tweets;
    $.getJSON("https://api.twitter.com/1/statuses/user_timeline.json?include_entities=true&include_rts=true&screen_name="+username+"&count="+count+"&callback=?", function(tweets) {
      var i = 0;
      $.each(tweets, function(i,post) {
				if (i < 5) {
          $("#twitter-list").append(
           '<li id="post'+i+'">'+post.text+'</li>'+
           '<li class="divider"></li>'
          );
				}
      });
    });
  };
  var username = "riclothingco";
  tweets = updateTwitterFeed(username,5);
});
