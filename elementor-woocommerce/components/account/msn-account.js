(function () {
  Array.prototype.forEach.call(document.querySelectorAll(".woocommerce-account .woocommerce-MyAccount-navigation a"), function (link) {
    if (link.getAttribute("aria-current")) return;
    if (link.parentElement && link.parentElement.classList.contains("is-active")) {
      link.setAttribute("aria-current", "page");
    }
  });
})();
