$(document).ready(function() {
    $('.read-more').click(function(event){
        event.preventDefault() 
        $(this).parent('.short-text').toggleClass('d-none').next().toggleClass('d-none');
    });

    $('.read-less').click(function(event){
        event.preventDefault() 
        $(this).parent('.full-text').toggleClass('d-none').prev().toggleClass('d-none');
    });
});