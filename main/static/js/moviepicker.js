/***** ANIMATION FOR LOGIN PAGE *****/
$('#switch-to-create').click(function(e){
    e.preventDefault();

    $('#user-login-form').fadeOut(function(){
        $('#user-create-form').fadeIn()
    });
    
})

$('#switch-to-login').click(function(e){
    e.preventDefault();

    $('#user-create-form').fadeOut(function(){
        $('#user-login-form').fadeIn()
    });
    
})


function vote(button) {
    var movie = button.closest('.movie')
    var id = $(movie).attr('data-movie-id')

    $.ajax({
        url: '/create-vote/',
        method: 'POST',
        data: {
            id: id
        },
        beforeSend: function(xhr) {
            xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'))
        },
        success: function() {
            $(button).removeClass('fa fa-star')
            $(button).removeClass('favorite-button')
            $(button).addClass('fa fa-star-o')
            $(button).addClass('unfavorite-button')
        },
    })
}


function unvote(button) {
    var movie = button.closest('.movie')
    var id = $(movie).attr('data-movie-id')

    $.ajax({
        url: '/create-vote/',
        method: 'POST',
        data: {
            id: id
        },
        beforeSend: function(xhr) {
            xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'))
        },
        success: function() {
            $(button).removeClass('fa fa-star-o')
            $(button).removeClass('unfavorite-button')
            $(button).addClass('fa fa-star')
            $(button).addClass('favorite-button')
        },
    })
}


// get the cookie containing the CSRF token (needed for POSTing with ajax)
function getCookie(name) {
  var value = "; " + document.cookie;
  var parts = value.split("; " + name + "=");
  if (parts.length == 2) return parts.pop().split(";").shift();
}