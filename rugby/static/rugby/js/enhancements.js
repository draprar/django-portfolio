(function () {
  'use strict';

  function buildLightbox() {
    const overlay = document.createElement('div');
    overlay.id = 'lb-overlay';
    overlay.innerHTML = `
      <div id="lb-inner">
        <button id="lb-close" aria-label="Zamknij">&times;</button>
        <button id="lb-prev" aria-label="Poprzedni">&#8592;</button>
        <img id="lb-img" src="" alt="">
        <button id="lb-next" aria-label="Następny">&#8594;</button>
        <p id="lb-caption"></p>
      </div>
    `;
    document.body.appendChild(overlay);

    const lbStyle = document.createElement('style');
    lbStyle.textContent = `
      #lb-overlay {
        display: none;
        position: fixed;
        inset: 0;
        z-index: 9999;
        background: rgba(0,0,0,0.93);
        align-items: center;
        justify-content: center;
        animation: lbFadeIn 0.2s ease;
      }
      #lb-overlay.open { display: flex; }
      @keyframes lbFadeIn { from { opacity:0 } to { opacity:1 } }
      #lb-inner {
        position: relative;
        display: flex;
        flex-direction: column;
        align-items: center;
        max-width: 92vw;
        max-height: 92vh;
      }
      #lb-img {
        max-width: 88vw;
        max-height: 80vh;
        object-fit: contain;
        border-radius: 6px;
        box-shadow: 0 20px 60px rgba(0,0,0,0.7);
        animation: lbZoomIn 0.25s cubic-bezier(0.22,1,0.36,1);
      }
      @keyframes lbZoomIn { from { transform: scale(0.92); opacity:0 } to { transform: scale(1); opacity:1 } }
      #lb-caption {
        margin-top: 0.9rem;
        font-family: 'Montserrat', sans-serif;
        font-size: 0.88rem;
        color: rgba(232,232,232,0.65);
        text-align: center;
      }
      #lb-close {
        position: fixed;
        top: 18px; right: 22px;
        background: none; border: none;
        color: #fff; font-size: 2rem;
        cursor: pointer; line-height: 1;
        opacity: 0.7; transition: opacity 0.2s;
      }
      #lb-close:hover { opacity: 1; }
      #lb-prev, #lb-next {
        position: fixed;
        top: 50%; transform: translateY(-50%);
        background: rgba(255,255,255,0.08);
        border: 1px solid rgba(255,255,255,0.15);
        color: #fff; font-size: 1.4rem;
        padding: 0.6rem 0.9rem;
        cursor: pointer; border-radius: 6px;
        transition: background 0.2s;
        line-height: 1;
      }
      #lb-prev { left: 14px; }
      #lb-next { right: 14px; }
      #lb-prev:hover, #lb-next:hover { background: rgba(196,146,42,0.35); }
    `;
    document.head.appendChild(lbStyle);

    const mediaSection = document.querySelector('#media');
    if (!mediaSection) return;

    const items = [];
    mediaSection.querySelectorAll('.card').forEach((card) => {
      const img = card.querySelector('img');
      if (!img) return;
      const captionEl = card.querySelector('.card-body p:first-child');
      const caption = captionEl ? captionEl.textContent : '';
      const idx = items.length;
      items.push({ src: img.src, caption });
      img.style.cursor = 'pointer';
      img.addEventListener('click', () => open(idx));
    });

    let current = 0;

    function open(idx) { current = idx; show(); }

    function show() {
      const item = items[current];
      const lbImg = document.getElementById('lb-img');
      lbImg.style.animation = 'none';
      lbImg.offsetHeight;
      lbImg.style.animation = '';
      lbImg.src = item.src;
      document.getElementById('lb-caption').textContent = item.caption;
      overlay.classList.add('open');
      document.body.style.overflow = 'hidden';
    }

    function close() {
      overlay.classList.remove('open');
      document.body.style.overflow = '';
    }

    document.getElementById('lb-close').addEventListener('click', close);
    document.getElementById('lb-prev').addEventListener('click', () => { current = (current - 1 + items.length) % items.length; show(); });
    document.getElementById('lb-next').addEventListener('click', () => { current = (current + 1) % items.length; show(); });
    overlay.addEventListener('click', (e) => { if (e.target === overlay) close(); });
    document.addEventListener('keydown', (e) => {
      if (!overlay.classList.contains('open')) return;
      if (e.key === 'Escape') close();
      if (e.key === 'ArrowLeft')  { current = (current - 1 + items.length) % items.length; show(); }
      if (e.key === 'ArrowRight') { current = (current + 1) % items.length; show(); }
    });
  }

  function animateTimelineLine() {
    const timeline = document.querySelector('.timeline');
    if (!timeline) return;
    const obs = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          timeline.classList.add('line-visible');
          obs.unobserve(timeline);
        }
      });
    }, { threshold: 0.05 });
    obs.observe(timeline);
  }

  document.addEventListener('DOMContentLoaded', () => {
    buildLightbox();
    animateTimelineLine();
  });

})();