// Initialise settings for Reveal.js
Reveal.initialize({                                                             
	width: 1000,                                                                
        height: 600,                                                                
        minScale: 0.5,                                                              
        maxScale: 0.7,                                                              
        controls: true,                                                             
        progress: true,                                                             
        history: true,                                                              
        overview: false,                                                            
        transition: 'convex',                                                       
	showNotes: false,
        mouseWheel: false                                                           
});

// Add listeners for different classes of slides to change properties
Reveal.addEventListener('lecture', function() {
    Reveal.configure({
	keyboard: true,
	controls: true
      });
}, false );

Reveal.addEventListener('filler', function() {
    Reveal.configure({
	keyboard: true,
	controls: true
      });
}, false );

Reveal.addEventListener('interactive', function() {
    Reveal.configure({
	keyboard: false,
	touch: false,
	controls: false
      });
}, false );

Reveal.addEventListener('quiz', function() {
    Reveal.configure({
	keyboard: false,
	touch: false,
	controls: false
      });
}, false );

// The following script is the one we used to trigger
// the NotificationFx in the Interactive Scenario section 
// Following the code from Codrops by Tympanus
// http://tympanus.net/codrops/2014/07/23/notification-styles-inspiration/
$('.interact_select').click(function(e) {
    e.preventDefault();
    $aid = $(this).attr("id");
    // get selected option and delete the others
    var choice = $($(this).parent()).detach();
    $('#interact_answers').empty().append(choice);
    // currently doing manual check, will eventually check against database
    if ($aid == 1) {
	var notification = new NotificationFx({
	    wrapper : document.body,
	    message : 'Correct! Good Work!',
	    layout : 'other',
	    effect : 'boxspinner',
	    type : 'notice',
	});
    } else {
	var notification = new NotificationFx({
	    wrapper : document.body,
	    message : 'Wrong! You can\'t trust Mr Sugar Rush Cat.',
	    layout : 'other',
	    effect : 'boxspinner2',
	    type : 'error',
	});
    }

    notification.show();
    // after notification displays, create button with link to next slide
    $('#interact_answers').append('<div class="large-4 columns">\
		<button class="button radius green interact_select" id="next">\
		    <span class="content">Continue!</span>\
		</button>\
	    </div>');
});

// Sends user to next page on clicking Continue button in interactive section
$('#interact_answers').on('click', '#next', function(e) {
    e.preventDefault();
    Reveal.next();
});

// Sends answer to each quiz question off to another url to be checked
$('.question').bind('submit', function(e) {
    e.preventDefault();
    if (!$("input[type='radio']:checked").val()) {
	console.log("ANSWER THE THING");
    } else {
	$.getJSON($SCRIPT_ROOT + '/check_answer', {
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
		return "<input type='submit' class='tiny round green button next' value='Next'/>"
	    });                                                         
	});
    }
    return false;
});

$('.quiz_submit').on('click', '.next', function(e) {
    e.preventDefault();
    $(".q_err").empty();
    $(".quiz_submit").html(function() {                               
        return "<input type='submit' class='tiny round button' value='Submit'>"
    });                                                         
    Reveal.next();
});

Reveal.addEventListener( 'slidechanged', function( event ) {
    $("input[type='radio']").prop('checked', false);
    $.getJSON($SCRIPT_ROOT + '/update_user_progress',
	slide: Reveal.getState().indexh,
	name: $.trim($('p.title').text().split(":")[1])
    }, function(data) {
    });
});
