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

  const svg     = document.getElementById("kolo-svg");
  const group   = document.getElementById("kolo-nodes");
  const tooltip = document.getElementById("kolo-tooltip");
  if (!svg || !group) return;

  const CX = 250;
  const CY = 250;
  const isMobile = window.innerWidth < 768;

  const NODE_R  = isMobile ? 130 : 155;
  const LABEL_R = isMobile ? 170 : 192;

  const currentLang = () => {
    try { return localStorage.getItem(LANG_KEY) || "pl"; } catch (_) { return "pl"; }
  };

  // ── build the "active feast" panel above the wheel ──────────────────────────
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

  // pointer to panel elements
  const panelName = panel.querySelector(".kolo-panel-name");
  const panelSub  = panel.querySelector(".kolo-panel-sub");
  const panelBtn  = panel.querySelector(".kolo-panel-btn");

  // ── build SVG nodes (static positions, wheel rotates as a whole) ─────────────
  const nodeEls = []; // {g, halo, circle, label, data}

  data.forEach((s) => {
    const rad = ((s.kat - 90) * Math.PI) / 180;
    const x = CX + NODE_R * Math.cos(rad);
    const y = CY + NODE_R * Math.sin(rad);

    const g = document.createElementNS("http://www.w3.org/2000/svg", "g");
    g.setAttribute("class", "kolo-node");
    g.setAttribute("tabindex", "-1"); // focus managed by dial mode
    g.setAttribute("role", "button");
    g.setAttribute("aria-label", s.tytul_pl);
    g.style.cursor = "default";

    const halo = document.createElementNS("http://www.w3.org/2000/svg", "circle");
    halo.setAttribute("cx", x); halo.setAttribute("cy", y); halo.setAttribute("r", "20");
    halo.setAttribute("fill", s.kolor); halo.setAttribute("opacity", "0.1");
    halo.setAttribute("class", "node-halo");

    const circle = document.createElementNS("http://www.w3.org/2000/svg", "circle");
    circle.setAttribute("cx", x); circle.setAttribute("cy", y); circle.setAttribute("r", "10");
    circle.setAttribute("fill", s.kolor);
    circle.setAttribute("stroke", "#0f1117"); circle.setAttribute("stroke-width", "2");
    circle.setAttribute("filter", "url(#glow)");

    const label = document.createElementNS("http://www.w3.org/2000/svg", "text");
    const lx = CX + LABEL_R * Math.cos(rad);
    const ly = CY + LABEL_R * Math.sin(rad);
    label.setAttribute("x", lx); label.setAttribute("y", ly);
    const anchor = lx < CX - 8 ? "end" : lx > CX + 8 ? "start" : "middle";
    label.setAttribute("text-anchor", anchor);
    label.setAttribute("dominant-baseline", "middle");
    label.setAttribute("font-size", isMobile ? "13" : "14");
    label.setAttribute("font-family", "'Playfair Display', serif");
    label.setAttribute("fill", "rgba(245,225,164,0.75)");
    label.setAttribute("class", "node-label");
    label.setAttribute("data-pl", s.tytul_pl);
    label.setAttribute("data-en", s.tytul_en);

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

    buildLabel(label, s.tytul_pl, lx);

    g.appendChild(halo);
    g.appendChild(circle);
    g.appendChild(label);
    group.appendChild(g);

    nodeEls.push({ g, halo, circle, label, data: s });
  });

  // ── DIAL STATE ────────────────────────────────────────────────────────────────
  // currentAngle: current rotation of the whole SVG (in degrees).
  // Each node lives at s.kat degrees. The "active" node is whichever one,
  // after rotation, lands closest to 0° (top = 12 o'clock).
  // Active node angle (in wheel space) = (s.kat + currentAngle) mod 360.
  // We want that to be 0°, so we want currentAngle = -s.kat (mod 360).

  let currentAngle = 0; // degrees, applied as transform to #kolo-nodes
  let activeIdx    = 0;
  let dialActive   = false; // true after spin-in ends

  // Snap angles: for each node, the rotation that brings it to the top
  const snapAngles = data.map(s => {
    let a = -s.kat % 360;
    if (a > 180) a -= 360;
    if (a < -180) a += 360;
    return a;
  });

  const setActiveNode = (idx, animate = true) => {
    activeIdx = ((idx % data.length) + data.length) % data.length;
    const lang = currentLang();
    const s = data[activeIdx];

    // panel update
    panel.classList.add("kolo-panel-changing");
    setTimeout(() => {
      panelName.textContent = lang === "en" ? s.tytul_en : s.tytul_pl;
      panelSub.textContent  = s.data_pl ? (lang === "en" ? (s.data_en || "") : s.data_pl) : "";
      panelBtn.href         = s.url;
      panel.classList.remove("kolo-panel-changing");
    }, 180);

    // highlight active node
    nodeEls.forEach(({ halo: h, circle: c, label: l }, i) => {
      if (i === activeIdx) {
        h.setAttribute("opacity", "0.38");
        c.setAttribute("r", "14");
        c.setAttribute("filter", "url(#glow)");
        l.setAttribute("fill", "rgba(245,225,164,1)");
        l.style.fontWeight = "900";
      } else {
        h.setAttribute("opacity", "0.08");
        c.setAttribute("r", "10");
        l.setAttribute("fill", "rgba(245,225,164,0.6)");
        l.style.fontWeight = "";
      }
    });
  };

  // Apply rotation to the nodes group (not the whole SVG to keep decorative rings static)
  const applyRotation = (deg, transition = false) => {
    group.style.transition = transition ? "transform 0.45s cubic-bezier(0.25,1,0.5,1)" : "none";
    group.style.transformOrigin = `${CX}px ${CY}px`;
    group.style.transform = `rotate(${deg}deg)`;
  };

  // Snap to nearest node
  const snapToNearest = () => {
    // Normalize currentAngle
    let norm = ((currentAngle % 360) + 360) % 360;
    if (norm > 180) norm -= 360;

    let bestIdx = 0, bestDist = Infinity;
    snapAngles.forEach((sa, i) => {
      // distance between norm and sa (both -180..180)
      let d = Math.abs(norm - sa);
      if (d > 180) d = 360 - d;
      if (d < bestDist) { bestDist = d; bestIdx = i; }
    });

    currentAngle = snapAngles[bestIdx];
    applyRotation(currentAngle, true);
    setActiveNode(bestIdx);
  };

  // ── DRAG / SWIPE ─────────────────────────────────────────────────────────────
  let dragging   = false;
  let lastAngle  = 0; // angle of pointer relative to wheel centre at drag start
  let startRot   = 0; // currentAngle at drag start
  let velocity   = 0;
  let lastTime   = 0;
  let lastDeltaA = 0;

  const pointerAngle = (e) => {
    const rect = svg.getBoundingClientRect();
    const cx   = rect.left + rect.width / 2;
    const cy   = rect.top  + rect.height / 2;
    const px   = (e.touches ? e.touches[0].clientX : e.clientX) - cx;
    const py   = (e.touches ? e.touches[0].clientY : e.clientY) - cy;
    return (Math.atan2(py, px) * 180) / Math.PI;
  };

  const onDragStart = (e) => {
    if (!dialActive) return;
    dragging  = true;
    lastAngle = pointerAngle(e);
    startRot  = currentAngle;
    velocity  = 0;
    lastTime  = Date.now();
    group.style.transition = "none";
    e.preventDefault();
  };

  const onDragMove = (e) => {
    if (!dragging) return;
    const pa    = pointerAngle(e);
    let delta   = pa - lastAngle;
    if (delta > 180)  delta -= 360;
    if (delta < -180) delta += 360;
    lastDeltaA   = delta;
    currentAngle = startRot + delta;

    // velocity tracking
    const now = Date.now();
    velocity  = delta / Math.max(1, now - lastTime);
    lastTime  = now;

    applyRotation(currentAngle);
    // live preview of closest node
    let norm = ((currentAngle % 360) + 360) % 360;
    if (norm > 180) norm -= 360;
    let bestIdx = 0, bestDist = Infinity;
    snapAngles.forEach((sa, i) => {
      let d = Math.abs(norm - sa);
      if (d > 180) d = 360 - d;
      if (d < bestDist) { bestDist = d; bestIdx = i; }
    });
    if (bestIdx !== activeIdx) setActiveNode(bestIdx);
    e.preventDefault();
  };

  const onDragEnd = () => {
    if (!dragging) return;
    dragging = false;
    // add a small momentum nudge, then snap
    currentAngle += velocity * 80;
    snapToNearest();
  };

  // Mouse
  svg.addEventListener("mousedown",  onDragStart, { passive: false });
  window.addEventListener("mousemove", onDragMove, { passive: false });
  window.addEventListener("mouseup",   onDragEnd);
  // Touch
  svg.addEventListener("touchstart",  onDragStart, { passive: false });
  svg.addEventListener("touchmove",   onDragMove,  { passive: false });
  svg.addEventListener("touchend",    onDragEnd);

  // Scroll wheel (desktop convenience)
  svg.addEventListener("wheel", (e) => {
    if (!dialActive) return;
    e.preventDefault();
    const step = e.deltaY > 0 ? 1 : -1;
    const next = ((activeIdx + step) + data.length) % data.length;
    currentAngle = snapAngles[next];
    applyRotation(currentAngle, true);
    setActiveNode(next);
  }, { passive: false });

  // Keyboard: arrow keys when wheel is focused
  svg.setAttribute("tabindex", "0");
  svg.addEventListener("keydown", (e) => {
    if (!dialActive) return;
    if (e.key === "ArrowLeft" || e.key === "ArrowUp") {
      e.preventDefault();
      const next = ((activeIdx - 1) + data.length) % data.length;
      currentAngle = snapAngles[next];
      applyRotation(currentAngle, true);
      setActiveNode(next);
    }
    if (e.key === "ArrowRight" || e.key === "ArrowDown") {
      e.preventDefault();
      const next = (activeIdx + 1) % data.length;
      currentAngle = snapAngles[next];
      applyRotation(currentAngle, true);
      setActiveNode(next);
    }
    if (e.key === "Enter" || e.key === " ") {
      e.preventDefault();
      window.location.href = data[activeIdx].url;
    }
  });

  // ── SPIN-IN INTRO ────────────────────────────────────────────────────────────
  svg.classList.add("spinning");

  svg.addEventListener("animationend", () => {
    svg.classList.remove("spinning");
    dialActive = true;

    // Find node closest to top (kat closest to 0)
    let startIdx = 0, minKat = Infinity;
    data.forEach((s, i) => {
      const k = Math.abs(((s.kat + 180) % 360) - 180);
      if (k < minKat) { minKat = k; startIdx = i; }
    });
    currentAngle = snapAngles[startIdx];
    applyRotation(currentAngle, true);
    setActiveNode(startIdx);

    // reveal panel
    panel.classList.add("kolo-panel-visible");
    svg.style.cursor = "grab";
  }, { once: true });

  // ── LANGUAGE SWITCH hook ─────────────────────────────────────────────────────
  const origSwitch = window.switchLang;
  window.switchLang = function (lang) {
    origSwitch(lang);

    // update node labels
    document.querySelectorAll(".node-label").forEach(el => {
      const title = lang === "en" ? el.dataset.en : el.dataset.pl;
      const atX = el.getAttribute("x");
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
    });

    // update panel
    if (dialActive) {
      const s = data[activeIdx];
      panelName.textContent = lang === "en" ? s.tytul_en : s.tytul_pl;
    }

    // toggle button labels
    panel.querySelectorAll(".kolo-panel-btn-label-pl, .kolo-panel-btn-label-en").forEach(el => {
      el.style.display = el.classList.contains(`kolo-panel-btn-label-${lang}`) ? "" : "none";
    });
    panel.querySelectorAll(".kolo-panel-hint-pl, .kolo-panel-hint-en").forEach(el => {
      el.style.display = el.classList.contains(`kolo-panel-hint-${lang}`) ? "" : "none";
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

  // Restore saved state
  let saved = true;
  try { saved = localStorage.getItem(READER_KEY) === "1"; } catch (_) {}
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