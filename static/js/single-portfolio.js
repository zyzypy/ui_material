
(function() {
    var support = { animations : Modernizr.cssanimations },
        animEndEventNames = {
            'WebkitAnimation' : 'webkitAnimationEnd',
            'OAnimation' : 'oAnimationEnd',
            'msAnimation' : 'MSAnimationEnd',
            'animation' : 'animationend'
        },
        // animation end event name
        animEndEventName = animEndEventNames[ Modernizr.prefixed( 'animation' ) ],
        effectSel = document.getElementById( 'fxselect' ),
        component = document.getElementById( 'component' ),
        items = component.querySelector( 'ul.itemwrap' ).children,
        current = 0,
        itemsCount = items.length,
        nav = component.querySelector( 'nav' ),
        navNext = nav.querySelector( '.next' ),
        navPrev = nav.querySelector( '.prev' ),
        isAnimating = false;

    function init() {
        navNext.addEventListener( 'click', function( ev ) { ev.preventDefault(); navigate( 'next' ); } );
        navPrev.addEventListener( 'click', function( ev ) { ev.preventDefault(); navigate( 'prev' ); } );
    }




    function navigate( dir ) {
        if( isAnimating) return false;
        isAnimating = true;
        var cntAnims = 0;


        var currentItem = items[ current ];

        if( dir === 'next' ) {
            current = current < itemsCount - 1 ? current + 1 : 0;
        }
        else if( dir === 'prev' ) {
            current = current > 0 ? current - 1 : itemsCount - 1;
        }

        var nextItem = items[ current ];

        var onEndAnimationCurrentItem = function() {
            this.removeEventListener( animEndEventName, onEndAnimationCurrentItem );
            classie.removeClass( this, 'current' );
            classie.removeClass( this, dir === 'next' ? 'navOutNext' : 'navOutPrev' );
            ++cntAnims;
            if( cntAnims === 2 ) {
                isAnimating = false;
            }
        }

        var onEndAnimationNextItem = function() {
            this.removeEventListener( animEndEventName, onEndAnimationNextItem );
            classie.addClass( this, 'current' );
            classie.removeClass( this, dir === 'next' ? 'navInNext' : 'navInPrev' );
            ++cntAnims;
            if( cntAnims === 2 ) {
                isAnimating = false;
            }
        }

        if( support.animations ) {
            currentItem.addEventListener( animEndEventName, onEndAnimationCurrentItem );
            nextItem.addEventListener( animEndEventName, onEndAnimationNextItem );
        }
        else {
            onEndAnimationCurrentItem();
            onEndAnimationNextItem();
        }

        classie.addClass( currentItem, dir === 'next' ? 'navOutNext' : 'navOutPrev' );
        classie.addClass( nextItem, dir === 'next' ? 'navInNext' : 'navInPrev' );
    }

    init();
})();