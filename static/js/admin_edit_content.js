$('#lecture').on("click", function(e) {
    e.preventDefault();
    $('#lecture').addClass('current');
    $('#interactive').removeClass('current');
    $('#quiz').removeClass('current');
    if ($('.edit__lecture').hasClass('hidden')) {
	$('.edit__lecture').toggleClass('hidden');
    }
    $('.edit__interactive').addClass('hidden');
    $('.edit__quiz').addClass('hidden');
});

$('#interactive').on("click", function(e) {
    e.preventDefault();
    $('#interactive').addClass('current');
    $('#lecture').removeClass('current');
    $('#quiz').removeClass('current');
    if ($('.edit__interactive').hasClass('hidden')) {
	$('.edit__interactive').toggleClass('hidden');
    }
    $('.edit__lecture').addClass('hidden');
    $('.edit__quiz').addClass('hidden');
});

$('#quiz').on("click", function(e) {
    e.preventDefault();
    $('#quiz').addClass('current');
    $('#interactive').removeClass('current');
    $('#lecture').removeClass('current');
    if ($('.edit__quiz').hasClass('hidden')) {
	$('.edit__quiz').toggleClass('hidden');
    }
    $('.edit__lecture').addClass('hidden');
    $('.edit__interactive').addClass('hidden');
});

$(document).foundation();
$(document).foundation('reflow');
