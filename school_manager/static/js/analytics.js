function myFunction()
{
alert("Page is loaded");
}

$( window ).load(function() {
        console.log( "window loaded" );
    });

model_url = 'http://127.0.0.1:8000/api'

model_list = $.ajax({
  dataType: "json",
  url: model_url,
  // data: data,
  // success: success
	
});   

model_list = $.getJSON(model_url, function(data){
    var html = '';
    var len = data.length;
    for (var i = 0; i< len; i++) {
        html += '<ul="' + data[i].monthId + '">' + data[i].month + '</ul>';
    }
    // $('select.month').append(html);
    console.log( "model_list", model_list );
    console.log( "html", html );   
    console.log( "data from model_list", len );       

});

// $( "#test" ).
