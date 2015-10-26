$(document).foundation('alert', 'reflow');
$('#admins').bind('submit', function(e) {                               
    e.preventDefault();                                                    
    $url = "/admin_mod/action=add";
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

$(document).foundation('alert', 'reflow');
$('#admins2').bind('submit', function(e) {
    e.preventDefault();
    $url = "/admin_mod/action=add";
    if ($("#large-2 columns panel listing text-left span").prop("title").indexOf("uq") == 0) {
    $url += "&user=";
    $url += $("#large-2 columns panel listing text-left span").prop("title");
    if ($('#write_access2').prop('checked')) {
        $url += "&write=true";
    }
    if ($('#read_access2').prop('checked')) {
        $url += "&read=true";
    }
    if ($("#admins2 input:checkbox:checked").length >= 1) {
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

$(document).on('close.fndtn.alert', function(event) {
    $(document).foundation();
});
