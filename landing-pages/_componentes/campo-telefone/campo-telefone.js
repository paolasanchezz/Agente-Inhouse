/* campo-telefone v1 — fonte: landing-pages/_componentes/campo-telefone/ (README la).
   Nao edite a copia dentro da LP: edite aqui e rode sincronizar.py.

   Campo de telefone com seletor de pais por bandeira. O visitante escolhe o pais, o prefixo
   "+DDI" aparece na frente do numero e CampoTelefone.ler(form) devolve o numero completo so
   com digitos (DDI + numero, sem "+"), que e o formato gravado no ClickMeeting (campo 11).

   Bandeiras em SVG embutido (data URI): o Windows nao desenha emoji de bandeira (mostra "BR"),
   e o CSP dos guarda-chuvas aceita img-src data:. Desenho simplificado, feito pra 20x14 px. */
(function () {
  'use strict';

  function svg(body) {
    return 'data:image/svg+xml,' + encodeURIComponent(
      '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 30 20">' + body + '</svg>');
  }
  function h3(a, b, c) { // tres faixas horizontais
    return '<rect width="30" height="20" fill="' + b + '"/><rect width="30" height="6.67" fill="' + a +
      '"/><rect y="13.33" width="30" height="6.67" fill="' + c + '"/>';
  }
  function v3(a, b, c) { // tres faixas verticais
    return '<rect width="30" height="20" fill="' + b + '"/><rect width="10" height="20" fill="' + a +
      '"/><rect x="20" width="10" height="20" fill="' + c + '"/>';
  }
  function dot(cx, cy, r, fill) {
    return '<circle cx="' + cx + '" cy="' + cy + '" r="' + r + '" fill="' + fill + '"/>';
  }
  var STAR = 'M0,-1L.24,-.31L.95,-.31L.38,.12L.59,.81L0,.4L-.59,.81L-.38,.12L-.95,-.31L-.24,-.31Z';
  function star(cx, cy, s, fill) {
    return '<path d="' + STAR + '" fill="' + fill + '" transform="translate(' + cx + ' ' + cy + ') scale(' + s + ')"/>';
  }

  var FLAGS = {
    BR: svg('<rect width="30" height="20" fill="#009c3b"/><path d="M15 2.2L27.6 10L15 17.8L2.4 10Z" fill="#ffdf00"/>' + dot(15, 10, 4.6, '#002776')),
    PT: svg('<rect width="30" height="20" fill="#ff0000"/><rect width="12" height="20" fill="#006600"/>' + dot(12, 10, 4.4, '#ffcc00') + dot(12, 10, 2.6, '#ff0000') + dot(12, 10, 1.4, '#ffffff')),
    MX: svg(v3('#006847', '#ffffff', '#ce1126') + dot(15, 10, 2.6, '#8c5a2b')),
    AR: svg(h3('#74acdf', '#ffffff', '#74acdf') + dot(15, 10, 2.2, '#f6b40e')),
    CO: svg('<rect width="30" height="20" fill="#ce1126"/><rect width="30" height="10" fill="#fcd116"/><rect y="10" width="30" height="5" fill="#003893"/>'),
    CL: svg('<rect width="30" height="20" fill="#d52b1e"/><rect width="30" height="10" fill="#ffffff"/><rect width="10" height="10" fill="#0039a6"/>' + star(5, 5, 2.6, '#ffffff')),
    PE: svg(v3('#d91023', '#ffffff', '#d91023')),
    EC: svg('<rect width="30" height="20" fill="#ed1c24"/><rect width="30" height="10" fill="#ffdd00"/><rect y="10" width="30" height="5" fill="#034ea2"/>' + dot(15, 10, 2.6, '#8b6b3d')),
    UY: svg('<rect width="30" height="20" fill="#ffffff"/><rect y="2.22" width="30" height="2.22" fill="#0038a8"/><rect y="6.67" width="30" height="2.22" fill="#0038a8"/><rect y="11.11" width="30" height="2.22" fill="#0038a8"/><rect y="15.56" width="30" height="2.22" fill="#0038a8"/><rect width="11" height="11.11" fill="#ffffff"/>' + dot(5.5, 5.5, 3, '#fcd116')),
    PY: svg(h3('#d52b1e', '#ffffff', '#0038a8') + dot(15, 10, 2.2, '#f5c400')),
    BO: svg(h3('#d52b1e', '#f9e300', '#007934')),
    VE: svg(h3('#ffcc00', '#00247d', '#cf142b') + dot(10.5, 11.2, .7, '#fff') + dot(12.6, 9.6, .7, '#fff') + dot(15, 9, .7, '#fff') + dot(17.4, 9.6, .7, '#fff') + dot(19.5, 11.2, .7, '#fff')),
    CR: svg('<rect width="30" height="20" fill="#002b7f"/><rect y="3.33" width="30" height="13.33" fill="#ffffff"/><rect y="6.67" width="30" height="6.67" fill="#ce1126"/>'),
    PA: svg('<rect width="30" height="20" fill="#ffffff"/><rect x="15" width="15" height="10" fill="#d21034"/><rect y="10" width="15" height="10" fill="#005293"/>' + star(7.5, 5, 2.6, '#005293') + star(22.5, 15, 2.6, '#d21034')),
    GT: svg(v3('#4997d0', '#ffffff', '#4997d0') + dot(15, 10, 2.4, '#6c9a3c')),
    SV: svg(h3('#0047ab', '#ffffff', '#0047ab') + dot(15, 10, 2.2, '#e0b000')),
    HN: svg(h3('#0073cf', '#ffffff', '#0073cf') + star(15, 10, 1.2, '#0073cf') + star(11, 8.4, 1.1, '#0073cf') + star(19, 8.4, 1.1, '#0073cf') + star(11, 11.6, 1.1, '#0073cf') + star(19, 11.6, 1.1, '#0073cf')),
    NI: svg(h3('#0067c6', '#ffffff', '#0067c6') + '<path d="M15 7.6L17.4 11.8H12.6Z" fill="#2e8b57"/>'),
    DO: svg('<rect width="30" height="20" fill="#ffffff"/><rect width="13" height="8.5" fill="#002d62"/><rect x="17" width="13" height="8.5" fill="#ce1126"/><rect y="11.5" width="13" height="8.5" fill="#ce1126"/><rect x="17" y="11.5" width="13" height="8.5" fill="#002d62"/>'),
    ES: svg('<rect width="30" height="20" fill="#aa151b"/><rect y="5" width="30" height="10" fill="#f1bf00"/>'),
    US: svg('<rect width="30" height="20" fill="#ffffff"/><path d="M0 0H30V1.54H0ZM0 3.08H30V4.62H0ZM0 6.15H30V7.69H0ZM0 9.23H30V10.77H0ZM0 12.31H30V13.85H0ZM0 15.38H30V16.92H0ZM0 18.46H30V20H0Z" fill="#b22234"/><rect width="12" height="10.77" fill="#3c3b6e"/>'),
    XX: svg('<rect width="30" height="20" rx="2" fill="#e6e6ec"/><g fill="none" stroke="#6b6b76" stroke-width="1.2"><circle cx="15" cy="10" r="6.5"/><ellipse cx="15" cy="10" rx="2.8" ry="6.5"/><path d="M8.5 10H21.5"/></g>')
  };

  // Ordem importa so pro DDI repetido: +1 colado cai em Estados Unidos (vem antes).
  // min/max = quantidade de digitos do numero nacional (sem DDI e sem o 0 de tronco).
  // Faixa generosa de proposito: o objetivo e barrar erro de digitacao, nao validar operadora.
  var COUNTRIES = [
    { iso: 'BR', dial: '55', min: 10, max: 11, pt: 'Brasil', es: 'Brasil', ex: '11 91234-5678' },
    { iso: 'PT', dial: '351', min: 9, max: 9, pt: 'Portugal', es: 'Portugal', ex: '912 345 678' },
    { iso: 'MX', dial: '52', min: 10, max: 10, pt: 'México', es: 'México', ex: '55 1234 5678' },
    { iso: 'AR', dial: '54', min: 10, max: 11, pt: 'Argentina', es: 'Argentina', ex: '9 11 2345-6789' },
    { iso: 'CO', dial: '57', min: 10, max: 10, pt: 'Colômbia', es: 'Colombia', ex: '321 1234567' },
    { iso: 'CL', dial: '56', min: 9, max: 9, pt: 'Chile', es: 'Chile', ex: '9 1234 5678' },
    { iso: 'PE', dial: '51', min: 8, max: 9, pt: 'Peru', es: 'Perú', ex: '912 345 678' },
    { iso: 'EC', dial: '593', min: 8, max: 9, pt: 'Equador', es: 'Ecuador', ex: '99 123 4567' },
    { iso: 'UY', dial: '598', min: 8, max: 8, pt: 'Uruguai', es: 'Uruguay', ex: '94 123 456' },
    { iso: 'PY', dial: '595', min: 8, max: 9, pt: 'Paraguai', es: 'Paraguay', ex: '981 123456' },
    { iso: 'BO', dial: '591', min: 8, max: 8, pt: 'Bolívia', es: 'Bolivia', ex: '7123 4567' },
    { iso: 'VE', dial: '58', min: 10, max: 10, pt: 'Venezuela', es: 'Venezuela', ex: '412 1234567' },
    { iso: 'CR', dial: '506', min: 8, max: 8, pt: 'Costa Rica', es: 'Costa Rica', ex: '8312 3456' },
    { iso: 'PA', dial: '507', min: 7, max: 8, pt: 'Panamá', es: 'Panamá', ex: '6123 4567' },
    { iso: 'GT', dial: '502', min: 8, max: 8, pt: 'Guatemala', es: 'Guatemala', ex: '5123 4567' },
    { iso: 'SV', dial: '503', min: 8, max: 8, pt: 'El Salvador', es: 'El Salvador', ex: '7012 3456' },
    { iso: 'HN', dial: '504', min: 8, max: 8, pt: 'Honduras', es: 'Honduras', ex: '9123 4567' },
    { iso: 'NI', dial: '505', min: 8, max: 8, pt: 'Nicarágua', es: 'Nicaragua', ex: '8123 4567' },
    { iso: 'ES', dial: '34', min: 9, max: 9, pt: 'Espanha', es: 'España', ex: '612 34 56 78' },
    { iso: 'US', dial: '1', min: 10, max: 10, pt: 'Estados Unidos', es: 'Estados Unidos', ex: '201 555 0123' },
    { iso: 'DO', dial: '1', min: 10, max: 10, pt: 'República Dominicana', es: 'República Dominicana', ex: '809 234 5678' }
  ];

  var TEXT = {
    'pt-BR': {
      other: 'Outro país', otherPh: 'Código do país + número', country: 'País do telefone',
      invalid: 'Telefone inválido. Confira o número.', invalidBR: 'Telefone inválido. Confira o DDD e o número.', invalidOther: 'Telefone inválido. Digite o código do país e o número.'
    },
    'pt-PT': {
      other: 'Outro país', otherPh: 'Indicativo do país + número', country: 'País do telefone',
      invalid: 'Número de telefone inválido. Confirme o número.', invalidOther: 'Número de telefone inválido. Indique o indicativo do país e o número.'
    },
    es: {
      other: 'Otro país', otherPh: 'Código de país + número', country: 'País del teléfono',
      invalid: 'Teléfono inválido. Revisa el número.', invalidOther: 'Teléfono inválido. Escribe el código de país y el número.'
    }
  };

  var CHEVRON = '<svg class="pf-chev" viewBox="0 0 10 6" width="10" height="6" aria-hidden="true"><path d="M1 1l4 4 4-4" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>';

  function langOf(root) {
    var l = (root.getAttribute('data-idioma') || document.documentElement.lang || 'pt-BR');
    if (/^pt-PT/i.test(l)) return 'pt-PT';
    if (/^es/i.test(l)) return 'es';
    return 'pt-BR';
  }

  function byIso(iso) {
    for (var i = 0; i < COUNTRIES.length; i++) if (COUNTRIES[i].iso === iso) return COUNTRIES[i];
    return null;
  }

  // Pais inicial = o da LP (data-pais). So nas LPs em espanhol o navegador pode trocar, e so se
  // ele estiver em espanhol: es-CO vira Colombia. Nas LPs em portugues o pais da LP manda,
  // porque navegador pt-BR nao quer dizer numero brasileiro (brasileiro morando em Portugal).
  function initialCountry(root, lang) {
    var fallback = byIso(root.getAttribute('data-pais') || '') ||
      byIso(lang === 'pt-PT' ? 'PT' : lang === 'es' ? 'MX' : 'BR');
    if (lang !== 'es') return fallback;
    var langs = navigator.languages || [navigator.language || ''];
    for (var i = 0; i < langs.length; i++) {
      var m = /^([a-z]{2})-([A-Z]{2})$/i.exec(langs[i] || '');
      if (m && m[1].toLowerCase() === 'es') {
        var c = byIso(m[2].toUpperCase());
        if (c) return c;
      }
    }
    return fallback;
  }

  // DDI mais longo que casa com o inicio dos digitos (+1 fica com o pais atual se ele for +1).
  function matchDial(digits, current) {
    if (current && current.dial !== '' && digits.indexOf(current.dial) === 0) return current;
    var best = null;
    for (var i = 0; i < COUNTRIES.length; i++) {
      var c = COUNTRIES[i];
      if (digits.indexOf(c.dial) === 0 && (!best || c.dial.length > best.dial.length)) best = c;
    }
    return best;
  }

  var uid = 0;

  function init(root) {
    if (!root || root.__campoTelefone) return root && root.__campoTelefone;
    var lang = langOf(root);
    var t = TEXT[lang];
    var nameKey = lang === 'es' ? 'es' : 'pt';
    var input = root.querySelector('input[type="tel"]');
    var box = root.querySelector('.pf-box');
    if (!input || !box) return null;
    uid += 1;

    var other = { iso: 'XX', dial: '', min: 8, max: 15, pt: t.other, es: t.other, ex: t.otherPh };
    var list = COUNTRIES.slice().sort(function (a, b) { return a[nameKey].localeCompare(b[nameKey], lang); });
    var current = initialCountry(root, lang);
    // pais inicial no topo, depois alfabetico, "Outro pais" no fim
    list = [current].concat(list.filter(function (c) { return c !== current; })).concat([other]);

    var btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'pf-btn';
    btn.setAttribute('aria-haspopup', 'listbox');
    btn.setAttribute('aria-expanded', 'false');
    btn.innerHTML = '<img class="pf-flag" alt="" width="20" height="14"><span class="pf-dial"></span>' + CHEVRON;

    var ul = document.createElement('ul');
    ul.className = 'pf-list';
    ul.id = 'pfList' + uid;
    ul.setAttribute('role', 'listbox');
    ul.setAttribute('tabindex', '-1');
    ul.setAttribute('aria-label', t.country);
    ul.hidden = true;
    btn.setAttribute('aria-controls', ul.id);

    list.forEach(function (c, i) {
      var li = document.createElement('li');
      li.id = ul.id + '-' + i;
      li.setAttribute('role', 'option');
      li.dataset.iso = c.iso;
      li.innerHTML = '<img class="pf-flag" alt="" width="20" height="14" src="' + FLAGS[c.iso] + '">' +
        '<span class="pf-li-name"></span><span class="pf-li-dial">' + (c.dial ? '+' + c.dial : '') + '</span>';
      li.querySelector('.pf-li-name').textContent = c[nameKey];
      li.addEventListener('mousedown', function (e) { e.preventDefault(); });
      li.addEventListener('click', function () { choose(c, true); });
      ul.appendChild(li);
    });

    box.insertBefore(btn, input);
    box.appendChild(ul);

    var active = 0;

    function paint() {
      btn.querySelector('.pf-flag').src = FLAGS[current.iso];
      btn.querySelector('.pf-dial').textContent = '+' + current.dial;
      btn.setAttribute('aria-label', t.country + ': ' + current[nameKey] + (current.dial ? ' (+' + current.dial + ')' : ''));
      input.placeholder = current.ex;
      Array.prototype.forEach.call(ul.children, function (li) {
        li.setAttribute('aria-selected', li.dataset.iso === current.iso ? 'true' : 'false');
      });
      // o prefixo fica por cima do input: o recuo acompanha a largura real do botao
      input.style.paddingLeft = (btn.offsetWidth + 10) + 'px';
    }

    function setActive(i) {
      var items = ul.children;
      if (!items.length) return;
      active = (i + items.length) % items.length;
      Array.prototype.forEach.call(items, function (li, j) { li.classList.toggle('is-active', j === active); });
      ul.setAttribute('aria-activedescendant', items[active].id);
      var li = items[active];
      if (li.offsetTop < ul.scrollTop) ul.scrollTop = li.offsetTop;
      else if (li.offsetTop + li.offsetHeight > ul.scrollTop + ul.clientHeight) ul.scrollTop = li.offsetTop + li.offsetHeight - ul.clientHeight;
    }

    function open() {
      ul.hidden = false;
      btn.setAttribute('aria-expanded', 'true');
      root.classList.add('pf-open');
      var idx = 0;
      Array.prototype.forEach.call(ul.children, function (li, j) { if (li.dataset.iso === current.iso) idx = j; });
      setActive(idx);
      ul.focus({ preventScroll: true });
    }

    function close(focusBtn) {
      if (ul.hidden) return;
      ul.hidden = true;
      btn.setAttribute('aria-expanded', 'false');
      root.classList.remove('pf-open');
      if (focusBtn) btn.focus();
    }

    function choose(c, focusInput) {
      current = c;
      paint();
      close(false);
      input.removeAttribute('aria-invalid');
      if (focusInput) input.focus();
    }

    btn.addEventListener('click', function () { if (ul.hidden) open(); else close(true); });
    btn.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowDown' || e.key === 'ArrowUp') { e.preventDefault(); open(); }
    });

    var typed = '', typedAt = 0;
    ul.addEventListener('keydown', function (e) {
      var n = ul.children.length;
      if (e.key === 'ArrowDown') { e.preventDefault(); setActive(active + 1); }
      else if (e.key === 'ArrowUp') { e.preventDefault(); setActive(active - 1); }
      else if (e.key === 'Home') { e.preventDefault(); setActive(0); }
      else if (e.key === 'End') { e.preventDefault(); setActive(n - 1); }
      else if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); choose(list[active], true); }
      else if (e.key === 'Escape') { e.preventDefault(); close(true); }
      else if (e.key === 'Tab') { close(false); }
      else if (e.key.length === 1 && /\S/.test(e.key)) {
        var now = Date.now();
        typed = (now - typedAt > 700 ? '' : typed) + e.key.toLowerCase();
        typedAt = now;
        for (var i = 0; i < n; i++) {
          var j = (active + (typed.length === 1 ? 1 : 0) + i) % n;
          var name = list[j][nameKey].toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '');
          if (name.indexOf(typed) === 0) { setActive(j); break; }
        }
      }
    });
    ul.addEventListener('blur', function () { setTimeout(function () { if (!root.contains(document.activeElement)) close(false); }, 0); });
    document.addEventListener('click', function (e) { if (!root.contains(e.target)) close(false); });

    // Colou "+52 55 1234 5678" (ou 0052...)? Troca o pais e deixa so o numero no campo.
    input.addEventListener('input', function () {
      input.removeAttribute('aria-invalid');
      var raw = input.value;
      var m = /^\s*(\+|00)\s*([\d\s().-]+)$/.exec(raw);
      if (!m) return;
      var digits = m[2].replace(/\D/g, '');
      var c = matchDial(digits, current);
      if (c && digits.length > c.dial.length) {
        if (c !== current) { current = c; paint(); }
        input.value = digits.slice(c.dial.length);
      }
    });

    function read() {
      var digits = input.value.replace(/\D/g, '');
      if (!digits) return { ok: false, empty: true, value: '', message: '' };
      var c = current;
      if (c.iso === 'XX') {
        var ok = digits.length >= 8 && digits.length <= 15;
        return ok ? { ok: true, value: digits } : { ok: false, value: '', message: t.invalidOther };
      }
      // digitou o DDI de novo dentro do numero (5511987654321 com Brasil selecionado)
      if (digits.indexOf(c.dial) === 0 && digits.length > c.max && digits.length - c.dial.length >= c.min) {
        digits = digits.slice(c.dial.length);
      }
      digits = digits.replace(/^0+/, ''); // 0 de tronco (011 9...)
      if (digits.length < c.min || digits.length > c.max) return { ok: false, value: '', message: (c.iso === 'BR' && t.invalidBR) || t.invalid };
      return { ok: true, value: c.dial + digits };
    }

    paint();
    // fonte web pode chegar depois e mudar a largura do prefixo
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(paint);
    window.addEventListener('resize', paint);

    var api = {
      read: read,
      markInvalid: function () { input.setAttribute('aria-invalid', 'true'); input.focus(); }
    };
    root.__campoTelefone = api;
    return api;
  }

  // Le o campo de telefone de um form: { ok, empty, value, message }. value = so digitos, com DDI.
  function ler(form) {
    var root = form.querySelector('[data-campo-telefone]');
    var api = root && init(root);
    if (!api) return { ok: false, empty: true, value: '', message: '' };
    var r = api.read();
    if (!r.ok && !r.empty) api.markInvalid(); // vazio cai na mensagem de campos obrigatorios
    return r;
  }

  function initAll() {
    Array.prototype.forEach.call(document.querySelectorAll('[data-campo-telefone]'), init);
  }

  window.CampoTelefone = { init: init, ler: ler };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', initAll);
  else initAll();
})();
