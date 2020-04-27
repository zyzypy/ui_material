(function($) {

    'use strict';


    /*-----------------------------------------------------------------------------------*/
    /*  Initialize
    /*-----------------------------------------------------------------------------------*/

    new WOW().init();
    $.material.ripples();


    /*-----------------------------------------------------------------------------------*/
    /*  Animsition
    /*-----------------------------------------------------------------------------------*/
    $(document).ready(function() {

        $(".animsition").animsition({

            inClass: 'fade-in',
            outClass: 'fade-out',
            inDuration: 1500,
            outDuration: 800,
            linkElement: 'a:not([target="_blank"]):not([href^=#])',
            loading: true,
            loadingParentElement: 'body', //animsition wrapper element
            loadingClass: 'animsition-loading',
            unSupportCss: ['animation-duration',
                '-webkit-animation-duration',
                '-o-animation-duration'
            ],
            overlay: false,

            overlayClass: 'animsition-overlay-slide',
            overlayParentElement: 'body'
        });


        /*-----------------------------------------------------------------------------------*/
        /*  TAB
        /*-----------------------------------------------------------------------------------*/

        $('.feature-box-services .feature-icon a').on('click', function(e) {
            var currentAttrValue = $(this).attr('href');

            // Show/Hide Tabs
            $('.tab-pane ' + currentAttrValue).show().siblings().hide();

            // Change/remove current tab to active
            $(this).parent('li').addClass('active').siblings().removeClass('active');

            e.preventDefault();
        });



        /*-----------------------------------------------------------------------------------*/
        /*  Background Header
        /*-----------------------------------------------------------------------------------*/


        var backgroundHeader = $('.background-header'),
            siteHeaderHeight = $('.site-header').height(),
            backgroundSlider = $('.bannercontainer');

        backgroundHeader.css('margin-top', -siteHeaderHeight);
        backgroundSlider.css('margin-top', -siteHeaderHeight);


        /*-----------------------------------------------------------------------------------*/
        /*  Team List
        /*-----------------------------------------------------------------------------------*/


        $(".team-list").hover(function(e) {
            $('.team-list').stop().animate({
                opacity: "0.5"
            }, 'slow');
            $(this).stop().animate({
                opacity: "1"
            }, 'slow');
        }, function() {
            $('.team-list').stop().animate({
                opacity: "1"
            }, 'slow');
        });


        /*-----------------------------------------------------------------------------------*/
        /*  Skill Section
        /*-----------------------------------------------------------------------------------*/

        $('.skills-bar').each(function() {
            $(this).find('.bar').animate({
                width: $(this).attr('data-percent')
            }, 6000);
        });

    });



    /*-----------------------------------------------------------------------------------*/
    /*  Mobile Menu
    /*-----------------------------------------------------------------------------------*/

    $('.burger').click(function() {

        $('#main-nav, .logo, .slider-home').toggleClass('mobile-menu');
        $('.burger').toggleClass('active');
    });



    /*-----------------------------------------------------------------------------------*/
    /*  Team Section
    /*-----------------------------------------------------------------------------------*/

    function teamEqualHeight() {

        var teamLeftHeight = $('.team-person'),
            teamRightHeight = $('.team-right').height();

        teamLeftHeight.css('height', teamRightHeight);
    }

    window.onload = teamEqualHeight;
    window.onresize = teamEqualHeight;


})(jQuery);
