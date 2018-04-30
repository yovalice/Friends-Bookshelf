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

    $('.delete-post').click(function(){
        var form = $(this).find('form');

        swal({
          title: "Are you sure?",
          text: "You will delete this post forever.",
          type: "warning",
          showCancelButton: true,
          confirmButtonClass: "btn-primary",
          cancelButtonClass: "btn-danger",
          confirmButtonText: "Delete it!",
          cancelButtonText: "Cancel",
          closeOnConfirm: false,
          closeOnCancel: true
        },
        function(isConfirm) {
          if (isConfirm) {
            form.submit();
            swal("Deleted!", "Your Post is being deleted right now.", "success");
          }
        });
    });
});