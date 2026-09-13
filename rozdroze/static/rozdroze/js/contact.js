document.addEventListener("DOMContentLoaded", () => {
  const form = document.querySelector("#contact-form");
  if (!form) return;

  const button = form.querySelector("button[type=submit]");
  const alertBox = document.querySelector("#contact-alerts");

  function getMessage(id) {
    const lang = document.documentElement.lang || "pl";
    const el = document.getElementById(id);
    if (!el) return "";
    return (
      el.getAttribute(`data-${lang}`) ||
      el.getAttribute("data-pl") ||
      el.getAttribute("data-en") ||
      el.textContent.trim() ||
      ""
    );
  }

  function showAlert(type, messageId) {
    if (!alertBox) return;
    const message = getMessage(messageId);
    alertBox.innerHTML = `<div class="portal-alert portal-alert-${type}" role="alert">${message}</div>`;
  }

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    if (!button) return;

    button.disabled = true;
    button.setAttribute("aria-busy", "true");

    try {
      const response = await fetch(form.action, {
        method: "POST",
        body: new FormData(form),
        headers: { "X-Requested-With": "XMLHttpRequest" },
      });

      const data = await response.json();

      if (data.success) {
        showAlert("success", data.message_key);
        form.reset();
      } else {
        showAlert("warning", data.message_key || "msg-fail");
      }
    } catch (err) {
      showAlert("danger", "msg-error");
    } finally {
      button.disabled = false;
      button.removeAttribute("aria-busy");
    }
  });
});
