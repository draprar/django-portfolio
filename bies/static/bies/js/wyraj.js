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

  // Node radius and label radius — kept inside the decorative ring at r=218
  const NODE_R   = isMobile ? 130 : 155;
  const LABEL_R  = isMobile ? 170 : 192;

  const currentLang = () => {
    try { return localStorage.getItem(LANG_KEY) || "pl"; } catch (_) { return "pl"; }
  };

  data.forEach((s) => {
    // Angle: 0° = top, clockwise
    const rad = ((s.kat - 90) * Math.PI) / 180;
    const x = CX + NODE_R * Math.cos(rad);
    const y = CY + NODE_R * Math.sin(rad);

    // Clickable group
    const g = document.createElementNS("http://www.w3.org/2000/svg", "g");
    g.setAttribute("class", "kolo-node");
    g.setAttribute("tabindex", "0");
    g.setAttribute("role", "link");
    g.setAttribute("aria-label", s.tytul_pl);
    g.style.cursor = "pointer";

    // Glow halo
    const halo = document.createElementNS("http://www.w3.org/2000/svg", "circle");
    halo.setAttribute("cx", x); halo.setAttribute("cy", y); halo.setAttribute("r", "18");
    halo.setAttribute("fill", s.kolor); halo.setAttribute("opacity", "0.12");
    halo.setAttribute("class", "node-halo");

    // Main node circle
    const circle = document.createElementNS("http://www.w3.org/2000/svg", "circle");
    circle.setAttribute("cx", x); circle.setAttribute("cy", y); circle.setAttribute("r", "10");
    circle.setAttribute("fill", s.kolor);
    circle.setAttribute("stroke", "#0f1117"); circle.setAttribute("stroke-width", "2");
    circle.setAttribute("filter", "url(#glow)");

    // Label — positioned between node and decorative ring
    const label = document.createElementNS("http://www.w3.org/2000/svg", "text");
    const lx = CX + LABEL_R * Math.cos(rad);
    const ly = CY + LABEL_R * Math.sin(rad);
    label.setAttribute("x", lx); label.setAttribute("y", ly);

    // Anchor: left / right / centre depending on position on the wheel
    const anchor = lx < CX - 8 ? "end" : lx > CX + 8 ? "start" : "middle";
    label.setAttribute("text-anchor", anchor);
    label.setAttribute("dominant-baseline", "middle");
    label.setAttribute("font-size", isMobile ? "13" : "14");
    label.setAttribute("font-family", "'Playfair Display', serif");
    label.setAttribute("fill", "rgba(245,225,164,0.88)");
    label.setAttribute("class", "node-label");
    label.setAttribute("data-pl", s.tytul_pl);
    label.setAttribute("data-en", s.tytul_en);

    const buildLabel = (el, title, atX) => {
      el.replaceChildren();
      if (title.length > 7 && title.includes(" ")) {
        const words = title.split(" ");
        const mid = Math.ceil(words.length / 2);
        const line1 = words.slice(0, mid).join(" ");
        const line2 = words.slice(mid).join(" ");

        const first = document.createElementNS("http://www.w3.org/2000/svg", "tspan");
        first.setAttribute("x", atX);
        first.setAttribute("dy", "-0.55em");
        first.textContent = line1;

        const second = document.createElementNS("http://www.w3.org/2000/svg", "tspan");
        second.setAttribute("x", atX);
        second.setAttribute("dy", "1.15em");
        second.textContent = line2;

        el.append(first, second);
      } else {
        el.textContent = title;
      }
    };

    buildLabel(label, s.tytul_pl, lx);

    g.appendChild(halo);
    g.appendChild(circle);
    g.appendChild(label);
    group.appendChild(g);

    // Interactions
    const goTo = () => { window.location.href = s.url; };

    g.addEventListener("click", goTo);
    g.addEventListener("keydown", e => { if (e.key === "Enter" || e.key === " ") goTo(); });

    g.addEventListener("mouseenter", () => {
      halo.setAttribute("opacity", "0.35");
      circle.setAttribute("r", "13");
      if (tooltip) {
        const lang = currentLang();
        tooltip.querySelector(".kolo-tooltip-title").textContent =
          lang === "en" ? s.tytul_en : s.tytul_pl;
        tooltip.classList.add("visible");
      }
    });
    g.addEventListener("mouseleave", () => {
      halo.setAttribute("opacity", "0.12");
      circle.setAttribute("r", "10");
      if (tooltip) tooltip.classList.remove("visible");
    });
  });

  // WHEEL SPIN-IN INTRO
  svg.classList.add("spinning");

  // Re-enable pointer events on nodes once the spin is done
  svg.addEventListener("animationend", () => {
    svg.classList.remove("spinning");
  }, { once: true });

  // Update labels when language switches
  const origSwitch = window.switchLang;
  window.switchLang = function (lang) {
    origSwitch(lang);
    document.querySelectorAll(".node-label").forEach(el => {
        const title = lang === "en" ? el.dataset.en : el.dataset.pl;
        const atX = el.getAttribute("x");

        el.replaceChildren();

        if (title.length > 7 && title.includes(" ")) {
            const words = title.split(" ");
            const mid = Math.ceil(words.length / 2);
            const line1 = words.slice(0, mid).join(" ");
            const line2 = words.slice(mid).join(" ");

            const first = document.createElementNS("http://www.w3.org/2000/svg", "tspan");
            first.setAttribute("x", atX);
            first.setAttribute("dy", "-0.55em");
            first.textContent = line1;

            const second = document.createElementNS("http://www.w3.org/2000/svg", "tspan");
            second.setAttribute("x", atX);
            second.setAttribute("dy", "1.15em");
            second.textContent = line2;

            el.append(first, second);
        } else {
            el.textContent = title;
        }
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