(function () {
  'use strict';

  // Converts \n to <br> — needed for post body text from Django (no linebreaksbr server-side)
  function nl2br(str) {
    return str.replace(/\n/g, '<br>');
  }

  function applyTextToElement(el, text) {
    if (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA') {
      if ('placeholder' in el) el.placeholder = text;
      if ('value' in el && (el.type === 'button' || el.type === 'submit')) el.value = text;
      return;
    }
    // For accordion bodies (post text): convert newlines to <br>
    if (el.classList.contains('accordion-body')) {
      el.innerHTML = nl2br(text);
    } else {
      el.innerHTML = text;
    }
  }

  function switchLang(lang) {
    if (!lang) return;
    document.documentElement.setAttribute('lang', lang);

    document.querySelectorAll('[data-en][data-pl]').forEach(el => {
      const text = el.getAttribute('data-' + lang) || el.getAttribute('data-en') || '';
      applyTextToElement(el, text);
    });

    document.querySelectorAll('.lang-btn').forEach(btn => {
      const isActive = btn.dataset.lang === lang;
      btn.classList.toggle('active', isActive);
      btn.setAttribute('aria-pressed', isActive ? 'true' : 'false');
    });

    try { localStorage.setItem('rugby_lang', lang); } catch (e) { /* ignore */ }
  }

  function bindLangButtons() {
    document.querySelectorAll('.lang-btn').forEach(btn => {
      btn.removeAttribute('onclick');
      btn.addEventListener('click', function () {
        switchLang(btn.dataset.lang);
      }, { passive: true });
    });
  }

  function init() {
    bindLangButtons();

    let lang = null;
    try { lang = localStorage.getItem('rugby_lang'); } catch (e) { lang = null; }

    if (!lang) {
      const nav = (navigator.languages && navigator.languages[0]) || navigator.language || '';
      lang = nav.toLowerCase().startsWith('pl') ? 'pl' : 'en';
    }

    switchLang(lang);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  window.rugbyLang = { switch: switchLang };
})();