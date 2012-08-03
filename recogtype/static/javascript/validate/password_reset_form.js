$().ready(function() {
    // Validates the signup form
    $("#passwordResetForm").validate({
        rules: {
                email: {
                        required: true,
                        email: true
                }    
        },
        messages: {
                    email: {    
                            required: "You cannot leave this field blank",
                            email: "Please insert a valid email"
                    }
        }
    });
});
