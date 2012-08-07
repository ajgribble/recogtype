// Disables cutting, copying and pasting from challenge input
$(document).ready(function() {
    $('#raw_data').on("cut copy paste", function(e) {
        e.preventDefault();
    });
    $('#raw_data').on("contextmenu", function(e) {
        e.preventDefault();
    });
});
