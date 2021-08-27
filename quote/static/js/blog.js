// Like
$(document).ready(function () {
    $(".like").click(function () {
        $(this).toggleClass("red");
        const userId = $('#userId').html()
        const postId = $('#postId').html()
        // const likeCounter = $('#likeCounter').html()
        $.ajax({

            url: '/api/like/',
            type: 'POST',
            data: {
                'userId': userId
                , 'postId': postId
            },

            success: function (data) {
                // const likeCounter = $('#likeCounter').html()
                if (data === 'Added') {
                    $('#likeCounter').html('Thanks for your support')

                } else {
                    $('#likeCounter').html('Do you like this post?')

                }
            }
            ,
            error: function (e) {


                console.log("ERROR : ", e);
            }
        });

    });
})
;


// Comment
// Send from data when user clicked on Send button
$(document).ready(function () {

    $("#comment-btn").click(function (event) {

        //Stop submit the form, we will post it manually.
        event.preventDefault();

        // Get form
        const form = $('#commentForm')[0];

        // Create an FormData object
        const data = new FormData(form);

        const comment = $('#comment').val()
        const postId = $('#postId').html()
        const userId = $('#userId').html()
        const userFirstName = $('#userFirstName').html()

        // Add an extra field for the FormData
        data.append("comment", comment);
        data.append("postId", postId);
        data.append("userId", userId);


        $.ajax({
            type: "POST",
            enctype: 'multipart/form-data',
            url: "/api/create_comment/",
            data: data,
            processData: false,
            contentType: false,
            cache: false,
            timeout: 600000,
            success: function () {

                // Cleaning comment text area
                $('#comment').val('')
                console.log("SUCCESS :");


                // Add comment which is sent by user
                $('#comment-row').append(`<div class="col-8 " id="comment-col"
                         style="border-bottom: 5px solid #797979;border-top: 5px solid #797979;margin-top: 25px;">
                        <h4>${userFirstName}</h4>
                        <p> ${comment} </p>
                    </div>`)

            },
            error: function (e) {


                console.log("ERROR : ", e);
                $("#createBtn").prop("disabled", false);

            }
        });

    });

});