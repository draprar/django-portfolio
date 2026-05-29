document.addEventListener("DOMContentLoaded", () => {
    const fadeInElements = document.querySelectorAll(".fade-in");

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add("visible");

                if (entry.target.classList.contains('instagram-section')) {
                    if (window.instgrm) {
                        window.instgrm.Embeds.process();
                    }
                }
            }
        });
    }, { threshold: 0.1, rootMargin: "0px 0px -30px 0px" });

    fadeInElements.forEach(element => observer.observe(element));

    // Smooth scrolling for navbar links
    const navbarLinks = document.querySelectorAll('.navbar-nav .nav-link');
    navbarLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            const href = link.getAttribute('href');
            if (href && href.startsWith('#')) {
                e.preventDefault();
                const target = document.querySelector(href);
                if (target) {
                    target.scrollIntoView({ behavior: 'smooth' });
                }
            }
        });
    });

    // Blur-up effect for gallery images
    document.querySelectorAll('.gallery-item img').forEach(img => {
        if (img.complete) {
            img.classList.add('loaded');
        } else {
            img.addEventListener('load', () => img.classList.add('loaded'));
        }
    });

    // ── Instagram embeds ────────────────────────────────────────────────
    const processEmbeds = () => {
        if (window.instgrm && window.instgrm.Embeds) {
            window.instgrm.Embeds.process();
        }
    };

    processEmbeds();
    setTimeout(processEmbeds, 1000);
    setTimeout(processEmbeds, 3000);
    window.addEventListener('load', processEmbeds);

    /**
     * Gdy IG wstrzyknie iframe do .instagram-item, obserwuj jego
     * rzeczywistą wysokość i ustaw min-height kontenera na tę wartość.
     * Dzięki temu kontener nigdy nie utnie embeda.
     */
    const watchIframes = () => {
        document.querySelectorAll('.instagram-item').forEach(item => {
            const iframe = item.querySelector('iframe');
            if (!iframe || item.dataset.watched) return;
            item.dataset.watched = '1';

            const syncHeight = () => {
                const h = iframe.getAttribute('height') || iframe.offsetHeight;
                if (h && parseInt(h) > 100) {
                    item.style.minHeight = parseInt(h) + 20 + 'px';
                }
            };

            // MutationObserver na atrybut height iframe
            const mo = new MutationObserver(syncHeight);
            mo.observe(iframe, { attributes: true, attributeFilter: ['height', 'style'] });

            // ResizeObserver jako backup
            if (window.ResizeObserver) {
                const ro = new ResizeObserver(syncHeight);
                ro.observe(iframe);
            }

            syncHeight();
        });
    };

    // Obserwuj DOM — reaguj gdy IG doda iframe do blockquote
    const domObserver = new MutationObserver(() => watchIframes());
    domObserver.observe(document.body, { childList: true, subtree: true });

    setTimeout(watchIframes, 500);
    setTimeout(watchIframes, 2000);
    setTimeout(watchIframes, 5000);
});