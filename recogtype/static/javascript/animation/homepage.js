$(function() {
    // Function to give challenge instructions ability to expand/contract
    $('.expander').click(function(e) {
        e.preventDefault();
        $(this).closest('a').next('.expandable').toggle();
    });
});
