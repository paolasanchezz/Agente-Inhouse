// Fluxo do quiosque (totem.html): atrair -> marca -> dados -> analise -> resultado -> encerrar.
// Voltar sozinho ao inicio apos 2 minutos sem toque (teste: totem?idle=8000 usa 8s). Limpa tudo ao encerrar.

(function () {
  'use strict';

  var $ = function (id) { return document.getElementById(id); };
  var params = new URLSearchParams(location.search);
  // Celular: index.html marca o body com .phone antes do script rodar. Sem reinicio por inatividade, links dos posts abertos, autofill ligado.
  var PHONE = document.body.classList.contains('phone');
  var IDLE_MS = Math.max(3000, Number(params.get('idle')) || 120000);
  var AVISO_MS = Math.max(1500, IDLE_MS - 10000);
  var TIMEOUT_ANALISE_MS = 75000;
  var EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  var ETAPAS_MS = 3200;

  var tela = 'attract';
  var estado = novoEstado();
  var timerAviso = null, timerIdle = null, timerEtapas = null, timerToast = null;

  function novoEstado() {
    return { marca: '', segmento: '', instagram: '', concorrentes: [], nome: '', email: '', formTs: 0, leadEnviado: false, leadStatus: null, controller: null, link: '' };
  }

  // --- Navegacao ---

  function mostrar(nome) {
    tela = nome;
    Array.prototype.forEach.call(document.querySelectorAll('.screen'), function (s) { s.classList.toggle('on', s.id === 's-' + nome); });
    document.body.classList.toggle('com-fechar', nome !== 'attract');
    armarIdle();
  }

  // --- Inatividade ---

  function armarIdle() {
    clearTimeout(timerAviso); clearTimeout(timerIdle);
    esconderToast();
    // Na tela de atracao nao ha sessao para encerrar; durante a analise quem manda e o timeout da propria chamada.
    if (PHONE || tela === 'attract' || tela === 'loading') return;
    timerAviso = setTimeout(function () {
      mostrarToast('Regresamos al inicio en ' + Math.round((IDLE_MS - AVISO_MS) / 1000) + ' segundos. Toca la pantalla para continuar.');
    }, AVISO_MS);
    timerIdle = setTimeout(resetarTudo, IDLE_MS);
  }
  ['pointerdown', 'touchstart', 'keydown', 'input'].forEach(function (ev) { document.addEventListener(ev, armarIdle, { passive: true, capture: true }); });
  document.addEventListener('scroll', armarIdle, { passive: true, capture: true });

  function mostrarToast(texto) {
    var t = $('toast');
    t.textContent = texto;
    t.classList.add('on');
  }
  function esconderToast() { $('toast').classList.remove('on'); }

  // --- Encerrar ---

  function resetarTudo() {
    clearTimeout(timerAviso); clearTimeout(timerIdle); clearInterval(timerEtapas);
    if (estado.controller) estado.controller.abort();
    estado = novoEstado();
    Array.prototype.forEach.call(document.querySelectorAll('#app input'), function (i) { i.value = ''; });
    Array.prototype.forEach.call(document.querySelectorAll('.field.erro'), function (f) { f.classList.remove('erro'); });
    $('resBody').innerHTML = '';
    $('fim').innerHTML = '';
    $('resScroll').scrollTop = 0;
    $('loadBox').classList.remove('com-falha');
    esconderToast();
    if (document.activeElement && document.activeElement.blur) document.activeElement.blur();
    mostrar('attract');
  }

  // --- Passo 1: marca e concorrentes ---

  function irParaMarca() {
    mostrar('marca');
    setTimeout(function () { $('marca').focus(); }, 350);
  }

  function marcarErro(idCampo, ligado) { $(idCampo).classList.toggle('erro', ligado); }

  $('f-marca').addEventListener('submit', function (e) {
    e.preventDefault();
    var marca = $('marca').value.trim();
    var segmento = $('segmento').value.trim();
    marcarErro('fld-marca', marca.length < 2);
    marcarErro('fld-segmento', segmento.length < 2);
    if (marca.length < 2) { $('marca').focus(); return; }
    if (segmento.length < 2) { $('segmento').focus(); return; }
    estado.marca = marca;
    estado.segmento = segmento;
    estado.instagram = TotemRender.limparPerfil($('instagram').value);
    estado.concorrentes = ['c1', 'c2', 'c3'].map(function (id) { return $(id).value.trim(); }).filter(function (v) { return v.length >= 2; });
    estado.formTs = Date.now();
    mostrar('lead');
    setTimeout(function () { $('nome').focus(); }, 350);
  });

  // --- Passo 2: dados do lead ---

  $('btnVoltar').addEventListener('click', function () { mostrar('marca'); });

  $('f-lead').addEventListener('submit', function (e) {
    e.preventDefault();
    var nome = $('nome').value.trim();
    var email = $('email').value.trim();
    var okNome = nome.length >= 2, okEmail = EMAIL_RE.test(email);
    marcarErro('fld-nome', !okNome);
    marcarErro('fld-email', !okEmail);
    if (!okNome) { $('nome').focus(); return; }
    if (!okEmail) { $('email').focus(); return; }
    estado.nome = nome;
    estado.email = email;
    iniciarAnalise();
  });

  // --- Analise ---

  function iniciarEtapas() {
    var itens = Array.prototype.slice.call($('etapas').children);
    var i = 0;
    itens.forEach(function (li) { li.className = ''; });
    itens[0].className = 'on';
    clearInterval(timerEtapas);
    timerEtapas = setInterval(function () {
      if (i >= itens.length - 1) return;
      itens[i].className = 'ok';
      i++;
      itens[i].className = 'on';
    }, ETAPAS_MS);
    $('loadAviso').textContent = '';
    setTimeout(function () { if (tela === 'loading') $('loadAviso').textContent = 'Las marcas con mucha conversación tardan un poco más. Ya casi está.'; }, 30000);
  }

  function concluirEtapas() {
    clearInterval(timerEtapas);
    Array.prototype.forEach.call($('etapas').children, function (li) { li.className = 'ok'; });
  }

  function iniciarAnalise() {
    $('loadMarca').textContent = estado.marca;
    $('loadBox').classList.remove('com-falha');
    mostrar('loading');
    iniciarEtapas();
    enviarLead();
    buscarAnalise();
  }

  // O lead sai no mesmo instante e independe do resultado: se a analise falhar, o contato nao se perde.
  function enviarLead() {
    if (estado.leadEnviado) return;
    estado.leadEnviado = true;
    var sessao = estado;
    fetch(TotemRender.base + '/api/totem-lead', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ url_conversao: location.origin + location.pathname + location.search, nome: estado.nome, email: estado.email, marca: estado.marca, segmento: estado.segmento, instagram: estado.instagram, concorrentes: estado.concorrentes, _hp: $('hp').value, _ts: estado.formTs }),
    }).then(function (r) { return r.json(); }).then(function (j) {
      if (estado !== sessao) return; // a sessao ja foi encerrada
      estado.leadStatus = j;
      atualizarStatusEmail();
    }).catch(function () {
      if (estado === sessao) { estado.leadStatus = { ok: false }; atualizarStatusEmail(); }
    });
  }

  function buscarAnalise() {
    var sessao = estado;
    var controller = new AbortController();
    estado.controller = controller;
    var limite = setTimeout(function () { controller.abort(); }, TIMEOUT_ANALISE_MS);
    fetch(TotemRender.apiUrl(estado.marca, estado.concorrentes, estado.segmento, estado.instagram), { signal: controller.signal })
      .then(function (r) { return r.json().then(function (j) { return { ok: r.ok, json: j }; }); })
      .then(function (res) {
        clearTimeout(limite);
        if (estado !== sessao) return;
        if (!res.ok || !res.json || !res.json.ok) throw new Error('analise');
        concluirEtapas();
        setTimeout(function () { if (estado === sessao) mostrarResultado(res.json); }, 700);
      })
      .catch(function () {
        clearTimeout(limite);
        if (estado !== sessao) return; // abortado por encerramento
        clearInterval(timerEtapas);
        $('falhaMsg').textContent = 'La consulta tardó más de lo esperado o Trends no respondió. Tus datos ya quedaron guardados.';
        $('loadBox').classList.add('com-falha');
        armarIdleNaFalha();
      });
  }

  function armarIdleNaFalha() {
    // Na falha ninguem esta olhando a analise: volta a valer o tempo de inatividade.
    clearTimeout(timerIdle);
    if (PHONE) return;
    timerIdle = setTimeout(resetarTudo, IDLE_MS);
  }

  $('btnTentar').addEventListener('click', function () {
    $('loadBox').classList.remove('com-falha');
    iniciarEtapas();
    buscarAnalise();
  });
  $('btnEncerrarFalha').addEventListener('click', resetarTudo);

  // --- Resultado ---

  function mostrarResultado(data) {
    TotemRender.render($('resBody'), data, { nome: estado.nome, marca: estado.marca, segmento: estado.segmento, kiosk: !PHONE });
    // O QR leva a mesma analise ja consultada aqui (mesma URL = cache da borda): so marca, segmento e concorrentes digitados.
    estado.link = TotemRender.linkDoResultado(location.origin, estado.marca, estado.concorrentes, estado.segmento, estado.instagram);
    var qr = '';
    // No celular a pessoa ja esta com o resultado na mao: sem QR, so o aviso do e-mail e o botao para analisar outra marca.
    if (!PHONE) { try { qr = QR.toSvg(estado.link, { ecc: 'M', margin: 2 }); } catch (err) { qr = ''; } }
    $('fim').innerHTML =
      '<section class="fim">' + (qr ? '<div class="qr">' + qr + '</div>' : '') +
      '<div><h2>' + (PHONE ? 'Guarda tu Compass' : 'Llévate tu Compass en el celular') + '</h2>' +
      (PHONE ? '<p>El enlace del resultado funciona en cualquier dispositivo y en cualquier momento.</p>' : '<p>Apunta la cámara de tu celular al código QR y abre el resultado completo, con las mismas gráficas.</p>') +
      '<p class="email-status" id="emailStatus"></p></div></section>' +
      '<p class="cta-final">¿Quieres el Compass completo, con monitoreo continuo de tu marca y de tus competidores? Habla con el equipo de Buzzmonitor' + (PHONE ? '.' : ' aquí en el evento.') + '</p>' +
      '<div class="encerrar"><button type="button" class="btn btn--primary btn--lg" id="btnEncerrar">' + (PHONE ? 'Analizar otra marca' : 'Terminar sesión') + '</button></div>';
    $('btnEncerrar').addEventListener('click', function () { resetarTudo(); if (PHONE) irParaMarca(); });
    atualizarStatusEmail();
    $('resScroll').scrollTop = 0;
    mostrar('result');
  }

  function atualizarStatusEmail() {
    var el = $('emailStatus');
    if (!el) return;
    var s = estado.leadStatus;
    if (!s) el.textContent = 'Enviando el enlace a ' + estado.email + '…';
    else if (s.email === 'enviado' || s.email === 'via_ac') el.textContent = 'También te enviamos el enlace a ' + estado.email + '.';
    else el.textContent = '';
  }

  // --- Ligacoes ---

  $('s-attract').addEventListener('click', irParaMarca); // tocar em qualquer lugar da tela de atracao inicia
  $('btnStart').addEventListener('click', function (e) { e.stopPropagation(); irParaMarca(); });
  $('btnClose').addEventListener('click', resetarTudo);

  if (PHONE) {
    // Celular: o navegador pode preencher nome e e-mail, e o botao de falha deixa de falar em "sessao".
    $('nome').setAttribute('autocomplete', 'name');
    $('email').setAttribute('autocomplete', 'email');
    $('btnEncerrarFalha').textContent = 'Empezar de nuevo';
  } else {
    // Quiosque: sem menu de contexto, sem zoom por gesto.
    document.addEventListener('contextmenu', function (e) { e.preventDefault(); });
    ['gesturestart', 'gesturechange', 'gestureend'].forEach(function (ev) { document.addEventListener(ev, function (e) { e.preventDefault(); }); });
  }

  mostrar('attract');
})();
