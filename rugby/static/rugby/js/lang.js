(function () {
  'use strict';

  function nl2br(str) {
    return str.replace(/\n/g, '<br>');
  }

  function applyTextToElement(el, text) {
    if (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA') {
      if ('placeholder' in el) el.placeholder = text;
      if ('value' in el && (el.type === 'button' || el.type === 'submit')) el.value = text;
      return;
    }
    if (el.classList.contains('account-body')) {
      el.innerHTML = nl2br(text);
      return;
    }
    if (el.tagName === 'TITLE') {
      document.title = text;
      return;
    }
    if (el.tagName === 'META' && el.getAttribute('name') === 'description') {
      el.setAttribute('content', text);
      return;
    }
    el.innerHTML = text;
  }

  function switchLang(lang) {
    if (!lang) return;
    document.documentElement.setAttribute('lang', lang);

    document.querySelectorAll('[data-en][data-pl]').forEach((el) => {
      const text = el.getAttribute('data-' + lang) || el.getAttribute('data-en') || '';
      applyTextToElement(el, text);
    });

    document.querySelectorAll('[data-alt-pl][data-alt-en]').forEach((el) => {
      el.alt = el.getAttribute('data-alt-' + lang) || el.getAttribute('data-alt-en') || '';
    });

    document.querySelectorAll('[data-aria-pl][data-aria-en]').forEach((el) => {
      el.setAttribute('aria-label', el.getAttribute('data-aria-' + lang) || el.getAttribute('data-aria-en') || '');
    });

    document.querySelectorAll('.lang-btn').forEach((btn) => {
      const isActive = btn.dataset.lang === lang;
      btn.classList.toggle('active', isActive);
      btn.setAttribute('aria-pressed', isActive ? 'true' : 'false');
    });

    try { localStorage.setItem('rugby_lang', lang); } catch (e) { /* ignore */ }
    window.__rugbyLangReady = true;
    document.dispatchEvent(new CustomEvent('rugby:lang', { detail: { lang } }));
  }

  function bindLangButtons() {
    document.querySelectorAll('.lang-btn').forEach((btn) => {
      btn.addEventListener('click', () => switchLang(btn.dataset.lang), { passive: true });
    });
  }

  function init() {
    bindLangButtons();
    let lang = null;
    try { lang = localStorage.getItem('rugby_lang'); } catch (e) { lang = null; }
    if (!lang) lang = 'pl';
    switchLang(lang);
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();

  window.rugbyLang = { switch: switchLang };
})();
