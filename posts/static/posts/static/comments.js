
$(document).ready(function(){
    $(".reply-comments").click(function(event){
        console.log("I'm here");
        event.preventDefault();
        $(this).parent().next(".all-comments").next(".reply-form").show(1);
    });

    $(".show-comments").click(function(event){
        event.preventDefault();
        $(this).parent().next(".all-comments").show(1);
    });
});
