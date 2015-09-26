var $grid = $('.grid')

$(document).ready(function(){
    jQuery.timeago.settings.allowFuture = true;
    jQuery("abbr.timeago").timeago();
    $('[data-toggle="tooltip"]').tooltip;
    $grid.isotope({
        // options
        itemSelector: '.grid-item',

        layoutMode: 'fitRows',

        getSortData: {
            rating: '[data-rating]',
            truncated_title: '[data-truncated-title]',
            year: '[data-year]',
        },
        sortAscending: {
            rating: false,
            truncated_title: true,
            year: false,
        },
    })
})

// ========== login page animations ==========

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

// ========== isotope filter managment ==========

// filter items on button click
$('.filter-button-group').on( 'click', 'button', function() {
    var filterValue = $(this).attr('data-filter')
    $(this).addClass('btn-primary').siblings().removeClass('btn-primary');
    $grid.isotope({ filter: filterValue })
})

// sort items on button click
$('.sort-by-button-group').on( 'click', 'button', function() {
    var sortByValue = $(this).attr('data-sort-by')
    $(this).addClass('btn-primary').siblings().removeClass('btn-primary');
    $grid.isotope({ sortBy: sortByValue })
})

// ========== timezone cookie checks ==========

// note: longterm solution should be to create one page that sets the timezone,
// then check with django middleware if cookie is set.  if it's not set,
// redirect to the view that sets it, then use javascript from there to
// continue to the original destination when the cookie is set.  this allows
// the server to continually be aware of a user's time zone.

// try to get the timezone cookie
var timezone = getCookie("timezone")
console.log(timezone)

// if the timezone cookie has not been set yet
if ((typeof timezone === 'undefined') || (timezone === "")) {
    // create the timezone cookie and set to expire in seven days
    jstzResponse = jstz.determine()
    setCookie("timezone", jstzResponse.name(), 7)
}


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