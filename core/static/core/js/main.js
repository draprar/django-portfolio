document.addEventListener("DOMContentLoaded", () => {
    if (typeof AOS !== "undefined") {
        AOS.init({
            duration: 800,
            once: true,
            offset: 0
        });
    }
});

window.addEventListener("load", () => {
    AOS.refreshHard();
});