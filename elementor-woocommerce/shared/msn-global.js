(function () {
  var focusableSelector = [
    "a[href]",
    "button:not([disabled])",
    "input:not([disabled])",
    "select:not([disabled])",
    "textarea:not([disabled])",
    '[tabindex]:not([tabindex="-1"])'
  ].join(",");

  function lockScroll(locked) {
    document.body.classList.toggle("msn-lock-scroll", locked);
  }

  function trapFocus(container, event) {
    if (event.key !== "Tab") return;
    var focusable = Array.prototype.slice.call(container.querySelectorAll(focusableSelector));
    if (!focusable.length) return;
    var first = focusable[0];
    var last = focusable[focusable.length - 1];

    if (event.shiftKey && document.activeElement === first) {
      event.preventDefault();
      last.focus();
    }

    if (!event.shiftKey && document.activeElement === last) {
      event.preventDefault();
      first.focus();
    }
  }

  window.MSNStorefront = {
    focusableSelector: focusableSelector,
    lockScroll: lockScroll,
    trapFocus: trapFocus
  };

  Array.prototype.forEach.call(document.querySelectorAll("[data-msn-accordion]"), function (group) {
    Array.prototype.forEach.call(group.querySelectorAll("[data-msn-accordion-trigger]"), function (trigger) {
      trigger.addEventListener("click", function () {
        var panel = document.getElementById(trigger.getAttribute("aria-controls"));
        var isOpen = trigger.getAttribute("aria-expanded") === "true";
        trigger.setAttribute("aria-expanded", String(!isOpen));
        if (panel) panel.hidden = isOpen;
      });
    });
  });
})();
