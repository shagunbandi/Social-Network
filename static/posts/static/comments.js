
$(document).ready(function(){
    $(".reply-comments").click(function(event){
        event.preventDefault();
        $(this).parent().next(".all-comments").next(".reply-form").show(400);
    });

    $(".show-comments").click(function(event){
        event.preventDefault();
        $(this).parent().next(".all-comments").show(400);
    });
});
