// Renderiza o resultado do totem (GET /api/totem). Compartilhado por totem.html (quiosque) e totem-resultado.html (celular).
// Tudo que vem de fora (nomes, termos, posts) passa por esc()/safeHref() antes de entrar no HTML.

(function (raiz) {
  'use strict';

  // marca, concorrente 1, 2 e 3: tokens da marca Buzzmonitor (laranja, branco, rosa, amarelo) legiveis sobre preto.
  var CORES_GRUPO = ['#EB7C2E', '#FFFFFF', '#DE2451', '#FCBD4F'];
  var COR_POSITIVO = '#14B8A6';
  var COR_NEUTRO = '#6f6f76';
  var COR_NEGATIVO = '#DE2451';

  function esc(s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }
  function safeHref(url) { return /^https?:\/\//i.test(url || '') ? esc(url) : '#'; }
  function fmt(n) { return Number(n || 0).toLocaleString('es-MX'); }
  function pct(n) { return n == null ? '–' : n + '%'; }

  // Ordem fixa dos parametros (m, s, c...): e a chave do cache da borda, igual no totem, no QR code e no e-mail.
  function parametros(marca, concorrentes, segmento, instagram) {
    var p = new URLSearchParams();
    p.set('m', marca);
    if (segmento) p.set('s', segmento);
    if (instagram) p.set('i', instagram);
    (concorrentes || []).forEach(function (c) { p.append('c', c); });
    return p;
  }
  // A MESMA url de analise e usada pelo totem, pelo QR code e pelo e-mail: e ela que o cache da borda guarda.
  // Versao LATAM: tudo vive em buzzcompass.buzzmonitor.com/es (o projeto do Brasil faz proxy de /es/* para este projeto).
  var BASE = '/es';
  function apiUrl(marca, concorrentes, segmento, instagram) { return BASE + '/api/totem?' + parametros(marca, concorrentes, segmento, instagram).toString(); }
  // Sem dado pessoal na URL (ela vai para o QR code, o e-mail e o Google Analytics): so marca, segmento, @ da marca e concorrentes.
  function linkDoResultado(origem, marca, concorrentes, segmento, instagram) {
    return origem + BASE + '/totem-resultado?' + parametros(marca, concorrentes, segmento, instagram).toString();
  }
  // Mesma limpeza do servidor (api/_lib/perfil.js): "@natura", "natura" e "instagram.com/natura" viram "natura".
  function limparPerfil(v) {
    var s = String(v || '').trim().toLowerCase().replace(/^https?:\/\//, '').replace(/^(www\.)?instagram\.com\//, '').replace(/[\/?#].*$/, '').replace(/^@+/, '');
    s = s.replace(/[^a-z0-9._]/g, '').replace(/^\.+|\.+$/g, '');
    return s.length >= 2 ? s.slice(0, 30) : '';
  }

  // --- Graficos em SVG ---

  function anel(score) {
    var v = Math.max(0, Math.min(100, score || 0));
    var r = 78, c = 2 * Math.PI * r;
    return '<svg viewBox="0 0 180 180" role="img" aria-label="Compass Score ' + v + ' de 100">' +
      '<defs><linearGradient id="gRing" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#EB7C2E"/><stop offset="1" stop-color="#DE2451"/></linearGradient></defs>' +
      '<circle cx="90" cy="90" r="' + r + '" fill="none" stroke="rgba(255,255,255,.10)" stroke-width="14"/>' +
      '<circle cx="90" cy="90" r="' + r + '" fill="none" stroke="url(#gRing)" stroke-width="14" stroke-linecap="round" ' +
      'stroke-dasharray="' + c.toFixed(1) + '" stroke-dashoffset="' + (c * (1 - v / 100)).toFixed(1) + '" transform="rotate(-90 90 90)"/>' +
      '<text x="90" y="104" text-anchor="middle" font-family="League Spartan, sans-serif" font-size="56" font-weight="900" fill="#fff">' + v + '</text></svg>';
  }

  function polar(cx, cy, r, graus) {
    var rad = (graus - 90) * Math.PI / 180;
    return { x: cx + r * Math.cos(rad), y: cy + r * Math.sin(rad) };
  }
  function fatia(cx, cy, r, ini, fim) {
    var a = polar(cx, cy, r, fim), b = polar(cx, cy, r, ini);
    return ['M', cx, cy, 'L', a.x, a.y, 'A', r, r, 0, fim - ini <= 180 ? 0 : 1, 0, b.x, b.y, 'Z'].join(' ');
  }
  function pizza(segmentos) {
    var total = segmentos.reduce(function (s, x) { return s + Math.max(0, x.val || 0); }, 0);
    if (total <= 0) return { svg: '', legenda: '<p class="muted">Todavía no hay registros en este periodo.</p>' };
    var com = segmentos.filter(function (x) { return (x.val || 0) > 0; });
    if (com.length === 1) {
      return {
        svg: '<svg viewBox="0 0 150 150" aria-hidden="true"><circle cx="75" cy="75" r="70" fill="' + com[0].cor + '"/></svg>',
        legenda: '<span><i class="dot" style="background:' + com[0].cor + '"></i>' + esc(com[0].label) + ' <b>100%</b></span>',
      };
    }
    var ang = 0, paths = '', leg = '';
    segmentos.forEach(function (x) {
      var p = (x.val || 0) / total * 100;
      if (p <= 0) return;
      var fim = ang + p * 3.6;
      paths += '<path d="' + fatia(75, 75, 70, ang, fim) + '" fill="' + x.cor + '"/>';
      leg += '<span><i class="dot" style="background:' + x.cor + '"></i>' + esc(x.label) + ' <b>' + (Math.round(p * 10) / 10).toString().replace(/\.0$/, '') + '%</b></span>';
      ang = fim;
    });
    return { svg: '<svg viewBox="0 0 150 150" aria-hidden="true">' + paths + '</svg>', legenda: leg };
  }

  // Uma linha por grupo, cada uma na PROPRIA escala: serve para comparar o ritmo, nao o volume (o volume esta nas barras).
  // Grafico de linhas com eixo Y (menções por dia) e eixo X (datas). Todas as linhas dividem a MESMA escala, entao o eixo
  // diz a verdade para todas. Eixos em HTML (o texto nao pode esticar junto com o SVG); as linhas esticam com a largura.
  function tickCompacto(n) {
    if (n >= 10000) return Math.round(n / 1000) + ' mil';
    if (n >= 1000) return (n / 1000).toFixed(1).replace('.0', '') + ' mil';
    return String(Math.round(n * 10) / 10);
  }
  // maximo "redondo" para o eixo Y, com 4 intervalos de valor inteiro quando possivel (0, 25, 50, 75, 100)
  function maximoDoEixo(m) {
    m = Math.max(m, 4);
    var base = Math.pow(10, Math.floor(Math.log10(m / 4)));
    var passos = base >= 10 ? [1, 2, 2.5, 5, 10] : [1, 2, 5, 10];
    for (var i = 0; i < passos.length; i++) { if (passos[i] * base * 4 >= m) return passos[i] * base * 4; }
    return base * 40;
  }
  // AAAAMMDD -> dd/mm. Sem datas do servidor (resposta antiga em cache), conta os 30 dias para tras a partir de hoje.
  function rotuloDaData(datas, k, n) {
    var d = (datas || [])[k];
    if (d) return String(d).slice(6, 8) + '/' + String(d).slice(4, 6);
    var dt = new Date(Date.now() - 6 * 3600e3 - (n - 1 - k) * 86400e3);
    return String(dt.getUTCDate()).padStart(2, '0') + '/' + String(dt.getUTCMonth() + 1).padStart(2, '0');
  }
  function linhas(grupos, datas) {
    var w = 600, h = 150, pad = 4, out = '';
    var n = 0, maxV = 1;
    grupos.forEach(function (g) { var sr = g.serie || []; n = Math.max(n, sr.length); maxV = Math.max(maxV, Math.max.apply(null, sr.concat([1]))); });
    if (n < 2) return '';
    var topo = maximoDoEixo(maxV);
    var passo = w / (n - 1);
    var grade = '', rotulosY = '';
    for (var t = 0; t <= 4; t++) {
      var f = t / 4;
      var y = (h - pad - f * (h - pad * 2)).toFixed(1);
      grade += '<line x1="0" y1="' + y + '" x2="' + w + '" y2="' + y + '" stroke="rgba(255,255,255,' + (t === 0 ? '.28' : '.1') + ')" stroke-width="1" vector-effect="non-scaling-stroke"/>';
      rotulosY += '<span style="bottom:' + (f * 100).toFixed(1) + '%">' + tickCompacto(topo * f) + '</span>';
    }
    grupos.forEach(function (g, i) {
      var serie = g.serie || [];
      if (serie.length < 2) return;
      var pontos = serie.map(function (v, k) { return (k * passo).toFixed(1) + ',' + (h - pad - (v / topo) * (h - pad * 2)).toFixed(1); }).join(' ');
      out += '<polyline points="' + pontos + '" fill="none" stroke="' + CORES_GRUPO[i % 4] + '" stroke-width="' + (i === 0 ? 3.5 : 2.2) + '" stroke-linecap="round" stroke-linejoin="round" vector-effect="non-scaling-stroke" opacity="' + (i === 0 ? 1 : 0.85) + '"/>';
    });
    var idx = [0, Math.round((n - 1) / 4), Math.round((n - 1) / 2), Math.round(3 * (n - 1) / 4), n - 1];
    var rotulosX = idx.map(function (k) { return '<span>' + rotuloDaData(datas, k, n) + '</span>'; }).join('');
    return '<div class="grafico"><div class="grafico__y" aria-hidden="true">' + rotulosY + '</div>' +
      '<div class="grafico__plot"><svg viewBox="0 0 ' + w + ' ' + h + '" preserveAspectRatio="none" aria-hidden="true">' + grade + out + '</svg></div>' +
      '<div class="grafico__x" aria-hidden="true">' + rotulosX + '</div></div>';
  }

  // --- Seções ---

  // Etiqueta que diz, acima de cada parte, se o dado e da MARCA ou do SEGMENTO.
  function escopo(tipo, texto) { return '<span class="escopo escopo--' + tipo + '">' + esc(texto) + '</span>'; }

  // Linha do Instagram informado: perfil confirmado na base da Trends (nome e seguidores) ou, se nao estiver la, so a ancora.
  function linhaInstagram(ig) {
    if (!ig || !ig.handle) return '';
    var texto = ig.confirmado
      ? 'Perfil @' + ig.handle + ' confirmado en Trends: ' + ig.nome + ', ' + fmt(ig.seguidores) + ' seguidores.'
      : 'La búsqueda de la marca usa el perfil @' + ig.handle + ' como referencia.';
    return '<p class="muted small perfil-ig">' + esc(texto) + '</p>';
  }

  // Proporção de sentimentos nas menções da marca (positivas, neutras e negativas sobre o TOTAL), com barra empilhada.
  function legendaReputacao(g) {
    var total = g && g.volume ? g.volume : 0;
    if (!total) return 'sentimiento de las menciones: la marca todavía no aparece en los últimos 30 días';
    var pos = Math.round((g.positivos || 0) / total * 100);
    var neg = Math.round((g.negativos || 0) / total * 100);
    var neu = Math.max(0, 100 - pos - neg);
    return '<span class="sent-bar" aria-hidden="true"><i style="width:' + pos + '%;background:' + COR_POSITIVO + '"></i><i style="width:' + neu + '%;background:' + COR_NEUTRO + '"></i><i style="width:' + neg + '%;background:' + COR_NEGATIVO + '"></i></span>' +
      'De ' + fmt(total) + ' menciones: <b class="sent-pos">' + pos + '% positivas</b> · ' + neu + '% neutras · <b class="sent-neg">' + neg + '% negativas</b>';
  }

  function secaoPlacar(scores, nomeMarca, instagram, marcaComp) {
    if (!scores) return ''; // resposta antiga (sem score da marca): melhor sem o bloco do que com zeros
    var s = scores;
    var est = s.estimado || {};
    var itens = [
      ['Presencia', 'participación en la conversación frente a tus competidores', s.presenca, '#EB7C2E', false],
      ['Reputación', legendaReputacao(marcaComp), s.reputacao, '#14B8A6', est.reputacao],
      ['Ritmo de crecimiento', 'última semana contra la anterior', s.ritmo, '#FCBD4F', est.ritmo],
      ['Ventaja competitiva', 'reputación y ritmo contra el promedio de tus competidores', s.vantagem, '#DE2451', est.vantagem],
    ];
    var barras = itens.map(function (it) {
      var v = Math.max(0, Math.min(100, it[2] || 0));
      return '<div class="sub"><span class="sub__label">' + it[0] + (it[4] ? ' <em class="tag">estimado</em>' : '') + '<small>' + it[1] + '</small></span>' +
        '<span class="sub__bar"><span style="width:' + v + '%;background:' + it[3] + '"></span></span><b class="sub__val">' + v + '</b></div>';
    }).join('');
    return '<section class="panel"><div class="panel__head">' + escopo('marca', 'Marca · ' + nomeMarca) + '<h2>Compass Score de ' + esc(nomeMarca) + '</h2>' + linhaInstagram(instagram) + '</div>' +
      '<div class="score-grid"><div class="score-ring">' + anel(s.compass_score) + '<span class="score-ring__cap">Compass Score</span></div>' +
      '<div class="subs">' + barras + '</div></div></section>';
  }

  // Os 4 cards sao TEXTO com insight pronto. Cada um separa, com etiqueta, o que vale para a MARCA (primeiro) e para o SEGMENTO.
  function cartoes(narrativa, nomeMarca) {
    if (!narrativa) return '';
    var lista = [
      ['oportunidade', 'Oportunidad', 'card--oportunidade', 'Sector'],
      ['risco', 'Riesgo', 'card--risco', 'Sector'],
      ['tendencia_emergente', 'Tendencia emergente', 'card--tendencia', 'Sector'],
      ['concorrentes', 'Competidores', 'card--comparacao', 'Competidores en el sector'],
    ].filter(function (c) { return narrativa[c[0]]; }).map(function (c) {
      var d = narrativa[c[0]];
      var corpo = d.segmento !== undefined
        ? '<div class="card__bloco">' + escopo('marca', 'Marca · ' + nomeMarca) + '<p>' + esc(d.marca) + '</p></div>' +
          '<div class="card__bloco">' + escopo('segmento', c[3]) + '<p>' + esc(d.segmento) + '</p></div>'
        : '<p>' + esc(d.texto) + '</p>'; // formato antigo (resposta guardada no cache antes desta mudanca)
      return '<div class="card ' + c[2] + '"><span class="card__tag">' + c[1] + '</span><h3>' + esc(d.titulo) + '</h3>' + corpo + '</div>';
    }).join('');
    return '<section class="cards">' + lista + '</section>';
  }

  function secaoComparacao(data, nomeMarca) {
    var grupos = data.comparacao || [];
    var linhasHtml = grupos.map(function (g, i) {
      // sentimento e crescimento aparecem para TODAS as marcas da comparacao, a propria marca e os concorrentes
      var cresc = g.crescimento_pct;
      var chipCresc = cresc == null ? '' : cresc === 0
        ? '<span class="chip">● estable en 7 días</span>'
        : '<span class="chip ' + (cresc > 0 ? 'chip--up' : 'chip--down') + '">' + (cresc > 0 ? '▲ ' : '▼ ') + Math.abs(cresc) + '% en 7 días</span>';
      var chipPos = g.pct_positivo == null ? '<span class="chip">sin posts positivos ni negativos</span>' : '<span class="chip">' + g.pct_positivo + '% positivo</span>';
      var chipIncerta = g.busca_incerta ? '<span class="chip chip--aviso">nombre común: la búsqueda puede mezclar otros temas</span>' : '';
      return '<div class="cmp' + (g.tipo === 'marca' ? ' cmp--marca' : '') + '">' +
        '<div class="cmp__nome"><i class="dot" style="background:' + CORES_GRUPO[i % 4] + '"></i><b>' + esc(g.rotulo) + '</b>' +
        (g.tipo === 'marca' ? '<em class="tag tag--marca">tu marca</em>' : (g.origem === 'sugerido' ? '<em class="tag">sugerido por Buzzmonitor</em>' : '')) + '</div>' +
        '<div class="cmp__bar"><span style="width:' + Math.max(g.share_pct, g.volume > 0 ? 2 : 0) + '%;background:' + CORES_GRUPO[i % 4] + '"></span></div>' +
        '<div class="cmp__nums"><strong>' + g.share_pct + '%</strong> de la conversación <span>' + fmt(g.volume) + ' menciones</span></div>' +
        '<div class="chips">' + chipPos + chipCresc + chipIncerta + '</div></div>';
    }).join('');
    var legenda = grupos.map(function (g, i) {
      return '<span><i class="dot" style="background:' + CORES_GRUPO[i % 4] + '"></i>' + esc(g.rotulo) + '</span>';
    }).join('');
    return '<section class="panel"><div class="panel__head">' + escopo('marca', 'Marca y competidores') + '<h2>' + esc(nomeMarca) + ' y sus competidores en la conversación</h2></div>' +
      '<p class="muted lead">Participación de cada marca en la conversación de los últimos 30 días, entre las marcas de esta comparación.</p>' +
      '<div class="cmp-list">' + linhasHtml + '</div>' +
      '<div class="chart-block"><div class="chart-title">Menciones por día, marca por marca</div><div class="lines">' + linhas(grupos, ((data.mercado || {}).charts || {}).datas) + '</div>' +
      '<div class="legend">' + legenda + '</div><p class="muted small">Eje vertical: menciones por día, en la misma escala para todas las marcas.</p></div></section>';
  }

  function pizzaGenero(genero) {
    var arr = genero || [];
    var valor = function (l) { return (arr.find(function (x) { return x.label === l; }) || {}).value || 0; };
    // "Nao identificado" e a maioria esmagadora dos perfis e nao ajuda a leitura: Feminino e Masculino somam 100% entre si.
    return pizza([
      { label: 'Femenino', val: valor('FEMALE'), cor: '#EB7C2E' },
      { label: 'Masculino', val: valor('MALE'), cor: '#FFFFFF' },
    ]);
  }

  // Graficos da conversa do mercado (a marca e os concorrentes estao dentro dela).
  function secaoNumeros(titulo, ch, nomeSegmento) {
    ch = ch || {};
    var s = ch.sentimento || { positivos: 0, neutros: 0, negativos: 0 };
    var p = pizza([
      { label: 'Positivo', val: s.positivos, cor: COR_POSITIVO },
      { label: 'Neutro', val: s.neutros, cor: COR_NEUTRO },
      { label: 'Negativo', val: s.negativos, cor: COR_NEGATIVO },
    ]);
    var g = pizzaGenero(ch.genero);

    var canais = (ch.canais || []).filter(function (c) { return c.value > 0; });
    var nomeCanal = { misc: 'Sitios web', instagram: 'Instagram', facebook: 'Facebook', twitter: 'X (Twitter)', youtube: 'YouTube' };
    var totalCanais = Math.max(1, canais.reduce(function (t, c) { return t + c.value; }, 0));
    var maxCanal = Math.max(1, Math.max.apply(null, canais.map(function (c) { return c.value; }).concat([0])));
    var canaisHtml = canais.map(function (c) {
      return '<div class="bar-row"><span class="bar-row__label"><b>' + Math.round(c.value / totalCanais * 100) + '%</b> ' + esc(nomeCanal[c.label] || c.label) + '</span>' +
        '<span class="bar-row__track"><span style="width:' + Math.round(c.value / maxCanal * 100) + '%"></span></span></div>';
    }).join('') || '<p class="muted">Todavía no hay registros en este periodo.</p>';

    var serieHtml = (ch.serie_diaria || []).length > 1
      ? '<div class="chart-block"><div class="chart-title">Volumen de menciones, día a día</div><div class="lines">' + linhas([{ serie: ch.serie_diaria }], ch.datas) + '</div><p class="muted small">Eje vertical: menciones por día.</p></div>'
      : '';

    var termos = (ch.termos || []).slice(0, 16).sort(function (a, b) { return b.value - a.value; });
    var max = Math.max.apply(null, termos.map(function (t) { return t.value; }).concat([1]));
    var min = Math.min.apply(null, termos.map(function (t) { return t.value; }).concat([max]));
    var nuvem = termos.map(function (t, i) {
      var r = max === min ? 1 : (t.value - min) / (max - min);
      return '<span class="cloud__term' + (i < 3 ? ' cloud__term--top' : '') + '" style="font-size:' + (1.1 + r * 2.9).toFixed(2) + 'rem" title="' + t.value + ' menciones">' + esc(t.label) + '</span>';
    }).join('') || '<p class="muted">Todavía no hay registros en este periodo.</p>';

    return '<section class="panel"><div class="panel__head">' + escopo('segmento', 'Sector' + (nomeSegmento ? ' · ' + nomeSegmento : '')) + '<h2>' + titulo + '</h2></div>' +
      '<div class="grid-2">' +
      '<div class="chart-block"><div class="chart-title">Sentimiento de las conversaciones</div><div class="pie-wrap">' + p.svg + '<div class="pie-legend">' + p.legenda + '</div></div></div>' +
      '<div class="chart-block"><div class="chart-title">Género de quienes comentan</div><div class="pie-wrap">' + g.svg + '<div class="pie-legend">' + g.legenda + '</div></div>' +
      '<p class="muted small">Solo perfiles con género identificado.</p></div></div>' +
      '<div class="grid-2"><div class="chart-block"><div class="chart-title">Dónde ocurren las conversaciones</div>' + canaisHtml + '</div>' +
      serieHtml + '</div>' +
      '<div class="chart-block"><div class="chart-title">De qué está hablando el mercado</div><div class="cloud">' + nuvem + '</div></div></section>';
  }

  function dataDoPost(raw) {
    var s = String(raw || '');
    return s.length < 14 ? '' : s.slice(8, 10) + ':' + s.slice(10, 12) + ' ' + s.slice(6, 8) + '/' + s.slice(4, 6) + '/' + s.slice(0, 4);
  }
  function compacto(n) {
    n = n || 0;
    if (n >= 1000000) return (n / 1000000).toFixed(1).replace('.0', '') + 'M';
    if (n >= 1000) return (n / 1000).toFixed(1).replace('.0', '') + 'K';
    return String(n);
  }

  // Post real: o quadro oficial da rede (Instagram e Facebook), do mesmo jeito que aparece na rede. So as duas redes que
  // devolvem o link do post; o endereco do quadro e montado aqui, so a partir do link, e so para esses dois dominios.
  function urlDoQuadro(p) {
    var link = String(p.link || '');
    if (p.rede === 'instagram') {
      var m = link.match(/^https:\/\/(?:www\.)?instagram\.com\/(p|reel|tv)\/([\w-]+)/i);
      return m ? 'https://www.instagram.com/' + m[1].toLowerCase() + '/' + m[2] + '/embed/captioned/' : '';
    }
    if (p.rede === 'x') {
      var t = link.match(/^https?:\/\/(?:www\.|mobile\.)?(?:twitter|x)\.com\/[^\/]+\/status(?:es)?\/(\d+)/i);
      return t ? 'https://platform.twitter.com/embed/Tweet.html?dnt=true&theme=dark&lang=es&id=' + t[1] : '';
    }
    if (p.rede === 'facebook' && /^https:\/\/(?:www\.|m\.)?facebook\.com\//i.test(link)) {
      var video = /\/(reel|videos?|watch)\b/i.test(link);
      return 'https://www.facebook.com/plugins/' + (video ? 'video' : 'post') + '.php?show_text=true&width=500&href=' + encodeURIComponent(link);
    }
    return '';
  }

  // Sem loading=lazy de proposito: em alguns navegadores o quadro preguicoso nao carrega nem estando na tela, e no totem
  // o resultado precisa aparecer inteiro.
  // No totem o quadro roda isolado (sem abrir janelas nem sair da pagina: quem esta na frente do totem nao pode ser
  // levado para dentro do Instagram). No celular, os links do quadro abrem normalmente.
  function quadroDoPost(p, kiosk) {
    var url = urlDoQuadro(p);
    if (!url) return '';
    var sandbox = kiosk ? 'allow-scripts allow-same-origin' : 'allow-scripts allow-same-origin allow-popups allow-popups-to-escape-sandbox';
    return '<iframe class="post-quadro post-quadro--' + esc(p.rede) + '" src="' + esc(url) + '" sandbox="' + sandbox + '" ' +
      'referrerpolicy="no-referrer" title="Post de ' + esc(p.autor || 'perfil') + ' en ' + ({ instagram: 'Instagram', facebook: 'Facebook', x: 'X' }[p.rede] || 'redes') + '"></iframe>';
  }

  // Site: quase nenhum deixa ser embutido, entao o post aparece como a previa do link (foto, titulo e resumo da pagina);
  // sem previa, cai para o texto da mencao.
  function previaDoSite(p) {
    var pv = p.previa || {};
    var img = pv.imagem || p.imagem;
    return '<div class="previa">' +
      (img ? '<img class="post-card__img" src="' + esc(img) + '" alt="" loading="lazy" referrerpolicy="no-referrer" onerror="this.remove()">' : '') +
      '<div class="previa__corpo"><span class="previa__site">' + esc(pv.site || 'Sitio web') + '</span>' +
      (pv.titulo ? '<b class="previa__titulo">' + esc(pv.titulo) + '</b>' : '') +
      '<p class="post-card__texto">' + esc(pv.descricao || p.texto) + '</p></div></div>';
  }

  // Quem fala da MARCA: os posts reais mais engajados (quadro da rede) e os perfis ligados ao nome.
  function secaoProva(prova, nomeMarca, kiosk) {
    prova = prova || {};
    var posts = prova.posts || [];
    var inf = prova.influenciadores || [];
    if (!posts.length && !inf.length) return '';
    var nomeRede = { instagram: 'Instagram', facebook: 'Facebook', x: 'X (Twitter)', site: 'Sitio web' };
    var cards = posts.map(function (p) {
      var stats = [['Me gusta', p.curtidas], ['Comentarios', p.comentarios], ['Compartidos', p.compartilhamentos]].filter(function (st) { return st[1] > 0; })
        .map(function (st) { return '<span>' + st[0] + ' <b>' + compacto(st[1]) + '</b></span>'; }).join('');
      return '<article class="post-card">' +
        '<div class="post-card__topo"><span class="post-card__rede">' + esc(nomeRede[p.rede] || p.rede) + '</span>' +
        (p.propria ? '<span class="post-card__propria">perfil de la marca</span>' : '') + '</div>' +
        (urlDoQuadro(p) ? quadroDoPost(p, kiosk) : previaDoSite(p)) +
        '<div class="post-card__meta"><b>' + esc(p.autor || 'Perfil no identificado') + '</b>' + (dataDoPost(p.data) ? ' · ' + esc(dataDoPost(p.data)) : '') + '</div>' +
        (stats ? '<div class="post-card__stats">' + stats + '</div>' : '') +
        (kiosk ? '' : '<a class="post-card__link" href="' + safeHref(p.link) + '" target="_blank" rel="noopener">Ver post original ↗</a>') +
        '</article>';
    }).join('');
    var seguidores = function (n) { return n >= 1000000 ? (n / 1000000).toFixed(1).replace('.0', '') + 'M' : n >= 1000 ? (n / 1000).toFixed(1).replace('.0', '') + ' mil' : String(n); };
    var chips = inf.map(function (i) {
      return '<span class="influencer-chip">' + esc(i.nome) + (i.seguidores ? ' · ' + seguidores(i.seguidores) : '') + ' <span class="rede">' + esc(i.rede || '') + '</span></span>';
    }).join('');
    return '<section class="panel"><div class="panel__head">' + escopo('marca', 'Marca · ' + nomeMarca) + '<h2>Quién está hablando de ' + esc(nomeMarca) + '</h2></div>' +
      (posts.length ? '<div class="chart-block"><div class="chart-title">Posts reales con más interacción de los últimos 30 días</div><div class="posts-reais">' + cards + '</div></div>' : '') +
      (inf.length ? '<div class="chart-block"><div class="chart-title">Perfiles relacionados con la marca</div><div class="influencer-list">' + chips + '</div></div>' : '') +
      '</section>';
  }

  // opts: { nome, marca, segmento, kiosk }
  function render(container, data, opts) {
    var o = opts || {};
    var nomeMarca = (data.marca && data.marca.nome) || o.marca || 'tu marca';
    var primeiro = String(o.nome || '').trim().split(/\s+/)[0];
    var meta = data.meta || {};
    var mercado = data.mercado || {};
    var segmento = (data.marca && data.marca.segmento) || o.segmento || mercado.nome || '';
    var aviso = meta.dados_parciais
      ? '<p class="notice">Algunos datos de esta consulta llegaron incompletos. La lectura de abajo puede ser parcial.</p>' : '';

    container.innerHTML =
      '<header class="res-head"><span class="eyebrow">Tu Compass de Mercado</span>' +
      '<h1>' + (primeiro ? '¡Hola, ' + esc(primeiro) + '! ' : '') + 'Aquí está el Buzz Compass de ' + esc(nomeMarca) + '.</h1>' +
      '<p class="muted">' + (segmento ? 'Sector: ' + esc(segmento) + ' · ' : '') + 'Basado en conversaciones reales de los últimos 30 días, en español, en Buzzmonitor Trends.</p></header>' +
      aviso +
      secaoPlacar((data.marca || {}).scores, nomeMarca, (data.marca || {}).instagram, (data.comparacao || [])[0]) +
      cartoes(data.narrativa, nomeMarca) +
      secaoNumeros('Los números del sector', mercado.charts, segmento) +
      secaoComparacao(data, nomeMarca) +
      secaoProva(data.prova, nomeMarca, o.kiosk);
  }

  raiz.TotemRender = { base: BASE, render: render, apiUrl: apiUrl, linkDoResultado: linkDoResultado, limparPerfil: limparPerfil, esc: esc, fmt: fmt };
})(window);
