(function () {
  var form = document.querySelector("[data-msn-order-review-form]");
  if (!(form instanceof HTMLFormElement)) return;

  var status = form.querySelector("[data-msn-order-review-status]");
  var phone = "551134393836";

  form.addEventListener("submit", function (event) {
    event.preventDefault();
    var data = new FormData(form);

    if (String(data.get("empresa") || "").trim()) {
      return;
    }

    var nome = String(data.get("nome") || "").trim();
    var pedido = String(data.get("pedido") || "").trim();
    var contato = String(data.get("contato") || "").trim();
    var nota = String(data.get("nota") || "").trim();
    var tema = String(data.get("tema") || "").trim();
    var mensagem = String(data.get("mensagem") || "").trim();

    if (!nome || !pedido || !contato || !nota || !tema || !mensagem) {
      if (status) status.textContent = "Preencha nome, pedido, contato, nota, tema e comentario.";
      return;
    }

    var text = [
      "Ola! Quero avaliar meu pedido da MSN Distribuidora.",
      "Nome: " + nome,
      "Pedido: " + pedido,
      "Contato: " + contato,
      "Nota: " + nota,
      "Tema: " + tema,
      "Comentario: " + mensagem
    ].join("\n");

    window.open("https://wa.me/" + phone + "?text=" + encodeURIComponent(text), "_blank", "noopener,noreferrer");
    if (status) status.textContent = "";
  });
})();
