var ajax_request = function(request_url, method_type, post_params, success_callback, fail_callback) {

    if (!success_callback) {
        success_callback = function() { };
        //console.log("success callback function does not exit. ajax_common_gateway") ;
    }
    if (!fail_callback) { fail_callback = function() { }; }
    $.ajax({
        url : request_url,
        //url : '/resources/json/' + method_name,
        type: method_type,
        data: method_params,
        accepts: 'application/json',
        success: function ( json ) {
            //Ext.MessageBox.alert('Success', 'Data return from the server: '+ result.responseText);
                var responseData = json;
                console.log(json)
                success_callback(json);
        },
        error: function (xhr, textStatus, errorThrown) {
            console.log(xhr);
            console.log(xhr.responseText);
            fail_callback();
        }
    });
}

