$(function() {
    $.ajax({
        url: '/user_stats/',
        success: function(counts) {

            counts = jQuery.parseJSON(counts);
            users = counts.users;
            countries = counts.countries;
            languages = counts.languages;

            $('span#stat_users').html(users);
            $('span#stat_countries').html(countries);
            $('span#stat_languages').html(languages);
            
        }
    });
});
