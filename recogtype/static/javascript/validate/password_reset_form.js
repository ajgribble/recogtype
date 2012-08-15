$(function() {
    // Validates the signup form
    validator = $("#passwordResetForm").validate({
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

    // If the form is valid then check if the email address is in the system
    if (validator.form()) {
        email = $('#id_email').html();
        $.ajax({
            url: '/user_stats/',
            data: {'email': email},
            success: function(response) {
                if (response == true) {
                    return true
                } else {
                    error = '<label for="id_email" generated="true" class="error">' +
                            'Email not registered.</label>';
                    $(error).insertAfter('#id_email').html();
                    return false
                }         
            }
        });
    }
});
