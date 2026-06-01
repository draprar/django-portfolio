document.addEventListener('DOMContentLoaded', function() {
    // Initialize Swiper with autoHeight so it always fits the active slide's content.
    // No manual height calculation needed — Swiper handles it natively.
    var mainSwiper = new Swiper(".mySwiper", {
        autoHeight: true,
        pagination: {
            el: ".swiper-pagination",
            type: "progressbar",
        },
        navigation: {
            nextEl: '.swiper-button-next',
            prevEl: '.swiper-button-prev'
        },
        simulateTouch: true,
        allowTouchMove: true,
    });

    /**
     * Tell Swiper to recalculate height after dynamic content changes.
     * Called after AJAX loads, button clicks that add/remove DOM nodes, etc.
     * Two calls with a gap catch both immediate DOM changes and slower renders.
     */
    function updateSwiperHeight() {
        if (mainSwiper && !mainSwiper.destroyed) {
            mainSwiper.updateAutoHeight(0);
            // Second call after a short delay catches late-rendering content
            // (e.g. card-twister revealed by style.display = 'block')
            setTimeout(function() {
                mainSwiper.updateAutoHeight(0);
            }, 350);
        }
    }

    /**
     * Dynamic content trigger buttons — call updateSwiperHeight after click.
     */
    const dynamicContentTriggers = [
        '.toggle-articulator-btn',
        '#load-more-btn',
        '#mirror-btn',
        '#mirror-btn-articulators',
        '#mirror-btn-exercises',
        '#mirror-btn-twisters',
        '#mirror-btn-bonuses',
        '.toggle-exercise-btn',
        '#load-more-exercises-btn',
        '.toggle-twister-btn',
        '#load-more-twisters-btn',
        '#load-more-trivia-btn',
        '#load-more-facts-btn'
    ];

    dynamicContentTriggers.forEach(function(selector) {
        document.querySelectorAll(selector).forEach(function(button) {
            button.addEventListener('click', function() {
                updateSwiperHeight();
            });
        });
    });

    /**
     * Observe these elements for display changes (style attribute mutations).
     * When they become visible, trigger a Swiper height update.
     */
    const elementsToObserve = [
        '#video-container-articulators',
        '#video-container-twisters',
        '#video-container-exercises',
        '#video-container-bonuses',
        '#video-container',
        '#card-articulator',
        '#card-exercises',
        '#card-twister',
        '#trivia-container',
        '#facts-container',
        '#congratulations-modal'
    ];

    elementsToObserve.forEach(function(selector) {
        const element = document.querySelector(selector);
        if (element) {
            const observer = new MutationObserver(function(mutations) {
                mutations.forEach(function(mutation) {
                    if (mutation.attributeName === 'style') {
                        // Small delay so the browser paints the new display state first
                        setTimeout(function() { mainSwiper.updateAutoHeight(0); }, 50);
                        setTimeout(function() { mainSwiper.updateAutoHeight(0); }, 400);
                    }
                });
            });
            observer.observe(element, { attributes: true });
        }
    });

    // Also observe the twisters/exercises/articulators containers for child additions
    // (AJAX clears innerHTML then appends new nodes — childList catches this)
    const contentContainers = [
        '#twisters-container',
        '#exercises-container',
        '#articulators-container',
        '#trivia-container',
        '#facts-container'
    ];

    contentContainers.forEach(function(selector) {
        const element = document.querySelector(selector);
        if (element) {
            const observer = new MutationObserver(function() {
                setTimeout(function() { mainSwiper.updateAutoHeight(0); }, 100);
                setTimeout(function() { mainSwiper.updateAutoHeight(0); }, 500);
            });
            observer.observe(element, { childList: true, subtree: true });
        }
    });

    // Custom event from other scripts
    document.addEventListener('ajaxContentLoaded', function() {
        updateSwiperHeight();
    });

    // Catch-all for any button click
    document.querySelectorAll('button').forEach(function(button) {
        button.addEventListener('click', function() {
            updateSwiperHeight();
        });
    });
});