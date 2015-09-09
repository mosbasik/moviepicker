
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
            var votes = $('#'+id).find('.num-votes')
            var current_vote_count = parseInt($(votes).html())
            $(votes).html(current_vote_count + 1)
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
            var votes = $('#'+id).find('.num-votes')
            var current_vote_count = parseInt($(votes).html())
            $(votes).html(current_vote_count - 1)
        },
    })
}

// ========== Group Membership Mangement ==========

$('.join-group-button, .leave-group-button').click(function(e){
    e.preventDefault();
    var action = $(this).attr('data-group-action')
    var group_slug = $(this).attr('data-group-slug')
    $.ajax({
        url: window.location.href,
        method: 'POST',
        data: {
            action: action,
            group_slug: group_slug,
        },
        beforeSend: function(xhr) {
            xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'))
        },
        success: function(data) {
            if (data.redirect) {
                window.location.replace(data.redirect)
            } else {
                location.reload()
            }
        },
    })
})


// ========== Get CSRF Cookie ==========

// get the cookie containing the CSRF token (needed for POSTing with ajax)
function getCookie(name) {
  var value = "; " + document.cookie;
  var parts = value.split("; " + name + "=");
  if (parts.length == 2) return parts.pop().split(";").shift();
}

// ========== Event Membership Mangement ==========

$('.join-event-button').click(function(e){
    e.preventDefault();
    var group_slug = $(this).attr('data-group-slug')
    var event_id = $(this).attr('data-event-id')
    var join_event_url = '/group/' + group_slug + '/event/' + event_id + '/join/'

    $.ajax({
        url: join_event_url,
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
            window.location.replace('/login/?next=' + join_event_url)
        }
    })
})

$('.leave-event-button').click(function(e){
    e.preventDefault();
    var group_slug = $(this).attr('data-group-slug')
    var event_id = $(this).attr('data-event-id')
    var leave_event_url = '/group/' + group_slug + '/event/' + event_id + '/leave/'

    $.ajax({
        url: leave_event_url,
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
            window.location.replace('/login/?next=' + leave_event_url)
        }
    })
})

$('.delete-lockin').click(function(){
    var lockin = $(this).attr('data-lockin-id')
    var group_slug = $(this).attr('data-group-slug')
    var event_id = $(this).attr('data-event-id')
    var event_url = '/group/' + group_slug + '/event/' + event_id + '/'
    var movie = $(this).attr('data-movie-id')
    if (confirm('Are you sure you want to remove this Locked in movie?')){
        $.ajax({
            url: event_url,
            method: 'POST',
            data: {
                type: 'delete',
                group_slug: group_slug,
                event_id: event_id,
                movie: movie,
            },
            beforeSend: function(xhr) {
                xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'))
            },
            success: function() {
                location.reload()
            },
        })
    }
})