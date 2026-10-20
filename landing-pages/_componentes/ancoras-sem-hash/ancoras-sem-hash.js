/* ancoras-sem-hash: injetado pelo build_umbrella.py em toda LP dos guarda-chuvas.
   Fonte: landing-pages/_componentes/ancoras-sem-hash/ (nao editar a copia no deploy).
   Botao com href="#inscricao" (ou #form, #agendar, skip-link...) continua rolando ate a
   secao, mas o #secao nao fica na URL: ele vazava pro url_conversao do CRM, pro ?lp= do
   redirect pos-form e pro link copiado da barra (UTM colada depois do # se perde). */
(function () {
  var h = window.history;
  if (!h || !h.pushState || !h.replaceState || window.__ancorasSemHash) return;
  window.__ancorasSemHash = true;
  var push = h.pushState, replace = h.replaceState;

  function semHash(url) {
    try {
      var s = String(url);
      if (s.indexOf('#') < 0) return url;
      var u = new URL(s, location.href);
      return u.origin === location.origin ? u.pathname + u.search : url;
    } catch (err) { return url; }
  }

  function limpar() {
    if (location.href.indexOf('#') > -1) {
      replace.call(h, h.state, '', location.pathname + location.search);
    }
  }

  // JS que grava hash por conta propria (ex: webflow.js faz pushState('#secao')).
  h.pushState = function (state, title, url) {
    return arguments.length > 2 ? push.call(h, state, title, semHash(url)) : push.apply(h, arguments);
  };
  h.replaceState = function (state, title, url) {
    return arguments.length > 2 ? replace.call(h, state, title, semHash(url)) : replace.apply(h, arguments);
  };

  // Ancora nativa: location.replace rola, move o foco e dispara hashchange como o clique
  // faria, sem empilhar entrada no historico. Handler proprio da LP que ja deu
  // preventDefault manda (roda antes: este listener fica na window).
  window.addEventListener('click', function (e) {
    if (e.defaultPrevented || e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
    var a = e.target && e.target.closest ? e.target.closest('a[href]') : null;
    if (!a || (a.target && a.target !== '_self') || a.hasAttribute('download')) return;
    var href = a.getAttribute('href');
    if (href.charAt(0) !== '#') return;
    e.preventDefault();
    location.replace(href);
  });

  // Listeners de hashchange da propria LP (ex: abrir <details>) leem o hash antes: os
  // scripts da pagina vem antes deste no HTML.
  window.addEventListener('hashchange', limpar);

  // Link de fora com #secao: deixa o browser rolar no carregamento e limpa depois.
  if (document.readyState === 'complete') setTimeout(limpar, 0);
  else window.addEventListener('load', function () { setTimeout(limpar, 0); });
})();
