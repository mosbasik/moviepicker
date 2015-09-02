
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
    var group_slug = $(this).attr('data-group-slug')
    var action = $(this).attr('data-group-action')
    if (action === 'join') {
        join_group(this, group_slug)
    } else if (action === 'leave') {
        leave_group(this, group_slug)
    }
})

function join_group(button, group_slug) {
    var group_url = '/group/' + group_slug + '/'
    $.ajax({
        url: group_url + 'join/',
        method: 'POST',
        data: {
            group_slug: group_slug,
        },
        beforeSend: function(xhr) {
            xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'))
        },
        success: function() {
            location.reload()
        },
        error: function() {
            window.location.replace('/login/?next=' + group_url)
        }
    })
}

function leave_group(button, group_slug) {
    var group_url = '/group/' + group_slug + '/'
    $.ajax({
        url: group_url + 'leave/',
        method: 'POST',
        data: {
            group_slug: group_slug,
        },
        beforeSend: function(xhr) {
            xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'))
        },
        success: function() {
            location.reload()
        },
        error: function() {
            window.location.replace('/login/?next=' + group_url)
        }
    })
}


// get the cookie containing the CSRF token (needed for POSTing with ajax)
function getCookie(name) {
  var value = "; " + document.cookie;
  var parts = value.split("; " + name + "=");
  if (parts.length == 2) return parts.pop().split(";").shift();
}

$('#event-membership-button').click(function(){
    var event_id = $(this).attr('data-event-id')
    var action = $(this).attr('data-event-action')
    var group_slug = $(this).attr('event-group-slug')
    console.log(this, action, group_slug)

    if (action === 'join') {
        join_event(group_slug, event_id)
    } else if(action === 'leave') {
        leave_event(group_slug, event_id)
    }
})

function join_event(group_slug, event_id) {
    console.log('started Join function')
    var event_url = '/group/' + group_slug + '/event/' + event_id + '/'
    $.ajax({
        url: event_url + 'join/',
        method: 'POST',
        data: {
            group_slug: group_slug,
            event_id: event_id
        },
        beforeSend: function(xhr) {
            xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'))
        },
        success: function() {
            location.reload()
        },
        error: function() {
            window.location.replace('/login/?next=' + event_url)
        }
    })
}
function leave_event(group_slug, event_id) {
    console.log('started Leave function')
    var event_url = '/group/' + group_slug + '/event/' + event_id + '/'
    $.ajax({
        url: event_url + 'leave/',
        method: 'POST',
        data: {
            group_slug: group_slug,
            event_id: event_id
        },
        beforeSend: function(xhr) {
            xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'))
        },
        success: function() {
            location.reload()
        },
        error: function() {
            window.location.replace('/login/?next=' + event_url)
        }
    })
}