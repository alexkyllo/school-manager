//$(window).load(function() {
$(document).ready(function() {
    console.log("window loaded");
    // $("#measure1").css("border", "3px solid red");


    $("#chart_refresh").click(function() {
        $("#base_chart").attr("src", "/analytics/chart?" + d.getTime());
    })

    $("#base_chart").click(function() {
        $("#base_chart").attr("src", "/analytics/chart?" + d.getTime());
    })

    $("#dim_list").click(function() {
        $("#base_chart").attr("src", "/analytics/chart?" + d.getTime());
    })

    $("#measure_list").click(function() {
        $("#base_chart").attr("src", "/analytics/chart?" + d.getTime());
    })

    $("#chart_refresh_bottom").click(function() {
        $("#base_chart").attr("src", "/analytics/chart?" + d.getTime());
    })

    $("#chart_refresh_bottom").click(function() {
        $(".bchart").attr("src", "/analytics/chart?" + d.getTime());
    })


    $.getJSON(model_url, function(data) {

        $("#ops").css("border", "3px solid red");

        $.each(data, function(index, item) {
            $('#dim_list').append(
                $('<li class="lis"></li>').html('<a id="l' + index + '" class="model_link" href="#">' + index + '</a>')
            );
        });

        for (var key in data) {
            console.log(key);
        }
    })

});

model_url = 'http://127.0.0.1:8000/api'

d = new Date();
