document.addEventListener('DOMContentLoaded', () => {
    const panels = document.querySelectorAll('.panel');
    const stage = document.querySelector('.carousel-stage');
    const cards = stage ? [...stage.querySelectorAll(':scope > .panel')] : [];
    let index = 0;
    let pointerX = null;
    let pointerY = null;
    let suppressClick = false;
    const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    const TURN_MS = 680;
    const TURN_EASE = 'cubic-bezier(0.22, 1, 0.36, 1)';

    const fixed = (n) => {
        const text = n.toFixed(2);
        return text === '-0.00' ? '0.00' : text;
    };

    const slotFor = (delta, n, index, card, allCards) => {
        if (delta === 0) return 'active';
        if (delta === 1) return 'next';
        if (delta === n - 1) {
            const last = allCards[n - 1];
            if (card === last && index < n - 1) return 'hidden';
            return 'prev';
        }
        if (n === 4 && delta === 2 && index === 0) return 'prev';
        return 'hidden';
    };

    const poseFor = (slot, peek) => {
        if (slot === 'active') return { x: 0, y: 0, z: 40, ry: 0 };
        if (slot === 'prev') return { x: -peek, y: 0, z: -72, ry: 28 };
        if (slot === 'next') return { x: peek, y: 0, z: -72, ry: -28 };
        return { x: 0, y: 0, z: -200, ry: 0 };
    };

    const frameFor = (pose, width) =>
        `translate3d(${fixed(-width / 2 + pose.x)}px, ${fixed(pose.y)}px, ${fixed(pose.z)}px) rotateY(${fixed(pose.ry)}deg)`;

    const frameNow = (turn) => {
        const raw = getComputedStyle(turn).transform;
        if (!raw || raw === 'none' || !raw.startsWith('matrix3d(')) return '';
        const values = raw.slice(9, -1).split(',').map((part) => parseFloat(part));
        if (values.length !== 16 || values.some((n) => Number.isNaN(n))) return '';
        const ry = Math.atan2(-values[2], values[0]) * (180 / Math.PI);
        return `translate3d(${fixed(values[12])}px, ${fixed(values[13])}px, ${fixed(values[14])}px) rotateY(${fixed(ry)}deg)`;
    };

    const peekPx = (root) => {
        if (!root._peekProbe) {
            const probe = document.createElement('div');
            probe.setAttribute('aria-hidden', 'true');
            probe.style.cssText = 'position:absolute;left:0;top:0;width:var(--peek);height:0;visibility:hidden;pointer-events:none;';
            root.appendChild(probe);
            root._peekProbe = probe;
        }
        return root._peekProbe.getBoundingClientRect().width;
    };

    const spin = (turn, next, animate) => {
        const from = frameNow(turn);
        turn.getAnimations().forEach((anim) => anim.cancel());
        turn.style.transform = next;
        if (!animate || reducedMotion || !from || from === next) return;
        turn.animate(
            [{ transform: from }, { transform: next }],
            { duration: TURN_MS, easing: TURN_EASE, fill: 'forwards' },
        );
    };

    const place = (animate) => {
        const n = cards.length;
        const peek = stage ? peekPx(stage) : 0;
        cards.forEach((card, i) => {
            const delta = (i - index + n) % n;
            const slot = slotFor(delta, n, index, card, cards);
            card.dataset.slot = slot;
            const hidden = slot === 'hidden';
            card.style.visibility = hidden ? 'hidden' : '';
            card.style.pointerEvents = hidden ? 'none' : '';
            if (slot === 'active') card.setAttribute('aria-current', 'true');
            else card.removeAttribute('aria-current');
            card.tabIndex = slot === 'active' ? 0 : -1;
            const turn = card.querySelector(':scope > .panel-turn');
            const width = turn ? turn.offsetWidth : 0;
            if (turn && width >= 1) spin(turn, frameFor(poseFor(slot, peek), width), animate && !hidden);
        });
    };

    const go = (step) => {
        if (!cards.length) return;
        index = (index + step + cards.length) % cards.length;
        place(true);
    };

    place(false);
    if (stage && window.ResizeObserver) {
        let frame = 0;
        const observer = new ResizeObserver(() => {
            cancelAnimationFrame(frame);
            frame = requestAnimationFrame(() => place(false));
        });
        observer.observe(stage);
    }

    document.querySelector('.carousel-prev')?.addEventListener('click', () => go(-1));
    document.querySelector('.carousel-next')?.addEventListener('click', () => go(1));

    cards.forEach((card, i) => {
        card.addEventListener('click', (event) => {
            if (suppressClick) {
                event.preventDefault();
                suppressClick = false;
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

        const endPointer = (event) => {
            if (pointerX == null) return;
            const dx = event.clientX - pointerX;
            const dy = event.clientY - pointerY;
            pointerX = null;
            pointerY = null;
            if (Math.abs(dx) < 24 || Math.abs(dx) < Math.abs(dy)) return;
            suppressClick = true;
            go(dx < 0 ? 1 : -1);
        };

        stage.addEventListener('pointerdown', (event) => {
            if (event.pointerType === 'mouse' && event.button !== 0) return;
            suppressClick = false;
            pointerX = event.clientX;
            pointerY = event.clientY;
            stage.setPointerCapture?.(event.pointerId);
        });
        stage.addEventListener('pointerup', endPointer);
        stage.addEventListener('pointercancel', () => {
            pointerX = null;
            pointerY = null;
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

    // ── Live terminal for codzillin' (replaces code-bg.gif)
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

            await beat('who?', [['"codzillin\'"', 't-green']], { hold: 950 });

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
                        span('"codzillin\'"', 't-green'),
                    );
                    await sleep(1500);
                }
            }
        })();
    }
});
