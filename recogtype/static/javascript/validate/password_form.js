$().ready(function() {
    // Validates the signup form
    $("#passwordChangeForm").validate({
        rules: {
            old_password: {
                required: true,
            },
            new_password1: { 
                required: true,
                minlength: 6
            },
            new_password2: {
                required: true,
                minlength: 6,
                equalTo: "#id_new_password1"
            }
        },
        messages: {
            old_password:   "You cannot leave this field blank",
            new_password1: {
                required: "You cannot leave this field blank",
                minlength: "Your password must be at least 6 \
                            characters long",
            },
            new_password2: {
                required: "You cannot leave this field blank",
                minlength: "Your password must be at least 6 \
                            characters long",
                equalTo: "Your passwords do not match."
            }
        }
    });
});
