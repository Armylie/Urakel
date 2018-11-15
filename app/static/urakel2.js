$(function() {
    var timer = null;
    $('.user_popup').hover(
        function(event) {
            // mouse in event handler
            var elem = event.currentTarget;
            timer = setTimeout(function() {
                timer = null;
                // popup logic goes here
            }, 1000);
        },
        function(event) {
            // mouse out event handler
            var elem = event.currentTarget;
            if (timer) {
                clearTimeout(timer);
                timer = null;
            }
        }
    )
});