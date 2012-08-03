$().ready(function() {
    // Validates the signup form
    $("#signupForm").validate({
        rules: {
            email: {
                required: true,
                email: true
            },
            password1: { 
                required: true,
                minlength: 6
            },
            password2: {
                required: true,
                minlength: 6,
                equalTo: "#id_password1"
            },
            terms_services: {
                required: true
            }
        },
        messages: {
            email:   "Please enter a valid email address",
            password1: {
                required: "You cannot leave this field blank",
                minlength: "Your password must be at least 6 \
                            characters long",
            },
            password2: {
                required: "You cannot leave this field blank",
                minlength: "Your password must be at least 6 \
                            characters long",
                equalTo: "Your passwords do not match."
            },
            terms_services: "You must accept our terms"
        }
    });
});
