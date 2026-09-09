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

  function render(d, alvo) {
    charts.forEach((c) => c.destroy());
    charts = [];
    const k = d.kpis;

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
      + 'e a etapa mostrada é onde cada um está <b>hoje</b> — não por onde passou. '
      + 'Em Portugal não há data de reunião, de proposta nem de fecho no CRM, e não existe histórico '
      + 'de mudança de etapa, então não é possível medir conversão entre etapas nem datar fechamento. '
      + 'Coortes recentes parecem piores porque ainda não amadureceram.</div>';

    const b1 = '<section><div class="section-head"><div class="icon">1</div>'
      + '<h2>Visão geral da coorte</h2>'
      + `<span class="tag">${fData(d.periodo.ini)} – ${fData(d.periodo.fim)}</span></div>`
      + '<div class="kpi-row">'
      + kpi('Deals criados', fInt(k.total), null, `${fInt(k.inbound)} inbound · ${fInt(k.outbound)} outbound`)
      + kpi('Rastreados como CM', fInt(k.cm), fPct(k.cm, k.total), 'UTM de CM ou conversão em página de conteúdo')
      + kpi('Sem rastreio', fInt(k.sem_rastreio), fPct(k.sem_rastreio, k.total), 'sem UTM útil e sem URL de conversão')
      + kpi('Em aberto', fInt(k.aberto), fPct(k.aberto, k.total), 'fora de perdido/desqualificado/churn')
      + kpi('Ganhos', fInt(k.ganho), fPct(k.ganho, k.total), fEur(k.valor_ganho) + ' em valor')
      + kpi('Perdidos e desqual.', fInt(k.perdido), fPct(k.perdido, k.total), 'por etapa, não por status')
      + '</div></section>';

    const b2 = '<section><div class="section-head"><div class="icon">2</div>'
      + '<h2>Onde a coorte está hoje</h2>'
      + '<span class="tag">estado atual, não progressão</span></div>'
      + barrasEtapa(d) + '</section>';

    const b3 = '<section><div class="section-head"><div class="icon">3</div>'
      + '<h2>Rastreio ao longo do tempo</h2>'
      + '<span class="tag">deals criados por mês</span></div>'
      + '<div class="chart-wrap"><canvas id="cSerie" class="chart-canvas"></canvas></div>'
      + '</section>';

    const linhasFonte = d.fontes.slice(0, 25).map((f, i) => '<tr>'
      + `<td class="rk rk-${i < 3 ? i + 1 : 'n'}">${i + 1}</td>`
      + `<td>${esc(f.fonte)}</td>`
      + `<td class="num">${fInt(f.n)}</td>`
      + `<td class="num">${fPct(f.n, k.total)}</td>`
      + `<td class="num">${fInt(f.cm)}</td></tr>`);
    const b4 = '<section><div class="section-head"><div class="icon">4</div>'
      + '<h2>Fontes</h2><span class="tag">utm_source normalizada</span></div>'
      + tabela('<tr><th>#</th><th>Fonte</th><th class="num">Deals</th><th class="num">% da coorte</th>'
        + '<th class="num">dos quais CM</th></tr>', linhasFonte)
      + '</section>';

    const linhasPag = d.paginas.slice(0, 25).map((p, i) => '<tr>'
      + `<td class="rk rk-${i < 3 ? i + 1 : 'n'}">${i + 1}</td>`
      + `<td class="quebra">${esc(p.pagina)}</td>`
      + `<td class="num">${fInt(p.n)}</td></tr>`);
    const b5 = '<section><div class="section-head"><div class="icon">5</div>'
      + '<h2>Páginas de conversão</h2><span class="tag">url_conversao</span></div>'
      + tabela('<tr><th>#</th><th>Página</th><th class="num">Deals</th></tr>', linhasPag,
        'Nenhum deal da coorte tem URL de conversão.')
      + '</section>';

    const linhasDeal = d.deals.slice()
      .sort((a, b) => (a.d < b.d ? 1 : -1))
      .slice(0, 300)
      .map((x) => '<tr>'
        + `<td>${fData(x.d)}</td>`
        + `<td class="quebra">${esc(x.t)}</td>`
        + `<td>${esc(d.rotuloEtapa(x.e))}</td>`
        + `<td>${esc(x.o)}</td>`
        + `<td><span class="b ${x.c === 'cm' ? 'b-lp' : (x.c === 'sem_rastreio' ? 'b-reason-soft' : 'b-blog')}">`
        + `${x.c === 'cm' ? 'CM' : (x.c === 'sem_rastreio' ? 'sem rastreio' : 'não CM')}</span></td>`
        + `<td>${esc(x.f || '—')}</td>`
        + `<td class="num">${x.v ? fEur(x.v) : '—'}</td></tr>`);
    const b6 = '<section><div class="section-head"><div class="icon">6</div>'
      + '<h2>Deals da coorte</h2>'
      + `<span class="tag">${d.deals.length > 300 ? 'mostrando 300 de ' + fInt(d.deals.length) : fInt(d.deals.length) + ' deals'}</span></div>`
      + tabela('<tr><th>Criado</th><th>Deal</th><th>Etapa</th><th>Origem</th><th>Rastreio</th>'
        + '<th>Fonte</th><th class="num">Valor</th></tr>', linhasDeal)
      + '</section>';

    alvo.innerHTML = header + aviso + b1 + b2 + b3 + b4 + b5 + b6;

    const cv = document.getElementById('cSerie');
    if (cv && d.serie.length) {
      charts.push(new Chart(cv.getContext('2d'), {
        type: 'bar',
        data: {
          labels: d.serie.map((s) => fMes(s.mes)),
          datasets: [
            { label: 'CM', data: d.serie.map((s) => s.cm), backgroundColor: CORES.cm },
            { label: 'Não CM', data: d.serie.map((s) => s.nao_cm), backgroundColor: CORES.nao_cm },
            { label: 'Sem rastreio', data: d.serie.map((s) => s.sem_rastreio), backgroundColor: CORES.sem_rastreio },
          ],
        },
        options: {
          responsive: true, maintainAspectRatio: false,
          scales: { x: { stacked: true, grid: { display: false } }, y: { stacked: true, beginAtZero: true } },
          plugins: { legend: { position: 'bottom' } },
        },
      }));
    }
  }

  return { render };
})();
