/* nav.js — barra de navegacao compartilhada do guarda-chuva de dashboards.
 * GERADO por dashboards-umbrella/build_umbrella.py a partir do manifest.json.
 * Nao editar na sibling: editar templates/nav.js.tpl e rebuildar.
 *
 * Autocontido de proposito: as 4 dashboards tem CSS proprio (uma inline, tres
 * com estilo.css) e nao compartilham design system. Tudo aqui e prefixado
 * `dnav-` pra nao colidir com .top/.picker/.container das paginas.
 */
(function () {
  'use strict';

  var DASHBOARDS = __DASHBOARDS_JSON__;
  var BAR_H = 52;

  /* Slug da pagina atual pelo primeiro segmento do path. Raiz = hub. */
  function slugAtual() {
    var seg = window.location.pathname.split('/').filter(Boolean)[0] || '';
    for (var i = 0; i < DASHBOARDS.length; i++) {
      if (DASHBOARDS[i].slug === seg) return seg;
    }
    return '';
  }

  var CSS = [
    '.dnav{position:fixed;top:0;left:0;right:0;z-index:900;height:' + BAR_H + 'px;',
    'background:rgba(255,255,255,.92);backdrop-filter:saturate(180%) blur(12px);',
    '-webkit-backdrop-filter:saturate(180%) blur(12px);border-bottom:1px solid #E5E7EB;',
    "font-family:'Inter',-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;}",
    '.dnav *{box-sizing:border-box;}',
    '.dnav__in{max-width:1320px;margin:0 auto;height:100%;padding:0 20px;',
    'display:flex;align-items:center;gap:20px;}',
    '.dnav__home{display:inline-flex;align-items:center;gap:8px;flex:none;',
    'font-size:13px;font-weight:700;letter-spacing:-.01em;color:#0F172A;text-decoration:none;',
    'white-space:nowrap;border-radius:8px;padding:6px 8px;margin-left:-8px;}',
    '.dnav__home:hover{background:#F1F5F9;}',
    '.dnav__mark{width:18px;height:18px;flex:none;border-radius:5px;background:#0F172A;',
    'display:grid;grid-template-columns:1fr 1fr;grid-template-rows:1fr 1fr;gap:2px;padding:3px;}',
    '.dnav__mark i{background:#fff;border-radius:1px;opacity:.55;}',
    '.dnav__mark i:first-child{opacity:1;}',
    '.dnav__links{display:flex;align-items:center;gap:4px;overflow-x:auto;',
    'scrollbar-width:none;-ms-overflow-style:none;}',
    '.dnav__links::-webkit-scrollbar{display:none;}',
    '.dnav__pill{flex:none;font-size:13px;font-weight:600;line-height:1;color:#475569;',
    'text-decoration:none;padding:8px 12px;border-radius:8px;white-space:nowrap;',
    'transition:background .12s ease,color .12s ease;}',
    '.dnav__pill:hover{background:#F1F5F9;color:#0F172A;}',
    '.dnav__pill[aria-current="page"]{background:#0F172A;color:#fff;}',
    '.dnav__pill:focus-visible,.dnav__home:focus-visible,.dnav__sel:focus-visible',
    '{outline:2px solid #0B63FF;outline-offset:2px;}',
    '.dnav__sel{display:none;flex:1;min-width:0;font:inherit;font-size:13px;font-weight:600;',
    'color:#0F172A;background:#fff;border:1px solid #E5E7EB;border-radius:8px;padding:8px 10px;}',
    '@media (max-width:720px){',
    '.dnav__in{gap:12px;padding:0 14px;}',
    '.dnav__links{display:none;}',
    '.dnav__sel{display:block;}',
    '.dnav__label{display:none;}',
    '}',
    '@media print{.dnav{display:none;}}'
  ].join('');

  function montar() {
    if (document.querySelector('.dnav')) return;
    var atual = slugAtual();

    var style = document.createElement('style');
    style.setAttribute('data-dnav', '');
    style.textContent = CSS;
    document.head.appendChild(style);

    var bar = document.createElement('div');
    bar.className = 'dnav';

    var inner = document.createElement('div');
    inner.className = 'dnav__in';
    bar.appendChild(inner);

    var home = document.createElement('a');
    home.className = 'dnav__home';
    home.href = '/';
    home.innerHTML = '<span class="dnav__mark"><i></i><i></i><i></i><i></i></span>';
    var homeTxt = document.createElement('span');
    homeTxt.className = 'dnav__label';
    homeTxt.textContent = 'Dashboards';
    home.appendChild(homeTxt);
    inner.appendChild(home);

    var links = document.createElement('nav');
    links.className = 'dnav__links';
    links.setAttribute('aria-label', 'Dashboards');

    var sel = document.createElement('select');
    sel.className = 'dnav__sel';
    sel.setAttribute('aria-label', 'Trocar de dashboard');

    DASHBOARDS.forEach(function (d) {
      var href = '/' + d.slug + '/';

      var a = document.createElement('a');
      a.className = 'dnav__pill';
      a.href = href;
      a.textContent = d.curto;
      a.title = d.nome;
      if (d.slug === atual) a.setAttribute('aria-current', 'page');
      links.appendChild(a);

      var o = document.createElement('option');
      o.value = href;
      o.textContent = d.nome;
      if (d.slug === atual) o.selected = true;
      sel.appendChild(o);
    });

    if (!atual) {
      var o0 = document.createElement('option');
      o0.value = '/';
      o0.textContent = 'Escolher dashboard...';
      o0.selected = true;
      sel.insertBefore(o0, sel.firstChild);
    }

    sel.addEventListener('change', function () {
      if (sel.value && sel.value !== window.location.pathname) window.location.href = sel.value;
    });

    inner.appendChild(links);
    inner.appendChild(sel);
    document.body.insertBefore(bar, document.body.firstChild);

    /* As paginas tem padding proprio no body (28px desktop / 20px mobile) e
     * `html{overflow-x:hidden}`, que quebraria position:sticky. Dai a barra ser
     * fixed: some o padding-top original e reservamos a altura da barra. */
    var pad = parseFloat(getComputedStyle(document.body).paddingTop) || 0;
    document.body.style.paddingTop = (BAR_H + Math.min(pad, 20)) + 'px';
    document.documentElement.style.scrollPaddingTop = BAR_H + 'px';

    /* Pill ativa visivel quando a barra rola horizontalmente no mobile. */
    var ativa = links.querySelector('[aria-current="page"]');
    if (ativa && links.scrollWidth > links.clientWidth) {
      links.scrollLeft = ativa.offsetLeft - 12;
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', montar);
  } else {
    montar();
  }
})();
