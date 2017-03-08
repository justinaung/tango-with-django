$(document).ready( function() {
    $("#about-btn").click( function(event) {
        msgstr = $("#msg").html()
        msgstr = msgstr + "ooo"
        $('#msg').html()
    });

    $("p").hover( function() {
        $(this).css('color', 'red');
    },
    function() {
        $(this).css('color', 'black');
    });
});
