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

    // ── Basic protection: block right-click and drag on gallery / Instagram
    // media, in the grid AND inside the open Fancybox lightbox.
    document.addEventListener('contextmenu', (e) => {
        if (e.target.closest('.gallery-item, .ig-post-media, .g-card, .fancybox__container')) {
            e.preventDefault();
        }
    });

    document.addEventListener('dragstart', (e) => {
        if (
            (e.target.tagName === 'IMG' || e.target.tagName === 'VIDEO') &&
            e.target.closest('.gallery-item, .ig-post-media, .g-card, .fancybox__container')
        ) {
            e.preventDefault();
        }
    });

    // ── Instagram-style post carousels (manually added photos/reels) ──────
    document.querySelectorAll('[data-carousel]').forEach(carousel => {
        const track = carousel.querySelector('.ig-post-track');
        const slides = carousel.querySelectorAll('.ig-post-slide');
        const dots = carousel.querySelectorAll('.ig-post-dot');
        const prevBtn = carousel.querySelector('.ig-post-prev');
        const nextBtn = carousel.querySelector('.ig-post-next');

        // Pause any reel that isn't on the currently active slide
        const pauseInactive = (activeIndex) => {
            slides.forEach((slide, si) => {
                if (si === activeIndex) return;
                const video = slide.querySelector('video');
                if (video && !video.paused) video.pause();
            });
        };

        if (!track || slides.length <= 1) return;

        let index = 0;

        const goTo = (i) => {
            index = (i + slides.length) % slides.length;
            track.style.transform = `translateX(-${index * 100}%)`;
            dots.forEach((dot, di) => dot.classList.toggle('active', di === index));
            pauseInactive(index);
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
    });

    // Reels start paused; a click on the play button starts them (with sound)
    document.querySelectorAll('.ig-post-slide').forEach(slide => {
        const video = slide.querySelector('video');
        const playBtn = slide.querySelector('.ig-post-play-btn');
        if (!video || !playBtn) return;

        playBtn.addEventListener('click', () => {
            video.play().catch(() => {});
        });

        video.addEventListener('click', () => {
            if (!video.paused) video.pause();
        });

        video.addEventListener('play', () => playBtn.classList.add('hidden'));
        video.addEventListener('pause', () => playBtn.classList.remove('hidden'));
    });

    // If a playing reel's card scrolls off screen, pause it (never auto-starts it)
    const reelObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            const video = entry.target;
            if (!entry.isIntersecting && !video.paused) {
                video.pause();
            }
        });
    }, { threshold: 0.1 });

    document.querySelectorAll('.ig-post-media video').forEach(video => {
        reelObserver.observe(video);
    });

    // ── Hub-style gallery carousel (default view). Side cards rotate in;
    // the active image opens in Fancybox. Only three slots are visible.
    const galleryCarousel = document.querySelector('[data-gallery-carousel]');
    if (galleryCarousel) {
        const stage = galleryCarousel.querySelector('.gallery-carousel-stage');
        const cards = stage ? [...stage.querySelectorAll('.g-card')] : [];
        let index = Math.max(0, cards.findIndex((card) => card.dataset.slot === 'active'));
        let pointerX = null;
        let dragged = false;

        const place = () => {
            const n = cards.length;
            cards.forEach((card, i) => {
                const delta = (i - index + n) % n;
                let slot = 'off';
                if (delta === 0) slot = 'active';
                else if (n === 2 || delta === 1) slot = 'next';
                else if (delta === n - 1) slot = 'prev';
                card.dataset.slot = slot;
                if (slot === 'active') card.setAttribute('aria-current', 'true');
                else card.removeAttribute('aria-current');
                card.tabIndex = slot === 'active' ? 0 : -1;
                if (slot === 'off') card.setAttribute('aria-hidden', 'true');
                else card.removeAttribute('aria-hidden');
                const video = card.querySelector('video');
                if (video && slot !== 'active' && !video.paused) video.pause();
            });
        };

        const go = (step) => {
            if (!cards.length) return;
            index = (index + step + cards.length) % cards.length;
            place();
        };

        place();

        galleryCarousel.querySelector('.gallery-carousel-prev')?.addEventListener('click', () => go(-1));
        galleryCarousel.querySelector('.gallery-carousel-next')?.addEventListener('click', () => go(1));

        if (stage) {
            stage.addEventListener('click', (event) => {
                const card = event.target.closest('.g-card');
                if (!card || !stage.contains(card)) return;
                if (dragged) {
                    event.preventDefault();
                    event.stopPropagation();
                    dragged = false;
                    return;
                }
                if (card.dataset.slot !== 'active') {
                    event.preventDefault();
                    event.stopPropagation();
                    const i = cards.indexOf(card);
                    const n = cards.length;
                    const delta = (i - index + n) % n;
                    go(delta === 1 ? 1 : -1);
                }
            }, true);

            stage.addEventListener('keydown', (event) => {
                if (event.key === 'ArrowRight') {
                    event.preventDefault();
                    go(1);
                } else if (event.key === 'ArrowLeft') {
                    event.preventDefault();
                    go(-1);
                }
            });

            stage.addEventListener('pointerdown', (event) => {
                if (event.target.closest('.g-card-play')) return;
                pointerX = event.clientX;
                dragged = false;
            });
            stage.addEventListener('pointerup', (event) => {
                if (pointerX == null) return;
                const dx = event.clientX - pointerX;
                pointerX = null;
                if (Math.abs(dx) < 48) return;
                dragged = true;
                go(dx < 0 ? 1 : -1);
            });
        }

        cards.forEach((card) => {
            const video = card.querySelector('video');
            const playBtn = card.querySelector('.g-card-play');
            if (!video || !playBtn) return;

            playBtn.addEventListener('click', (event) => {
                if (card.dataset.slot !== 'active') return;
                event.stopPropagation();
                video.play().catch(() => {});
            });

            video.addEventListener('click', (event) => {
                if (card.dataset.slot !== 'active' || video.paused) return;
                event.preventDefault();
                event.stopPropagation();
                video.pause();
            });

            video.addEventListener('play', () => playBtn.classList.add('hidden'));
            video.addEventListener('pause', () => playBtn.classList.remove('hidden'));
        });
    }
});