$(document).ready(function () {
   
   $('ul.tab-list li a').click(function() {
       classAttr = $(this).attr('class');
       $('ul.tab-list li').removeClass('active')
       $(this).parent().addClass("active")
       $('.information').addClass('out-of-focus')
       $('#' + classAttr).removeClass('out-of-focus')
   });
});