$(document).ready(function() {
    var rate = 10; // seconds
    var url = '/number_deadlines';
    var n = $('#number_deadlines').text();

    function update_deadlines() {
        $.getJSON(url).done(function(data) {
            console.log('Deadlines: ' + data['number_deadlines']);
            
            var current = data['number_deadlines'];

            if (n != current) {
                $('#number_deadlines').text(data['number_deadlines']);
                $('#number_deadlines').css("color", "red");
            }
        });
    }

    var get_loop = setInterval(update_deadlines, rate * 1000);
});
