// Progress bar animation
$(function () {
    if (complete <= 0) {
        $('#progress_meter').hide();
    } else if (complete >= 100) {
        $('#progress_meter').css('width', '100%');
    } else {
        $('#progress_meter').css('width', complete + '%');
    };
});
