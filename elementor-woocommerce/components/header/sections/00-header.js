(function () {
  var lastFocused = null;

  function getParts() {
    return {
      header: document.querySelector("[data-msn-header], .msn-header"),
      openButton: document.querySelector("[data-msn-menu-open]"),
      closeButton: document.querySelector("[data-msn-menu-close]"),
      panel: document.querySelector("[data-msn-menu-panel]"),
      backdrop: document.querySelector("[data-msn-menu-backdrop]")
    };
  }

  function setCompact() {
    var header = getParts().header;
    if (!header) return;
    header.classList.toggle("is-compact", window.scrollY > 12);
  }

  function setOpen(isOpen) {
    var parts = getParts();
    if (!parts.openButton || !parts.panel || !parts.backdrop) return;

    parts.openButton.setAttribute("aria-expanded", String(isOpen));
    parts.panel.setAttribute("aria-hidden", String(!isOpen));
    parts.panel.classList.toggle("is-open", isOpen);
    parts.backdrop.classList.toggle("is-open", isOpen);
    document.documentElement.classList.toggle("msn-menu-open", isOpen);

    if (window.MSNStorefront) window.MSNStorefront.lockScroll(isOpen);

    if (isOpen) {
      lastFocused = document.activeElement;
      if (parts.closeButton) parts.closeButton.focus();
    } else if (lastFocused instanceof HTMLElement) {
      lastFocused.focus();
    }
  }

  function bindHeader() {
    var parts = getParts();
    if (!parts.openButton || !parts.panel || !parts.backdrop) return false;

    if (!parts.openButton.dataset.msnHeaderBound) {
      parts.openButton.addEventListener("click", function () { setOpen(true); });
      parts.openButton.dataset.msnHeaderBound = "true";
    }

    if (parts.closeButton && !parts.closeButton.dataset.msnHeaderBound) {
      parts.closeButton.addEventListener("click", function () { setOpen(false); });
      parts.closeButton.dataset.msnHeaderBound = "true";
    }

    if (!parts.backdrop.dataset.msnHeaderBound) {
      parts.backdrop.addEventListener("click", function () { setOpen(false); });
      parts.backdrop.dataset.msnHeaderBound = "true";
    }

    Array.prototype.forEach.call(parts.panel.querySelectorAll("a"), function (link) {
      if (link.dataset.msnHeaderBound) return;
      link.addEventListener("click", function () { setOpen(false); });
      link.dataset.msnHeaderBound = "true";
    });

    setCompact();
    return true;
  }

  function init() {
    bindHeader();
  }

  document.addEventListener("keydown", function (event) {
    var panel = getParts().panel;
    if (!panel || panel.getAttribute("aria-hidden") === "true") return;
    if (event.key === "Escape") setOpen(false);
    if (window.MSNStorefront) window.MSNStorefront.trapFocus(panel, event);
  });

  window.addEventListener("scroll", setCompact, { passive: true });

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }

  if (window.MutationObserver) {
    new MutationObserver(function () {
      bindHeader();
    }).observe(document.documentElement, { childList: true, subtree: true });
  }
})();
