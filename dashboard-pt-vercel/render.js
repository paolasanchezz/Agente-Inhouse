/* render.js — Portugal: desenha o painel a partir do agregado do MotorPT.
 * Mesma linguagem visual das outras dashboards (classes de estilo.css).
 */
const RenderPT = (function () {
  'use strict';

  const MESES = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez'];
  const CORES = { cm: '#0B63FF', nao_cm: '#94A3B8', sem_rastreio: '#E2E8F0' };
  let charts = [];

  const esc = (s) => String(s == null ? '' : s)
    .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  const fInt = (n) => (n == null ? '—' : Number(n).toLocaleString('pt-PT'));
  const fPct = (n, d) => (d ? (100 * n / d).toFixed(1).replace('.', ',') + '%' : '—');
  const fEur = (n) => '€ ' + Number(n || 0).toLocaleString('pt-PT', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
  // Deals noutra moeda nao entram na soma em EUR (motor.js); diz quantos ficaram de fora.
  const foraDaSoma = (n) => (n ? ` · ${fInt(n)} noutra moeda, fora da soma` : '');

  function fData(iso) {
    if (!iso) return '—';
    const [a, m, d] = iso.split('-');
    return `${d}/${m}/${a}`;
  }
  function fMes(ym) {
    const [a, m] = ym.split('-');
    return `${MESES[Number(m) - 1]}/${a.slice(2)}`;
  }

  function kpi(label, val, sub, foot) {
    return `<div class="kpi-item"><div class="label">${label}</div>`
      + `<div class="main"><div class="val">${val}</div>`
      + (sub ? `<div class="pct">${sub}</div>` : '') + '</div>'
      + (foot ? `<div class="foot">${foot}</div>` : '') + '</div>';
  }

  function barrasEtapa(d) {
    if (!d.etapas.length) return '<p class="vazio">Nenhum deal criado neste período.</p>';
    const max = Math.max(...d.etapas.map((e) => e.n));
    return '<div class="etapas">' + d.etapas.map((e) => {
      const larg = max ? (100 * e.n / max) : 0;
      return '<div class="etapa-row">'
        + `<div class="etapa-nome">${esc(e.rotulo)}</div>`
        + `<div class="etapa-bar"><span style="width:${larg.toFixed(1)}%" class="et-${e.chave}"></span></div>`
        + `<div class="etapa-num">${fInt(e.n)}<em>${e.pct.toFixed(1).replace('.', ',')}%</em></div>`
        + '</div>';
    }).join('') + '</div>';
  }

  function tabela(thead, linhas, vazio) {
    const corpo = linhas.length ? linhas.join('')
      : `<tr><td colspan="9" class="vazio">${vazio || 'Sem dados no período.'}</td></tr>`;
    return `<div class="table-wrap"><table><thead>${thead}</thead><tbody>${corpo}</tbody></table></div>`;
  }

  const TH_DEAL = '<tr><th>Criado</th><th>Deal</th><th>Etapa</th><th>Origem</th><th>Rastreio</th>'
    + '<th>Fonte</th><th class="num">Valor</th></tr>';

  function linhaDeal(x, d) {
    return '<tr>'
      + `<td>${fData(x.d)}</td>`
      + `<td class="quebra">${esc(x.t)}</td>`
      + `<td>${esc(d.rotuloEtapa(x.e))}</td>`
      + `<td>${esc(x.o)}</td>`
      + `<td><span class="b ${x.c === 'cm' ? 'b-lp' : (x.c === 'sem_rastreio' ? 'b-reason-soft' : 'b-blog')}">`
      + `${x.c === 'cm' ? 'CM' : (x.c === 'sem_rastreio' ? 'sem rastreio' : 'não CM')}</span></td>`
      + `<td>${esc(x.f || '—')}</td>`
      + `<td class="num">${x.v ? fEur(x.v) : '—'}</td></tr>`;
  }

  // Lista aberta por padrao: e ela que deixa conferir o numero do KPI deal a deal.
  function toggleDeals(titulo, deals, d) {
    return '<details class="toggle" open><summary><span class="toggle-title">'
      + `<span>${titulo}</span><span class="toggle-count">${fInt(deals.length)} deals</span>`
      + '</span><span class="caret">▼</span></summary>'
      + `<div class="table-wrap"><table><thead>${TH_DEAL}</thead>`
      + `<tbody>${deals.map((x) => linhaDeal(x, d)).join('')}</tbody></table></div></details>`;
  }

  const porEtapaTexto = (m) => m.etapas.map((e) => `${esc(e.rotulo)} <b>${fInt(e.n)}</b>`).join(' · ');

  function grafico(id, chartClass) {
    return `<div class="chart-wrap"><div class="chart-canvas ${chartClass || ''}"><canvas id="${id}"></canvas></div></div>`;
  }

  function desenharSerie(id, serie) {
    const cv = document.getElementById(id);
    if (!cv || !serie.length) return;
    charts.push(new Chart(cv.getContext('2d'), {
      type: 'bar',
      data: {
        labels: serie.map((s) => fMes(s.mes)),
        datasets: [
          { label: 'CM', data: serie.map((s) => s.cm), backgroundColor: CORES.cm },
          { label: 'Não CM', data: serie.map((s) => s.nao_cm), backgroundColor: CORES.nao_cm },
          { label: 'Sem rastreio', data: serie.map((s) => s.sem_rastreio), backgroundColor: CORES.sem_rastreio },
        ],
      },
      options: {
        responsive: true, maintainAspectRatio: false,
        scales: {
          x: { stacked: true, grid: { display: false } },
          y: { stacked: true, beginAtZero: true, ticks: { precision: 0 } },
        },
        plugins: { legend: { position: 'bottom' } },
      },
    }));
  }

  function render(d, alvo) {
    charts.forEach((c) => c.destroy());
    charts = [];
    const k = d.kpis;
    const r = d.reunioes;
    const f = d.fechamentos;

    const header = '<div class="top">'
      + `<div class="chip">Content Marketing · ${esc(d.nome)}</div>`
      + '<h1>Resultados — Content Marketing</h1>'
      + `<div class="sub">Coorte por data de criação do deal · ${esc(d.nome)}</div>`
      + '<div class="meta">'
      + `<div class="item"><span class="lbl">Coorte</span><span class="val">${fData(d.periodo.ini)} → ${fData(d.periodo.fim)}</span></div>`
      + `<div class="item"><span class="lbl">Deals na coorte</span><span class="val">${fInt(k.total)}</span></div>`
      + `<div class="item"><span class="lbl">Inbound · Outbound</span><span class="val">${fInt(k.inbound)} · ${fInt(k.outbound)}</span></div>`
      + `<div class="item"><span class="lbl">Gerado em</span><span class="val">${fData(d.gerado_em)}</span></div>`
      + '</div>'
      + '<div class="sources"><b>Fonte:</b> Supabase · ActiveCampaign Portugal (deals inbound + outbound) · '
      + 'lógica em <code>dashboard/queries_portugal.py</code>. Moeda: EUR.</div>'
      + '</div>';

    // O aviso nao e decoracao: sem ele o leitor supoe um funil de conversao que
    // este dado nao sustenta. Detalhe em dashboard/AUDITORIA-PORTUGAL.md.
    const aviso = '<div class="aviso"><b>Como ler:</b> o período filtra os deals <b>criados</b> nele, '
      + 'e a etapa mostrada é onde cada um está <b>hoje</b>, não por onde passou. '
      + 'Em Portugal não há data de reunião, de proposta nem de fecho no CRM, e não existe histórico '
      + 'de mudança de etapa. Por isso <b>Reuniões</b> e <b>Fechamento</b> também saem da etapa atual, '
      + 'contados pela data de criação do deal. '
      + 'Coortes recentes parecem piores porque ainda não amadureceram.</div>';

    const b1 = '<section><div class="section-head"><div class="icon">1</div>'
      + '<h2>Visão geral da coorte</h2>'
      + `<span class="tag">${fData(d.periodo.ini)} – ${fData(d.periodo.fim)}</span></div>`
      + '<div class="kpi-row">'
      + kpi('Deals criados', fInt(k.total), null, `${fInt(k.inbound)} inbound · ${fInt(k.outbound)} outbound`)
      + kpi('Rastreados como CM', fInt(k.cm), fPct(k.cm, k.total), 'UTM de CM ou conversão em página de conteúdo')
      + kpi('Sem rastreio', fInt(k.sem_rastreio), fPct(k.sem_rastreio, k.total), 'sem UTM útil e sem URL de conversão')
      + kpi('Em aberto', fInt(k.aberto), fPct(k.aberto, k.total), 'fora de fecho e de perdido/desqual./churn')
      + kpi('Reuniões', fInt(r.total), fPct(r.total, k.total), 'etapa Reunião ou além')
      + kpi('Fechamentos', fInt(k.fechamento), fPct(k.fechamento, k.total), fEur(k.valor_fechamento) + ' em valor' + foraDaSoma(k.fechamento_outra_moeda))
      + kpi('Perdidos e desqual.', fInt(k.perdido), fPct(k.perdido, k.total), 'por etapa, não por status')
      + '</div></section>';

    const b2 = '<section><div class="section-head"><div class="icon">2</div>'
      + '<h2>Onde a coorte está hoje</h2>'
      + '<span class="tag">estado atual, não progressão</span></div>'
      + barrasEtapa(d) + '</section>';

    // ---- 3 · Reunioes
    const hojeEmReuniao = (r.etapas.find((e) => e.chave === 'reuniao') || { n: 0 }).n;
    const b3 = '<section><div class="section-head"><div class="icon">3</div>'
      + '<h2>Reuniões</h2>'
      + '<span class="tag">etapa Reunião ou além · por data de criação</span></div>'
      + '<div class="kpi-row k4">'
      + kpi('Reuniões', fInt(r.total), fPct(r.total, k.total), 'deals da coorte que chegaram à Reunião')
      + kpi('Hoje em Reunião', fInt(hojeEmReuniao), null, 'etapa atual = Reunião')
      + kpi('Já avançaram', fInt(r.total - hojeEmReuniao), null, 'etapa atual depois da Reunião')
      + kpi('Via CM', fInt(r.cm), fPct(r.cm, r.total), `${fInt(r.nao_cm)} não CM · ${fInt(r.sem_rastreio)} sem rastreio`)
      + '</div>'
      + '<p class="nota">Conta pela posição da etapa no pipeline: quem está hoje em Reunião ou numa etapa '
      + 'depois dela (Proposta, Negociação, Fecho, Cliente e, nos pipelines em que vem depois da Proposta, '
      + 'Follow-Up) passou pela Reunião. É um piso: quem teve reunião e hoje está em Perdidos ou '
      + 'Desqualificado não entra, porque o CRM não guarda por onde o deal passou.'
      + (r.total ? `<br><b>Etapa atual:</b> ${porEtapaTexto(r)}` : '') + '</p>'
      + (r.total
        ? '<h3 class="sub-head">Reuniões por mês de criação do deal</h3>'
          + grafico('cReunioes', 'chart-canvas-tall')
          + toggleDeals('Deals que chegaram à Reunião', r.deals, d)
        : '<p class="vazio">Nenhum deal da coorte chegou à Reunião.</p>')
      + '</section>';

    // ---- 4 · Fechamento
    const fora = d.statusGanhoForaDaEtapa;
    const notaFora = fora.length
      ? `<br><b>Não contam:</b> ${fInt(fora.length)} ${fora.length === 1 ? 'deal está marcado' : 'deals estão marcados'} `
        + 'como <i>Ganho</i> no CRM mas com a etapa em outro ponto do funil — '
        + fora.map((x) => `${esc(x.t.trim())} (${esc(d.rotuloEtapa(x.e))})`).join('; ')
        + '. Se fecharam, basta mover a etapa no ActiveCampaign.'
      : '';
    const b4 = '<section><div class="section-head"><div class="icon">4</div>'
      + '<h2>Fechamento</h2>'
      + '<span class="tag">etapa Fecho de Negócio ou Cliente · por data de criação</span></div>'
      + '<div class="kpi-row k4">'
      + kpi('Fechamentos', fInt(f.total), fPct(f.total, k.total), 'etapa atual Fecho de Negócio ou Cliente')
      + kpi('Valor', fEur(f.valor), null, 'soma do valor dos deals' + foraDaSoma(f.fora_da_moeda))
      + kpi('Das reuniões', fPct(f.total, r.total), null, `${fInt(f.total)} de ${fInt(r.total)} reuniões`)
      + kpi('Via CM', fInt(f.cm), fPct(f.cm, f.total), `${fInt(f.nao_cm)} não CM · ${fInt(f.sem_rastreio)} sem rastreio`)
      + '</div>'
      + '<p class="nota">Só a etapa conta: o campo <i>status</i> do CRM não entra. '
      + 'Cliente agrupa Contrato, A formalizar contrato e Clientes.'
      + (f.total ? `<br><b>Etapa atual:</b> ${porEtapaTexto(f)}` : '')
      + notaFora + '</p>'
      + (f.total
        ? '<h3 class="sub-head">Fechamentos por mês de criação do deal</h3>'
          + grafico('cFechamentos', 'chart-canvas-tall')
          + toggleDeals('Deals em fecho', f.deals, d)
        : '<p class="vazio">Nenhum deal da coorte está em Fecho de Negócio ou Cliente.</p>')
      + '</section>';

    const b5 = '<section><div class="section-head"><div class="icon">5</div>'
      + '<h2>Rastreio ao longo do tempo</h2>'
      + '<span class="tag">deals criados por mês</span></div>'
      + '<div class="chart-wrap"><canvas id="cSerie" class="chart-canvas"></canvas></div>'
      + '</section>';

    const linhasFonte = d.fontes.slice(0, 25).map((x, i) => '<tr>'
      + `<td class="rk rk-${i < 3 ? i + 1 : 'n'}">${i + 1}</td>`
      + `<td>${esc(x.fonte)}</td>`
      + `<td class="num">${fInt(x.n)}</td>`
      + `<td class="num">${fPct(x.n, k.total)}</td>`
      + `<td class="num">${fInt(x.cm)}</td></tr>`);
    const b6 = '<section><div class="section-head"><div class="icon">6</div>'
      + '<h2>Fontes</h2><span class="tag">utm_source normalizada</span></div>'
      + tabela('<tr><th>#</th><th>Fonte</th><th class="num">Deals</th><th class="num">% da coorte</th>'
        + '<th class="num">dos quais CM</th></tr>', linhasFonte)
      + '</section>';

    const linhasPag = d.paginas.slice(0, 25).map((p, i) => '<tr>'
      + `<td class="rk rk-${i < 3 ? i + 1 : 'n'}">${i + 1}</td>`
      + `<td class="quebra">${esc(p.pagina)}</td>`
      + `<td class="num">${fInt(p.n)}</td></tr>`);
    const b7 = '<section><div class="section-head"><div class="icon">7</div>'
      + '<h2>Páginas de conversão</h2><span class="tag">url_conversao</span></div>'
      + tabela('<tr><th>#</th><th>Página</th><th class="num">Deals</th></tr>', linhasPag,
        'Nenhum deal da coorte tem URL de conversão.')
      + '</section>';

    // Sem corte: a lista truncada em 300 escondia os deals mais antigos do YtD (e,
    // com eles, fechamentos de jan/fev que o KPI contava).
    const linhasDeal = d.deals.slice()
      .sort((a, b) => (a.d < b.d ? 1 : -1))
      .map((x) => linhaDeal(x, d));
    const b8 = '<section><div class="section-head"><div class="icon">8</div>'
      + '<h2>Deals da coorte</h2>'
      + `<span class="tag">${fInt(d.deals.length)} deals</span></div>`
      + tabela(TH_DEAL, linhasDeal)
      + '</section>';

    alvo.innerHTML = header + aviso + b1 + b2 + b3 + b4 + b5 + b6 + b7 + b8;

    desenharSerie('cReunioes', r.serie);
    desenharSerie('cFechamentos', f.serie);
    desenharSerie('cSerie', d.serie);
  }

  return { render };
})();
