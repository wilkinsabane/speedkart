function prepareDocument() {

    // using jQuery
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');
    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });


    jQuery("form#search").submit(function () {
        var text = jQuery("#id_q").val();
        if (text == "" || text == "Search"){
            // if empty, pop up alert
            alert("Enter a search term.");
            // halt submission of form.
            return false;
        }
    });
    jQuery("#submit_review").click(addProductReview);
    jQuery("#review_form").addClass('hidden');
    jQuery("#add_review").click(slideToggleReviewForm);
    jQuery("#add_review").addClass('visible');
    jQuery("#cancel_review").click(slideToggleReviewForm);


    // toggles visibility of write review link
    // and the review form
    function slideToggleReviewForm() {
        jQuery("#review_form").slideToggle();
        jQuery("#add_review").slideToggle();
    }

    // function for adding product reviews
    function addProductReview() {
        // build an object of review data to submit
        var review = {
            title: jQuery("#id_title").val(),
            content: jQuery("#id_content").val(),
            rating: jQuery("#id_rating").val(),
            slug: jQuery("#id_slug").val()
        };
        // make request, process response
        jQuery.post("/review/product/add/", review, function (response) {
            jQuery("#review_errors").empty();
            // evaluate the "success" parameter
            if(response.success == "True"){
                // disable the submit button to prevent duplicates
                jQuery("#submit_review").attr('disabled', 'disabled');
                // if this is first review, get rid of "no review" text
                jQuery("#no_reviews").empty();
                // add the new reviews to the reviews section
                jQuery("#reviews").prepend(response.html).slideDown();
                // get the newly added review and style it with color
                var new_review = jQuery("#reviews").children(":first");
                new_review.addClass('new_review');
                // hide the review form
                jQuery("#review_form").slideToggle();
            }
            else {
                // add the error text to the review_errors div
                jQuery("#review_errors").append(response.html);
            }
        }, "json");
    }


    function statusBox() {
        jQuery('<div id="loading">Loading...</div>')
            .prependTo("#main")
            .ajaxStart(function () {jQuery(this).show();})
            .ajaxStop(function () {jQuery(this).hide();})
    }
}

jQuery(document).ready(prepareDocument);