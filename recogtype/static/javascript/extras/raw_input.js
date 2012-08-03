$(function() {
    var data = []
    var browser = $.browser.name + $.browser.versionX
    var os = $.os.name

    function keyObj(val_press, press_code, val_up, up_code, down, press, up) {
        this.down = down
        this.press = press
        this.up = up
        this.val_press = val_press
        this.press_code = press_code
        this.val_up = val_up
        this.up_code = up_code
    }
    $('#raw_data').keydown(function(event) {
        if (event.which != 16 && event.which != 17 && event.which != 18) {
            down = event.timeStamp;
        }
    });
    $('#raw_data').keypress(function(event) { 
        if (event.which != 16 && event.which != 17 && event.which != 18) {
            val_press = String.fromCharCode(event.which);
            press_code = event.which;
            press = event.timeStamp;
        }
    });
    $('#raw_data').keyup(function(event) {
        if (event.which != 16 && event.which != 17 && event.which != 18) {
            val_up = String.fromCharCode(event.which)
            up_code = event.which
            up = event.timeStamp
            data.push(new keyObj(val_press, press_code, val_up, up_code,
                                 down,  press, up));
        }
    });
    // Validates the challenge form
    var validator = $("#raw_data_form").validate({
                        rules: {
                            data: {
                                required: true,
                            }
                        },
                        messages: {
                            data:   "You cannot submit an empty form"
                        }
                    });
    $('#raw_data_form').submit(function() {
        var raw_data = JSON.stringify(data);
        var keyboard = $('#id_keyboard').val();
        if (validator.form()) {
            $.post(match_submit,
                    { raw_data: raw_data,
                      browser: browser,
                      os: os,
                      keyboard: keyboard },
                      function(responseData) {
                            window.location.replace(guide_user); 
                    });
            }
        return false;
    });
});
