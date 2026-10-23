(function () {
  'use strict';

  const PHASES = [
    {
      key: 'run',
      namePl: 'Bieg z piłką',
      nameEn: 'Run with the ball',
      descPl: 'Zawodnik niosący piłkę szuka wolnej przestrzeni, by przesunąć akcję do przodu.',
      descEn: 'The ball carrier looks for space to move the attack forward.',
      score: '0:0',
      ball: { x: 680, y: 170 },
      players: [
        { n: 1, x: 250, y: 150 },
        { n: 2, x: 360, y: 310 },
        { n: 3, x: 430, y: 210 },
        { n: 4, x: 520, y: 120 },
        { n: 5, x: 590, y: 280 },
        { n: 6, x: 680, y: 170 },
        { n: 7, x: 760, y: 330 },
      ],
      active: [6],
    },
    {
      key: 'pass',
      namePl: 'Podanie ręką',
      nameEn: 'Hand pass',
      descPl: 'Podanie nie może iść do przodu — kluczowa zasada! Pozycja partnera nie decyduje o kierunku podania.',
      descEn: 'The pass must not travel forward — a core rule. The receiver’s position alone does not define the direction of the pass.',
      score: '0:0',
      ball: { x: 590, y: 280 },
      players: [
        { n: 1, x: 250, y: 150 },
        { n: 2, x: 360, y: 310 },
        { n: 3, x: 430, y: 210 },
        { n: 4, x: 520, y: 120 },
        { n: 5, x: 590, y: 280 },
        { n: 6, x: 700, y: 200 },
        { n: 7, x: 760, y: 330 },
      ],
      active: [5, 6],
    },
    {
      key: 'tackle',
      namePl: 'Szarża',
      nameEn: 'Tackle',
      descPl: 'Obrońca chwyta niosącego i sprowadza go na ziemię. Po szarży piłka musi być natychmiast udostępniona.',
      descEn: 'A defender brings the carrier to ground. After the tackle, the ball must be made available immediately.',
      score: '0:0',
      ball: { x: 820, y: 300 },
      players: [
        { n: 1, x: 250, y: 150 },
        { n: 2, x: 360, y: 310 },
        { n: 3, x: 430, y: 210 },
        { n: 4, x: 520, y: 120 },
        { n: 5, x: 820, y: 300 },
        { n: 6, x: 780, y: 260 },
        { n: 7, x: 800, y: 320 },
      ],
      active: [5, 7],
    },
    {
      key: 'ruck',
      namePl: 'Ruck',
      nameEn: 'Ruck',
      descPl: 'Powstaje, gdy zawodnicy obu drużyn pozostają w kontakcie nad piłką leżącą na ziemi. Nie każda szarża kończy się ruckiem!',
      descEn: 'Forms when players from both teams stay in contact over the ball on the ground. Not every tackle leads to a ruck.',
      score: '0:0',
      ball: { x: 810, y: 310 },
      players: [
        { n: 1, x: 250, y: 150 },
        { n: 2, x: 360, y: 310 },
        { n: 3, x: 430, y: 210 },
        { n: 4, x: 520, y: 120 },
        { n: 5, x: 790, y: 290 },
        { n: 6, x: 770, y: 250 },
        { n: 7, x: 830, y: 310 },
      ],
      active: [5, 6, 7],
    },
    {
      key: 'try',
      namePl: 'Przyłożenie',
      nameEn: 'Try',
      descPl: 'Zawodnik przykłada piłkę do ziemi w polu punktowym przeciwnika — 5 punktów!',
      descEn: 'The player grounds the ball in the opponents’ in-goal area — 5 points.',
      score: '5:0',
      ball: { x: 930, y: 230 },
      players: [
        { n: 1, x: 250, y: 150 },
        { n: 2, x: 360, y: 310 },
        { n: 3, x: 430, y: 210 },
        { n: 4, x: 520, y: 120 },
        { n: 5, x: 900, y: 230 },
        { n: 6, x: 860, y: 200 },
        { n: 7, x: 760, y: 330 },
      ],
      active: [5],
      highlight: 'in_goal',
    },
    {
      key: 'conversion',
      namePl: 'Podwyższenie',
      nameEn: 'Conversion',
      descPl: 'Po przyłożeniu drużyna może zdobyć dodatkowe 2 punkty. W rugby 7 podwyższenie to drop-kick wykonany w 30 sekund.',
      descEn: 'After a try, the team can add 2 points. In sevens, the conversion is a drop kick within 30 seconds.',
      score: '7:0',
      ball: { x: 840, y: 230 },
      players: [
        { n: 1, x: 250, y: 150 },
        { n: 2, x: 360, y: 310 },
        { n: 3, x: 430, y: 210 },
        { n: 4, x: 520, y: 120 },
        { n: 5, x: 900, y: 280 },
        { n: 6, x: 860, y: 200 },
        { n: 7, x: 760, y: 330 },
      ],
      active: [5],
      highlight: 'posts',
    },
    {
      key: 'restart',
      namePl: 'Wznowienie gry',
      nameEn: 'Restart',
      descPl: 'Drużyna, która zdobyła punkty, wznawia grę drop-kickiem z linii środkowej — unikalna zasada rugby 7!',
      descEn: 'The team that scored restarts with a drop kick from halfway — a distinctive sevens rule.',
      score: '7:0',
      ball: { x: 500, y: 230 },
      players: [
        { n: 1, x: 250, y: 150 },
        { n: 2, x: 360, y: 310 },
        { n: 3, x: 430, y: 210 },
        { n: 4, x: 520, y: 120 },
        { n: 5, x: 480, y: 280 },
        { n: 6, x: 460, y: 200 },
        { n: 7, x: 760, y: 330 },
      ],
      active: [5],
      highlight: 'halfway',
    },
  ];

  let stepIndex = 0;
  let scoringPreviewKey = '';

  const SCORING = {
    try: {
      highlight: 'in_goal',
      explainerPl: 'Przyłożenie to 5 punktów — przyłożenie piłki do ziemi w polu punktowym przeciwnika.',
      explainerEn: 'A try is worth 5 points — grounding the ball on the ground in the opponents’ in-goal area.',
    },
    conversion: {
      highlight: 'posts',
      explainerPl: 'Podwyższenie to 2 punkty za celny kop po przyłożeniu. W rugby 7 drop-kick w ciągu 30 sekund od przyznania przyłożenia.',
      explainerEn: 'A conversion is worth 2 points for a successful kick after a try. In sevens, a drop kick within 30 seconds of the try being awarded.',
    },
    penalty_try: {
      highlight: 'in_goal',
      explainerPl: 'Przyłożenie karne to 7 punktów — przyznawane, gdy przewinienie przeciwnika uniemożliwia zdobycie prawdopodobnego przyłożenia albo przyłożenia w korzystniejszej pozycji. Nie wykonuje się podwyższenia.',
      explainerEn: 'A penalty try is worth 7 points — awarded when an infringement prevents a probable try or a try in a more advantageous position. No conversion is attempted.',
    },
    penalty_goal: {
      highlight: 'posts',
      explainerPl: 'Rzut karny na bramkę to 3 punkty — celny kop na bramkę z rzutu karnego.',
      explainerEn: 'A penalty goal is worth 3 points — a successful kick at goal from a penalty.',
    },
    drop_goal: {
      highlight: 'posts',
      explainerPl: 'Drop-goal to 3 punkty — celny kop na bramkę w grze otwartej, wykonany po odbiciu piłki od ziemi.',
      explainerEn: 'A dropped goal is worth 3 points — a successful kick at goal in open play, taken after the ball bounces off the ground.',
    },
  };

  function lang() {
    return document.documentElement.getAttribute('lang') || 'pl';
  }

  function reducedMotion() {
    return window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  }

  function setPlayerPos(n, x, y) {
    const g = document.querySelector('#rugby-pitch .pitch-player[data-player="' + n + '"]');
    if (!g) return;
    g.querySelectorAll('circle').forEach((circle) => {
      circle.setAttribute('cx', x);
      circle.setAttribute('cy', y);
    });
    const text = g.querySelector('text');
    if (text) {
      text.setAttribute('x', x);
      text.setAttribute('y', y + 6);
    }
  }

  function clearScoringHighlights(root) {
    if (!root) return;
    root.querySelectorAll('.pitch-hit.is-scoring').forEach((el) => el.classList.remove('is-scoring'));
  }

  function applyScoringPreview(key) {
    const root = document.getElementById('rugby-pitch');
    const explainer = document.getElementById('pitch-explainer');
    const spec = SCORING[key];
    if (!root || !spec) return;
    clearScoringHighlights(root);
    root.querySelectorAll('[data-pitch-key="' + spec.highlight + '"]').forEach((el) => el.classList.add('is-scoring'));
    if (explainer) {
      const L = lang();
      explainer.textContent = L === 'en' ? spec.explainerEn : spec.explainerPl;
    }
  }

  function clearScoringPreview() {
    scoringPreviewKey = '';
    document.querySelectorAll('.scoring-btn').forEach((btn) => {
      btn.classList.remove('is-on');
      btn.setAttribute('aria-pressed', 'false');
    });
    clearScoringHighlights(document.getElementById('rugby-pitch'));
  }

  function setScoringPreview(key) {
    scoringPreviewKey = key;
    document.querySelectorAll('.scoring-btn').forEach((btn) => {
      const on = btn.getAttribute('data-scoring') === key;
      btn.classList.toggle('is-on', on);
      btn.setAttribute('aria-pressed', on ? 'true' : 'false');
    });
    applyScoringPreview(key);
  }

  function renderPhase(index) {
    clearScoringPreview();
    const phase = PHASES[index];
    const L = lang();
    const heading = document.getElementById('phase-heading');
    const explainer = document.getElementById('pitch-explainer');
    const scoreEl = document.getElementById('phase-score');
    const prev = document.getElementById('phase-prev');
    const next = document.getElementById('phase-next');

    if (heading) {
      heading.textContent = (L === 'en' ? phase.nameEn : phase.namePl) + ' (' + (index + 1) + '/' + PHASES.length + ')';
    }
    if (explainer) explainer.textContent = L === 'en' ? phase.descEn : phase.descPl;
    if (scoreEl) scoreEl.textContent = phase.score;
    if (prev) prev.disabled = index === 0;
    if (next) {
      const replay = index === PHASES.length - 1;
      next.textContent = replay
        ? (L === 'en' ? 'Replay the move' : 'Pokaż ponownie')
        : (L === 'en' ? 'Next' : 'Dalej');
      next.setAttribute('data-pl', replay ? 'Pokaż ponownie' : 'Dalej');
      next.setAttribute('data-en', replay ? 'Replay the move' : 'Next');
    }

    phase.players.forEach((p) => setPlayerPos(p.n, p.x, p.y));
    const ball = document.getElementById('phase-ball');
    if (ball) {
      ball.setAttribute('cx', phase.ball.x);
      ball.setAttribute('cy', phase.ball.y);
      ball.classList.add('is-on');
    }

    const root = document.getElementById('rugby-pitch');
    if (root) {
      root.querySelectorAll('.phase-mark.is-on').forEach((el) => el.classList.remove('is-on'));
      root.querySelectorAll('.pitch-hit.is-on, .pitch-player.is-on').forEach((el) => el.classList.remove('is-on'));
      phase.active.forEach((n) => {
        const g = root.querySelector('.pitch-player[data-player="' + n + '"]');
        if (g) g.classList.add('is-on');
      });
      if (phase.highlight === 'in_goal') {
        root.querySelectorAll('[data-pitch-key="in_goal"]').forEach((el) => el.classList.add('is-on'));
      }
      if (phase.highlight === 'posts') {
        root.querySelectorAll('[data-pitch-key="posts"]').forEach((el) => el.classList.add('is-on'));
      }
      if (phase.highlight === 'halfway') {
        const line = document.getElementById('phase-halfway');
        if (line) line.classList.add('is-on');
      }
    }

    document.querySelectorAll('#phase-steps .phase-btn').forEach((btn, i) => {
      btn.classList.toggle('is-on', i === index);
      btn.setAttribute('aria-current', i === index ? 'step' : 'false');
    });
  }

  function goTo(index) {
    stepIndex = Math.max(0, Math.min(PHASES.length - 1, index));
    renderPhase(stepIndex);
  }

  function buildStepper() {
    const row = document.getElementById('phase-steps');
    if (!row || row.childElementCount) return;
    PHASES.forEach((phase, i) => {
      const btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'phase-btn';
      btn.setAttribute('data-phase-step', String(i));
      btn.setAttribute('data-aria-pl', (i + 1) + ' ' + phase.namePl);
      btn.setAttribute('data-aria-en', (i + 1) + ' ' + phase.nameEn);
      btn.setAttribute('aria-label', (i + 1) + ' ' + phase.namePl);

      const num = document.createElement('span');
      num.className = 'phase-btn-num';
      num.setAttribute('aria-hidden', 'true');
      num.textContent = String(i + 1);

      const label = document.createElement('span');
      label.className = 'phase-btn-label';
      label.setAttribute('data-pl', phase.namePl);
      label.setAttribute('data-en', phase.nameEn);
      label.textContent = phase.namePl;

      btn.appendChild(num);
      btn.appendChild(label);
      btn.addEventListener('click', () => goTo(i));
      row.appendChild(btn);
    });
  }

  function bindPitch() {
    const root = document.getElementById('rugby-pitch');
    if (!root) return;
    buildStepper();
    goTo(0);

    const prev = document.getElementById('phase-prev');
    const next = document.getElementById('phase-next');
    if (prev) prev.addEventListener('click', () => goTo(stepIndex - 1));
    if (next) {
      next.addEventListener('click', () => {
        if (stepIndex >= PHASES.length - 1) goTo(0);
        else goTo(stepIndex + 1);
      });
    }

    document.querySelectorAll('.scoring-btn').forEach((btn) => {
      const activate = () => setScoringPreview(btn.getAttribute('data-scoring') || '');
      btn.addEventListener('click', activate);
      btn.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          activate();
        }
      });
    });

    root.querySelectorAll('.pitch-hit').forEach((hit) => {
      const activate = () => {
        const key = hit.getAttribute('data-pitch-key');
        if (key === 'in_goal') goTo(4);
        else if (key === 'posts') goTo(5);
      };
      hit.addEventListener('click', activate);
      hit.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          activate();
        }
      });
    });

    root.querySelectorAll('.pitch-player').forEach((hit) => {
      const activate = () => {
        const n = Number(hit.getAttribute('data-player'));
        if (!n) return;
        const later = PHASES.findIndex((phase, i) => i > stepIndex && phase.active.includes(n));
        const first = PHASES.findIndex((phase) => phase.active.includes(n));
        if (later >= 0) goTo(later);
        else if (first >= 0) goTo(first);
      };
      hit.addEventListener('click', activate);
      hit.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          activate();
        }
      });
    });
  }

  document.addEventListener('DOMContentLoaded', bindPitch);
  document.addEventListener('rugby:lang', () => {
    renderPhase(stepIndex);
    if (scoringPreviewKey) applyScoringPreview(scoringPreviewKey);
  });
})();
