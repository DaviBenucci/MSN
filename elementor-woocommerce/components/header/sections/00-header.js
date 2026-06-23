(function () {
  function getHeader() {
    return document.querySelector("[data-msn-header], .msn-header");
  }

  function setCompact() {
    var header = getHeader();
    if (!header) return;
    header.classList.toggle("is-compact", window.scrollY > 12);
  }

  function init() {
    setCompact();
  }

  window.addEventListener("scroll", setCompact, { passive: true });

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }

  if (window.MutationObserver) {
    new MutationObserver(setCompact).observe(document.documentElement, { childList: true, subtree: true });
  }
})();
