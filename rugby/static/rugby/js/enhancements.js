(function () {
  'use strict';

  const FOCUSABLE = 'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])';

  function lang() {
    return document.documentElement.getAttribute('lang') || 'pl';
  }

  function buildLightbox() {
    const triggers = Array.from(document.querySelectorAll('[data-lightbox-item]'));
    if (!triggers.length) return;

    const overlay = document.createElement('div');
    overlay.id = 'lb-overlay';
    overlay.setAttribute('role', 'dialog');
    overlay.setAttribute('aria-modal', 'true');
    overlay.setAttribute('data-aria-pl', 'Podgląd materiału');
    overlay.setAttribute('data-aria-en', 'Item preview');
    overlay.setAttribute('aria-label', lang() === 'en' ? 'Item preview' : 'Podgląd materiału');
    overlay.innerHTML =
      '<div id="lb-inner">' +
      '<button type="button" id="lb-close" data-aria-pl="Zamknij" data-aria-en="Close">&times;</button>' +
      '<button type="button" id="lb-prev" data-aria-pl="Poprzedni materiał" data-aria-en="Previous item">&#8592;</button>' +
      '<img id="lb-img" src="" alt="">' +
      '<button type="button" id="lb-next" data-aria-pl="Następny materiał" data-aria-en="Next item">&#8594;</button>' +
      '<p id="lb-caption"></p>' +
      '<p id="lb-counter" class="small text-muted"></p>' +
      '</div>';
    document.body.appendChild(overlay);

    const items = triggers.map((btn) => ({
      src: btn.getAttribute('data-src'),
      titlePl: btn.getAttribute('data-title-pl') || '',
      titleEn: btn.getAttribute('data-title-en') || '',
      altPl: btn.getAttribute('data-alt-pl') || '',
      altEn: btn.getAttribute('data-alt-en') || '',
      trigger: btn,
    }));

    let current = 0;
    let lastFocus = null;

    function label(el, L) {
      const t = el.getAttribute('data-aria-' + L) || el.getAttribute('data-aria-en') || el.textContent;
      if (el.id === 'lb-close' || el.id === 'lb-prev' || el.id === 'lb-next') el.setAttribute('aria-label', t);
    }

    function show(idx) {
      current = idx;
      const item = items[current];
      const L = lang();
      const img = document.getElementById('lb-img');
      img.src = item.src;
      img.alt = L === 'en' ? item.altEn : item.altPl;
      document.getElementById('lb-caption').textContent = L === 'en' ? item.titleEn : item.titlePl;
      document.getElementById('lb-counter').textContent =
        (L === 'en' ? 'Item ' : 'Materiał ') + (current + 1) + (L === 'en' ? ' of ' : ' z ') + items.length;
      ['lb-close', 'lb-prev', 'lb-next'].forEach((id) => label(document.getElementById(id), L));
      overlay.classList.add('open');
      document.body.style.overflow = 'hidden';
      document.getElementById('lb-close').focus();
    }

    function close() {
      overlay.classList.remove('open');
      document.body.style.overflow = '';
      if (lastFocus) lastFocus.focus();
    }

    triggers.forEach((btn, i) => {
      btn.addEventListener('click', () => {
        lastFocus = btn;
        show(i);
      });
    });

    document.getElementById('lb-close').addEventListener('click', close);
    document.getElementById('lb-prev').addEventListener('click', () => show((current - 1 + items.length) % items.length));
    document.getElementById('lb-next').addEventListener('click', () => show((current + 1) % items.length));
    overlay.addEventListener('click', (e) => { if (e.target === overlay) close(); });
    document.getElementById('lb-img').addEventListener('click', (e) => e.stopPropagation());

    let swipeX = 0;
    overlay.addEventListener('touchstart', (e) => {
      if (e.touches.length === 1) swipeX = e.touches[0].clientX;
    }, { passive: true });
    overlay.addEventListener('touchend', (e) => {
      if (!overlay.classList.contains('open')) return;
      const dx = e.changedTouches[0].clientX - swipeX;
      if (Math.abs(dx) < 48) return;
      if (dx < 0) show((current + 1) % items.length);
      else show((current - 1 + items.length) % items.length);
    }, { passive: true });

    overlay.addEventListener('keydown', (e) => {
      if (!overlay.classList.contains('open')) return;
      if (e.key === 'Escape') close();
      if (e.key === 'ArrowLeft') show((current - 1 + items.length) % items.length);
      if (e.key === 'ArrowRight') show((current + 1) % items.length);
      if (e.key === 'Tab') {
        const nodes = overlay.querySelectorAll(FOCUSABLE);
        const list = Array.from(nodes).filter((n) => !n.disabled);
        const first = list[0];
        const last = list[list.length - 1];
        if (e.shiftKey && document.activeElement === first) {
          e.preventDefault();
          last.focus();
        } else if (!e.shiftKey && document.activeElement === last) {
          e.preventDefault();
          first.focus();
        }
      }
    });
  }

  function animateTimelineLine() {
    const timeline = document.querySelector('.timeline');
    if (!timeline) return;
    const obs = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          timeline.classList.add('line-visible');
          obs.unobserve(timeline);
        }
      });
    }, { threshold: 0.05 });
    obs.observe(timeline);
  }

  function bindYearRail() {
    document.querySelectorAll('[data-year-filter]').forEach((btn) => {
      btn.addEventListener('click', () => {
        const year = btn.getAttribute('data-year-filter');
        document.querySelectorAll('[data-year-filter]').forEach((item) => {
          const on = item === btn;
          item.classList.toggle('is-active', on);
          item.setAttribute('aria-pressed', on ? 'true' : 'false');
        });
        document.querySelectorAll('.timeline [data-year]').forEach((el) => {
          const itemYear = el.getAttribute('data-year');
          el.classList.toggle('is-dimmed', year !== 'all' && itemYear !== year);
        });
      });
    });
  }

  function bindAccountJump() {
    document.querySelectorAll('a[href*="#account-"]').forEach((link) => {
      link.addEventListener('click', () => {
        const id = (link.getAttribute('href') || '').split('#').pop();
        const card = id && document.getElementById(id);
        if (!card) return;
        document.querySelectorAll('.account-card.is-linked').forEach((el) => el.classList.remove('is-linked'));
        window.setTimeout(() => {
          card.classList.add('is-linked');
          const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
          if (!reduce) window.setTimeout(() => card.classList.remove('is-linked'), 1100);
        }, 350);
      });
    });
  }

  function bindParallax() {
    const bg = document.querySelector('.hero-bg');
    const hero = document.querySelector('.hero');
    if (!bg || !hero) return;
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
    const onScroll = () => {
      const amp = window.innerWidth < 768 ? 0.04 : 0.08;
      const y = Math.min(window.scrollY, hero.offsetHeight);
      bg.style.transform = 'translate3d(0,' + (y * amp) + 'px,0)';
    };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  document.addEventListener('DOMContentLoaded', () => {
    buildLightbox();
    bindYearRail();
    bindAccountJump();
    bindParallax();
    animateTimelineLine();
  });
})();
