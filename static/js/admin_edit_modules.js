$(document).foundation('reflow');
$('.add__module').on("click", function(e) {
    $('#add__modal').foundation('reveal', 'open');
    $('#add__modal textarea').attr('rows', '7');
});

$('.open__profile__modal').on("submit", function(e) {
    e.preventDefault();
    var id = $(this).attr('id');
    $.getJSON($SCRIPT_ROOT + '/get_module_edit_info', {
	mid: id,
    }, function(data) {
	$('<input>').attr('type','hidden').appendTo('#profile__modal');
	$('#profile__modal input[name="id"]').val(id);
	$('#profile__modal input[type="text"]').val(data.name);
	$('#profile__modal textarea').val(data.blurb);
	$('#profile__modal textarea').attr('rows', '7');
    });
    $('#profile__modal').foundation('reveal', 'open');
});

$('a.status__mod').on("click", function(e) {
    e.preventDefault();
    var id = $(this).attr('href');
    $.getJSON($SCRIPT_ROOT + '/change_module_status', {
	mid: id,
    }, function(data) {
	if (data.result == 0) {
	    $msg = "Module status changed";
	    $type = "teal"
	} else {
	    $msg = data.result;
	    $type = "warning"
	}
	$(".module_err").html(function() {
	    return "<div data-alert class='alert-box quiz-feedback large-6 large-offset-3 columns " +
	    $type + " radius text-center'>" + "<b>" + $msg + "</b>" +
	    "<a href='#' class='close'>&times;</a>" + "</div>";
	});
	refresh();
    });
});

$("#new__module__form").on("submit", function(e){
    e.preventDefault();
    $.getJSON($SCRIPT_ROOT + '/add_module_profile', {
	name: $("#new__module__form input[type='text']").val(),
	blurb: $("#new__module__form textarea").val()
    }, function(data) {
	$('#add__modal').foundation('reveal', 'close');
	if (data.result == 0) {
	    $msg = "Successfully created new module";
	    $type = "teal"
	} else {
	    $msg = "Could not create new module";
	    $type = "warning"
	}
	$(".module_err").html(function() {
	    return "<div data-alert class='alert-box quiz-feedback large-6 large-offset-3 columns " +
	    $type + " radius text-center'>" + "<b>" + $msg + "</b>" +
	    "<a href='#' class='close'>&times;</a>" + "</div>";
	});
	refresh();
    });
});

$("#module__profile__form").on("submit", function(e){
    e.preventDefault();
    $.getJSON($SCRIPT_ROOT + '/edit_module_profile', {
	mid: $("#module__profile__form input[name='id']").val(),
	name: $("#module__profile__form input[type='text']").val(),
	blurb: $("#module__profile__form textarea").val()
    }, function(data) {
	$('#profile__modal').foundation('reveal', 'close');
	if (data.result == 0) {
	    $msg = "Successfully edited module profile!";
	    $type = "teal"
	} else {
	    $msg = "Could not edit module profile";
	    $type = "warning"
	}
	$(".module_err").html(function() {
	    return "<div data-alert class='alert-box quiz-feedback large-6 large-offset-3 columns " +
	    $type + " radius text-center'>" + "<b>" + $msg + "</b>" +
	    "<a href='#' class='close'>&times;</a>" + "</div>";
	});
	refresh();
    });
});

function refresh() {
    $(document).foundation();
    $(document).foundation('reflow');
    setTimeout(function(){window.location.reload(true);}, 500);
}
