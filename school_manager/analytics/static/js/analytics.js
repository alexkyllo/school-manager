//$(window).load(function() {
$(document).ready(function() {
    console.log("window loaded");
    // $("#measure1").css("border", "3px solid red");


    $.getJSON(model_url, function(data) {
        var html = '';
        for (var key in data) {
            html += '<ul class="dropdown-menu">' + key + '</ul>';
        }

        var htmls = '<ul class="dropdown-menu">helo</ul><ul class="dropdown-menu">heoollo</ul>'

        // (htmls).insertAfter('#ops')
        $("#ops").css("border", "3px solid red");

        $.each(data, function(index, item) {
            $('#dim_list').append(
                $('<li></li>').html('<a href="#">' + index + '</a>')
            );
        });

        console.log("html", html);

        for (var key in data) {
            console.log(key);
        }
    })

});

model_url = 'http://127.0.0.1:8000/api'


//model_list = $.ajax({
//dataType: "json",
//url: model_url,
// data: data,
// success: success

//});   




// $( "#test" ).