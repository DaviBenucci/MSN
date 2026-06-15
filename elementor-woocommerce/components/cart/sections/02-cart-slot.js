(function () {
  var notices = document.querySelector(".woocommerce-notices-wrapper");
  if (!notices) return;

  var observer = new MutationObserver(function () {
    var message = notices.querySelector(".woocommerce-message, .woocommerce-error, .woocommerce-info");
    if (message instanceof HTMLElement) {
      message.setAttribute("tabindex", "-1");
      message.focus({ preventScroll: false });
    }
  });

  observer.observe(notices, { childList: true, subtree: true });
})();
