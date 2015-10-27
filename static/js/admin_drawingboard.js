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

$('#preview').on('click', function(e) {
    e.preventDefault();
    $url = document.URL.replace(/#.*$/, "").split("/");
    $url = $url[$url.length - 1];
    window.location = '/preview/' + $url;
});

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

$('.correct-answer').on("click", function(e) {
    if(this.checked) {
	$.getJSON($SCRIPT_ROOT + '/update_correct_answer', {
	    qid: $(this).attr("name"),
	    aid: $(this).val(),
	}, function(data) {
	});
    }
});

$('.lecture-save-slide').on("click", function(e) {
    e.preventDefault();
    $slide_id = $(this).attr("id").split("-")[1];
    $new_title = "";
    info = [];
    $url = document.URL.replace(/#.*$/, "").split("/");
    $url = $url[$url.length - 1];
    info.push({"TITLE": $url});
    $("div.quill-wrapper").each(function( index ) {
	if ($(this).attr("id") != "slide_new") {
	    info.push({TITLE: $(this).find(".slide-title").val(),
	    CONTENT: $(this).find(".ql-editor").html()});
	    if ($(this).attr("id") == "slide_" + $slide_id) {
		$new_title = $(this).find(".slide-title").val();
	    }
	}
    });
    $("span.slide-" + $slide_id + "-title").text($new_title);
    $.ajax({
	url: '/edit_module_content',
	type: "POST",
	data: JSON.stringify(info),
	contentType: 'application/json;charset=UTF-8',
	success: function(response) {
	},
    });
});

$('.lecture-delete-slide').on("click", function(e) {
    e.preventDefault();
    $('div#lecture li.accordion-navigation.active').remove();
    info = [];
    $url = document.URL.replace(/#.*$/, "").split("/");
    $url = $url[$url.length - 1];
    info.push({"TITLE": $url});
    $("div.quill-wrapper").each(function( index ) {
	if ($(this).attr("id") != "slide_new") {
	    info.push({TITLE: $(this).find(".slide-title").val(),
	    CONTENT: $(this).find(".ql-editor").html()});
	}
    });
    $.ajax({
	url: '/edit_module_content',
	type: "POST",
	data: JSON.stringify(info),
	contentType: 'application/json;charset=UTF-8',
	success: function(response) {
	},
    });
});

$('#lecture-add-new').on("click", function(e) {
    e.preventDefault();
    info = [];
    $url = document.URL.replace(/#.*$/, "").split("/");
    $url = $url[$url.length - 1];
    info.push({"TITLE": $url});
    $("div.quill-wrapper").each(function( index ) {
	info.push({TITLE: $(this).find(".slide-title").val(),
	CONTENT: $(this).find(".ql-editor").html()});
    });
    $.ajax({
	url: '/edit_module_content',
	type: "POST",
	data: JSON.stringify(info),
	contentType: 'application/json;charset=UTF-8',
	success: function(response) {
	    location.reload();
	},
    });
});

$(document).ready(function() {
    $("div.quill-wrapper").each(function( index ) {
	$id = $(this).attr("id").split("_")[1];
	$editor = new Quill('#full-editor-' + $id, {
	    modules: {
	    'toolbar': { container: '#full-toolbar-' + $id},
	    },
	    theme: 'snow'
	});
	$insert = $('#ql-editor-' + $id).html();
	$('#ql-editor-' + $id).empty()
	$editor.setHTML($insert);
    });
    $("div.quill-wrapper").each(function( index ) {
	$id = $(this).attr("id").split("_")[1];
	new Quill('#full-editor-' + $id, {
	    modules: {
	    'toolbar': { container: '#full-toolbar-' + $id},
	    },
	    theme: 'snow'
	});
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
