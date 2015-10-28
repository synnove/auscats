$(document).foundation('alert', 'reflow');
$('#admins').bind('submit', function(e) {                               
    e.preventDefault();                                                    
    $url = "/admin_mod_new/action=add";
    if ($("#admin_id").val().indexOf("uq") == 0) {
    $url += "&user=";
    $url += $("#admin_id").val();
    if ($('#write_access').prop('checked')) {
        $url += "&write=true";
    }
    if ($('#read_access').prop('checked')) {
        $url += "&read=true";
    }
    if ($("#admins input:checkbox:checked").length >= 1) {
        console.log("everything ok");
        console.log($url);
        window.location = $url;
    } else {
        console.log("no perms");
        $("#admin_err").html(function() {
	return "<div data-alert class='alert-box warning radius text-center'>" +
	    "<b>No permissions specified.</b>" + "<a href='#' class='close'>&times;</a>" + "</div>";
	});
        $(document).foundation();
        $(document).foundation('alert', 'reflow');
    }
    } else {
    $("#admin_err").html(function() {
        return "<div data-alert class='alert-box warning radius text-center'>" +
	"<b>Please enter a valid user.</b>" + "<a href='#' class='close'>&times;</a>" + "</div>";
        });
    $(document).foundation();
    $(document).foundation('alert', 'reflow');
    }
});

$('.mod-read').on('click', function(e) {
    if ($(this).prop('checked')) {
	$act = "add";
    } else {
	$act = "remove";
    }
    $.getJSON($SCRIPT_ROOT + '/admin_update_perms', {
	uid: $(this).val(),
	perm: "read",
	act: $act,
    }, function(data) {
    });
});

$('.mod-write').on('click', function(e) {
    if ($(this).prop('checked')) {
	$act = "add";
    } else {
	$act = "remove";
    }
    $.getJSON($SCRIPT_ROOT + '/admin_update_perms', {
	uid: $(this).val(),
	perm: "write",
	act: $act,
    }, function(data) {
    });
});

$('.delete-admin').on('click', function(e) {
    e.preventDefault();
    $.getJSON($SCRIPT_ROOT + '/delete_admin', {
	uid: $(this).val(),
    }, function(data) {
	location.reload();
    });
});

$(document).on('close.fndtn.alert', function(event) {
    $(document).foundation();
});
