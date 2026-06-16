(function () {
  var endpointData = {
    dashboard: { label: "Painel", description: "Resumo da conta" },
    orders: { label: "Pedidos", description: "Historico e status" },
    downloads: { label: "Downloads", description: "Arquivos comprados" },
    "edit-address": { label: "Enderecos", description: "Entrega e cobranca" },
    "payment-methods": { label: "Pagamentos", description: "Metodos salvos" },
    "edit-account": { label: "Dados da conta", description: "Senha e dados pessoais" },
    "customer-logout": { label: "Sair", description: "Encerrar acesso" }
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

    Array.prototype.forEach.call(links, function (link, index) {
      var item = link.closest("li");
      if (item && item.classList.contains("is-active")) {
        link.setAttribute("aria-current", "page");
      }

      if (link.getAttribute("data-msn-account-enhanced") === "true") return;

      var endpoint = getEndpoint(item, link);
      var data = endpointData[endpoint] || {};
      var originalLabel = String(link.textContent || "").replace(/\s+/g, " ").trim();
      var label = data.label || originalLabel || "Conta";
      var description = data.description || "Acessar area da conta";
      var number = String(index + 1).padStart(2, "0");

      link.setAttribute("data-msn-account-enhanced", "true");
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

      var subtitle = document.createElement("span");
      subtitle.className = "msn-account-nav__desc";
      subtitle.textContent = description;

      meta.appendChild(title);
      meta.appendChild(subtitle);
      link.appendChild(icon);
      link.appendChild(meta);
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", enhanceAccountNavigation);
  } else {
    enhanceAccountNavigation();
  }
})();
