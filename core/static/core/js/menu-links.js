const menuTrigger = document.querySelector('.menu-trigger');

if (menuTrigger) {

  const runMenuPreview = async () => {
    const collapseEl = document.getElementById('navbarNav');
    const toggler = document.querySelector('.navbar-toggler');

    const menuLinks = [
      '/gallery/',
      '/tonguetwister/',
      '/rugby/',
      '/docdiff/'
    ];

    const navLinks = menuLinks
      .map(href => document.querySelector(`.navbar .nav-link[href="${href}"]`))
      .filter(Boolean);

    const isMobile = window.innerWidth < 992;

    // MOBILE → open burger
    if (isMobile && collapseEl && !collapseEl.classList.contains('show')) {
      toggler?.click();

      await new Promise(r => setTimeout(r, 400));
    }

    // sequential hover simulation
    for (const link of navLinks) {

      link.classList.add('active');

      await new Promise(r => setTimeout(r, 260));

      link.classList.remove('active');
    }

    // MOBILE → close burger
    if (isMobile && collapseEl && collapseEl.classList.contains('show')) {

      await new Promise(r => setTimeout(r, 150));

      toggler?.click();
    }
  };

  let running = false;

  const trigger = async () => {
    if (running) return;

    running = true;

    await runMenuPreview();

    running = false;
  };

  menuTrigger.addEventListener('mouseenter', trigger);
  menuTrigger.addEventListener('click', (e) => {
    e.stopPropagation();
    trigger();
  });
  menuTrigger.addEventListener('touchstart', (e) => {
    e.stopPropagation();
    trigger();
  }, { passive: true });
}