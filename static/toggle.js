$(function() {
    $('button').click(function() {
        console.log('presionado');
        $.ajax({
            url: '/toggle/',
            type: 'GET',
            success: function(response) {
                console.log(response);
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
});/**
 * Created by simon on 3/06/2016.
 */
