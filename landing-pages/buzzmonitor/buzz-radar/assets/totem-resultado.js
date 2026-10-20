// Página do celular (totem-resultado.html): abre pelo QR code do totem ou pelo link do e-mail.
// Lê m (marca), s (segmento), i (@ do Instagram) e c (concorrentes) da URL e chama a MESMA url de análise do totem: quando o totem já consultou,
// a borda devolve o resultado do cache na hora; senão a análise roda de novo.

(function () {
  'use strict';
  var $ = function (id) { return document.getElementById(id); };
  var params = new URLSearchParams(location.search);
  var marca = (params.get('m') || '').trim();
  var segmento = (params.get('s') || '').trim();
  var instagram = TotemRender.limparPerfil(params.get('i'));
  var concorrentes = params.getAll('c').map(function (c) { return c.trim(); }).filter(Boolean).slice(0, 3);

  function falha(titulo, texto, podeTentar) {
    $('carregando').classList.add('com-falha');
    $('carregandoTitulo').textContent = titulo;
    $('carregandoTexto').textContent = texto;
    $('btnRecarregar').style.display = podeTentar ? 'inline-flex' : 'none';
  }

  function carregar() {
    if (marca.length < 2) { falha('Link incompleto', 'Não encontramos a marca neste link. Rode o Buzz Compass de novo no totem.', false); return; }
    $('carregando').classList.remove('com-falha');
    $('btnRecarregar').style.display = 'none';
    var controller = new AbortController();
    var limite = setTimeout(function () { controller.abort(); }, 75000);
    fetch(TotemRender.apiUrl(marca, concorrentes, segmento, instagram), { signal: controller.signal })
      .then(function (r) { return r.json().then(function (j) { return { ok: r.ok, json: j }; }); })
      .then(function (res) {
        clearTimeout(limite);
        if (!res.ok || !res.json || !res.json.ok) throw new Error('analise');
        TotemRender.render($('resBody'), res.json, { marca: marca, segmento: segmento });
        document.title = 'Buzz Compass de ' + ((res.json.marca && res.json.marca.nome) || marca) + ' | Buzzmonitor';
        $('carregando').style.display = 'none';
        $('proposta').classList.remove('aguardando');
      })
      .catch(function () {
        clearTimeout(limite);
        falha('Não conseguimos abrir agora', 'A consulta demorou mais do que o esperado. Tente de novo em instantes.', true);
      });
  }

  $('btnRecarregar').addEventListener('click', carregar);
  carregar();
})();
