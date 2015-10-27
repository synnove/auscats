// Initialise settings for Reveal.js
Reveal.initialize({                                                             
	width: 1100,
        height: 600,
        minScale: 0.5,
        maxScale: 0.9,
        controls: true,
        progress: false,
        history: true,
        overview: false,
        transition: 'convex',
	showNotes: false,
        mouseWheel: false                                                           
});

$('a#back').on('click', function(e) {
    e.preventDefault();
    $url = document.URL.replace(/#.*$/, "").split("/");
    $url = $url[$url.length - 1];
    window.location = '/drawingboard/' + $url;
});

// Sends answer to each quiz question off to another url to be checked
$('.question').bind('submit', function(e) {
    e.preventDefault();
    if (!$("input[type='radio']:checked").val()) {
	console.log("ANSWER THE THING");
    } else {
	$.getJSON($SCRIPT_ROOT + '/review_check_quiz_answer', {
	    aid: $("input[type='radio']:checked").val(),
	    qid: $(this).closest(".question").attr("id"),
	}, function(data) {
	    if (data.result == 0) {
		$msg = "Answer correct!";
		$type = "success"
	    } else if (data.result == 1) {
		$msg = "Wrong answer!";
		$type = "warning"
	    } else {
		$msg = "Invalid answer. Try again?";
		$type = "warning"
	    }
	    $(".q_err").html(function() {                               
		return "<div data-alert class='alert-box quiz-feedback " + 
		$type + " radius text-center'>" + "<b>" + $msg + "</b>" + 
		"<a href='#' class='close'>&times;</a>" + "</div>";
	    });                                                         
	    $(document).foundation();                                       
	    $(document).foundation('alert', 'reflow');
	    $(".quiz_submit").html(function() {                               
		return "<input type='submit' class='tiny radius success button next' value='Next'/>"
	    });                                                         
	});
    }
    return false;
});

$('.quiz_submit').on('click', '.next', function(e) {
    e.preventDefault();
    $(".q_err").empty();
    $(".quiz_submit").html(function() {                               
        return "<input type='submit' class='tiny radius purple button' value='Submit'>"
    });                                                         
    Reveal.next();
});

// Sends answer to each interactive question off to another url to be checked
$('.interactive_question').bind('submit', function(e) {
    e.preventDefault();
    $btn = $(document.activeElement);
    $btn.prop('disabled', true);
    $curr = '.interact_answers.int_' + $(this).closest("form").attr("id");
    $choice = $($btn.parent()).detach();
    $($curr + ' form').empty().append($choice);
    $($curr).append('<div class="large-4 large-offset-4 columns"><button class="button radius success interact_select" id="next"><span class="content">Continue!</span></button></div>');
    $.getJSON($SCRIPT_ROOT + '/review_check_int_answer', {
	aid: $btn.attr("id"),
	qid: $(this).closest("form").attr("id"),
    }, function(data) {
	if (data.result[0] == 0) {
	    $type = "success";
	    $title = "Awesome!";
	} else {
	    $type = "warning";
	    $title = "Whoops!";
	}
	$msg = data.result[1];
	$('.interactive_feedback').html('<div id="feedback_modal" class="small reveal-modal text-center ' + $type + '" data-reveal aria-hidden="false" role="dialog"><h3>' + $title + '</h3><p>' + $msg + '</p></div>');
	$('#feedback_modal').foundation('reveal', 'open');
	$(document).foundation();                                       
	$(document).foundation('alert', 'reflow');
    });
});

// Sends user to next page on clicking Continue button in interactive section
$('.interact_answers').on('click', '#next', function(e) {
    e.preventDefault();
    Reveal.next();
});

Reveal.addEventListener('slidechanged', function(e) {
    $("input[type='radio']").prop('checked', false);
    $.getJSON($SCRIPT_ROOT + '/update_user_progress', {
	slide: Reveal.getState().indexh,
	name: $.trim($('p.title').text().split(":")[1]),
    }, function(data) {
    });
});
