jQuery(document).ready(function($) {
    var index = 0;
    $("#navbar-menu .nav-item .nav-link").each(function(oi) {
        var url = $(this).attr("href")
        var pathname = window.location.pathname.substr(0,url.length)
        if (pathname == url) { index = oi; }
    });
    $("#navbar-menu .nav-item").eq(index).addClass('active');
});

(function( jQuery, window ){
    jQuery.fn.serializeObject = function() {
        var obj = null;
        try {
            if (this[0].tagName && this[0].tagName.toUpperCase() == "FORM") {
                var arr = this.serializeArray();
                if (arr) {
                    obj = {};
                    jQuery.each(arr, function() {
                        obj[this.name] = this.value;
                    });
                }//if ( arr ) {
            }
        } catch (e) {
            alert(e.message);
        } finally {
        }
        
        return obj;
    };
})( jQuery, window );

function ajaxReady(ajax) {
    jQuery.ajax({
        url: ajax.url,
        type: ajax.type,
        headers: { 'X-CSRFTOKEN' : ajax.csrf },
        data: ajax.data,
        dataType: ajax.dataType,
        success:function(data) {
            if (typeof ajax.success === 'function') {
                ajax.success(data);
            }
        },
        error : function(xhr,errmsg,err) {
            console.log(xhr.status + ": " + xhr.responseText); 
        }
    });
}
