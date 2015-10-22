$('#edit__lecture').on("click", function(e) {
    $('#edit__lecture').addClass('current');
    $('#edit__interactive').removeClass('current');
    $('#edit__quiz').removeClass('current');
    if ($('#lecture').hasClass('hidden')) {
	$('#lecture').toggleClass('hidden');
    }
    $('#interactive').addClass('hidden');
    $('#quiz').addClass('hidden');
});

$('#edit__interactive').on("click", function(e) {
    $('#edit__interactive').addClass('current');
    $('#edit__lecture').removeClass('current');
    $('#edit__quiz').removeClass('current');
    if ($('#interactive').hasClass('hidden')) {
	$('#interactive').toggleClass('hidden');
    }
    $('#lecture').addClass('hidden');
    $('#quiz').addClass('hidden');
});

$('#edit__quiz').on("click", function(e) {
    $('#edit__quiz').addClass('current');
    $('#edit__interactive').removeClass('current');
    $('#edit__lecture').removeClass('current');
    if ($('#quiz').hasClass('hidden')) {
	$('#quiz').toggleClass('hidden');
    }
    $('#lecture').addClass('hidden');
    $('#interactive').addClass('hidden');
});

$div = window.location.hash;
if ($div == "#lecture" || $div == "#interactive" || $div == "#quiz") {
    $('#lecture').addClass('hidden');
    $('#interactive').addClass('hidden');
    $('#quiz').addClass('hidden');
    $($div).removeClass('hidden');
    $breadcrumb = "#edit__" + $div.substring(1);
    $('#edit__lecture').removeClass('current');
    $('#edit__interactive').removeClass('current');
    $('#edit__quiz').removeClass('current');
    $($breadcrumb).addClass('current');
}

$('#create_new_question').on("submit", function(e) {
    e.preventDefault();
    $.getJSON($SCRIPT_ROOT + '/add_new_question', {
	q: $('input:text[name=q_new]').val(),
	a1: $('input:text[name=q_new_a_1]').val(),
	a2: $('input:text[name=q_new_a_2]').val(),
	a3: $('input:text[name=q_new_a_3]').val(),
	a4: $('input:text[name=q_new_a_4]').val(),
	correct: $('input:radio[name=q_new_correct]').val(),
	module_id: $('input:hidden[name=module_id]').val(),
    }, function(data) {
	location.reload();
    });
});

$('#create_new_int_q').on("submit", function(e) {
    e.preventDefault();
    var info = new FormData(document.querySelector("#create_new_int_q"));
    $.ajax({
	url: '/add_new_int_q',
	type: "POST",
	data: info,
	processData: false,  // tell jQuery not to process the data
	contentType: false,   // tell jQuery not to set contentType
	success: function(response) {
	    location.reload();
	},
    });
});

$(document).ready(function() {
    var fullEditor = new Quill('.full-editor', {
	modules: {
	'toolbar': { container: '.full-toolbar' },
	'link-tooltip': true
	},
	theme: 'snow'
    });
});
$(document).ready(function() {
    $('.edit').editable($SCRIPT_ROOT + '/edit_question', {
	indicator : 'Saving...',
	tooltip   : 'Click to edit...',
    });
    $('.edit_area').editable($SCRIPT_ROOT + '/edit_question', {
	type      : 'textarea',
	cancel    : 'Cancel',
	submit    : 'OK',
	indicator : 'Saving...',
	tooltip   : 'Click to edit...'
    });
});
$(document).ready(function() {
    $.uploadPreview({
	input_field: ".image-upload",
	preview_box: ".image-preview",
	label_field: ".image-label",
	label_default: "Choose File",
	label_selected: "Change File",
	no_label: false
    });
});

$(document).foundation();
$(document).foundation('reflow');
