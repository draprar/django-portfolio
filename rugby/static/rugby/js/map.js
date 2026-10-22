(function () {
  'use strict';

  function readProjection() {
    const el = document.getElementById('rugby-map-projection');
    if (!el) return null;
    try { return JSON.parse(el.textContent); } catch (e) { return null; }
  }
  const CFG = readProjection() || {};
  const LON_MIN = CFG.lonMin ?? 5.0;
  const LON_MAX = CFG.lonMax ?? 32.0;
  const LAT_MIN = CFG.latMin ?? 44.0;
  const LAT_MAX = CFG.latMax ?? 58.5;
  const MAP_W = CFG.mapW ?? 960;
  const MAP_H = CFG.mapH ?? 720;
  const MAP_PAD = CFG.mapPad ?? 24;
  const POLAND = CFG.poland || { lonMin: 13.7, lonMax: 24.5, latMin: 48.7, latMax: 55.05 };
  const POLAND_PAD = CFG.polandPad ?? 1.36;

  function lang() {
    return document.documentElement.getAttribute('lang') || 'pl';
  }

  function merc(lat) {
    const rad = Math.max(Math.min(lat, 85), -85) * Math.PI / 180;
    return Math.log(Math.tan(Math.PI / 4 + rad / 2));
  }

  function project(lon, lat) {
    const x = ((lon - LON_MIN) / (LON_MAX - LON_MIN)) * (MAP_W - 2 * MAP_PAD) + MAP_PAD;
    const yTop = merc(LAT_MAX);
    const yBot = merc(LAT_MIN);
    const y = ((yTop - merc(lat)) / (yTop - yBot)) * (MAP_H - 2 * MAP_PAD) + MAP_PAD;
    return { x, y };
  }

  function initMap() {
    const stage = document.getElementById('rugby-map-stage');
    const viewport = document.querySelector('.rugby-map-viewport');
    const card = document.getElementById('map-card');
    if (!stage || !viewport) return;

    let scale = 1;
    let openingScale = 1;
    let tx = 0;
    let ty = 0;
    let dragging = false;
    let sx = 0;
    let sy = 0;
    let league = 'all';
    let openCluster = '';
    let activeId = '';
    let lastMarkerFocus = null;
    let restoringFocus = false;
    const pointers = new Map();

    const leaders = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    leaders.classList.add('map-leaders');
    leaders.setAttribute('aria-hidden', 'true');
    stage.appendChild(leaders);

    const markers = Array.from(document.querySelectorAll('.map-marker'));
    const narrow = () => window.matchMedia('(max-width: 767.98px)').matches;
    const zoomOutBtn = document.querySelector('[data-map-action="zoom-out"]');

    function userZoomed() {
      return scale > openingScale + 0.08;
    }

    function updateZoomButtons() {
      if (zoomOutBtn) zoomOutBtn.disabled = scale <= openingScale + 0.02;
    }

    function applyMarkerScale() {
      const inv = scale > 0 ? (1 / scale) : 1;
      markers.forEach((marker) => {
        marker.style.scale = String(inv);
        const dot = marker.querySelector('.map-marker-dot');
        if (dot) dot.style.transform = '';
      });
    }

    function apply() {
      stage.style.transform = 'translate(' + tx + 'px,' + ty + 'px) scale(' + scale + ')';
      viewport.classList.toggle('is-zoomed', userZoomed());
      updateZoomButtons();
      spiderfy();
      applyMarkerScale();
      if (activeId) window.requestAnimationFrame(() => placeTip(markerById(activeId)));
    }

    function clampScale(next) {
      const floor = openingScale > 1 ? openingScale : 1;
      return Math.min(28, Math.max(floor, next));
    }

    function clampPan() {
      const vpW = viewport.clientWidth;
      const vpH = viewport.clientHeight;
      const w = stage.offsetWidth * scale;
      const h = stage.offsetHeight * scale;
      if (w <= vpW) tx = (vpW - w) / 2;
      else tx = Math.min(0, Math.max(tx, vpW - w));
      if (h <= vpH) ty = (vpH - h) / 2;
      else ty = Math.min(0, Math.max(ty, vpH - h));
    }

    function focusBBox(lonMin, lonMax, latMin, latMax, paddingFactor) {
      const vpW = viewport.clientWidth;
      const vpH = viewport.clientHeight || stage.offsetHeight;
      const baseW = stage.offsetWidth;
      const baseH = stage.offsetHeight;
      const p1 = project(lonMin, latMax);
      const p2 = project(lonMax, latMin);
      const x1 = (p1.x / MAP_W) * baseW;
      const y1 = (p1.y / MAP_H) * baseH;
      const x2 = (p2.x / MAP_W) * baseW;
      const y2 = (p2.y / MAP_H) * baseH;
      const boxW = Math.max(x2 - x1, 48);
      const boxH = Math.max(y2 - y1, 48);
      const pad = paddingFactor || 1.12;
      scale = clampScale(Math.min(vpW / (boxW * pad), vpH / (boxH * pad)));
      tx = vpW / 2 - ((x1 + x2) / 2) * scale;
      ty = vpH / 2 - ((y1 + y2) / 2) * scale;
      apply();
      spiderfy();
    }

    function markerVisible(marker) {
      const kind = marker.getAttribute('data-place-kind') || '';
      if (kind === 'historic') return true;
      if (league === 'all' || kind === 'both') return true;
      return kind === league;
    }

    function applyVisibility() {
      markers.forEach((marker) => {
        const show = markerVisible(marker);
        marker.hidden = !show;
        marker.classList.toggle('is-filtered-out', !show);
        const L = lang();
        const label = marker.getAttribute('data-label-' + L) || marker.getAttribute('data-label-en');
        const city = marker.getAttribute('data-city-' + L) || marker.getAttribute('data-city-en');
        marker.setAttribute('aria-label', (L === 'en' ? 'Rugby club: ' : 'Klub rugby: ') + label + (L === 'en' ? ', city ' : ', miasto ') + city);
        const cityLabel = marker.querySelector('.map-marker-label');
        if (cityLabel) {
          const cityText = cityLabel.getAttribute('data-' + L) || cityLabel.getAttribute('data-en') || city;
          cityLabel.textContent = cityText;
        }
      });
      if (activeId) {
        const active = markerById(activeId);
        if (!active || active.hidden) {
          const hadFocus = lastMarkerFocus && (active === lastMarkerFocus || document.activeElement === lastMarkerFocus);
          unpin();
          if (hadFocus) focusActiveLeagueFilter();
        }
      }
    }

    function focusActiveLeagueFilter() {
      const btn = document.querySelector('[data-map-filter][aria-pressed="true"]');
      if (btn) btn.focus({ preventScroll: true });
    }

    function markerById(id) {
      return markers.find((marker) => marker.getAttribute('data-place-id') === id);
    }

    function markerTranslate(marker) {
      const raw = marker.style.translate || window.getComputedStyle(marker).translate || '';
      if (!raw || raw === 'none') return { dx: 0, dy: 0 };
      const parts = raw.trim().split(/\s+/);
      const dx = parseFloat(parts[0]) || 0;
      const dy = parseFloat(parts[1]) || 0;
      return { dx, dy };
    }

    function screenToLeaderPoint(clientX, clientY) {
      const pt = leaders.createSVGPoint();
      pt.x = clientX;
      pt.y = clientY;
      const ctm = leaders.getScreenCTM();
      if (!ctm) return { x: 0, y: 0 };
      return pt.matrixTransform(ctm.inverse());
    }

    function drawLeaders() {
      while (leaders.firstChild) leaders.removeChild(leaders.firstChild);
      if (!openCluster) return;
      const w = stage.offsetWidth;
      const h = stage.offsetHeight;
      if (!w || !h || scale <= 0) return;
      leaders.setAttribute('viewBox', '0 0 ' + w + ' ' + h);
      leaders.setAttribute('preserveAspectRatio', 'none');
      leaders.removeAttribute('width');
      leaders.removeAttribute('height');
      markers.forEach((marker) => {
        if (!marker.classList.contains('is-clustered') || marker.hidden) return;
        if (clusterId(marker) !== openCluster) return;
        const kind = marker.getAttribute('data-place-kind') || '';
        if (kind === 'historic') return;
        const { dx, dy } = markerTranslate(marker);
        if (Math.abs(dx) < 0.5 && Math.abs(dy) < 0.5) return;
        const mr = marker.getBoundingClientRect();
        const cx = mr.left + mr.width / 2;
        const cy = mr.top + mr.height / 2;
        const tip = screenToLeaderPoint(cx, cy);
        const anchor = screenToLeaderPoint(cx - dx * scale, cy - dy * scale);
        const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
        line.setAttribute('x1', String(anchor.x));
        line.setAttribute('y1', String(anchor.y));
        line.setAttribute('x2', String(tip.x));
        line.setAttribute('y2', String(tip.y));
        leaders.appendChild(line);
      });
    }

    function spiderfy() {
      const clusterPx = 48;
      markers.forEach((marker) => {
        marker.style.translate = '';
        marker.classList.remove('is-clustered');
      });
      const shown = markers.filter((marker) => !marker.hidden);
      const points = shown.map((marker) => ({
        marker,
        x: marker.offsetLeft + marker.offsetWidth / 2,
        y: marker.offsetTop + marker.offsetHeight / 2,
      }));
      const used = new Set();
      points.forEach((point, index) => {
        if (used.has(index)) return;
        const group = [index];
        for (let j = index + 1; j < points.length; j += 1) {
          const dx = (points[j].x - point.x) * scale;
          const dy = (points[j].y - point.y) * scale;
          if (Math.hypot(dx, dy) < clusterPx) group.push(j);
        }
        group.forEach((i) => used.add(i));
        if (group.length < 2) return;
        const id = group.map((i) => points[i].marker.getAttribute('data-place-id')).sort().join('|');
        if (openCluster !== id) return;
        group.forEach((i) => points[i].marker.classList.add('is-clustered'));
        const zoomBoost = Math.max(1, scale / openingScale);
        const screenRadius = Math.min(72, 34 + group.length * 7) * zoomBoost;
        const radius = screenRadius / scale;
        group.forEach((i, n) => {
          const angle = (Math.PI * 2 * n) / group.length - Math.PI / 2;
          const dx = Math.cos(angle) * radius;
          const dy = Math.sin(angle) * radius;
          points[i].marker.style.translate = dx + 'px ' + dy + 'px';
        });
      });
      drawLeaders();
    }

    function clusterId(marker) {
      const shown = markers.filter((item) => !item.hidden);
      const x = marker.offsetLeft;
      const y = marker.offsetTop;
      const group = shown.filter((item) => {
        const dx = (item.offsetLeft - x) * scale;
        const dy = (item.offsetTop - y) * scale;
        return Math.hypot(dx, dy) < 48;
      });
      if (group.length < 2) return '';
      return group.map((item) => item.getAttribute('data-place-id')).sort().join('|');
    }

    function srNewTab() {
      const L = lang();
      const span = document.createElement('span');
      span.className = 'visually-hidden';
      span.textContent = L === 'en' ? ' (opens in a new tab)' : ' (otwiera się w nowej karcie)';
      return span;
    }

    function showCard(marker, focusCard) {
      if (!card || !marker) return;
      const L = lang();
      const city = marker.getAttribute('data-city-' + L) || marker.getAttribute('data-city-en');
      const label = marker.getAttribute('data-label-' + L) || marker.getAttribute('data-label-en');
      const comp = marker.getAttribute('data-comp-' + L) || marker.getAttribute('data-comp-en') || '';
      const seasons = marker.getAttribute('data-seasons-' + L) || marker.getAttribute('data-seasons-en') || '';
      const kind = marker.getAttribute('data-place-kind') || '';

      const cityEl = card.querySelector('.map-card-city');
      const clubEl = card.querySelector('.map-card-club');
      const bodyEl = card.querySelector('.map-card-body');
      if (cityEl) cityEl.textContent = city;
      if (clubEl) clubEl.textContent = label;
      if (bodyEl) {
        const lines = [];
        if (kind === 'historic') {
          lines.push(seasons);
        } else {
          if (comp) lines.push(comp);
          if (seasons) lines.push((L === 'en' ? 'Seasons: ' : 'Sezony: ') + seasons);
        }
        bodyEl.textContent = lines.join('\n');
      }

      const wrap = card.querySelector('.map-card-link-wrap');
      wrap.innerHTML = '';
      const clubUrl = marker.getAttribute('data-club-url');
      const pzrProfile = marker.getAttribute('data-pzr-profile-url');
      const sourceUrl = marker.getAttribute('data-source-url');
      const internal = marker.getAttribute('data-internal');

      function addExternalLink(href, label) {
        const p = document.createElement('p');
        p.className = 'map-card-link-row mb-1';
        const a = document.createElement('a');
        a.className = 'rugby-link';
        a.href = href;
        a.target = '_blank';
        a.rel = 'noopener noreferrer';
        a.textContent = label;
        a.appendChild(srNewTab());
        p.appendChild(a);
        wrap.appendChild(p);
      }

      if (clubUrl) {
        addExternalLink(clubUrl, L === 'en' ? 'Club website' : 'Strona klubu');
      } else if (kind !== 'historic') {
        const p = document.createElement('p');
        p.className = 'small text-muted mb-1';
        p.textContent = L === 'en'
          ? 'No verified official club link was found.'
          : 'Nie znaleziono potwierdzonego oficjalnego linku do klubu.';
        wrap.appendChild(p);
      }
      if (pzrProfile) {
        addExternalLink(pzrProfile, L === 'en' ? 'Club profile at the Polish Rugby Union' : 'Profil klubu w PZR');
      }
      if (sourceUrl) {
        addExternalLink(
          sourceUrl,
          L === 'en' ? 'Source at the Polish Rugby Union' : 'Źródło w Polskim Związku Rugby'
        );
      }
      if (internal) {
        const p = document.createElement('p');
        p.className = 'map-card-link-row mb-0';
        const a = document.createElement('a');
        a.className = 'rugby-link';
        a.href = internal;
        a.textContent = kind === 'historic'
          ? (L === 'en' ? 'Read the farewell' : 'Czytaj pożegnanie')
          : (L === 'en' ? 'Read on' : 'Czytaj dalej');
        p.appendChild(a);
        wrap.appendChild(p);
      }

      card.classList.remove('d-none');
      activeId = marker.getAttribute('data-place-id') || '';
      placeTip(marker);
      markers.forEach((item) => {
        const on = item === marker;
        item.classList.toggle('is-active', on);
        item.setAttribute('aria-expanded', on ? 'true' : 'false');
        if (on) item.setAttribute('aria-controls', 'map-card');
        else item.removeAttribute('aria-controls');
      });
      if (focusCard && card) card.focus({ preventScroll: true });
    }

    function placeTip(marker) {
      if (!card || !viewport || !marker || card.classList.contains('d-none')) return;
      const pad = 10;
      const vr = viewport.getBoundingClientRect();
      const mr = marker.getBoundingClientRect();
      const maxW = Math.min(260, vr.width - pad * 2, window.innerWidth - pad * 2);
      card.style.maxWidth = maxW + 'px';
      card.style.width = maxW + 'px';
      const tipW = card.offsetWidth;
      const tipH = card.offsetHeight;
      let left;
      let top;
      if (narrow()) {
        left = mr.left + (mr.width - tipW) / 2;
        const below = mr.bottom + 8;
        const above = mr.top - tipH - 8;
        if (below + tipH <= window.innerHeight - pad) top = below;
        else if (above >= pad) top = above;
        else top = Math.max(pad, window.innerHeight - tipH - pad);
        if (left < pad) left = pad;
        if (left + tipW > window.innerWidth - pad) left = window.innerWidth - tipW - pad;
        card.style.left = left + 'px';
        card.style.top = top + 'px';
        return;
      }
      left = mr.right + 8;
      top = mr.top + mr.height / 2 - tipH / 2;
      if (left + tipW > vr.right - pad) left = mr.left - tipW - 8;
      const minLeft = Math.max(pad, vr.left + pad);
      const maxLeft = Math.min(window.innerWidth, vr.right) - tipW - pad;
      if (left < minLeft) left = minLeft;
      if (left > maxLeft) left = Math.max(pad, maxLeft);
      const minTop = Math.max(pad, vr.top + pad);
      const maxTop = Math.min(window.innerHeight, vr.bottom) - tipH - pad;
      if (top < minTop) top = minTop;
      if (top > maxTop) top = Math.max(pad, maxTop);
      card.style.left = left + 'px';
      card.style.top = top + 'px';
    }

    function hideCard() {
      if (card) {
        card.classList.add('d-none');
        card.style.left = '';
        card.style.top = '';
      }
      activeId = '';
      markers.forEach((item) => {
        item.classList.remove('is-active');
        item.setAttribute('aria-expanded', 'false');
        item.removeAttribute('aria-controls');
      });
    }

    function closeCard() {
      hideCard();
      if (lastMarkerFocus) {
        restoringFocus = true;
        lastMarkerFocus.focus({ preventScroll: true });
        restoringFocus = false;
      }
    }

    function selectMarker(marker) {
      if (!marker) return;
      if (narrow()) {
        openCluster = '';
        spiderfy();
        showCard(marker, false);
        return;
      }
      const id = clusterId(marker);
      openCluster = id || openCluster;
      spiderfy();
      showCard(marker, true);
    }

    function zoomAt(clientX, clientY, nextScale) {
      const rect = viewport.getBoundingClientRect();
      const mx = clientX - rect.left;
      const my = clientY - rect.top;
      const clamped = clampScale(nextScale);
      const k = clamped / scale;
      tx = mx - (mx - tx) * k;
      ty = my - (my - ty) * k;
      scale = clamped;
      clampPan();
      apply();
      spiderfy();
    }

    document.querySelectorAll('[data-map-action]').forEach((btn) => {
      btn.addEventListener('click', () => {
        const action = btn.getAttribute('data-map-action');
        const cx = viewport.clientWidth / 2 + viewport.getBoundingClientRect().left;
        const cy = viewport.clientHeight / 2 + viewport.getBoundingClientRect().top;
        if (action === 'zoom-in') zoomAt(cx, cy, scale * 1.35);
        if (action === 'zoom-out' && !btn.disabled) zoomAt(cx, cy, scale / 1.35);
        if (action === 'reset') {
          focusBBox(POLAND.lonMin, POLAND.lonMax, POLAND.latMin, POLAND.latMax, POLAND_PAD);
        }
      });
    });

    document.querySelectorAll('[data-map-filter]').forEach((btn) => {
      btn.addEventListener('click', () => {
        league = btn.getAttribute('data-map-filter') || 'all';
        document.querySelectorAll('[data-map-filter]').forEach((item) => {
          const on = item === btn;
          item.classList.toggle('is-active', on);
          item.setAttribute('aria-pressed', on ? 'true' : 'false');
        });
        unpin();
        applyVisibility();
        spiderfy();
      });
    });

    viewport.addEventListener('wheel', (e) => {
      if (!e.ctrlKey && !e.metaKey) return;
      const factor = e.deltaY < 0 ? 1.12 : 1 / 1.12;
      const next = clampScale(scale * factor);
      if (Math.abs(next - scale) < 0.001) return;
      e.preventDefault();
      zoomAt(e.clientX, e.clientY, next);
    }, { passive: false });

    viewport.addEventListener('pointerdown', (e) => {
      pointers.set(e.pointerId, { x: e.clientX, y: e.clientY });
      if (e.target.closest('.map-marker')) return;
      if (pointers.size >= 2) {
        dragging = false;
        return;
      }
      if (e.pointerType === 'touch' && !userZoomed()) return;
      dragging = true;
      sx = e.clientX - tx;
      sy = e.clientY - ty;
      viewport.setPointerCapture(e.pointerId);
    });
    viewport.addEventListener('pointermove', (e) => {
      if (!pointers.has(e.pointerId)) return;
      pointers.set(e.pointerId, { x: e.clientX, y: e.clientY });
      if (pointers.size === 2) {
        const pts = Array.from(pointers.values());
        const dist = Math.hypot(pts[0].x - pts[1].x, pts[0].y - pts[1].y);
        if (!viewport.dataset.pinch) {
          viewport.dataset.pinch = String(dist);
          viewport.dataset.pinchScale = String(scale);
        }
        const start = Number(viewport.dataset.pinch);
        const startScale = Number(viewport.dataset.pinchScale);
        const midX = (pts[0].x + pts[1].x) / 2;
        const midY = (pts[0].y + pts[1].y) / 2;
        zoomAt(midX, midY, startScale * (dist / (start || dist)));
        return;
      }
      if (!dragging) return;
      tx = e.clientX - sx;
      ty = e.clientY - sy;
      clampPan();
      apply();
    });
    function endPointer(e) {
      pointers.delete(e.pointerId);
      dragging = false;
      if (pointers.size < 2) {
        delete viewport.dataset.pinch;
        delete viewport.dataset.pinchScale;
      }
    }
    viewport.addEventListener('pointerup', endPointer);
    viewport.addEventListener('pointercancel', endPointer);
    viewport.addEventListener('touchmove', (e) => {
      if (e.touches.length === 2) e.preventDefault();
    }, { passive: false });

    let pinned = false;
    let hideTimer = 0;

    function unpin() {
      pinned = false;
      openCluster = '';
      closeCard();
      spiderfy();
    }
    markers.forEach((marker) => {
      marker.addEventListener('pointerenter', () => {
        if (pinned || narrow()) return;
        window.clearTimeout(hideTimer);
        showCard(marker);
      });
      marker.addEventListener('pointerleave', () => {
        if (pinned || narrow()) return;
        hideTimer = window.setTimeout(hideCard, 160);
      });
      marker.addEventListener('click', () => {
        pinned = true;
        lastMarkerFocus = marker;
        selectMarker(marker);
      });
      marker.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          if (e.key === ' ' && e.detail !== 0) return;
          e.preventDefault();
          pinned = true;
          lastMarkerFocus = marker;
          selectMarker(marker);
        }
      });
      marker.addEventListener('focus', () => {
        if (restoringFocus) return;
        lastMarkerFocus = marker;
        pinned = true;
        if (narrow()) {
          openCluster = '';
          spiderfy();
        }
        showCard(marker);
      });
    });
    if (card) {
      card.addEventListener('pointerenter', () => window.clearTimeout(hideTimer));
      card.addEventListener('pointerleave', () => {
        if (pinned || narrow()) return;
        hideTimer = window.setTimeout(hideCard, 160);
      });
    }
    const closeBtn = card && card.querySelector('.map-card-close');
    if (closeBtn) closeBtn.addEventListener('click', unpin);

    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && card && !card.classList.contains('d-none')) {
        e.preventDefault();
        unpin();
      }
    });

    function afterMapLayout() {
      focusBBox(POLAND.lonMin, POLAND.lonMax, POLAND.latMin, POLAND.latMax, POLAND_PAD);
      openingScale = scale;
      apply();
    }

    const mapImg = stage.querySelector('.rugby-map-base');
    applyVisibility();
    if (mapImg && !mapImg.complete) {
      mapImg.addEventListener('load', () => window.requestAnimationFrame(afterMapLayout), { once: true });
    }
    window.requestAnimationFrame(afterMapLayout);
    let resizeTimer = 0;
    window.addEventListener('resize', () => {
      window.clearTimeout(resizeTimer);
      resizeTimer = window.setTimeout(() => {
        if (!userZoomed()) {
          focusBBox(POLAND.lonMin, POLAND.lonMax, POLAND.latMin, POLAND.latMax, POLAND_PAD);
          openingScale = scale;
        }
        spiderfy();
        if (activeId) placeTip(markerById(activeId));
      }, 150);
    });
    window.addEventListener('scroll', () => {
      if (activeId && card && !card.classList.contains('d-none')) {
        placeTip(markerById(activeId));
      }
    }, { passive: true, capture: true });
    document.addEventListener('rugby:lang', () => {
      applyVisibility();
      if (activeId) showCard(markerById(activeId));
    });
  }

  document.addEventListener('DOMContentLoaded', initMap);
})();
