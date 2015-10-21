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
}


$(document).foundation();
$(document).foundation('reflow');
