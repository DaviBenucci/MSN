(function () {
  var openButton = document.querySelector("[data-msn-filter-open]");
  var closeButton = document.querySelector("[data-msn-filter-close]");
  var panel = document.querySelector(".msn-shop-filter");
  var backdrop = document.querySelector("[data-msn-filter-backdrop]");
  var lastFocused = null;

  function setOpen(isOpen) {
    if (!panel || !backdrop) return;
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

  document.addEventListener("keydown", function (event) {
    if (!panel || !panel.classList.contains("is-open")) return;
    if (event.key === "Escape") setOpen(false);
    if (window.MSNStorefront) window.MSNStorefront.trapFocus(panel, event);
  });
})();
