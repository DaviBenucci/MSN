(function () {
  var endpointData = {
    dashboard: { label: "Painel", shortLabel: "Painel", description: "Resumo da conta" },
    orders: { label: "Pedidos", shortLabel: "Pedidos", description: "Historico e status" },
    downloads: { label: "Downloads", shortLabel: "Downloads", description: "Arquivos comprados" },
    "edit-address": { label: "Endereços", shortLabel: "Endereços", description: "Entrega e cobrança" },
    "payment-methods": { label: "Pagamentos", shortLabel: "Pagamentos", description: "Métodos salvos" },
    "edit-account": { label: "Dados da conta", shortLabel: "Conta", description: "Senha e dados pessoais" },
    "customer-logout": { label: "Sair", shortLabel: "Sair", description: "Encerrar acesso" }
  };

  var hiddenEndpoints = {
    downloads: true
  };

  function getEndpoint(item, link) {
    var className = item ? item.className : "";
    var match = String(className).match(/woocommerce-MyAccount-navigation-link--([^\s]+)/);
    if (match) return match[1];

    var href = link.getAttribute("href") || "";
    var known = Object.keys(endpointData);
    for (var index = 0; index < known.length; index += 1) {
      if (href.indexOf(known[index]) !== -1) return known[index];
    }

    return "";
  }

  function enhanceAccountNavigation() {
    var links = document.querySelectorAll(
      ".msn-account-woo-slot .woocommerce-MyAccount-navigation a, .woocommerce-account .woocommerce-MyAccount-navigation a"
    );

    var activeData = null;
    var visibleIndex = 0;

    Array.prototype.forEach.call(links, function (link) {
      var item = link.closest("li");
      if (item && item.classList.contains("is-active")) {
        link.setAttribute("aria-current", "page");
      }

      var endpoint = getEndpoint(item, link);
      if (hiddenEndpoints[endpoint]) {
        if (item) {
          item.hidden = true;
          item.classList.add("msn-account-nav__item--hidden");
        }
        return;
      }

      var data = endpointData[endpoint] || {};
      var originalLabel = String(link.textContent || "").replace(/\s+/g, " ").trim();
      var label = data.label || originalLabel || "Conta";
      var shortLabel = data.shortLabel || label;
      var description = data.description || "Acessar area da conta";

      if (!activeData && (link.getAttribute("aria-current") === "page" || (item && item.classList.contains("is-active")))) {
        activeData = { label: label, description: description };
      }

      if (link.getAttribute("data-msn-account-enhanced") === "true") return;

      visibleIndex += 1;

      var number = String(visibleIndex).padStart(2, "0");

      link.setAttribute("data-msn-account-enhanced", "true");
      link.setAttribute("data-msn-account-short-label", shortLabel);
      link.setAttribute("aria-label", label + ": " + description);
      link.textContent = "";

      var icon = document.createElement("span");
      icon.className = "msn-account-nav__icon";
      icon.setAttribute("aria-hidden", "true");
      icon.textContent = number;

      var meta = document.createElement("span");
      meta.className = "msn-account-nav__meta";

      var title = document.createElement("span");
      title.className = "msn-account-nav__label";
      title.textContent = label;

      var mobileTitle = document.createElement("span");
      mobileTitle.className = "msn-account-nav__short";
      mobileTitle.textContent = shortLabel;

      var subtitle = document.createElement("span");
      subtitle.className = "msn-account-nav__desc";
      subtitle.textContent = description;

      meta.appendChild(title);
      meta.appendChild(mobileTitle);
      meta.appendChild(subtitle);
      link.appendChild(icon);
      link.appendChild(meta);
    });

    if (activeData) {
      enhanceAccountMobileSummary(activeData);
    }
  }

  function enhanceAccountMobileSummary(activeData) {
    var account = document.querySelector(".msn-account-woo-slot .woocommerce, .woocommerce-account .msn-account-woo-slot .woocommerce");
    if (!account || account.querySelector(".msn-account-mobile-summary")) return;

    var summary = document.createElement("div");
    summary.className = "msn-account-mobile-summary";

    var eyebrow = document.createElement("span");
    eyebrow.className = "msn-account-mobile-summary__eyebrow";
    eyebrow.textContent = "Minha conta";

    var title = document.createElement("strong");
    title.className = "msn-account-mobile-summary__title";
    title.textContent = activeData.label;

    var description = document.createElement("small");
    description.className = "msn-account-mobile-summary__desc";
    description.textContent = activeData.description;

    summary.appendChild(eyebrow);
    summary.appendChild(title);
    summary.appendChild(description);
    account.insertBefore(summary, account.firstChild);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", enhanceAccountNavigation);
  } else {
    enhanceAccountNavigation();
  }
})();
