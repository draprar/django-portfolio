/* =============================================
   WYRAJ — wyraj.js
   • Loader
   • Lang switch
   • Scroll reveal
   • Hero parallax
   • Particle sparks on card hover
   ============================================= */

// ── 1. LOADER ───────────────────────────────────
document.addEventListener("DOMContentLoaded", () => {
  const loader = document.getElementById("loader");
  if (!loader) return;
  window.addEventListener("load", () => {
    loader.style.opacity = "0";
    setTimeout(() => { loader.style.display = "none"; }, 600);
  });
  setTimeout(() => {
    loader.style.opacity = "0";
    setTimeout(() => { loader.style.display = "none"; }, 600);
  }, 3500);
});

// ── 2. LANG SWITCH ──────────────────────────────
window.switchLang = function (lang) {
  const ids = [["pl","en"], ["pl-footer","en-footer"]];

  function fadeSwitch(showEl, hideEl) {
    if (!showEl || !hideEl) return;
    hideEl.style.opacity = "0";
    hideEl.classList.remove("active");
    showEl.classList.add("active");
    showEl.style.opacity = "0";
    setTimeout(() => (showEl.style.opacity = "1"), 50);
  }

  ids.forEach(([plId, enId]) => {
    const pl = document.getElementById(plId);
    const en = document.getElementById(enId);
    if (lang === "pl") fadeSwitch(pl, en);
    else               fadeSwitch(en, pl);
  });

  document.querySelectorAll(".switch button").forEach(btn => {
    btn.classList.toggle("active", btn.textContent.trim().toLowerCase() === lang);
  });
};

// ── 3. SCROLL REVEAL ────────────────────────────
document.addEventListener("DOMContentLoaded", () => {
  const targets = document.querySelectorAll(
    ".section-title, .tresc, .zrodla, .box, .swieto-card, .ornament"
  );
  targets.forEach(el => el.classList.add("reveal"));

  const obs = new IntersectionObserver(entries => {
    entries.forEach(e => {
      if (e.isIntersecting) {
        e.target.classList.add("visible");
        obs.unobserve(e.target);
      }
    });
  }, { threshold: 0.1 });

  targets.forEach(el => obs.observe(el));
});

// ── 4. HERO PARALLAX ────────────────────────────
document.addEventListener("DOMContentLoaded", () => {
  const heroImg = document.querySelector(".hero-img");
  if (!heroImg) return;

  let ticking = false;
  window.addEventListener("scroll", () => {
    if (!ticking) {
      requestAnimationFrame(() => {
        const scrollY = window.scrollY;
        heroImg.style.transform = `scale(1.06) translateY(${scrollY * 0.25}px)`;
        ticking = false;
      });
      ticking = true;
    }
  });
});

// ── 5. SPARK PARTICLES ON CARD HOVER ────────────
document.addEventListener("DOMContentLoaded", () => {
  const cards = document.querySelectorAll(".swieto-card");
  if (!cards.length) return;

  cards.forEach(card => {
    card.addEventListener("mouseenter", e => spawnSparks(e, card));
  });

  function spawnSparks(e, parent) {
    const rect = parent.getBoundingClientRect();
    const count = 7;

    for (let i = 0; i < count; i++) {
      const spark = document.createElement("span");
      spark.className = "spark";

      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;
      const angle = (360 / count) * i;
      const dist  = 28 + Math.random() * 22;
      const dx = Math.cos((angle * Math.PI) / 180) * dist;
      const dy = Math.sin((angle * Math.PI) / 180) * dist;

      Object.assign(spark.style, {
        position:   "absolute",
        left:        x + "px",
        top:         y + "px",
        width:       "4px",
        height:      "4px",
        borderRadius:"50%",
        background:  "radial-gradient(circle, #f5e1a4, #c4922a)",
        pointerEvents: "none",
        zIndex:      "20",
        transform:   "translate(-50%,-50%) scale(1)",
        transition:  `transform 0.5s ease, opacity 0.5s ease`,
        opacity:     "1",
      });

      parent.style.position = "relative";
      parent.appendChild(spark);

      requestAnimationFrame(() => {
        spark.style.transform =
          `translate(calc(-50% + ${dx}px), calc(-50% + ${dy}px)) scale(0)`;
        spark.style.opacity = "0";
      });

      setTimeout(() => spark.remove(), 520);
    }
  }
});