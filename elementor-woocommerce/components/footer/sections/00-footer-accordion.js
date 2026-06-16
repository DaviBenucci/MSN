(function () {
  function initFooterAccordions() {
    var triggers = Array.prototype.slice.call(document.querySelectorAll(".msn-footer [data-msn-accordion-trigger]"));
    if (!triggers.length) return;

    function isMobileFooter() {
      return window.matchMedia("(max-width: 768px)").matches;
    }

    function setPanelState(trigger, isOpen) {
      var panel = document.getElementById(trigger.getAttribute("aria-controls"));
      trigger.setAttribute("aria-expanded", String(isOpen));
      if (panel) panel.hidden = !isOpen;
    }

    function syncFooterAccordions() {
      var isMobile = isMobileFooter();

      triggers.forEach(function (trigger, index) {
        setPanelState(trigger, isMobile ? index === 0 : true);
      });
    }

    triggers.forEach(function (trigger) {
      trigger.addEventListener("click", function () {
        if (!isMobileFooter()) return;
        setPanelState(trigger, trigger.getAttribute("aria-expanded") !== "true");
      });
    });

    syncFooterAccordions();
    window.addEventListener("resize", syncFooterAccordions);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initFooterAccordions);
  } else {
    initFooterAccordions();
  }
})();
