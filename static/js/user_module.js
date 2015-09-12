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
    $url = "/check_answer/qid="
    e.preventDefault();
    $qid = $(this).closest(".question").attr("id");
    $url += $qid + "&aid=";
    $aid = $("input[type='radio']:checked").val();
    $url += $aid;
    window.location = $url;
});
