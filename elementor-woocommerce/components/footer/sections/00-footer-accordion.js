(function () {
  function initFooterAccordions() {
    var triggers = Array.prototype.slice.call(document.querySelectorAll(".msn-footer [data-msn-accordion-trigger]"));
    if (!triggers.length) return;

    var motionQuery = window.matchMedia("(prefers-reduced-motion: reduce)");

    function isMobileFooter() {
      return window.matchMedia("(max-width: 768px)").matches;
    }

    function stopPanelTimer(panel) {
      if (panel._msnFooterTimer) {
        window.clearTimeout(panel._msnFooterTimer);
        panel._msnFooterTimer = null;
      }

      if (panel._msnFooterFrame) {
        window.cancelAnimationFrame(panel._msnFooterFrame);
        panel._msnFooterFrame = null;
      }
    }

    function finishPanelTransition(panel, isOpen) {
      panel.style.maxHeight = "";
      panel.classList.toggle("is-open", isOpen);
      panel.classList.toggle("is-collapsed", !isOpen);
      panel.hidden = !isOpen;
      stopPanelTimer(panel);
    }

    function setPanelState(trigger, isOpen, shouldAnimate) {
      var panel = document.getElementById(trigger.getAttribute("aria-controls"));
      trigger.setAttribute("aria-expanded", String(isOpen));
      if (!panel) return;

      stopPanelTimer(panel);

      if (!isMobileFooter()) {
        panel.hidden = false;
        panel.style.maxHeight = "";
        panel.classList.remove("is-open", "is-collapsed");
        return;
      }

      if (!shouldAnimate || motionQuery.matches) {
        finishPanelTransition(panel, isOpen);
        return;
      }

      if (isOpen) {
        panel.hidden = false;
        panel.classList.add("is-collapsed");
        panel.classList.remove("is-open");
        panel.style.maxHeight = "0px";

        panel._msnFooterFrame = window.requestAnimationFrame(function () {
          panel._msnFooterFrame = null;
          panel.classList.remove("is-collapsed");
          panel.classList.add("is-open");
          panel.style.maxHeight = panel.scrollHeight + "px";
        });
      } else {
        panel.hidden = false;
        panel.classList.add("is-open");
        panel.classList.remove("is-collapsed");
        panel.style.maxHeight = panel.scrollHeight + "px";

        panel._msnFooterFrame = window.requestAnimationFrame(function () {
          panel._msnFooterFrame = null;
          panel.classList.remove("is-open");
          panel.classList.add("is-collapsed");
          panel.style.maxHeight = "0px";
        });
      }

      panel._msnFooterTimer = window.setTimeout(function () {
        finishPanelTransition(panel, isOpen);
      }, 300);
    }

    function syncFooterAccordions() {
      var isMobile = isMobileFooter();

      triggers.forEach(function (trigger, index) {
        setPanelState(trigger, isMobile ? index === 0 : true, false);
      });
    }

    triggers.forEach(function (trigger) {
      trigger.addEventListener("click", function () {
        if (!isMobileFooter()) return;
        setPanelState(trigger, trigger.getAttribute("aria-expanded") !== "true", true);
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
