(function () {
  function syncFooterAccordions() {
    var isMobile = window.matchMedia("(max-width: 768px)").matches;

    Array.prototype.forEach.call(document.querySelectorAll(".msn-footer [data-msn-accordion-trigger]"), function (trigger) {
      var panel = document.getElementById(trigger.getAttribute("aria-controls"));
      trigger.setAttribute("aria-expanded", String(!isMobile));
      if (panel) panel.hidden = isMobile;
    });
  }

  syncFooterAccordions();
  window.addEventListener("resize", syncFooterAccordions);
})();
