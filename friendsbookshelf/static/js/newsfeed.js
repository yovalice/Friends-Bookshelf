$(document).ready(function() {
    // Load more comments ajax
    $(".submit-comment").submit(function(event){
        var inputText = $(this).find('.comment-input');
        var commentBox = $(this).parents('.insert-comment-box').prev('.comments-box').find('.comments-box-ajax');

        $.ajax({
            type:"POST",
            url:"/ajax/comment/",
            data: {
                'text': inputText.val(),
                'post_id': $(this).parents('.ajax-post').attr('id')
            },
            success: function(data){
                var append_html = "<div class='detail-comment-box mb-2'><div class='user-comment-info'><a href='/user/" + data.user_id + "'><img class='newsfeed-comment-img-size rounded-circle' src='" + $('#comment-user-image').attr('val') + "' /><b> " + data.full_name + "</b></a><span class='user-comment-text'> " + inputText.val() + "</span></div></div><hr/ >";

                inputText.val('');
                commentBox.append(append_html);
            }
        });
        return false;

    });

    // Load more posts Ajax
    $("#load-more-posts").click(function(event){
        var inputText = $(this).parent('.input-group-append').prev();
        var commentBox = $(this).parents('.comments-box');
        $(this).prop('disabled', true);

        $.ajax({
            type:"POST",
            url:"/ajax/comment/",
            data: {
                'text': inputText.val(),
                'post_id': $(this).parents('.ajax-post').attr('id')
            },
            success: function(data){
                var append_html = "<div class='detail-comment-box'><div class='user-comment-info'><a href='/user/'{{ user.id }}>{% if user.image %}<img src='{{ user.image_thumbnail.url }}' class='rounded'>{% else %}<i class='fas fa-user'></i>{% endif %}<b>{{ user.first_name }} {{ user.last_name }}</b></a></div><div class='user-comment-text'>" + data.text + "</div></div>";

                commentBox.append(append_html);
                inputText.val('');
                $(this).prop('disabled', false);
            }
        });
        return false;
    });
});