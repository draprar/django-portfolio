document.addEventListener('DOMContentLoaded', () => {
    const split = document.querySelector('.split');
    const panels = document.querySelectorAll('.panel');

    const focus = (side) => {
        panels.forEach(p => p.classList.toggle('is-active', p.dataset.panel === side));
        if (split) split.classList.add('has-focus');
    };

    const reset = () => {
        if (split) split.classList.remove('has-focus');
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

        const staticFrame = () => {
            paint(
                span(`${PROMPT} what?`, 't-gold'),
                span('  "machine learning"', 't-green'),
            );
        };

        if (reducedMotion) {
            staticFrame();
        } else {
            (async () => {
                for (;;) {
                    try {
                        await runScript();
                    } catch (err) {
                        staticFrame();
                        await sleep(1500);
                    }
                }
            })();
        }
    }
});
