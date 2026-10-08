(function () {
  var STORAGE_KEY = "wiciedzy.mokuso.minutes";
  var INHALE_MS = 4000;
  var EXHALE_MS = 6000;
  var CYCLE_MS = INHALE_MS + EXHALE_MS;
  var SCALE_MIN = 0.85;
  var SCALE_MAX = 1;
  var TICK_MS = 250;
  var LATE_GONG_MS = 3000;
  var GONG_BASE_HZ = 174;
  var GONG_RATIOS = [1, 2.76, 5.4];
  var GONG_PARTIALS = [1, 0.45, 0.22];
  var GONG_DECAY_S = 6;
  var GONG_ATTACK_S = 0.025;
  var GONG_PEAK = 0.4;

  var root = document.querySelector(".mokuso");
  if (!root) return;

  var setupEl = root.querySelector("[data-mokuso-setup]");
  var sessionEl = root.querySelector("[data-mokuso-session]");
  var endEl = root.querySelector("[data-mokuso-end]");
  var startBtn = root.querySelector("[data-mokuso-start]");
  var stopBtn = root.querySelector("[data-mokuso-stop]");
  var againBtn = root.querySelector("[data-mokuso-again]");
  var screenlessInput = root.querySelector("[data-mokuso-screenless]");
  var ring = root.querySelector("[data-mokuso-ring]");
  var timerEl = root.querySelector("[data-mokuso-timer]");
  var wordEl = root.querySelector("[data-mokuso-word]");
  var inhaleEl = root.querySelector("[data-mokuso-inhale]");
  var exhaleEl = root.querySelector("[data-mokuso-exhale]");
  var minuteInputs = root.querySelectorAll('input[name="mokuso-minutes"]');

  var motionQuery = window.matchMedia("(prefers-reduced-motion: reduce)");
  var running = false;
  var perfStart = 0;
  var wallStart = 0;
  var durationMs = 0;
  var tickId = 0;
  var rafId = 0;
  var audioCtx = null;
  var bus = null;
  var wakeLock = null;
  var startGongPlayed = false;
  var endGongPlayed = false;
  var sessionToken = 0;

  function reducedMotion() {
    return motionQuery.matches;
  }

  function allowedMinutes(value) {
    return value === 5 || value === 10 || value === 20;
  }

  function applyStoredMinutes() {
    var minutes = 5;
    try {
      var parsed = Number(localStorage.getItem(STORAGE_KEY));
      if (allowedMinutes(parsed)) minutes = parsed;
    } catch (err) {
      minutes = 5;
    }
    minuteInputs.forEach(function (input) {
      input.checked = Number(input.value) === minutes;
    });
  }

  function selectedMinutes() {
    var checked = root.querySelector('input[name="mokuso-minutes"]:checked');
    var minutes = checked ? Number(checked.value) : 5;
    return allowedMinutes(minutes) ? minutes : 5;
  }

  function saveMinutes(minutes) {
    if (!allowedMinutes(minutes)) return;
    try {
      localStorage.setItem(STORAGE_KEY, String(minutes));
    } catch (err) {
      /* ignore */
    }
  }

  function elapsedMs() {
    return Math.max(0, Math.max(performance.now() - perfStart, Date.now() - wallStart));
  }

  function formatRemaining(ms) {
    var seconds = Math.max(0, Math.ceil(ms / 1000));
    var mins = Math.floor(seconds / 60);
    var rest = seconds % 60;
    return mins + ":" + (rest < 10 ? "0" : "") + rest;
  }

  function paintTimer() {
    var left = durationMs - elapsedMs();
    if (left < 0) left = 0;
    timerEl.textContent = formatRemaining(left);
  }

  function paintBreath() {
    var pos = elapsedMs() % CYCLE_MS;
    var inhale = pos < INHALE_MS;
    inhaleEl.hidden = !inhale;
    exhaleEl.hidden = inhale;
    wordEl.hidden = inhale;
    if (reducedMotion()) {
      ring.style.transform = "none";
      return;
    }
    var span = SCALE_MAX - SCALE_MIN;
    var scale;
    if (inhale) {
      scale = SCALE_MIN + span * Math.sin((pos / INHALE_MS) * Math.PI / 2);
    } else {
      var t = (pos - INHALE_MS) / EXHALE_MS;
      scale = SCALE_MAX - span * Math.sin(t * Math.PI / 2);
    }
    ring.style.transform = "scale(" + scale + ")";
  }

  function frame() {
    if (!running || document.hidden) return;
    paintBreath();
    rafId = window.requestAnimationFrame(frame);
  }

  function startFrame() {
    window.cancelAnimationFrame(rafId);
    if (!running || document.hidden) return;
    rafId = window.requestAnimationFrame(frame);
  }

  function ensureBus() {
    if (!audioCtx) return null;
    if (!bus) {
      bus = audioCtx.createGain();
      bus.gain.value = 1;
      bus.connect(audioCtx.destination);
    }
    return bus;
  }

  function silence() {
    if (!bus) return;
    try {
      bus.disconnect();
    } catch (err) {
      /* ignore */
    }
    bus = null;
  }

  function playGong() {
    if (!audioCtx || audioCtx.state !== "running") return false;
    var dest = ensureBus();
    if (!dest) return false;
    var now = audioCtx.currentTime;
    var master = audioCtx.createGain();
    master.gain.setValueAtTime(0, now);
    master.gain.linearRampToValueAtTime(GONG_PEAK, now + GONG_ATTACK_S);
    master.gain.exponentialRampToValueAtTime(0.0001, now + GONG_DECAY_S);
    master.connect(dest);
    GONG_RATIOS.forEach(function (ratio, index) {
      var osc = audioCtx.createOscillator();
      var partial = audioCtx.createGain();
      osc.type = "sine";
      osc.frequency.value = GONG_BASE_HZ * ratio;
      partial.gain.value = GONG_PARTIALS[index] || 0.2;
      osc.connect(partial);
      partial.connect(master);
      osc.start(now);
      osc.stop(now + GONG_DECAY_S + 0.05);
    });
    return true;
  }

  function armAudio() {
    try {
      if (navigator.audioSession) navigator.audioSession.type = "playback";
    } catch (err) {
      /* ignore */
    }
    var AudioCtx = window.AudioContext || window.webkitAudioContext;
    if (!AudioCtx) return;
    if (!audioCtx) {
      try {
        audioCtx = new AudioCtx();
      } catch (err) {
        audioCtx = null;
        return;
      }
    }
    audioCtx.resume().then(function () {
      if (running && !startGongPlayed && audioCtx && audioCtx.state === "running") {
        if (playGong()) startGongPlayed = true;
      }
    }).catch(function () {
      /* session continues without sound */
    });
  }

  function resumeAudio() {
    if (!audioCtx) return;
    if (audioCtx.state === "suspended" || audioCtx.state === "interrupted") {
      audioCtx.resume().catch(function () {});
    }
  }

  function acquireWake() {
    if (!navigator.wakeLock || !running) return;
    navigator.wakeLock.request("screen").then(function (lock) {
      if (!running) {
        lock.release().catch(function () {});
        return;
      }
      wakeLock = lock;
    }).catch(function () {});
  }

  function releaseWake() {
    var lock = wakeLock;
    wakeLock = null;
    if (!lock) return;
    lock.release().catch(function () {});
  }

  function showOnly(which) {
    setupEl.hidden = which !== "setup";
    sessionEl.hidden = which !== "session";
    endEl.hidden = which !== "end";
  }

  function clearClocks() {
    window.clearInterval(tickId);
    window.cancelAnimationFrame(rafId);
    tickId = 0;
    rafId = 0;
  }

  function leaveScreenless() {
    root.classList.remove("is-screenless");
  }

  function finish(fromReturn) {
    if (!running) return;
    var overshoot = elapsedMs() - durationMs;
    var token = sessionToken;
    running = false;
    clearClocks();
    releaseWake();
    leaveScreenless();
    ring.style.transform = "none";
    showOnly("end");
    var skipGong = fromReturn && overshoot > LATE_GONG_MS;
    if (!skipGong && !endGongPlayed) {
      if (playGong()) {
        endGongPlayed = true;
      } else if (audioCtx) {
        audioCtx.resume().then(function () {
          if (token !== sessionToken || endGongPlayed) return;
          if (playGong()) endGongPlayed = true;
        }).catch(function () {});
      }
    }
    againBtn.focus();
  }

  function tick(fromReturn) {
    if (!running) return;
    if (elapsedMs() >= durationMs) {
      finish(fromReturn);
      return;
    }
    paintTimer();
    if (!document.hidden) paintBreath();
  }

  function stop() {
    if (!running && sessionEl.hidden) return;
    running = false;
    clearClocks();
    releaseWake();
    silence();
    leaveScreenless();
    ring.style.transform = "none";
    showOnly("setup");
    startBtn.focus();
  }

  function begin() {
    if (running) return;
    durationMs = selectedMinutes() * 60 * 1000;
    sessionToken += 1;
    running = true;
    startGongPlayed = false;
    endGongPlayed = false;
    perfStart = performance.now();
    wallStart = Date.now();
    if (screenlessInput.checked) root.classList.add("is-screenless");
    else leaveScreenless();
    showOnly("session");
    paintTimer();
    paintBreath();
    sessionEl.focus();
    armAudio();
    acquireWake();
    tickId = window.setInterval(function () {
      tick(false);
    }, TICK_MS);
    startFrame();
  }

  function onReturn() {
    resumeAudio();
    if (!running) return;
    acquireWake();
    startFrame();
    tick(true);
  }

  minuteInputs.forEach(function (input) {
    input.addEventListener("change", function () {
      if (input.checked) saveMinutes(Number(input.value));
    });
  });
  startBtn.addEventListener("click", begin);
  stopBtn.addEventListener("click", stop);
  againBtn.addEventListener("click", function () {
    showOnly("setup");
    startBtn.focus();
  });
  document.addEventListener("visibilitychange", function () {
    if (document.visibilityState === "visible") onReturn();
    else window.cancelAnimationFrame(rafId);
  });
  window.addEventListener("pageshow", onReturn);
  window.addEventListener("focus", onReturn);
  if (motionQuery.addEventListener) {
    motionQuery.addEventListener("change", function () {
      if (reducedMotion()) ring.style.transform = "none";
    });
  }

  applyStoredMinutes();
})();
