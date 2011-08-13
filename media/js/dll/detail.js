$(document).ready(function () {
   
   $('ul.tab-list li a').click(function() {
       classAttr = $(this).attr('class');
       $('ul.tab-list li').removeClass('active')
       $(this).parent().addClass("active")
       $('.information').addClass('out-of-focus')
       $('#' + classAttr).removeClass('out-of-focus')
   });
   
   if(window.location.hash == '#comments') {
       $('.information').addClass('out-of-focus')
       $(window.location.hash).removeClass('out-of-focus')
       $('ul.tab-list li').removeClass('active')
       $('ul.tab-list li a.comments').parent().addClass('active')
   }
   
});