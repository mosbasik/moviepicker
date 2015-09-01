
$(document).ready(function(){
    $('[data-toggle="tooltip"]').tooltip;
});


/***** ANIMATIONS FOR LOGIN PAGE *****/
$('#switch-to-create').click(function(e) {
    e.preventDefault()
    $('#user-login-form').fadeOut(function() {
        $('#user-create-form').fadeIn()
    })
})

$('#switch-to-login').click(function(e) {
    e.preventDefault()
    $('#user-create-form').fadeOut(function(){
        $('#user-login-form').fadeIn()
    })
})


/**
 * Triggers when clicking on a movie poster. A parent div of the movie poster
 * needs the imdb_id and it needs the class movie-vote
 */
$('.movie-image').click(function(e){
    e.preventDefault();
    var movie_id = $(this).parents('.movie-vote').attr('id')
    if ($('#' + movie_id).hasClass('liked')) {
        unvote(movie_id);
    } else {
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
            $('#'+id).removeClass('liked')
        },
    })
}


/**
 *
 */
$('#group-membership-button').click(function() {
    var group_pk = parseInt($(this).attr('data-group-pk'))
    var action = $(this).attr('data-group-action')
    if (action === 'join') {
        join_group(group_pk)
    } else if (action === 'leave') {
        leave_group(group_pk)
    }
})

function join_group(group_pk) {
    console.log('joining group #' + group_pk)
}

function leave_group(group_pk) {
    console.log('leaving group #' + group_pk)
}


// get the cookie containing the CSRF token (needed for POSTing with ajax)
function getCookie(name) {
  var value = "; " + document.cookie;
  var parts = value.split("; " + name + "=");
  if (parts.length == 2) return parts.pop().split(";").shift();
}
