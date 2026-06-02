// --- Language switching function with fade transition (section + footer) ---
window.switchLang = function (lang) {
  const langs = document.querySelectorAll(".lang");
  const mainPL = document.getElementById("pl");
  const mainEN = document.getElementById("en");
  const footerPL = document.getElementById("pl-footer");
  const footerEN = document.getElementById("en-footer");

  // Helper function for fade transitions
  function fadeSwitch(showEl, hideEl) {
    if (!showEl || !hideEl) return;
    hideEl.style.opacity = "0";
    hideEl.classList.remove("active");
    showEl.classList.add("active");
    showEl.style.opacity = "0";
    setTimeout(() => (showEl.style.opacity = "1"), 50);
  }

  // Switch main content
  if (lang === "pl") fadeSwitch(mainPL, mainEN);
  else if (lang === "en") fadeSwitch(mainEN, mainPL);

  // Switch footer
  if (lang === "pl") fadeSwitch(footerPL, footerEN);
  else if (lang === "en") fadeSwitch(footerEN, footerPL);
};

// --- Main section (IIFE) ---
(function () {
  const galleryImages = Array.from(document.querySelectorAll(".gallery img"));
  const lightbox = document.getElementById("lightbox");
  const lightboxImg = document.getElementById("lightbox-img");
  const caption = document.getElementById("caption");

  if (!galleryImages.length || !lightbox || !lightboxImg || !caption) return;

  // --- Open Lightbox ---
  function openLightbox(index) {
    const img = galleryImages[index];
    lightboxImg.src = img.dataset.full || img.src;
    caption.textContent = img.alt || "";

    lightbox.classList.add("active");
    lightbox.style.opacity = "0";
    document.body.style.overflow = "hidden";

    setTimeout(() => {
      lightbox.style.transition = "opacity 0.3s ease";
      lightbox.style.opacity = "1";
    }, 10);
  }

  // --- Close Lightbox ---
  function closeLightbox() {
    lightbox.style.transition = "opacity 0.3s ease";
    lightbox.style.opacity = "0";
    setTimeout(() => {
      lightbox.classList.remove("active");
      document.body.style.overflow = "";
    }, 300);
  }

  // --- Open when thumbnail is clicked ---
  galleryImages.forEach((img, index) => {
    img.addEventListener("click", () => openLightbox(index));
  });

  // --- Click anywhere to close ---
  lightbox.addEventListener("click", closeLightbox);
  lightboxImg.addEventListener("click", closeLightbox);
  caption.addEventListener("click", closeLightbox);

  // --- Close with ESC key ---
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && lightbox.classList.contains("active")) {
      closeLightbox();
    }
  });
})();