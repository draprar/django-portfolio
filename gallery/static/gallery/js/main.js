document.addEventListener("DOMContentLoaded", () => {
    const fadeInElements = document.querySelectorAll(".fade-in");

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add("visible");
            }
        });
    }, { threshold: 0.1, rootMargin: "0px 0px -30px 0px" });

    fadeInElements.forEach(el => {
        if (el.getBoundingClientRect().top < window.innerHeight) {
            el.classList.add('visible');
        } else {
            observer.observe(el);  // ← tego brakuje
        }
    });


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

    // ── Instagram-style post carousels (manually added photos/reels) ──────
    document.querySelectorAll('[data-carousel]').forEach(carousel => {
        const track = carousel.querySelector('.ig-post-track');
        const slides = carousel.querySelectorAll('.ig-post-slide');
        const dots = carousel.querySelectorAll('.ig-post-dot');
        const prevBtn = carousel.querySelector('.ig-post-prev');
        const nextBtn = carousel.querySelector('.ig-post-next');

        // Only the active slide's reel should actually play, others stay paused
        const syncVideos = (activeIndex) => {
            slides.forEach((slide, si) => {
                const video = slide.querySelector('video');
                if (!video) return;
                if (si === activeIndex) {
                    video.play().catch(() => {});
                } else {
                    video.pause();
                }
            });
        };

        if (!track || slides.length <= 1) {
            syncVideos(0);
            return;
        }

        let index = 0;

        const goTo = (i) => {
            index = (i + slides.length) % slides.length;
            track.style.transform = `translateX(-${index * 100}%)`;
            dots.forEach((dot, di) => dot.classList.toggle('active', di === index));
            syncVideos(index);
        };

        prevBtn?.addEventListener('click', () => goTo(index - 1));
        nextBtn?.addEventListener('click', () => goTo(index + 1));
        dots.forEach((dot, di) => dot.addEventListener('click', () => goTo(di)));

        // Swipe support for touch devices
        let startX = 0;
        track.addEventListener('touchstart', e => {
            startX = e.touches[0].clientX;
        }, { passive: true });

        track.addEventListener('touchend', e => {
            const diff = e.changedTouches[0].clientX - startX;
            if (Math.abs(diff) > 40) goTo(index + (diff < 0 ? 1 : -1));
        });

        syncVideos(0);
    });

    // Pause reels when their card scrolls out of view, resume when it's back
    const reelObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            const video = entry.target;
            if (entry.isIntersecting) {
                video.play().catch(() => {});
            } else {
                video.pause();
            }
        });
    }, { threshold: 0.25 });

    document.querySelectorAll('.ig-post-media video').forEach(video => {
        reelObserver.observe(video);
    });
});