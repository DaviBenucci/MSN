(function () {
  var stickyBar = document.querySelector("[data-msn-product-sticky]");
  var addToCart = document.querySelector(".single_add_to_cart_button");

  if (!stickyBar || !addToCart) return;

  function syncBar() {
    var rect = addToCart.getBoundingClientRect();
    var shouldShow = rect.bottom < 0 || window.innerHeight < rect.top;
    stickyBar.classList.toggle("is-visible", shouldShow);
  }

  window.addEventListener("scroll", syncBar, { passive: true });
  window.addEventListener("resize", syncBar);
  syncBar();
})();
