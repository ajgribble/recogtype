$(function() {
    // Function to give challenge instructions ability to expand/contract
    $('a#instructions_expand').click(function(e) {
        e.preventDefault();
        $('p#challenge_instructions').toggle();
    });
});    
