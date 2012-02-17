$(document).ready( function () {

    // Autopopulate slug
    /**
    $('input #title').bind('input', function () {
        console.log($(this).val());
        
    });
    */

    // Append and |> to the end of any truncated HTML blog posts
    $('div .blog-entry-body p').each( function() {
        var str = $(this).text();

        if (str.lastIndexOf(' ...') >= 0) {
           $(this).append('<p id="readmore">&#x25b6;</p>');
        }
    });  

    // When |> is clicked, slide down the content
    $('p #readmore').each( function () {
        $(this).click( function() {
            $(this).parent('div .blog-entry-body').slideToggle('slow' function {
                // Animation complete.
            });
        });
    });
});

