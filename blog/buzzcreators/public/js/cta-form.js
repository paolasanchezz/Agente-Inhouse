// Handler do formulário mock do blog (newsletter placeholder).
// Fica em /public de propósito: script <script> processado pelo Astro é inlinado
// quando pequeno, e JS inline executável seria bloqueado pela CSP estrita
// (script-src 'self', sem 'unsafe-inline') definida em vercel.json. Servido daqui,
// é um asset do próprio domínio e passa na CSP.
// Ao integrar o CRM (ver comentário no topo de CtaForm.astro), remova este arquivo
// e a tag <script> que o referencia.
document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('cta-form');
  const ok = document.getElementById('cta-ok');
  if (!form) return;
  form.addEventListener('submit', (event) => {
    event.preventDefault();
    form.hidden = true;
    if (ok) ok.hidden = false;
  });
});
