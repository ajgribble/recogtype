// Progress bar animation
$(function () {
    if (complete <= 0) {
        $('div#progress_container span').css('margin-top', '30px');
        $('#progress_meter').hide();
    } else if (complete >= 100) {
        $('div#progress_container span').css('margin-top', '-70px');
        $('#progress_meter').css('width', '100%');
    } else {
        $('div#progress_container span').css('margin-top', '-70px');
        $('#progress_meter').css('width', complete + '%');
    };
});
