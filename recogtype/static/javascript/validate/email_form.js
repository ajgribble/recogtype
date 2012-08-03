$().ready(function() {
    // Validates the signup form
    $("#emailResetForm").validate({
        rules: {
            email: {
                required: true,
                email: true
            }
        },
        messages: {
            email:   "Please enter a valid email address"
        }
    });
});
