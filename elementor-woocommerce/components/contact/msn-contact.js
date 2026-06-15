(function () {
  var form = document.querySelector("[data-msn-contact-form]");
  if (!(form instanceof HTMLFormElement)) return;

  var status = form.querySelector("[data-msn-contact-status]");
  var phone = "551134393836";

  form.addEventListener("submit", function (event) {
    event.preventDefault();
    var data = new FormData(form);

    if (String(data.get("empresa") || "").trim()) {
      return;
    }

    var nome = String(data.get("nome") || "").trim();
    var telefone = String(data.get("telefone") || "").trim();
    var email = String(data.get("email") || "").trim();
    var motivo = String(data.get("motivo") || "").trim();
    var mensagem = String(data.get("mensagem") || "").trim();

    if (!nome || !telefone || !motivo || !mensagem) {
      if (status) status.textContent = "Preencha nome, telefone, motivo e mensagem.";
      return;
    }

    var text = [
      "Ola! Quero atendimento pela loja MSN Distribuidora.",
      "Nome: " + nome,
      "Telefone: " + telefone,
      email ? "E-mail: " + email : "",
      "Motivo: " + motivo,
      "Mensagem: " + mensagem
    ].filter(Boolean).join("\n");

    window.open("https://wa.me/" + phone + "?text=" + encodeURIComponent(text), "_blank", "noopener,noreferrer");
    if (status) status.textContent = "";
  });
})();
