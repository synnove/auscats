$(".toggle__side").on("click", function(e) {                            
    e.preventDefault();                                                 
    $(".side__navigation").toggleClass("side-navigation__toggle");         
    $(".main__page").toggleClass("main-page__expand");                  
    $(".side__navigation span").toggleClass("toggle__visibility");         
    $(".title").toggleClass("title__expand");                           
    $(".progress").toggleClass("progress-expand");                      
    $(".slides").toggleClass("slides-expand");                          
});                                                                     

if ($(".reveal").length ) {
    $(".side__navigation").toggleClass("side-navigation__toggle");         
    $(".main__page").toggleClass("main-page__expand");                  
    $(".side__navigation span").toggleClass("toggle__visibility");         
    $(".title").toggleClass("title__expand");                           
    $(".progress").toggleClass("progress-expand");                      
    $(".slides").toggleClass("slides-expand");                          
}
									
$(window).resize(function () {                                          
    if ($(window).width() <= 700) {                                     
	if ($(".side__navigation").hasClass("side-navigation__toggle")) {
	    $(".toggle__side").addClass("toggle__visibility");          
	} else {                                                        
	    $(".side__navigation").toggleClass("side-navigation__toggle");
	    $(".top__navigation").toggleClass("top-navigation__expand");
	    $(".title").toggleClass("title__expand");                   
	    $(".main__page").toggleClass("main-page__expand");          
	    $(".side__navigation span").toggleClass("toggle__visibility");
	}                                                               
    } else {                                                            
	$(".toggle__side").removeClass("toggle__visibility");           
    }                                                                   
});
