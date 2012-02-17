$(document).ready( 

   $('#title').bind('input', function() {
        $('#slug').attr('val', $(this).val());
   });

);

