document.addEventListener('DOMContentLoaded', () => {
    const split = document.querySelector('.split');
    const panels = document.querySelectorAll('.panel');

    const focus = (side) => {
        panels.forEach(p => p.classList.toggle('is-active', p.dataset.panel === side));
        split.classList.add('has-focus');
    };

    const reset = () => {
        split.classList.remove('has-focus');
    };

    panels.forEach(panel => {
        const side = panel.dataset.panel;
        panel.addEventListener('mouseenter', () => focus(side));
        panel.addEventListener('focus', () => focus(side));
        panel.addEventListener('mouseleave', reset);
        panel.addEventListener('blur', reset);
    });

    // ── Warm the destination up: fetch it in the background as soon as
    // someone shows intent (hover on desktop, touch on mobile), so the
    // actual navigation feels instant. Fires once per panel.
    const prefetched = new Set();
    const prefetch = (href) => {
        if (!href || prefetched.has(href)) return;
        prefetched.add(href);
        const link = document.createElement('link');
        link.rel = 'prefetch';
        link.href = href;
        document.head.appendChild(link);
    };

    panels.forEach(panel => {
        const href = panel.getAttribute('href');
        panel.addEventListener('mouseenter', () => prefetch(href), { once: true });
        panel.addEventListener('touchstart', () => prefetch(href), { once: true, passive: true });
    });

    // ── Cursor-tracking tilt + gold sheen. Purely a lighting effect, so it
    // only runs on devices with a real pointer, and only if the visitor
    // hasn't asked for reduced motion.
    const supportsTilt = window.matchMedia('(hover: hover) and (pointer: fine)').matches;
    const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    if (supportsTilt && !reducedMotion) {
        const MAX_TILT = 4; // degrees

        panels.forEach(panel => {
            panel.addEventListener('mousemove', (e) => {
                const rect = panel.getBoundingClientRect();
                const px = (e.clientX - rect.left) / rect.width;  // 0 → 1
                const py = (e.clientY - rect.top) / rect.height;  // 0 → 1

                const ry = (px - 0.5) * (MAX_TILT * 2);
                const rx = (0.5 - py) * (MAX_TILT * 2);

                panel.style.setProperty('--rx', `${rx.toFixed(2)}deg`);
                panel.style.setProperty('--ry', `${ry.toFixed(2)}deg`);
                panel.style.setProperty('--mx', `${(px * 100).toFixed(1)}%`);
                panel.style.setProperty('--my', `${(py * 100).toFixed(1)}%`);
            });

            panel.addEventListener('mouseleave', () => {
                panel.style.setProperty('--rx', '0deg');
                panel.style.setProperty('--ry', '0deg');
            });
        });
    }
});
