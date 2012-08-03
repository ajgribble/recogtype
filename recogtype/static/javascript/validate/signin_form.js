$().ready(function() {
    // Validates the signup form
    $("#signinForm").validate({
        rules: {
            identification: {
                required: true,
            },
            password: { 
                required: true,
            },
            remember_me: {
                required: false,
            },
        },
        messages: {
            identification:   "You cannot leave this field blank",
            password:   "You cannot leave this field blank"
        }
    });
});
