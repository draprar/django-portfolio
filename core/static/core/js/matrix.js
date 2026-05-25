(() => {
  const leftCanvas  = document.getElementById("matrixCanvas");
  const rightCanvas = document.getElementById("glitchCanvas");

  // Exit silently — script is loaded globally but matrix is only used on the home page
  if (!leftCanvas || !rightCanvas) return;

  const leftCtx  = leftCanvas.getContext("2d");
  const rightCtx = rightCanvas.getContext("2d");
  const leftContainer  = leftCanvas.parentElement;
  const rightContainer = rightCanvas.parentElement;

  // ── Config ────────────────────────────────────────────────────────────────
  //
  // Both canvases use mix-blend-mode: multiply (set in CSS).
  // Fade fills must be WHITE, not dark — white × image = image, so the trail
  // dissolves cleanly back to the underlying photo without tinting the background.
  // Gray glyphs: glyph × dark-bg ≈ invisible | glyph × bright-face = visible.
  //
  const GLYPH_COLOR = "#e8e8e8";
  const FADE_ALPHA  = 0.12;           // higher = shorter trail
  const FADE_COLOR  = `rgba(255, 255, 255, ${FADE_ALPHA})`;

  const FONT_LEFT  = 32;
  const FONT_RIGHT = 36;

  // ── Glyph sets ────────────────────────────────────────────────────────────
  const GLYPHS_LEFT  = ["0", "1"];
  const GLYPHS_RIGHT = [
    "✦", "✧", "✎", "✐", "✒", "✏",
    "★", "☆", "◆", "◇", "▲", "△", "●", "○"
  ];

  // ── State ─────────────────────────────────────────────────────────────────
  let columnsLeft  = 0, dropsLeft  = [];
  let columnsRight = 0, dropsRight = [];
  let matrixEnabled = true;
  let glitchEnabled = false;

  // ── Resize ────────────────────────────────────────────────────────────────
  function resizeAll() {
    leftCanvas.width   = leftContainer.offsetWidth;
    leftCanvas.height  = leftContainer.offsetHeight;
    columnsLeft  = Math.max(1, Math.floor(leftCanvas.width / FONT_LEFT));
    dropsLeft    = Array(columnsLeft).fill(1);

    rightCanvas.width  = rightContainer.offsetWidth;
    rightCanvas.height = rightContainer.offsetHeight;
    columnsRight = Math.max(1, Math.floor(rightCanvas.width / FONT_RIGHT));
    dropsRight   = Array.from(
      { length: columnsRight },
      () => -Math.floor(Math.random() * 100)  // staggered start positions
    );
  }

  // ResizeObserver fires on container layout changes (mobile, orientation, etc.)
  // Falls back to window resize for older browsers
  if (window.ResizeObserver) {
    const ro = new ResizeObserver(() => {
      clearTimeout(window._matrixResizeTimeout);
      window._matrixResizeTimeout = setTimeout(resizeAll, 80);
    });
    ro.observe(leftContainer);
    ro.observe(rightContainer);
  } else {
    window.addEventListener("resize", () => {
      clearTimeout(window._matrixResizeTimeout);
      window._matrixResizeTimeout = setTimeout(resizeAll, 120);
    });
  }

  document.addEventListener("DOMContentLoaded", resizeAll);
  resizeAll();

  // ── Draw functions ────────────────────────────────────────────────────────

  function drawMatrix() {
    if (!matrixEnabled) return;

    // White fill fades previous glyphs toward white each frame.
    // With multiply blend mode, white × image = image → visually transparent.
    leftCtx.fillStyle = FADE_COLOR;
    leftCtx.fillRect(0, 0, leftCanvas.width, leftCanvas.height);

    leftCtx.fillStyle    = GLYPH_COLOR;
    leftCtx.font         = `${FONT_LEFT}px monospace`;
    leftCtx.textBaseline = "top";

    dropsLeft.forEach((y, i) => {
      const char = GLYPHS_LEFT[Math.floor(Math.random() * GLYPHS_LEFT.length)];
      leftCtx.fillText(char, i * FONT_LEFT, (y - 1) * FONT_LEFT);

      if (y * FONT_LEFT > leftCanvas.height && Math.random() > 0.975) dropsLeft[i] = 0;
      dropsLeft[i] += 0.5;  // half-speed for a slower, more deliberate fall
    });
  }

  function drawArtMatrix() {
    if (!glitchEnabled) return;

    // Same fade strategy as the left canvas for visual consistency
    rightCtx.fillStyle = FADE_COLOR;
    rightCtx.fillRect(0, 0, rightCanvas.width, rightCanvas.height);

    rightCtx.fillStyle    = GLYPH_COLOR;
    rightCtx.font         = `${FONT_RIGHT}px monospace`;
    rightCtx.textBaseline = "top";

    dropsRight.forEach((y, i) => {
      const char = GLYPHS_RIGHT[Math.floor(Math.random() * GLYPHS_RIGHT.length)];
      rightCtx.fillText(char, i * FONT_RIGHT, (y - 1) * FONT_RIGHT);

      if (y * FONT_RIGHT > rightCanvas.height && Math.random() > 0.975) dropsRight[i] = 0;
      dropsRight[i] += 0.5;
    });
  }

  // ── Click toggle — left binary ↔ right symbols ────────────────────────────
  document.querySelector(".split-section")?.addEventListener("click", () => {
    matrixEnabled = !matrixEnabled;
    glitchEnabled = !matrixEnabled;

    if (!matrixEnabled) {
      leftCtx.clearRect(0, 0, leftCanvas.width, leftCanvas.height);
      dropsLeft = Array(columnsLeft).fill(1);
    }

    if (!glitchEnabled) {
      rightCtx.clearRect(0, 0, rightCanvas.width, rightCanvas.height);
      dropsRight = Array(columnsRight).fill(1);
    }
  });

  // ── Main loop (~30 fps) ───────────────────────────────────────────────────
  setInterval(() => {
    drawMatrix();
    drawArtMatrix();
  }, 33);
})();