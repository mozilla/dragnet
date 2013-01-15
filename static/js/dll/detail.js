var Tabs = (function() {
    return {
       clicked: function($element) {
           $('.active').removeClass('active');
           $('.information').addClass('out-of-focus');
           $($element.attr('href')).removeClass('out-of-focus');
           $element.closest('li').addClass('active');
       }
    };
})();

$(document).ready(function () {
    $('ul.tab-list li a').click(function() {
        Tabs.clicked($(this));
    });

    if (location.hash.search(/#(comments|details|history)/) > -1) {
        $('a[href="' + location.hash + '"]').click();
    }

});
