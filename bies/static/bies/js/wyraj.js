// LOADER
document.addEventListener("DOMContentLoaded", () => {
  const loader = document.getElementById("loader");
  if (!loader) return;
  const hide = () => {
    loader.style.opacity = "0";
    setTimeout(() => { loader.style.display = "none"; }, 620);
  };
  window.addEventListener("load", hide);
  setTimeout(hide, 3500); // safety fallback
});

// LANG SWITCH
const LANG_KEY = "wyraj_lang";

window.switchLang = function (lang) {
  // Hide all .lang elements, then show those matching lang or lang-
  document.querySelectorAll(".lang").forEach(el => {
    el.classList.remove("active");
  });
  document.querySelectorAll(`[id^="${lang}"]`).forEach(el => {
    // Exact match: "pl", "pl-footer", "pl-nav", "pl-grid"
    if (el.id === lang || el.id.startsWith(lang + "-")) {
      el.classList.add("active");
    }
  });

  document.querySelectorAll(".switch button").forEach(btn => {
    btn.classList.toggle("active", btn.textContent.trim().toLowerCase() === lang);
  });

  document.documentElement.lang = lang === "en" ? "en" : "pl";

  try { localStorage.setItem(LANG_KEY, lang); } catch (_) {}
};

// Restore saved language on load
(function () {
  let saved = "pl";
  try { saved = localStorage.getItem(LANG_KEY) || "pl"; } catch (_) {}
  if (saved === "en") window.switchLang("en");
})();

// SCROLL REVEAL
document.addEventListener("DOMContentLoaded", () => {
  const obs = new IntersectionObserver(entries => {
    entries.forEach(e => {
      if (e.isIntersecting) {
        e.target.classList.add("visible");
        obs.unobserve(e.target);
      }
    });
  }, { threshold: 0.08 });

  document.querySelectorAll(".reveal").forEach(el => obs.observe(el));
});

// HERO PARALLAX
document.addEventListener("DOMContentLoaded", () => {
  const heroImg = document.querySelector(".hero-img");
  if (!heroImg) return;
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
  });
});

// SPARK PARTICLES
document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".swieto-card").forEach(card => {
    card.addEventListener("mouseenter", e => {
      const rect = card.getBoundingClientRect();
      for (let i = 0; i < 7; i++) {
        const spark = document.createElement("span");
        const angle = (360 / 7) * i;
        const dist  = 28 + Math.random() * 22;
        const dx = Math.cos((angle * Math.PI) / 180) * dist;
        const dy = Math.sin((angle * Math.PI) / 180) * dist;
        Object.assign(spark.style, {
          position: "absolute",
          left: (e.clientX - rect.left) + "px",
          top:  (e.clientY - rect.top)  + "px",
          width: "4px", height: "4px", borderRadius: "50%",
          background: "radial-gradient(circle, #f5e1a4, #c4922a)",
          pointerEvents: "none", zIndex: "20",
          transform: "translate(-50%,-50%) scale(1)",
          transition: "transform .5s ease, opacity .5s ease",
          opacity: "1",
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

// WHEEL OF THE YEAR
document.addEventListener("DOMContentLoaded", () => {
  const data = window.KOLO_DATA;
  if (!data || !data.length) return;

  const svg   = document.getElementById("kolo-svg");
  const group = document.getElementById("kolo-nodes");
  if (!svg || !group) return;

  const CX = 250, CY = 250;
  const isMobile = window.innerWidth < 768;
  const NODE_R   = isMobile ? 130 : 155;
  const LABEL_R  = isMobile ? 170 : 192;

  const currentLang = () => {
    try { return localStorage.getItem(LANG_KEY) || "pl"; } catch (_) { return "pl"; }
  };

  // ── Panel ───────────────────────────────────────────────────────────────────
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

  // ── Label helpers ───────────────────────────────────────────────────────────
  const buildLabel = (el, title, atX) => {
    el.replaceChildren();
    if (title.length > 7 && title.includes(" ")) {
      const words = title.split(" ");
      const mid = Math.ceil(words.length / 2);
      [words.slice(0, mid).join(" "), words.slice(mid).join(" ")].forEach((line, i) => {
        const ts = document.createElementNS("http://www.w3.org/2000/svg", "tspan");
        ts.setAttribute("x", atX);
        ts.setAttribute("dy", i === 0 ? "-0.55em" : "1.15em");
        ts.textContent = line;
        el.appendChild(ts);
      });
    } else {
      el.textContent = title;
    }
  };

  // ── Build nodes ─────────────────────────────────────────────────────────────
  // Labels live in a SEPARATE group that is never CSS-transformed.
  // During spin-in it is hidden; revealed on animationend.
  const labelGroup = document.createElementNS("http://www.w3.org/2000/svg", "g");
  labelGroup.id = "kolo-labels";
  labelGroup.setAttribute("visibility", "hidden"); // hidden during spin-in
  svg.appendChild(labelGroup);

  const nodeEls = [];

  data.forEach((s) => {
    const rad0 = ((s.kat - 90) * Math.PI) / 180;
    const x0   = CX + NODE_R  * Math.cos(rad0);
    const y0   = CY + NODE_R  * Math.sin(rad0);
    const lx0  = CX + LABEL_R * Math.cos(rad0);
    const ly0  = CY + LABEL_R * Math.sin(rad0);

    // dot + halo in the rotating group
    const g = document.createElementNS("http://www.w3.org/2000/svg", "g");
    g.setAttribute("class", "kolo-node");

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

    // label in the STATIC group
    const label = document.createElementNS("http://www.w3.org/2000/svg", "text");
    label.setAttribute("x", lx0); label.setAttribute("y", ly0);
    label.setAttribute("text-anchor", lx0 < CX - 8 ? "end" : lx0 > CX + 8 ? "start" : "middle");
    label.setAttribute("dominant-baseline", "middle");
    label.setAttribute("font-size", isMobile ? "13" : "14");
    label.setAttribute("font-family", "'Playfair Display', serif");
    label.setAttribute("fill", "rgba(245,225,164,0.65)");
    label.setAttribute("class", "node-label");
    label.setAttribute("data-pl", s.tytul_pl);
    label.setAttribute("data-en", s.tytul_en);
    buildLabel(label, s.tytul_pl, lx0);
    labelGroup.appendChild(label);

    nodeEls.push({ g, halo, circle, label, data: s });
  });

  // ── State ───────────────────────────────────────────────────────────────────
  // wheelAngle: accumulated rotation in degrees (unbounded — never wraps).
  // Snapping always moves to the nearest snap angle *from the current value*
  // by the shortest path, so we never get surprise full-circle jumps.
  let wheelAngle = 0;
  let activeIdx  = 0;
  let dialActive = false;

  // snapBase[i]: the base angle (−180..180) that puts node i at the top.
  // During snapping we find the version of this angle nearest to wheelAngle.
  const snapBase = data.map(s => {
    let a = ((-s.kat) % 360 + 360) % 360;   // 0..360
    if (a > 180) a -= 360;                   // −180..180
    return a;
  });

  // Return the snap angle for node i that is closest to `from` (no wrap jump).
  const nearestSnap = (i, from) => {
    let base = snapBase[i];
    // Shift base by full rotations until it is closest to `from`
    const diff = from - base;
    base += Math.round(diff / 360) * 360;
    return base;
  };

  // ── Apply rotation ──────────────────────────────────────────────────────────
  // Dots: CSS rotate on group (GPU, smooth).
  // Labels: SVG x/y attributes only — zero CSS transform, always upright.
  const applyRotation = (deg, snap = false) => {
    group.style.transition    = snap ? "transform 0.42s cubic-bezier(0.25,1,0.5,1)" : "none";
    group.style.transformOrigin = `${CX}px ${CY}px`;
    group.style.transform     = `rotate(${deg}deg)`;

    const radOff = (deg * Math.PI) / 180;
    nodeEls.forEach(({ label }, i) => {
      const rad = ((data[i].kat - 90) * Math.PI) / 180 + radOff;
      const lx  = CX + LABEL_R * Math.cos(rad);
      const ly  = CY + LABEL_R * Math.sin(rad);
      label.setAttribute("x", lx);
      label.setAttribute("y", ly);
      label.setAttribute("text-anchor", lx < CX - 8 ? "end" : lx > CX + 8 ? "start" : "middle");
      label.querySelectorAll("tspan").forEach(ts => ts.setAttribute("x", lx));
    });
  };

  // ── Highlight active node ───────────────────────────────────────────────────
  let panelTimer = null;
  const setActiveNode = (idx) => {
    activeIdx = ((idx % data.length) + data.length) % data.length;
    const lang = currentLang();
    const s = data[activeIdx];

    clearTimeout(panelTimer);
    panel.classList.add("kolo-panel-changing");
    panelTimer = setTimeout(() => {
      panelName.textContent = lang === "en" ? s.tytul_en : s.tytul_pl;
      panelSub.textContent  = s.data_pl ? (lang === "en" ? (s.data_en || "") : s.data_pl) : "";
      panelBtn.href         = s.url;
      panel.classList.remove("kolo-panel-changing");
    }, 160);

    nodeEls.forEach(({ halo: h, circle: c, label: l }, i) => {
      const active = i === activeIdx;
      h.setAttribute("opacity", active ? "0.35" : "0.08");
      c.setAttribute("r",       active ? "14"   : "10");
      l.setAttribute("fill",    active ? "rgba(245,225,164,1)" : "rgba(245,225,164,0.65)");
      l.style.fontWeight = active ? "700" : "";
    });
  };

  // ── Snap to nearest node ────────────────────────────────────────────────────
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

  // ── Drag / swipe ────────────────────────────────────────────────────────────
  // Track delta between consecutive move events (not from drag-start),
  // so wrap-around at ±180° never causes a jump.
  let dragging    = false;
  let prevPtrAngle = 0;
  let velDeg      = 0;  // degrees/ms
  let prevTime    = 0;

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
    dragging     = true;
    prevPtrAngle = ptrAngle(e);
    velDeg       = 0;
    prevTime     = Date.now();
    group.style.transition = "none";
    e.preventDefault();
  };

  const onDragMove = (e) => {
    if (!dragging) return;
    e.preventDefault();

    const now  = Date.now();
    const cur  = ptrAngle(e);

    // shortest-arc delta between previous and current pointer angle
    let delta = cur - prevPtrAngle;
    if (delta >  180) delta -= 360;
    if (delta < -180) delta += 360;

    // update velocity (degrees per ms, smoothed slightly)
    const dt = Math.max(1, now - prevTime);
    velDeg   = velDeg * 0.6 + (delta / dt) * 0.4;

    wheelAngle   += delta;
    prevPtrAngle  = cur;
    prevTime      = now;

    applyRotation(wheelAngle);

    // live highlight closest node without snapping wheel
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
    // small momentum nudge (capped so it can't spin past 2 nodes)
    const nudge = Math.max(-60, Math.min(60, velDeg * 120));
    wheelAngle += nudge;
    snapToNearest();
  };

  svg.addEventListener("mousedown",   onDragStart, { passive: false });
  window.addEventListener("mousemove", onDragMove,  { passive: false });
  window.addEventListener("mouseup",   onDragEnd);

  svg.addEventListener("touchstart", onDragStart, { passive: false });
  svg.addEventListener("touchmove",  onDragMove,  { passive: false });
  svg.addEventListener("touchend",   onDragEnd);

  // Scroll wheel — one step per tick
  svg.addEventListener("wheel", (e) => {
    if (!dialActive) return;
    e.preventDefault();
    const dir  = e.deltaY > 0 ? 1 : -1;
    const next = ((activeIdx + dir) + data.length) % data.length;
    wheelAngle = nearestSnap(next, wheelAngle);
    applyRotation(wheelAngle, true);
    setActiveNode(next);
  }, { passive: false });

  // Keyboard
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

  // ── Spin-in intro ───────────────────────────────────────────────────────────
  // Labels hidden until spin ends (labelGroup visibility="hidden" set above).
  svg.classList.add("spinning");

  svg.addEventListener("animationend", () => {
    svg.classList.remove("spinning");

    // Snap to node closest to 0° (top)
    let startIdx = 0, minDist = Infinity;
    data.forEach((s, i) => {
      const d = Math.abs(nearestSnap(i, 0));
      if (d < minDist) { minDist = d; startIdx = i; }
    });
    wheelAngle = nearestSnap(startIdx, 0);
    applyRotation(wheelAngle, true);
    setActiveNode(startIdx);

    // Reveal labels and panel
    labelGroup.setAttribute("visibility", "visible");
    panel.classList.add("kolo-panel-visible");
    svg.style.cursor = "grab";
    dialActive = true;
  }, { once: true });

  // ── Language switch hook ────────────────────────────────────────────────────
  const origSwitch = window.switchLang;
  window.switchLang = function (lang) {
    origSwitch(lang);

    nodeEls.forEach(({ label }) => {
      const title = lang === "en" ? label.dataset.en : label.dataset.pl;
      const atX   = label.getAttribute("x");
      buildLabel(label, title, atX);
    });

    if (dialActive) {
      const s = data[activeIdx];
      panelName.textContent = lang === "en" ? s.tytul_en : s.tytul_pl;
    }

    panel.querySelectorAll(".kolo-panel-btn-label-pl, .kolo-panel-btn-label-en").forEach(el => {
      el.style.display = el.classList.contains(`kolo-panel-btn-label-${lang}`) ? "inline" : "none";
    });
    panel.querySelectorAll(".kolo-panel-hint-pl, .kolo-panel-hint-en").forEach(el => {
      el.style.display = el.classList.contains(`kolo-panel-hint-${lang}`) ? "inline" : "none";
    });
  };
});

// READER MODE
document.addEventListener("DOMContentLoaded", () => {
  const btn  = document.getElementById("readerToggle");
  if (!btn) return;

  const READER_KEY = "wyraj_reader";
  const body = document.body;

  const apply = (on) => {
    body.classList.toggle("reader-mode", on);
    btn.setAttribute("aria-pressed", String(on));
    btn.innerHTML = on
      ? '<i class="fa-solid fa-book-open-reader"></i>'
      : '<i class="fa-solid fa-book-open"></i>';
    btn.title = on ? "Wyłącz tryb czytania" : "Tryb czytania";
    try { localStorage.setItem(READER_KEY, on ? "1" : "0"); } catch (_) {}
  };

  // Restore saved state (default: reader mode OFF)
  let saved = false;
  try {
    const stored = localStorage.getItem(READER_KEY);
    if (stored !== null) saved = stored === "1";
  } catch (_) {}
  apply(saved);

  btn.addEventListener("click", () => apply(!body.classList.contains("reader-mode")));
});

document.addEventListener("keydown", e => {
  // Ignore when focus is inside a form field
  if (["INPUT", "TEXTAREA", "SELECT"].includes(document.activeElement.tagName)) return;
  const lang = (() => { try { return localStorage.getItem("wyraj_lang") || "pl"; } catch(_){return "pl";} })();
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

// Spawns a random Elder Futhark rune near the cursor that floats up and fades.
// Only active on non-touch devices to avoid lag on mobile.
(function () {
  if (window.matchMedia("(hover: none)").matches) return; // skip on touch

  const RUNES = ["ᚠ","ᚢ","ᚦ","ᚨ","ᚱ","ᚲ","ᚷ","ᚹ","ᚺ","ᚾ","ᛁ","ᛃ","ᛇ","ᛈ","ᛉ","ᛊ","ᛏ","ᛒ","ᛖ","ᛗ","ᛚ","ᛜ","ᛞ","ᛟ"];
  let last = 0;
  const THROTTLE = 120; // ms between spawns — keeps it subtle

  document.addEventListener("mousemove", e => {
    const now = Date.now();
    if (now - last < THROTTLE) return;
    last = now;

    const el = document.createElement("span");
    el.className = "rune-trail";
    el.textContent = RUNES[Math.floor(Math.random() * RUNES.length)];
    // Small random offset so consecutive runes don't stack
    el.style.left = (e.clientX + (Math.random() * 18 - 9)) + "px";
    el.style.top  = (e.clientY + (Math.random() * 18 - 9)) + "px";
    document.body.appendChild(el);

    // Remove after animation ends (~900ms)
    el.addEventListener("animationend", () => el.remove(), { once: true });
  });
})();

// Thin golden line at the very top of the page showing read progress.
(function () {
  const bar = document.createElement("div");
  bar.id = "scroll-progress";
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
  });
})();