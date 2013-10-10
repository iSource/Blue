var jq = jQuery.noConflict();

jq(document).ready(function() {
    jq('#login').click(function() {
        jq('#login_panel').slideDown('slow');
    });

    jq('#take-back').click(function() {
        jq('#login_panel').slideUp('fast');
    });

    jq('.pro_down_li').mouseenter(function() {
        jq('.pro_down').slideDown('fast');
    });

    jq('.pro_down').mouseleave(function() {
        jq(this).slideUp('fast');
    });

    jq('.pro_down_li').mouseleave(function() {
        jq('.pro_down').slideUp('fast');
    });

});
