/* ---------------------------------------------------------------------------
   JavaScript base do minicurso.
   Este arquivo é carregado em todas as telas (ver templates/base.html).
   --------------------------------------------------------------------------- */

document.addEventListener("DOMContentLoaded", function () {
  // Confirma, de forma visível, que o JS estático está sendo servido pelo Django.
  const status = document.getElementById("status");

  if (status) {
    status.textContent = status.dataset.status;
  }

  console.log("[minicurso] Ambiente base carregado: Django + HTML + CSS + JS.");
});
