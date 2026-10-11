document.addEventListener('DOMContentLoaded', () => {
    const body = document.body;

    document.querySelectorAll('.rugby-vtab').forEach((btn) => {
        btn.addEventListener('click', () => {
            const variant = btn.getAttribute('data-variant');
            body.setAttribute('data-variant', variant);
            document.querySelectorAll('.rugby-vtab').forEach((b) => {
                const on = b === btn;
                b.classList.toggle('is-active', on);
                b.setAttribute('aria-selected', on ? 'true' : 'false');
            });
        });
    });

    const dialog = document.getElementById('rugby-zoom');
    const zoomImg = document.getElementById('rugby-zoom-img');

    document.querySelectorAll('[data-full]').forEach((btn) => {
        btn.addEventListener('click', () => {
            if (!dialog || !zoomImg) return;
            zoomImg.src = btn.getAttribute('data-full');
            zoomImg.alt = btn.getAttribute('aria-label') || '';
            dialog.showModal();
        });
    });

    document.querySelectorAll('[data-youtube]').forEach((btn) => {
        btn.addEventListener('click', () => {
            const id = btn.getAttribute('data-youtube');
            const wrap = btn.parentElement.querySelector('.rugby-film-embed');
            if (!wrap || wrap.classList.contains('is-open')) return;
            wrap.classList.add('is-open');
            wrap.innerHTML = `<iframe width="100%" height="240" src="https://www.youtube.com/embed/${id}" title="Film AFC Rugby Giżycko" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen loading="lazy"></iframe>`;
        });
    });
});
