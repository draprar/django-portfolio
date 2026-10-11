document.addEventListener('DOMContentLoaded', () => {
    const panels = document.querySelectorAll('.panel');
    const stage = document.querySelector('.carousel-stage');
    const cards = stage ? [...stage.querySelectorAll('.panel')] : [];
    let index = 0;
    let pointerX = null;
    let dragged = false;

    const place = () => {
        const n = cards.length;
        cards.forEach((card, i) => {
            const delta = (i - index + n) % n;
            const slot = delta === 0 ? 'active' : delta === 1 ? 'next' : 'prev';
            card.dataset.slot = slot;
            if (slot === 'active') card.setAttribute('aria-current', 'true');
            else card.removeAttribute('aria-current');
            card.tabIndex = slot === 'active' ? 0 : -1;
        });
    };

    const go = (step) => {
        if (!cards.length) return;
        index = (index + step + cards.length) % cards.length;
        place();
    };

    place();

    document.querySelector('.carousel-prev')?.addEventListener('click', () => go(-1));
    document.querySelector('.carousel-next')?.addEventListener('click', () => go(1));

    cards.forEach((card, i) => {
        card.addEventListener('click', (event) => {
            if (dragged) {
                event.preventDefault();
                dragged = false;
                return;
            }
            if (card.dataset.slot !== 'active') {
                event.preventDefault();
                const n = cards.length;
                const delta = (i - index + n) % n;
                go(delta === 1 ? 1 : -1);
            }
        });
    });

    if (stage) {
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

        document.querySelectorAll('.panel-code').forEach(panel => {
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

    // ── Live terminal for kodzillin' (replaces code-bg.gif)
    // Always ≤2 lines: current command + one output — left-aligned,
    // vertically centered so they stay visible in the short strip.
    const termRoot = document.querySelector('.panel-code .code-terminal-lines');
    if (termRoot) {
        const PROMPT = '>>>';
        const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

        const esc = (s) => s
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;');

        const paint = (cmdHtml, outHtml) => {
            let html = cmdHtml || '';
            if (outHtml) html += `\n${outHtml}`;
            termRoot.innerHTML = `${html}<span class="code-terminal-cursor">█</span>`;
        };

        const span = (text, cls) =>
            `<span class="${cls}">${esc(text)}</span>`;

        const typeCmd = async (cmd, charMs = 55) => {
            let shown = '';
            for (const ch of cmd) {
                shown += ch;
                paint(span(`${PROMPT} ${shown}`, 't-gold'), null);
                await sleep(charMs);
            }
            return span(`${PROMPT} ${cmd}`, 't-gold');
        };

        const beat = async (cmd, outputs, opts = {}) => {
            const cmdHtml = await typeCmd(cmd);
            paint(cmdHtml, null);
            await sleep(120);

            for (const [text, cls] of outputs) {
                paint(cmdHtml, span(text, cls));
                await sleep(opts.outMs ?? 320);
            }
            await sleep(opts.hold ?? 850);
            termRoot.innerHTML = '';
            await sleep(200);
        };

        const flash = async (text, cls, ms = 700) => {
            paint(span(text, cls), null);
            await sleep(ms);
            termRoot.innerHTML = '';
            await sleep(180);
        };

        const runScript = async () => {
            await flash('walery@code:~$ python', 't-dim', 650);

            await beat('who?', [['"kodzillin\'"', 't-green']], { hold: 950 });

            await beat('what?', [
                ['[', 't-text'],
                ['  "web",', 't-green'],
                ['  "code",', 't-green'],
                ['  "power bi",', 't-green'],
                ['  "machine learning"', 't-green'],
                [']', 't-text'],
            ], { outMs: 300, hold: 700 });

            await beat('uuu', [['"nom"', 't-green']], { hold: 1100 });
        };

        // Always animate — iOS "Reduce Motion" would otherwise freeze on the
        // static what?/ML frame and look broken. Cursor blink stays CSS-gated.
        (async () => {
            for (;;) {
                try {
                    await runScript();
                } catch (err) {
                    paint(
                        span(`${PROMPT} who?`, 't-gold'),
                        span('"kodzillin\'"', 't-green'),
                    );
                    await sleep(1500);
                }
            }
        })();
    }
});
