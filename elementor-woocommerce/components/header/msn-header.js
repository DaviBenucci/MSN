(function () {
  var header = document.querySelector("[data-msn-header]");
  var openButton = document.querySelector("[data-msn-menu-open]");
  var closeButton = document.querySelector("[data-msn-menu-close]");
  var panel = document.querySelector("[data-msn-menu-panel]");
  var backdrop = document.querySelector("[data-msn-menu-backdrop]");
  var lastFocused = null;

  function setCompact() {
    if (!header) return;
    header.classList.toggle("is-compact", 12 < window.scrollY);
  }

  function setOpen(isOpen) {
    if (!openButton || !panel || !backdrop) return;
    openButton.setAttribute("aria-expanded", String(isOpen));
    panel.setAttribute("aria-hidden", String(!isOpen));
    panel.classList.toggle("is-open", isOpen);
    backdrop.classList.toggle("is-open", isOpen);
    if (window.MSNStorefront) window.MSNStorefront.lockScroll(isOpen);

    if (isOpen) {
      lastFocused = document.activeElement;
      if (closeButton) closeButton.focus();
    } else if (lastFocused instanceof HTMLElement) {
      lastFocused.focus();
    }
  }

  if (openButton) openButton.addEventListener("click", function () { setOpen(true); });
  if (closeButton) closeButton.addEventListener("click", function () { setOpen(false); });
  if (backdrop) backdrop.addEventListener("click", function () { setOpen(false); });

  if (panel) {
    Array.prototype.forEach.call(panel.querySelectorAll("a"), function (link) {
      link.addEventListener("click", function () { setOpen(false); });
    });
  }

  document.addEventListener("keydown", function (event) {
    if (!panel || panel.getAttribute("aria-hidden") === "true") return;
    if (event.key === "Escape") setOpen(false);
    if (window.MSNStorefront) window.MSNStorefront.trapFocus(panel, event);
  });

  setCompact();
  window.addEventListener("scroll", setCompact, { passive: true });
})();
