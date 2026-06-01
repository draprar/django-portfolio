(() => {
  const leftCanvas  = document.getElementById("matrixCanvas");
  const rightCanvas = document.getElementById("glitchCanvas");

  if (!leftCanvas || !rightCanvas) return;

  const leftCtx  = leftCanvas.getContext("2d");
  const rightCtx = rightCanvas.getContext("2d");
  const leftContainer  = leftCanvas.parentElement;
  const rightContainer = rightCanvas.parentElement;

  // ───────────────────────────────────────────────────────────────
  // CONFIG
  // ───────────────────────────────────────────────────────────────
  const GLYPH_COLOR = "#e8e8e8";
  const FADE_ALPHA  = 0.12;
  const FADE_COLOR  = `rgba(255,255,255,${FADE_ALPHA})`;

  const FONT_LEFT  = 32;
  const FONT_RIGHT = 36;

  const GLYPHS_LEFT  = ["0", "1"];
  const GLYPHS_RIGHT = ["✦","✧","✎","✐","✒","✏","★","☆","◆","◇","▲","△","●","○"];

  let columnsLeft  = 0, dropsLeft  = [];
  let columnsRight = 0, dropsRight = [];
  let matrixEnabled = true;
  let glitchEnabled = false;

  // ───────────────────────────────────────────────────────────────
  // MOBILE FIX: stabilizacja wysokości kontenerów
  // (Safari dynamicznie zmienia vh → powoduje reset canvasów)
  // ───────────────────────────────────────────────────────────────
  function getStableHeight(el) {
    // zamiast offsetHeight → boundingClientRect (stabilniejsze)
    return el.getBoundingClientRect().height;
  }

  // ───────────────────────────────────────────────────────────────
  // RESIZE
  // ───────────────────────────────────────────────────────────────
  let lastResize = 0;

  function resizeAll() {
    const hLeft  = getStableHeight(leftContainer);
    const hRight = getStableHeight(rightContainer);

    leftCanvas.width  = leftContainer.offsetWidth;
    leftCanvas.height = hLeft;

    rightCanvas.width  = rightContainer.offsetWidth;
    rightCanvas.height = hRight;

    columnsLeft  = Math.max(1, Math.floor(leftCanvas.width / FONT_LEFT));
    dropsLeft    = Array(columnsLeft).fill(1);

    columnsRight = Math.max(1, Math.floor(rightCanvas.width / FONT_RIGHT));
    dropsRight   = Array.from(
      { length: columnsRight },
      () => -Math.floor(Math.random() * 100)
    );
  }

  // ───────────────────────────────────────────────────────────────
  // ResizeObserver — throttling (iPhone Safari spam fix)
  // ───────────────────────────────────────────────────────────────
  if (window.ResizeObserver) {
    const ro = new ResizeObserver(() => {
      const now = Date.now();
      if (now - lastResize < 250) return; // ignoruj spam
      lastResize = now;
      resizeAll();
    });
    ro.observe(leftContainer);
    ro.observe(rightContainer);
  } else {
    window.addEventListener("resize", () => {
      const now = Date.now();
      if (now - lastResize < 250) return;
      lastResize = now;
      resizeAll();
    });
  }

  // ───────────────────────────────────────────────────────────────
  // INITIALIZATION — mobile Safari fix: wielokrotne wymuszenie resize
  // ───────────────────────────────────────────────────────────────
  document.addEventListener("DOMContentLoaded", () => {
    resizeAll();
    setTimeout(resizeAll, 200);
    setTimeout(resizeAll, 600);
    setTimeout(resizeAll, 1200); // killer fix dla iPhone Safari
  });

  resizeAll();

  // ───────────────────────────────────────────────────────────────
  // DRAW FUNCTIONS
  // ───────────────────────────────────────────────────────────────
  function drawMatrix() {
    if (!matrixEnabled) return;

    leftCtx.fillStyle = FADE_COLOR;
    leftCtx.fillRect(0, 0, leftCanvas.width, leftCanvas.height);

    leftCtx.fillStyle = GLYPH_COLOR;
    leftCtx.font = `${FONT_LEFT}px monospace`;
    leftCtx.textBaseline = "top";

    dropsLeft.forEach((y, i) => {
      const char = GLYPHS_LEFT[Math.floor(Math.random() * GLYPHS_LEFT.length)];
      leftCtx.fillText(char, i * FONT_LEFT, (y - 1) * FONT_LEFT);

      if (y * FONT_LEFT > leftCanvas.height && Math.random() > 0.975) dropsLeft[i] = 0;
      dropsLeft[i] += 0.5;
    });
  }

  function drawArtMatrix() {
    if (!glitchEnabled) return;

    rightCtx.fillStyle = FADE_COLOR;
    rightCtx.fillRect(0, 0, rightCanvas.width, rightCanvas.height);

    rightCtx.fillStyle = GLYPH_COLOR;
    rightCtx.font = `${FONT_RIGHT}px monospace`;
    rightCtx.textBaseline = "top";

    dropsRight.forEach((y, i) => {
      const char = GLYPHS_RIGHT[Math.floor(Math.random() * GLYPHS_RIGHT.length)];
      rightCtx.fillText(char, i * FONT_RIGHT, (y - 1) * FONT_RIGHT);

      if (y * FONT_RIGHT > rightCanvas.height && Math.random() > 0.975) dropsRight[i] = 0;
      dropsRight[i] += 0.5;
    });
  }

  // ───────────────────────────────────────────────────────────────
  // CLICK TOGGLE
  // ───────────────────────────────────────────────────────────────
  document.querySelector(".split-section")?.addEventListener("click", () => {
    matrixEnabled = !matrixEnabled;
    glitchEnabled = !matrixEnabled;

    if (!matrixEnabled) {
      leftCtx.clearRect(0, 0, leftCanvas.width, leftCanvas.height);
      dropsLeft = Array(columnsLeft).fill(1);

      rightCtx.clearRect(0, 0, rightCanvas.width, rightCanvas.height);
      dropsRight = Array.from(
        { length: columnsRight },
        () => -Math.floor(Math.random() * 30)
      );
    } else {
      rightCtx.clearRect(0, 0, rightCanvas.width, rightCanvas.height);
      dropsRight = Array.from(
        { length: columnsRight },
        () => -Math.floor(Math.random() * 100)
      );
    }
  });

  // ───────────────────────────────────────────────────────────────
  // MAIN LOOP
  // ───────────────────────────────────────────────────────────────
  setInterval(() => {
    drawMatrix();
    drawArtMatrix();
  }, 33);
})();
