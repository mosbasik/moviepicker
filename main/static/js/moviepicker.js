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

$('.dropdown-menu').on('click', function (e) {
e.stopPropagation() 
})

$(document).ready(function(){
    $('[data-toggle="tooltip"]').tooltip();
});

// focus on text box on page load
$(function() {
  $("input").focus();
});




/***** VOTE FUNCTIONALITY *****/
// triggers when clicking on a movie poster
// a parent div of the movie poster needs the imdb_id and
// it needs the class movie-vote
$('.movie-image').click(function(e){
    e.preventDefault();

    var movie_id = $(this).parents('.movie-vote').attr('id')

    if ($('#' + movie_id).hasClass('liked')) {
        // unvote
        unvote(movie_id);
    } else {
        // vote
        vote(movie_id);
    }

})


function vote(id) {
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
            console.log('voted')
            $('#'+id).addClass('liked')
        },
    })
}


function unvote(id) {

    $.ajax({
        url: '/delete-vote/',
        method: 'POST',
        data: {
            id: id
        },
        beforeSend: function(xhr) {
            xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'))
        },
        success: function() {
            console.log('unvoted')
            $('#'+id).removeClass('liked')
        },
    })
}


// get the cookie containing the CSRF token (needed for POSTing with ajax)
function getCookie(name) {
  var value = "; " + document.cookie;
  var parts = value.split("; " + name + "=");
  if (parts.length == 2) return parts.pop().split(";").shift();
}
