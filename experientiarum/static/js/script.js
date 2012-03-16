$(document).ready( function () {
        
        $("#date-input").datepicker({ dateFormat :'yy-mm-dd'});
        
        $(".ddd-wrapper").dotdotdot({
            wrapper: 'div',
            ellipsis: '... ',
            wrap : 'word',
            after: "a.read-more",
            watch: 'window',
            height: 500,
            tolerance: 0
        });
});

