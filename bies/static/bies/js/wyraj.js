// ─────────────────────────────────────────────────────────────────────────────
// LOADER
// ─────────────────────────────────────────────────────────────────────────────
(function () {
  const loader = document.getElementById("loader");
  if (!loader) return;

  const hide = () => {
    loader.style.opacity = "0";
    setTimeout(() => { loader.style.display = "none"; }, 620);
  };

  window.addEventListener("load", hide);
  setTimeout(hide, 3500); // safety fallback if "load" never fires
})();

// ─────────────────────────────────────────────────────────────────────────────
// LANG SWITCH
// Dispatches a CustomEvent("langchange") so other modules can react
// without monkey-patching this function.
// ─────────────────────────────────────────────────────────────────────────────
const LANG_KEY = "wyraj_lang";

window.switchLang = function (lang) {
  // Hide all .lang elements, then show those that match the chosen language.
  document.querySelectorAll(".lang").forEach(el => el.classList.remove("active"));
  document.querySelectorAll("[id]").forEach(el => {
    if (el.id === lang || el.id.startsWith(lang + "-")) {
      el.classList.add("active");
    }
  });

  document.querySelectorAll(".switch button").forEach(btn => {
    btn.classList.toggle("active", btn.textContent.trim().toLowerCase() === lang);
  });

  document.documentElement.lang = lang === "en" ? "en" : "pl";

  try { localStorage.setItem(LANG_KEY, lang); } catch (_) {}

  // Notify other modules (wheel, etc.) via a custom event.
  document.dispatchEvent(new CustomEvent("langchange", { detail: { lang } }));
};

// Restore saved language on load (before DOMContentLoaded so the IIFE below
// already has the right value when the wheel module reads it).
(function () {
  let saved = "pl";
  try { saved = localStorage.getItem(LANG_KEY) || "pl"; } catch (_) {}
  if (saved === "en") window.switchLang("en");
})();

// ─────────────────────────────────────────────────────────────────────────────
// SHARED DOM-READY BOOTSTRAP
// Scroll reveal, hero parallax, spark particles — all in one listener.
// ─────────────────────────────────────────────────────────────────────────────
document.addEventListener("DOMContentLoaded", () => {

  // ── Scroll reveal ──────────────────────────────────────────────────────────
  const revealObs = new IntersectionObserver(entries => {
    entries.forEach(e => {
      if (e.isIntersecting) {
        e.target.classList.add("visible");
        revealObs.unobserve(e.target); // stop observing once revealed
      }
    });
  }, { threshold: 0.08 });

  document.querySelectorAll(".reveal").forEach(el => revealObs.observe(el));

  // ── Hero parallax ──────────────────────────────────────────────────────────
  const heroImg = document.querySelector(".hero-img");
  if (heroImg) {
    let ticking = false;
    window.addEventListener("scroll", () => {
      if (!ticking) {
        requestAnimationFrame(() => {
          heroImg.style.transform =
            `scale(1.06) translateY(${window.scrollY * 0.25}px)`;
          ticking = false;
        });
        ticking = true;
      }
    }, { passive: true });
  }

  // ── Spark particles on card hover ──────────────────────────────────────────
  document.querySelectorAll(".swieto-card").forEach(card => {
    card.addEventListener("mouseenter", e => {
      const rect = card.getBoundingClientRect();
      for (let i = 0; i < 7; i++) {
        const spark = document.createElement("span");
        const angle = (360 / 7) * i;
        const dist  = 28 + Math.random() * 22;
        const dx    = Math.cos((angle * Math.PI) / 180) * dist;
        const dy    = Math.sin((angle * Math.PI) / 180) * dist;
        Object.assign(spark.style, {
          position:     "absolute",
          left:         (e.clientX - rect.left) + "px",
          top:          (e.clientY - rect.top)  + "px",
          width:        "4px",
          height:       "4px",
          borderRadius: "50%",
          background:   "radial-gradient(circle, #f5e1a4, #c4922a)",
          pointerEvents:"none",
          zIndex:       "20",
          transform:    "translate(-50%,-50%) scale(1)",
          transition:   "transform .5s ease, opacity .5s ease",
          opacity:      "1",
        });
        card.style.position = "relative";
        card.appendChild(spark);
        requestAnimationFrame(() => {
          spark.style.transform =
            `translate(calc(-50% + ${dx}px), calc(-50% + ${dy}px)) scale(0)`;
          spark.style.opacity = "0";
        });
        setTimeout(() => spark.remove(), 520);
      }
    });
  });
});

// ─────────────────────────────────────────────────────────────────────────────
// WHEEL OF THE YEAR
// ─────────────────────────────────────────────────────────────────────────────
document.addEventListener("DOMContentLoaded", () => {
  const data = window.KOLO_DATA;
  if (!data || !data.length) return;

  const svg   = document.getElementById("kolo-svg");
  const group = document.getElementById("kolo-nodes");
  if (!svg || !group) return;

  const CX       = 250, CY = 250;
  const isMobile = window.innerWidth < 768;
  const NODE_R   = isMobile ? 130 : 155;
  const LABEL_R  = isMobile ? 160 : 182;

  const currentLang = () => {
    try { return localStorage.getItem(LANG_KEY) || "pl"; } catch (_) { return "pl"; }
  };

  // ── Panel ──────────────────────────────────────────────────────────────────
  const koloWrap = document.querySelector(".kolo-wrap");
  const panel = document.createElement("div");
  panel.id = "kolo-panel";
  panel.innerHTML = `
    <div class="kolo-panel-inner">
      <div class="kolo-panel-rune" aria-hidden="true">ᛉ</div>
      <div class="kolo-panel-text">
        <span class="kolo-panel-name"></span>
        <span class="kolo-panel-sub"></span>
      </div>
      <a class="kolo-panel-btn" href="#" aria-label="Przejdź do święta">
        <span class="kolo-panel-btn-label-pl">Odwiedź</span>
        <span class="kolo-panel-btn-label-en">Visit</span>
      </a>
    </div>
    <div class="kolo-panel-hint">
      <span class="kolo-panel-hint-pl">Obróć koło, by wybrać święto</span>
      <span class="kolo-panel-hint-en">Spin the wheel to choose a feast</span>
    </div>
  `;
  koloWrap.parentNode.insertBefore(panel, koloWrap);

  const panelName = panel.querySelector(".kolo-panel-name");
  const panelSub  = panel.querySelector(".kolo-panel-sub");
  const panelBtn  = panel.querySelector(".kolo-panel-btn");

  // ── Tooltip (for nodes whose label is hidden) ───────────────────────────────
  const tooltip      = document.getElementById("kolo-tooltip");
  const tooltipTitle = tooltip ? tooltip.querySelector(".kolo-tooltip-title") : null;

  const showTooltip = (targetEl, text) => {
    if (!tooltip || !tooltipTitle) return;
    const wrapRect = koloWrap.getBoundingClientRect();
    const elRect   = targetEl.getBoundingClientRect();
    tooltipTitle.textContent = text;
    tooltip.style.left = (elRect.left + elRect.width / 2 - wrapRect.left) + "px";
    tooltip.style.top  = (elRect.top - wrapRect.top) + "px";
    tooltip.classList.add("kolo-tooltip-visible");
    tooltip.setAttribute("aria-hidden", "false");
  };
  const hideTooltip = () => {
    if (!tooltip) return;
    tooltip.classList.remove("kolo-tooltip-visible");
    tooltip.setAttribute("aria-hidden", "true");
  };

  // ── Label helpers ──────────────────────────────────────────────────────────
  const buildLabel = (el, title, atX) => {
    el.replaceChildren();
    // Wrap onto two lines only if the title is long enough and contains a space.
    if (title.length > 7 && title.includes(" ")) {
      const words = title.split(" ");
      const mid   = Math.ceil(words.length / 2);
      [words.slice(0, mid).join(" "), words.slice(mid).join(" ")].forEach((line, i) => {
        const ts = document.createElementNS("http://www.w3.org/2000/svg", "tspan");
        ts.setAttribute("x",  atX);
        ts.setAttribute("dy", i === 0 ? "-0.55em" : "1.15em");
        ts.textContent = line;
        el.appendChild(ts);
      });
    } else {
      el.textContent = title;
    }
  };

  // ── Build nodes ────────────────────────────────────────────────────────────
  // Labels live in a SEPARATE group that is never CSS-transformed.
  // Hidden during spin-in; revealed on animationend.
  const labelGroup = document.createElementNS("http://www.w3.org/2000/svg", "g");
  labelGroup.id = "kolo-labels";
  labelGroup.setAttribute("visibility", "hidden");
  svg.appendChild(labelGroup);

  const nodeEls = [];

  // Even spacing: position on the wheel comes from ORDER (index), not from
  // the real calendar date. The real date still drives the panel subtitle
  // and the "closest to today" snap on load — it just no longer squeezes
  // nodes together when two feasts happen to fall close in the calendar.
  const angleStep = 360 / data.length;
  const angles    = data.map((_, i) => i * angleStep);

  data.forEach((s, i) => {
    const rad0 = ((angles[i] - 90) * Math.PI) / 180;
    const x0   = CX + NODE_R  * Math.cos(rad0);
    const y0   = CY + NODE_R  * Math.sin(rad0);
    const lx0  = CX + LABEL_R * Math.cos(rad0);
    const ly0  = CY + LABEL_R * Math.sin(rad0);

    // Dot + halo in the rotating group.
    const g    = document.createElementNS("http://www.w3.org/2000/svg", "g");
    g.setAttribute("class", "kolo-node");
    g.setAttribute("tabindex", "-1"); // focus handled by the SVG root, not per-node

    const halo = document.createElementNS("http://www.w3.org/2000/svg", "circle");
    halo.setAttribute("cx", x0); halo.setAttribute("cy", y0); halo.setAttribute("r", "20");
    halo.setAttribute("fill", s.kolor); halo.setAttribute("opacity", "0.08");
    halo.setAttribute("class", "node-halo");

    const circle = document.createElementNS("http://www.w3.org/2000/svg", "circle");
    circle.setAttribute("cx", x0); circle.setAttribute("cy", y0); circle.setAttribute("r", "10");
    circle.setAttribute("fill", s.kolor);
    circle.setAttribute("stroke", "#0f1117"); circle.setAttribute("stroke-width", "2");
    circle.setAttribute("filter", "url(#glow)");

    g.appendChild(halo);
    g.appendChild(circle);
    group.appendChild(g);

    // Label in the STATIC group.
    const label = document.createElementNS("http://www.w3.org/2000/svg", "text");
    label.setAttribute("x", lx0); label.setAttribute("y", ly0);
    label.setAttribute("text-anchor",
      lx0 < CX - 8 ? "start" : lx0 > CX + 8 ? "end" : "middle");
    label.setAttribute("dominant-baseline", "middle");
    label.setAttribute("font-size", isMobile ? "13" : "14");
    label.setAttribute("font-family", "'Playfair Display', serif");
    label.setAttribute("fill", "rgba(245,225,164,0.65)");
    label.setAttribute("class", "node-label");
    label.setAttribute("data-pl", s.tytul_pl);
    label.setAttribute("data-en", s.tytul_en);
    buildLabel(label, s.tytul_pl, lx0);
    labelGroup.appendChild(label);

    const entry = { g, halo, circle, label, data: s, near: true };
    nodeEls.push(entry);

    // Tap/hover a dot directly: show its name if the label is currently
    // hidden, and jump the wheel to it on click (independent of drag).
    g.addEventListener("mouseenter", () => {
      if (!entry.near) showTooltip(circle, currentLang() === "en" ? s.tytul_en : s.tytul_pl);
    });
    g.addEventListener("mouseleave", hideTooltip);
    g.addEventListener("click", () => {
      if (didDrag) return;
      const idx = nodeEls.indexOf(entry);
      wheelAngle = nearestSnap(idx, wheelAngle);
      applyRotation(wheelAngle, true);
      setActiveNode(idx);
    });
  });

  // ── State ──────────────────────────────────────────────────────────────────
  // wheelAngle: accumulated rotation in degrees (unbounded — never wraps).
  // Snapping always moves to the nearest snap angle from the current value
  // by the shortest path, so there are no surprise full-circle jumps.
  let wheelAngle = 0;
  let activeIdx  = 0;
  let dialActive = false;

  // snapBase[i]: base angle (−180..180) that puts node i at the top.
  const snapBase = angles.map(kat => {
    let a = ((-kat) % 360 + 360) % 360; // 0..360
    if (a > 180) a -= 360;               // −180..180
    return a;
  });

  // Return the snap angle for node i closest to `from` (no wrap jump).
  const nearestSnap = (i, from) => {
    let base       = snapBase[i];
    const diff     = from - base;
    base          += Math.round(diff / 360) * 360;
    return base;
  };

  // ── Apply rotation ─────────────────────────────────────────────────────────
  // Dots: CSS rotate on group (GPU, smooth).
  // Labels: SVG x/y attributes — zero CSS transform, always upright.
  const applyRotation = (deg, snap = false) => {
    group.style.transition     = snap ? "transform 0.42s cubic-bezier(0.25,1,0.5,1)" : "none";
    group.style.transformOrigin = `${CX}px ${CY}px`;
    group.style.transform      = `rotate(${deg}deg)`;

    const radOff = (deg * Math.PI) / 180;
    const n      = data.length;

    nodeEls.forEach((entry, i) => {
      const { label } = entry;
      const rad = ((angles[i] - 90) * Math.PI) / 180 + radOff;
      const lx  = CX + LABEL_R * Math.cos(rad);
      const ly  = CY + LABEL_R * Math.sin(rad);
      label.setAttribute("x", lx);
      label.setAttribute("y", ly);
      // Anchor grows the text TOWARD the center rather than outward, so
      // labels near the left/right edge never run off the wheel.
      label.setAttribute("text-anchor", lx < CX - 8 ? "start" : lx > CX + 8 ? "end" : "middle");
      label.querySelectorAll("tspan").forEach(ts => ts.setAttribute("x", lx));

      // Only the active node and its immediate left/right neighbours ever
      // show a text label — max 3 labels on screen at any time, regardless
      // of how many feasts are on the wheel or how they're spaced. This is
      // what keeps a 20+ item wheel from turning into overlapping text.
      const idxDist = Math.min(
        Math.abs(i - activeIdx),
        n - Math.abs(i - activeIdx)
      );
      const near = idxDist <= 1;
      entry.near = near;
      label.style.visibility = near ? "visible" : "hidden";
      label.style.opacity    = idxDist === 0 ? "1" : near ? "0.55" : "0";
    });
  };

  // ── Highlight active node ──────────────────────────────────────────────────
  let panelTimer = null;
  const setActiveNode = (idx) => {
    activeIdx    = ((idx % data.length) + data.length) % data.length;
    const lang   = currentLang();
    const s      = data[activeIdx];

    clearTimeout(panelTimer);
    panel.classList.add("kolo-panel-changing");
    panelTimer = setTimeout(() => {
      panelName.textContent = lang === "en" ? s.tytul_en    : s.tytul_pl;
      // podtytul_* is now included in kolo_data by the view.
      panelSub.textContent  = lang === "en"
        ? (s.podtytul_en || "")
        : (s.podtytul_pl || "");
      panelBtn.href         = s.url;
      panel.classList.remove("kolo-panel-changing");
    }, 160);

    nodeEls.forEach(({ halo: h, circle: c, label: l }, i) => {
      const active = i === activeIdx;
      h.setAttribute("opacity", active ? "0.35" : "0.08");
      c.setAttribute("r",       active ? "14"   : "10");
      l.setAttribute("fill",    active
        ? "rgba(245,225,164,1)"
        : "rgba(245,225,164,0.65)");
      l.style.fontWeight = active ? "700" : "";
    });
  };

  // ── Snap to nearest node ───────────────────────────────────────────────────
  const snapToNearest = () => {
    let bestIdx = 0, bestDist = Infinity;
    data.forEach((_, i) => {
      const target = nearestSnap(i, wheelAngle);
      const dist   = Math.abs(wheelAngle - target);
      if (dist < bestDist) { bestDist = dist; bestIdx = i; }
    });
    wheelAngle = nearestSnap(bestIdx, wheelAngle);
    applyRotation(wheelAngle, true);
    setActiveNode(bestIdx);
  };

  // ── Drag / swipe ───────────────────────────────────────────────────────────
  // Track delta between consecutive move events (not from drag-start),
  // so wrap-around at ±180° never causes a jump.
  let dragging     = false;
  let prevPtrAngle = 0;
  let velDeg       = 0;   // degrees/ms
  let prevTime     = 0;

  // Distinguishes a real drag from a tap/click on a node. A tap should
  // select that node directly; a drag should fall back to snap-to-nearest.
  let didDrag            = false;
  let dragStartWheelAngle = 0;

  const ptrAngle = (e) => {
    const r  = svg.getBoundingClientRect();
    const cx = r.left + r.width  / 2;
    const cy = r.top  + r.height / 2;
    const px = (e.touches ? e.touches[0].clientX : e.clientX) - cx;
    const py = (e.touches ? e.touches[0].clientY : e.clientY) - cy;
    return Math.atan2(py, px) * 180 / Math.PI;
  };

  const onDragStart = (e) => {
    if (!dialActive) return;
    dragging             = true;
    didDrag              = false;
    dragStartWheelAngle  = wheelAngle;
    prevPtrAngle         = ptrAngle(e);
    velDeg               = 0;
    prevTime             = Date.now();
    group.style.transition = "none";
    e.preventDefault();
  };

  const onDragMove = (e) => {
    if (!dragging) return;
    e.preventDefault();

    const now = Date.now();
    const cur = ptrAngle(e);

    // Shortest-arc delta between previous and current pointer angle.
    let delta = cur - prevPtrAngle;
    if (delta >  180) delta -= 360;
    if (delta < -180) delta += 360;

    // Update velocity (degrees per ms), lightly smoothed.
    const dt     = Math.max(1, now - prevTime);
    velDeg       = velDeg * 0.6 + (delta / dt) * 0.4;

    wheelAngle  += delta;
    prevPtrAngle = cur;
    prevTime     = now;

    if (Math.abs(wheelAngle - dragStartWheelAngle) > 2) didDrag = true;

    applyRotation(wheelAngle);

    // Live-highlight closest node without snapping the wheel yet.
    let bestIdx = 0, bestDist = Infinity;
    data.forEach((_, i) => {
      const target = nearestSnap(i, wheelAngle);
      const dist   = Math.abs(wheelAngle - target);
      if (dist < bestDist) { bestDist = dist; bestIdx = i; }
    });
    if (bestIdx !== activeIdx) setActiveNode(bestIdx);
  };

  const onDragEnd = () => {
    if (!dragging) return;
    dragging = false;
    // A tap with no real movement is handled by the node's own click
    // handler instead — avoids fighting over which node to snap to.
    if (!didDrag) return;
    // Small momentum nudge — capped so it can't spin past 2 nodes.
    const nudge = Math.max(-60, Math.min(60, velDeg * 120));
    wheelAngle += nudge;
    snapToNearest();
  };

  svg.addEventListener("mousedown",    onDragStart, { passive: false });
  window.addEventListener("mousemove", onDragMove,  { passive: false });
  window.addEventListener("mouseup",   onDragEnd);

  svg.addEventListener("touchstart", onDragStart, { passive: false });
  svg.addEventListener("touchmove",  onDragMove,  { passive: false });
  svg.addEventListener("touchend",   onDragEnd);

  // Scroll wheel — one step per tick.
  svg.addEventListener("wheel", (e) => {
    if (!dialActive) return;
    e.preventDefault();
    const dir  = e.deltaY > 0 ? 1 : -1;
    const next = ((activeIdx + dir) + data.length) % data.length;
    wheelAngle = nearestSnap(next, wheelAngle);
    applyRotation(wheelAngle, true);
    setActiveNode(next);
  }, { passive: false });

  // Keyboard navigation.
  svg.setAttribute("tabindex", "0");
  svg.addEventListener("keydown", (e) => {
    if (!dialActive) return;
    if (e.key === "ArrowLeft" || e.key === "ArrowUp") {
      e.preventDefault();
      const next = ((activeIdx - 1) + data.length) % data.length;
      wheelAngle = nearestSnap(next, wheelAngle);
      applyRotation(wheelAngle, true);
      setActiveNode(next);
    }
    if (e.key === "ArrowRight" || e.key === "ArrowDown") {
      e.preventDefault();
      const next = (activeIdx + 1) % data.length;
      wheelAngle = nearestSnap(next, wheelAngle);
      applyRotation(wheelAngle, true);
      setActiveNode(next);
    }
    if (e.key === "Enter" || e.key === " ") {
      e.preventDefault();
      window.location.href = data[activeIdx].url;
    }
  });

  // ── Spin-in intro ──────────────────────────────────────────────────────────
  // Find the node closest to today's calendar date and snap to it on load.
  //
  // Each feast has a `dzien_roku` field (1–365, set in the admin) representing
  // its real calendar position. We compare today's day-of-year against those
  // values. The year is treated as circular so Dec 31 → Jan 1 wraps correctly.
  // This is fully robust to any number of feasts and any kolo_kat layout.
  const closestToToday = (() => {
    const now       = new Date();
    const start     = new Date(now.getFullYear(), 0, 0);
    const todayDoy  = Math.floor((now - start) / 86_400_000); // 1–365

    let bestIdx = 0, bestDist = Infinity;
    data.forEach((s, i) => {
      let diff = Math.abs(s.dzien_roku - todayDoy);
      if (diff > 182) diff = 365 - diff; // wrap-aware (circular year)
      if (diff < bestDist) { bestDist = diff; bestIdx = i; }
    });
    return bestIdx;
  })();

  svg.classList.add("spinning");

  svg.addEventListener("animationend", () => {
    svg.classList.remove("spinning");

    // Snap to the festival closest to today.
    wheelAngle = nearestSnap(closestToToday, 0);
    applyRotation(wheelAngle, true);
    setActiveNode(closestToToday);

    labelGroup.setAttribute("visibility", "visible");
    panel.classList.add("kolo-panel-visible");
    svg.style.cursor = "grab";
    dialActive       = true;
  }, { once: true });

  // ── Language switch hook ───────────────────────────────────────────────────
  // Uses CustomEvent instead of monkey-patching switchLang.
  document.addEventListener("langchange", ({ detail: { lang } }) => {
    nodeEls.forEach(({ label }) => {
      const title = lang === "en" ? label.dataset.en : label.dataset.pl;
      buildLabel(label, title, label.getAttribute("x"));
    });

    const centerLabel = document.getElementById("kolo-center-label");
    if (centerLabel) {
      centerLabel.textContent = lang === "en" ? centerLabel.dataset.en : centerLabel.dataset.pl;
    }

    if (dialActive) {
      const s = data[activeIdx];
      panelName.textContent = lang === "en" ? s.tytul_en : s.tytul_pl;
      panelSub.textContent  = lang === "en"
        ? (s.podtytul_en || "")
        : (s.podtytul_pl || "");
    }

    // Toggle bilingual button/hint labels.
    panel.querySelectorAll(
      ".kolo-panel-btn-label-pl, .kolo-panel-btn-label-en," +
      ".kolo-panel-hint-pl, .kolo-panel-hint-en"
    ).forEach(el => {
      el.style.display = el.classList.contains(`kolo-panel-btn-label-${lang}`) ||
                         el.classList.contains(`kolo-panel-hint-${lang}`)
        ? "inline" : "none";
    });
  });
});


// ─────────────────────────────────────────────────────────────────────────────
// PREV / NEXT KEYBOARD NAVIGATION (detail page)
// ─────────────────────────────────────────────────────────────────────────────
document.addEventListener("keydown", e => {
  // Ignore when focus is inside a form field or the wheel SVG handles it.
  if (["INPUT", "TEXTAREA", "SELECT"].includes(document.activeElement.tagName)) return;
  if (document.activeElement.id === "kolo-svg") return;

  const lang  = (() => { try { return localStorage.getItem(LANG_KEY) || "pl"; } catch (_) { return "pl"; } })();
  const navEl = document.getElementById(`${lang}-nav`);
  if (!navEl) return;

  if (e.key === "ArrowLeft") {
    const prev = navEl.querySelector(".nav-prev");
    if (prev) { e.preventDefault(); window.location.href = prev.href; }
  }
  if (e.key === "ArrowRight") {
    const next = navEl.querySelector(".nav-next");
    if (next) { e.preventDefault(); window.location.href = next.href; }
  }
});

// ─────────────────────────────────────────────────────────────────────────────
// GOLDEN RUNE CURSOR TRAIL
// Spawns a random Elder Futhark rune near the cursor; floats up and fades.
// Skipped on touch devices to avoid lag.
// ─────────────────────────────────────────────────────────────────────────────
(function () {
  if (window.matchMedia("(hover: none)").matches) return;

  const RUNES    = ["ᚠ","ᚢ","ᚦ","ᚨ","ᚱ","ᚲ","ᚷ","ᚹ","ᚺ","ᚾ","ᛁ","ᛃ","ᛇ","ᛈ","ᛉ","ᛊ","ᛏ","ᛒ","ᛖ","ᛗ","ᛚ","ᛜ","ᛞ","ᛟ"];
  const THROTTLE = 120; // ms between spawns — keeps it subtle
  let last       = 0;

  document.addEventListener("mousemove", e => {
    const now = Date.now();
    if (now - last < THROTTLE) return;
    last = now;

    const el       = document.createElement("span");
    el.className   = "rune-trail";
    el.textContent = RUNES[Math.floor(Math.random() * RUNES.length)];
    // Centered on cursor; small random jitter so consecutive runes don't stack.
    el.style.left  = (e.clientX + (Math.random() * 18 - 9)) + "px";
    el.style.top   = (e.clientY + (Math.random() * 18 - 9)) + "px";
    document.body.appendChild(el);

    el.addEventListener("animationend", () => el.remove(), { once: true });
  });
})();

// ─────────────────────────────────────────────────────────────────────────────
// SCROLL PROGRESS BAR
// Thin golden line at the very top of the page showing read progress.
// ─────────────────────────────────────────────────────────────────────────────
(function () {
  const bar  = document.createElement("div");
  bar.id     = "scroll-progress";
  document.body.prepend(bar);

  let ticking = false;
  window.addEventListener("scroll", () => {
    if (!ticking) {
      requestAnimationFrame(() => {
        const scrolled = window.scrollY;
        const total    = document.documentElement.scrollHeight - window.innerHeight;
        bar.style.width = total > 0 ? ((scrolled / total) * 100) + "%" : "0%";
        ticking = false;
      });
      ticking = true;
    }
  }, { passive: true });
})();