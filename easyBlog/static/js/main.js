$(document).ready(function() {
    $('#like button:first').click(function(event) {
        event.preventDefault();
        var element = $(this);

        $.ajax({
            url: '/blog/add_blog/',
            type: 'POST',
            data: {blog_id: $(this).attr("data-id")},

            success: function(data) {
                if (data === 'add') {
                    $('#like_num').text(parseInt($('#like_num').text())+1);
                    $('#new_like').text("取消点赞");
                } else if (data === 'remove') {
                    $('#like_num').text(parseInt($('#like_num').text())-1);
                    $('#new_dislike').text("点赞");
                } else {
                    alert("请先登录!");
                }
            },
            error: function(data) {
                alert("请先登录!");
            }
        })
    });

    $('#follow button:first').click(function(event) {
        event.preventDefault();
        var element = $(this);

        $.ajax({
            url: '/blog/add_fan_users/',
            type: 'POST',
            data: {blog_id: $(this).attr("data-id")},

            success: function(data) {
                if (data === 'add') {
                    $('#follow_num').text(parseInt($('#follow_num').text())+1);
                    $('#new_follow').text("取消关注");
                } else if (data === 'remove') {
                    $('#follow_num').text(parseInt($('#follow_num').text())-1);
                    $('#new_unfollow').text("关注");
                } else {
                    alert("不能关注自己!");
                }
            },
            error: function(data) {
                alert("请先登录!");
            }
        })
    });

//    $('#test_blog_comment button:first').click(function(event) {
//        event.preventDefault();
//        alert("test");
//        $.ajax({
//            url: '/blog/vote_blog_comment/',
//            type: 'POST',
//            data: {blog_comment_id: $(this).attr("data-f")},
//
//            success: function(data) {
//                if (data === 'up') {
//                    like_id = "#like_i_"+$(this).attr("data-f");
//                    alert(like_id);
//                    $(like_id).removeClass("text-muted").addClass("text-danger");
//                } else {
//                    dislike_id = "#dislike_i_"+$(this).attr("data-f");
//                    alert(dislike_id);
//                    $(dislike_id).removeClass("text-danger").addClass("text-muted");
//                }
//            },
//            error: function(data) {
//                alert("请先登录!");
//            }
//        })
//    });

})