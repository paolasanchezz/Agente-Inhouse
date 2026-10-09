/* render.js — LATAM: monta o HTML do conteudo a partir do objeto `d` do motor.js.
 *
 * Port fiel de dashboard/gerar_relatorio_latam.py::render_html + render_helpers_latam.py.
 * Idioma espanhol, moeda USD. Funil: Leads · Primer contacto · Reunión · Cierre (+ Perdido).
 * Retorna a string HTML do miolo (header + blocos 1-5 + nota + footer).
 */
(function (root, factory) {
  if (typeof module !== 'undefined' && module.exports) module.exports = factory();
  else root.RenderLatam = factory();
})(typeof self !== 'undefined' ? self : this, function () {
  'use strict';

  const MESES_F = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'];
  const MESES_C = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'];
  const DIA = ['lun', 'mar', 'mié', 'jue', 'vie', 'sáb', 'dom'];

  function fmtInt(n) {
    if (n === null || n === undefined) return '0';
    return Number(n).toLocaleString('es', { useGrouping: true }).replace(/,/g, '.').replace(/ /g, '.');
  }
  function fDec(n) { return Number(n).toFixed(1).replace('.', ','); }
  function fmtPct(num, den) { return den ? `${Math.round(100 * (num || 0) / den)}%` : '—'; }
  function fmtFecha(s) {
    if (!s) return '—';
    const d = new Date(s + 'T00:00:00');
    if (isNaN(d.getTime())) return s;
    return `${String(d.getDate()).padStart(2, '0')}/${String(d.getMonth() + 1).padStart(2, '0')}`;
  }
  function fLarga(s) {
    if (!s) return '—';
    const d = new Date(s + 'T00:00:00');
    if (isNaN(d.getTime())) return s;
    return `${String(d.getDate()).padStart(2, '0')} de ${MESES_F[d.getMonth()]} (${DIA[(d.getDay() + 6) % 7]})`;
  }
  function fmtUsd(v) {
    if (v === null || v === undefined || Number(v) === 0) return '—';
    const n = Math.round(Number(v));
    if (!isFinite(n)) return '—';
    return `US$ ${n.toLocaleString('en-US').replace(/,/g, '.')}/mes`;
  }
  function escapeHtml(s) {
    if (s === null || s === undefined) return '';
    return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  }
  function rankCell(idx) {
    const cls = idx === 0 ? 'rk-1' : idx === 1 ? 'rk-2' : idx === 2 ? 'rk-3' : 'rk-n';
    return `<span class="rk ${cls}">${idx + 1}</span>`;
  }
  const BADGE_CLASSES = {
    'meta': 'b-meta', 'chatgpt.com': 'b-chatgpt', 'email': 'b-email', 'blog': 'b-blog',
    'linkedin': 'b-linkedin', 'tiktok': 'b-tiktok',
  };
  function badgeSource(name) {
    const raw = (name == null) ? '' : String(name).trim();
    if (!raw || raw === '(vacío)') return '<span class="b">(vacío)</span>';
    const cls = BADGE_CLASSES[raw.toLowerCase()];
    return cls ? `<span class="b ${cls}">${escapeHtml(raw)}</span>` : `<span class="b">${escapeHtml(raw)}</span>`;
  }
  function formatDelta(atual, anterior, invert) {
    if (anterior === 0 && atual === 0) return { texto: '— igual', classe: 'd-flat' };
    if (anterior === 0 && atual > 0) return { texto: `▲ nuevo (0 → ${atual})`, classe: 'd-new' };
    if (atual === anterior) return { texto: '— igual', classe: 'd-flat' };
    const delta = atual - anterior;
    const pct = anterior ? Math.round((delta / anterior) * 100) : 0;
    const arrow = delta > 0 ? '▲' : '▼';
    const sign = delta > 0 ? '+' : '−';
    const texto = `${arrow} ${sign}${Math.abs(pct)}% vs sem. ant.`;
    const classe = invert ? (delta < 0 ? 'd-up' : 'd-down') : (delta > 0 ? 'd-up' : 'd-down');
    return { texto, classe };
  }

  const AC_DEALS_BASE = 'https://elifeeurope.activehosted.com/app/deals/';
  function dealCell(d) {
    const name = escapeHtml(d.deal);
    if (!d.id) return `<span class="deal-name">${name}</span>`;
    return `<a class="deal-name" href="${AC_DEALS_BASE}${d.id}" target="_blank" rel="noopener noreferrer" title="Abrir deal no ActiveCampaign">${name}</a>`;
  }
  function resp(d) { return escapeHtml(d.responsable || '—'); }
  function emptyRow(cols) { return `<tr><td colspan="${cols}" class="dim center">(sin datos en el período)</td></tr>`; }

  // ---------- ROWS ----------
  function rowLead(d) {
    return `<tr><td>${dealCell(d)}</td><td>${badgeSource(d.utm_source)}</td>`
      + `<td class="dim">${escapeHtml(d.utm_content || '—')}</td>`
      + `<td class="dim">${escapeHtml(d.pais || '—')}</td>`
      + `<td class="dim" data-sort="${d.data_conversao || ''}">${fmtFecha(d.data_conversao)}</td><td>${resp(d)}</td></tr>`;
  }
  function rowReunion(d) {
    return `<tr><td>${dealCell(d)}</td><td>${resp(d)}</td><td>${badgeSource(d.utm_source)}</td>`
      + `<td class="dim">${escapeHtml(d.utm_content || '—')}</td>`
      + `<td class="dim">${escapeHtml(d.pais || '—')}</td>`
      + `<td class="dim" data-sort="${d.data_evento || ''}">${fmtFecha(d.data_evento)}</td></tr>`;
  }
  function rowCierre(d) {
    const v = d.valor;
    const valorHtml = (v && Number(v) > 0) ? `<b>${fmtUsd(v)}</b>` : '—';
    return `<tr><td>${dealCell(d)}</td><td>${resp(d)}</td><td>${badgeSource(d.utm_source)}</td>`
      + `<td class="dim">${escapeHtml(d.pais || '—')}</td>`
      + `<td class="dim" data-sort="${d.data_fech || ''}">${fmtFecha(d.data_fech)}</td><td class="num">${valorHtml}</td></tr>`;
  }
  function rowPerda(d) {
    return `<tr><td>${dealCell(d)}</td><td>${badgeSource(d.utm_source)}</td>`
      + `<td class="dim">${escapeHtml(d.utm_content || '—')}</td>`
      + `<td class="dim">${escapeHtml(d.pais || '—')}</td>`
      + `<td class="dim" data-sort="${d.data_evento || ''}">${fmtFecha(d.data_evento)}</td></tr>`;
  }

  // ---------- RANKINGS ----------
  const _MET = ['leads', 'pc', 'reunion', 'cierre'];
  function renderRankingSource(rows, topN = 8) {
    if (!rows || !rows.length) return emptyRow(8);
    const top = rows.slice(0, topN), outros = rows.slice(topN);
    const out = top.map((r, i) => rowRkSrc(i, r));
    if (outros.length) {
      const ag = {}; _MET.forEach((k) => ag[k] = outros.reduce((s, r) => s + (r[k] || 0), 0));
      out.push('<tr><td><span class="rk rk-n">—</span></td>'
        + `<td class="dim">otros (${outros.length})</td>`
        + `<td class="num">${fmtInt(ag.leads)}</td>`
        + `<td class="num">${fmtInt(ag.pc)}</td><td class="num">—</td>`
        + `<td class="num">${fmtInt(ag.reunion)}</td><td class="num">—</td>`
        + `<td class="num">${fmtInt(ag.cierre)}</td></tr>`);
    }
    return out.join('\n              ');
  }
  function rowRkSrc(idx, r) {
    const leads = r.leads || 0;
    const leadsHtml = idx < 3 ? `<b>${fmtInt(leads)}</b>` : fmtInt(leads);
    return `<tr><td>${rankCell(idx)}</td><td>${badgeSource(r.dim)}</td>`
      + `<td class="num">${leadsHtml}</td>`
      + `<td class="num">${fmtInt(r.pc || 0)}</td>`
      + `<td class="num">${fmtPct(r.pc || 0, leads)}</td>`
      + `<td class="num">${fmtInt(r.reunion || 0)}</td>`
      + `<td class="num">${fmtPct(r.reunion || 0, r.pc || 0)}</td>`
      + `<td class="num">${fmtInt(r.cierre || 0)}</td></tr>`;
  }
  function renderRankingContent(rows, srcMap, topN = 12) {
    if (!rows || !rows.length) return emptyRow(7);
    const top = rows.slice(0, topN), outros = rows.slice(topN);
    const out = top.map((r, i) => rowRkCt(i, r, srcMap));
    if (outros.length) {
      const ag = {}; _MET.forEach((k) => ag[k] = outros.reduce((s, r) => s + (r[k] || 0), 0));
      out.push('<tr><td><span class="rk rk-n">—</span></td>'
        + `<td class="dim">otros (${outros.length})</td><td class="dim">—</td>`
        + `<td class="num">${fmtInt(ag.leads)}</td>`
        + `<td class="num">${fmtInt(ag.pc)}</td>`
        + `<td class="num">${fmtInt(ag.reunion)}</td>`
        + `<td class="num">${fmtInt(ag.cierre)}</td></tr>`);
    }
    return out.join('\n              ');
  }
  function rowRkCt(idx, r, srcMap) {
    const leads = r.leads || 0, cierre = r.cierre || 0;
    const leadsHtml = idx < 3 ? `<b>${fmtInt(leads)}</b>` : fmtInt(leads);
    const cierreHtml = cierre > 0 ? `<b>${fmtInt(cierre)}</b>` : fmtInt(cierre);
    const content = r.dim || '(vacío)';
    const src = srcMap ? srcMap[r.dim] : null;
    return `<tr><td>${rankCell(idx)}</td><td>${escapeHtml(content)}</td><td>${badgeSource(src)}</td>`
      + `<td class="num">${leadsHtml}</td>`
      + `<td class="num">${fmtInt(r.pc || 0)}</td>`
      + `<td class="num">${fmtInt(r.reunion || 0)}</td>`
      + `<td class="num">${cierreHtml}</td></tr>`;
  }

  // ---------- KPIs (5) ----------
  const KPIS = [
    ['leads', null, 'Leads'], ['pc', 'leads', 'Primer contacto'],
    ['reunion', 'pc', 'Reunión'], ['cierre', 'reunion', 'Cierres'],
    ['perd', 'leads', 'Perdidos'],
  ];
  const INVERT = new Set(['perd']);
  function kpiItem(label, val, pct, delta, med) {
    const pctH = pct != null ? `<div class="pct">${pct}</div>` : '';
    const deltaH = delta ? `<div class="delta ${delta.classe}">${delta.texto}</div>` : '';
    const medH = med ? `<div class="foot">${med}</div>` : '';
    return `<div class="kpi-item"><div class="label">${label}</div>`
      + `<div class="main"><div class="val">${fmtInt(val)}</div>${pctH}</div>${deltaH}${medH}</div>`;
  }
  function kpiRow(k, comp, ky, semDiv) {
    const items = KPIS.map(([key, denom, label]) => {
      const val = k[key];
      const pct = denom ? fmtPct(val, k[denom]) : null;
      let delta = null, med = null;
      if (comp) delta = formatDelta(val, comp[key], INVERT.has(key));
      if (ky && semDiv) med = `prom. ${fDec(ky[key] / semDiv)}`;
      return kpiItem(label, val, pct, delta, med);
    });
    return `<div class="kpi-row">${items.join('')}</div>`;
  }

  function toggle(titulo, countLabel, thead, rowsHtml) {
    return '<details class="toggle"><summary><span class="toggle-title">'
      + `<span>${titulo}</span><span class="toggle-count">${countLabel}</span>`
      + '</span><span class="caret">▼</span></summary>'
      + `<div class="table-wrap"><table><thead>${thead}</thead><tbody>${rowsHtml}</tbody></table></div></details>`;
  }
  function rkTable(title, period, thead, rowsHtml) {
    return `<div><div class="col-head"><span class="title">${title}</span>`
      + `<span class="period">${period}</span></div>`
      + `<div class="table-wrap"><table><thead>${thead}</thead><tbody>${rowsHtml}</tbody></table></div></div>`;
  }
  const TH_SRC = '<tr><th>#</th><th>Fuente</th><th class="num">Leads</th><th class="num">PC</th>'
    + '<th class="num">% PC</th><th class="num">Reun.</th><th class="num">% Reu</th><th class="num">Cierre</th></tr>';
  const TH_CT = '<tr><th>#</th><th>Contenido</th><th>Fuente</th><th class="num">Leads</th>'
    + '<th class="num">PC</th><th class="num">Reun.</th><th class="num">Cierre</th></tr>';

  function lst(rows, fn, cols) { return (rows && rows.length) ? rows.map(fn).join('') : emptyRow(cols); }

  // ---------- RENDER ----------
  function render(d) {
    const p = d.periodos;
    const fa = p.fim_atual, hoje = p.hoje;
    const semDiv = Math.max(1, p.semanas_decorridas_ytd);
    const pn = p.periodo_nome || 'Semana';
    const faY = new Date(fa + 'T00:00:00');
    const mtdFimD = new Date(p.mtd_fim + 'T00:00:00');
    const mtdIniD = new Date(p.mtd_ini + 'T00:00:00');
    const iniAtualD = new Date(p.ini_atual + 'T00:00:00');

    const header = '<div class="top"><div class="chip">Content Marketing · Buzzmonitor LATAM</div>'
      + '<h1>Resultados Content Marketing</h1><div class="sub">Dashboard · selector de período · LATAM</div>'
      + '<div class="meta">'
      + `<div class="item"><span class="lbl">Período</span><span class="val">${fLarga(p.ini_atual)} → ${fLarga(fa)} · ${faY.getFullYear()}</span></div>`
      + `<div class="item"><span class="lbl">vs. período anterior</span><span class="val">${fmtFecha(p.ini_ant)} → ${fmtFecha(p.fim_ant)}</span></div>`
      + `<div class="item"><span class="lbl"><span class="no-upper">MtD</span> · Mes actual</span><span class="val">${String(mtdIniD.getDate()).padStart(2, '0')} → ${String(mtdFimD.getDate()).padStart(2, '0')} ${MESES_C[mtdFimD.getMonth()]} ${faY.getFullYear()}</span></div>`
      + `<div class="item"><span class="lbl"><span class="no-upper">YtD</span> · Acumulado del año</span><span class="val">Ene → ${MESES_C[faY.getMonth()]} ${faY.getFullYear()} (${semDiv} semanas)</span></div>`
      + `<div class="item"><span class="lbl">Generado el</span><span class="val">${String(new Date(hoje + 'T00:00:00').getDate()).padStart(2, '0')} ${MESES_C[new Date(hoje + 'T00:00:00').getMonth()]} ${new Date(hoje + 'T00:00:00').getFullYear()}</span></div>`
      + '</div>'
      + '<div class="sources"><b>Fuentes:</b> Supabase (deals_latam_*_staging) · UTM tracking + dominio de contenido getbuzzmonitor.com · '
      + 'filtro Content Marketing (ver MAPEAMENTO-CAMPOS-latam.md). Moneda: USD.</div></div>';

    const tagSem = `${String(iniAtualD.getDate()).padStart(2, '0')}–${String(faY.getDate()).padStart(2, '0')} ${MESES_C[faY.getMonth()]} ${faY.getFullYear()}`;
    const bloco1 = '<section><div class="section-head"><div class="icon">1</div>'
      + `<h2>Visión General · ${pn}</h2><span class="tag">${tagSem}</span></div>`
      + kpiRow(d.semana, d.sem_ant, d.ytd, semDiv)
      + '<div class="sub-head">Acumulado <span class="no-upper">MtD</span></div>'
      + kpiRow(d.mtd)
      + '<div class="sub-head">Acumulado <span class="no-upper">YtD</span></div>'
      + kpiRow(d.ytd)
      + '</section>';

    function lossItem(lbl, k, periodo) {
      const perd = k.perd, leads = k.leads;
      const pct = leads ? Math.round(100 * perd / leads) : 0;
      return `<div class="loss-item"><div class="label">% Perdidos · ${lbl}</div>`
        + `<div class="pct">${pct}%</div>`
        + `<div class="abs">${perd} perdidos · ${leads} leads · ${periodo}</div>`
        + `<div class="bar"><span style="width:${Math.min(pct, 100)}%"></span></div></div>`;
    }
    const perdRows = (d.perdidos_mtd.length ? d.perdidos_mtd.map(rowPerda).join('') : emptyRow(5));
    const bloco2 = '<section><div class="section-head"><div class="icon">2</div>'
      + '<h2>Pérdidas · Período / MtD / YtD</h2><span class="tag">status = Perdido</span></div>'
      + '<div class="loss-panel">'
      + lossItem(pn, d.semana, `${String(iniAtualD.getDate()).padStart(2, '0')}–${String(faY.getDate()).padStart(2, '0')} ${MESES_C[faY.getMonth()]}`)
      + lossItem('<span class="no-upper">MtD</span>', d.mtd, `${String(mtdIniD.getDate()).padStart(2, '0')}–${String(mtdFimD.getDate()).padStart(2, '0')} ${MESES_C[mtdFimD.getMonth()]}`)
      + lossItem('<span class="no-upper">YtD</span>', d.ytd, `Ene–${MESES_C[faY.getMonth()]}`)
      + '</div>'
      + toggle('Leads perdidos en el MtD · detalle', `${d.perdidos_mtd.length} deals`,
        '<tr><th>Deal</th><th>Fuente</th><th>Contenido</th><th>País</th><th>Fecha</th></tr>', perdRows)
      + '</section>';

    const bloco3 = '<section><div class="section-head"><div class="icon">3</div>'
      + '<h2>Listas de Acceso Rápido · Período</h2><span class="tag">drill-down del embudo</span></div>'
      + toggle('3.1 · Leads del período', `${d.leads_semana.length} deals`,
        '<tr><th>Deal</th><th>Fuente</th><th>Contenido</th><th>País</th><th>Fecha</th><th>Responsable</th></tr>',
        lst(d.leads_semana, rowLead, 6))
      + toggle('3.2 · Reuniones del período', `${d.reuniones_semana.length} deals`,
        '<tr><th>Deal</th><th>Responsable</th><th>Fuente</th><th>Contenido</th><th>País</th><th>Fecha</th></tr>',
        lst(d.reuniones_semana, rowReunion, 6))
      + toggle('3.3 · Cierres del período', `${d.cierres_semana.length} deals`,
        '<tr><th>Deal</th><th>Responsable</th><th>Fuente</th><th>País</th><th>Fecha</th><th class="num">Valor</th></tr>',
        lst(d.cierres_semana, rowCierre, 6))
      + '</section>';

    const perLbls = {
      semana: `${fmtFecha(p.ini_atual)}–${fmtFecha(fa)} ${faY.getFullYear()}`,
      sem_ant: `${fmtFecha(p.ini_ant)}–${fmtFecha(p.fim_ant)} ${faY.getFullYear()}`,
      mtd: `${fmtFecha(p.mtd_ini)}–${fmtFecha(p.mtd_fim)} ${faY.getFullYear()}`,
      ytd: `Ene–${MESES_C[faY.getMonth()]} ${faY.getFullYear()}`,
    };
    const titles = { semana: pn, sem_ant: 'Período Anterior', mtd: 'MtD', ytd: 'YtD' };
    const srcTbl = (key) => rkTable(titles[key], perLbls[key], TH_SRC, renderRankingSource(d['rk_src_' + key]));
    const ctTbl = (key) => rkTable(titles[key], perLbls[key], TH_CT, renderRankingContent(d['rk_ct_' + key], d.src_map));
    const bloco4 = '<section><div class="section-head"><div class="icon">4</div>'
      + '<h2>Detalle · Período / Período Anterior / MtD / YtD</h2>'
      + '<span class="tag">% PC = PC/Leads · % Reu = Reu/PC</span></div>'
      + '<div class="sub-head">4.a · Ranking de Fuentes</div>'
      + `<div class="two-col">${srcTbl('semana')}${srcTbl('sem_ant')}</div>`
      + `<div class="two-col">${srcTbl('mtd')}${srcTbl('ytd')}</div>`
      + '<div class="sub-head">4.b · Ranking de Contenido (UTM Content)</div>'
      + `<div class="two-col">${ctTbl('semana')}${ctTbl('sem_ant')}</div>`
      + `<div class="two-col">${ctTbl('mtd')}${ctTbl('ytd')}</div>`
      + '</section>';

    // ---- bloco 5 (tendencia) ----
    const bloco5 = '<section><div class="section-head"><div class="icon">5</div>'
      + '<h2>Tendencias · Últimos 12 meses</h2><span class="tag">52 semanas</span></div>'
      + '<div class="chart-wrap"><div class="chart-head">'
      + '<h3>Reuniones por semana · Tx de conversión</h3>'
      + '<span class="ctx">Tx = Reuniones ÷ Deals creados en la semana · Media 4 sem. = media móvil de las últimas 4 semanas · clic en la leyenda para ocultar series</span></div>'
      + '<div class="chart-canvas"><canvas id="chartTimeseries"></canvas></div></div>'
      + '</section>';

    // ---- bloco 6 (motivos de perda) ----
    const j = d.janela_12m;
    const bloco6 = '<section><div class="section-head"><div class="icon">6</div>'
      + '<h2>Motivos de Pérdida</h2><span class="tag">status = Perdido · por fecha de última modificación</span></div>'
      + '<div class="two-col">'
      + pieWrap('chartMotivosPeriodo', pn === 'Período' ? 'Período seleccionado' : `Período seleccionado · ${pn}`, `${totalMotivos(d.motivos_periodo)} perdidos · ${`${fmtFecha(p.ini_atual)}–${fmtFecha(fa)} ${faY.getFullYear()}`}`, d.motivos_periodo)
      + pieWrap('chartMotivos12m', 'Últimos 12 meses', `${totalMotivos(d.motivos_12m)} perdidos · ${`${fmtFecha(j[0])}/${j[0].slice(0, 4)}–${fmtFecha(j[1])}/${j[1].slice(0, 4)}`} · misma ventana del gráfico de tendencia`, d.motivos_12m)
      + '</div></section>';

    const nota = '<div class="sources" style="margin-top:18px">⚠️ <b>Datos sobre tablas staging.</b> '
      + 'Solo se sincronizan los pipelines <b>Inbound</b> y <b>Outbound</b> Latam: los leads marcados como Perdidos '
      + 'y movidos al pipeline <b>Nutrición</b> salen del conjunto → <b>Leads y Perdidos quedan subestimados</b>. '
      + 'La atribución de canal tampoco cubre todos los leads (UTM vacío en inbound). Los cierres incluyen negocios '
      + 'con pago, contrato o fecha de cierre reales; el valor usa el campo <b>value</b> (USD). Valores y fechas de '
      + 'cierre son aproximados, pendientes de validación con el equipo LATAM.</div>';

    const footer = '<footer><b>Dashboard de Content Marketing · datos reales de Supabase (filtro CM)</b><br>'
      + `${pn} ${fmtFecha(p.ini_atual)}-${fmtFecha(fa)} ${faY.getFullYear()} · `
      + `MtD ${fmtFecha(p.mtd_ini)}-${fmtFecha(p.mtd_fim)} · YtD Ene-${MESES_C[faY.getMonth()]} ${faY.getFullYear()}<br>`
      + 'Reuniones y Cierres contabilizados por fecha del evento · Buzzmonitor LATAM · uso interno</footer>';

    return header + bloco1 + bloco2 + bloco3 + bloco4 + bloco5 + bloco6 + nota + footer;
  }

  // ---------- CHARTS ----------
  const PIE_CORES = ['#0B63FF', '#F59E0B', '#16A34A', '#DC2626', '#7C3AED', '#0E9D9B', '#DB2777', '#92400E', '#94A3B8'];
  const FONTE = { family: 'Inter', size: 12 };
  let _charts = { ts: null, pp: null, p12: null };

  function totalMotivos(rows) { return (rows || []).reduce((t, r) => t + r.n, 0); }
  function pieWrap(id, titulo, ctx, rows) {
    const corpo = (rows && rows.length)
      ? `<div class="chart-canvas chart-canvas-pie"><canvas id="${id}"></canvas></div>`
      : '<div class="dim center chart-vazio">(sin pérdidas en el intervalo)</div>';
    return `<div class="chart-wrap"><div class="chart-head"><h3>${titulo}</h3><span class="ctx">${ctx}</span></div>${corpo}</div>`;
  }

  // Linhas solidas = reuniones de la semana; linha tracejada (eixo %) = reuniones / deals creados en la semana. Sin línea de Propuestas: el embudo LATAM no tiene esa etapa.
  function chartTendencia(s) {
    const agend = s.reunion, leads = s.leads; 
    const tx = leads.map((l, i) => (l ? Math.round((agend[i] / l) * 100) : null));
    const mm4 = agend.map((_, i) => (i < 3 ? null : agend.slice(i - 3, i + 1).reduce((a, b) => a + b, 0) / 4)); // media movel 4 semanas (inclui a semana corrente)
    return new Chart(document.getElementById('chartTimeseries').getContext('2d'), {
      data: {
        labels: s.labels, datasets: [
          { type: 'line', label: 'Tx de conversión (%)', data: tx, borderColor: '#16A34A', backgroundColor: '#16A34A', borderWidth: 2, borderDash: [6, 3], cubicInterpolationMode: 'monotone', pointRadius: 2, pointHoverRadius: 5, spanGaps: true, yAxisID: 'yPct', order: 1 },
          { type: 'line', label: 'Reuniones', data: agend, borderColor: '#0B63FF', backgroundColor: '#0B63FF', borderWidth: 2.4, cubicInterpolationMode: 'monotone', pointRadius: 2, pointHoverRadius: 5, yAxisID: 'y', order: 2 },
          { type: 'line', label: 'Reuniones · media 4 sem.', data: mm4, borderColor: '#1E3A8A', backgroundColor: '#1E3A8A', borderWidth: 3, cubicInterpolationMode: 'monotone', pointRadius: 0, pointHoverRadius: 4, yAxisID: 'y', order: 2 },
        ],
      },
      options: {
        responsive: true, maintainAspectRatio: false, interaction: { mode: 'index', intersect: false },
        plugins: {
          legend: { position: 'top', align: 'end', labels: { font: { family: 'Inter', size: 13 }, color: '#374151', usePointStyle: true, pointStyle: 'rectRounded', padding: 16 } },
          tooltip: {
            backgroundColor: '#1F2937', padding: 12, cornerRadius: 8,
            callbacks: {
              label: (c) => c.dataset.yAxisID === 'yPct'
                ? `${c.dataset.label}: ${c.parsed.y == null ? '—' : c.parsed.y + '%'} (${agend[c.dataIndex]} de ${leads[c.dataIndex]} deals)`
                : `${c.dataset.label}: ${c.dataset.data === mm4 ? fDec(c.parsed.y) : c.parsed.y}`,
            },
          },
        },
        scales: {
          x: { ticks: { font: { family: 'Inter', size: 11 }, color: '#6B7280', maxRotation: 0, autoSkip: true, maxTicksLimit: 13 }, grid: { display: false } },
          y: { type: 'linear', position: 'left', beginAtZero: true, title: { display: true, text: 'Reuniones', font: { ...FONTE, weight: '600' }, color: '#4B5563' }, ticks: { font: FONTE, color: '#6B7280', precision: 0 }, grid: { color: '#F1F5F9' } },
          yPct: { type: 'linear', position: 'right', beginAtZero: true, suggestedMax: 100, title: { display: true, text: 'Tx de conversión (%)', font: { ...FONTE, weight: '600' }, color: '#16A34A' }, ticks: { callback: (v) => v + '%', font: FONTE, color: '#16A34A' }, grid: { display: false } },
        },
      },
    });
  }

  function chartMotivos(id, rows) {
    const el = document.getElementById(id);
    if (!el || !rows || !rows.length) return null;
    const total = totalMotivos(rows);
    const pct = (n) => `${Math.round((100 * n) / total)}%`;
    return new Chart(el.getContext('2d'), {
      type: 'doughnut',
      data: { labels: rows.map((r) => r.motivo), datasets: [{ data: rows.map((r) => r.n), backgroundColor: rows.map((_, i) => PIE_CORES[i % PIE_CORES.length]), borderColor: '#fff', borderWidth: 2 }] },
      options: {
        responsive: true, maintainAspectRatio: false, cutout: '52%',
        plugins: {
          legend: {
            position: 'bottom',
            labels: {
              font: FONTE, color: '#374151', usePointStyle: true, pointStyle: 'rectRounded', padding: 10,
              generateLabels: (ch) => Chart.overrides.doughnut.plugins.legend.labels.generateLabels(ch)
                .map((l, i) => Object.assign(l, { text: `${rows[i].motivo} · ${rows[i].n} (${pct(rows[i].n)})` })),
            },
          },
          tooltip: { backgroundColor: '#1F2937', padding: 12, cornerRadius: 8, callbacks: { label: (c) => ` ${c.label}: ${c.parsed} (${pct(c.parsed)})` } },
        },
      },
    });
  }

  function montarCharts(d) {
    if (typeof Chart === 'undefined') return;
    Object.values(_charts).forEach((c) => c && c.destroy());
    _charts = {
      ts: chartTendencia(d.serie),
      pp: chartMotivos('chartMotivosPeriodo', d.motivos_periodo),
      p12: chartMotivos('chartMotivos12m', d.motivos_12m),
    };
  }

  // ---------- SORTABLE ----------
  // Fecha en la celda viene como DD/MM: ordenar por el texto tomaba solo el dia ("03/10" -> 3).
  // Celda de fecha lleva data-sort=ISO; badge con fecha (✓ 03/10) cae en el parse DD/MM.
  function chaveCelula(td) {
    const t = (td?.innerText || '').trim();
    if (td && td.dataset.sort !== undefined) return { data: td.dataset.sort, t };
    const dm = t.match(/^(?:✓\s*)?(\d{1,2})\/(\d{1,2})(?:\/(\d{2,4}))?$/);
    if (dm) return { data: `${dm[3] || '0000'}-${dm[2].padStart(2, '0')}-${dm[1].padStart(2, '0')}`, t };
    return { data: null, t };
  }
  function compararCelulas(tdA, tdB, locale) {
    const a = chaveCelula(tdA), b = chaveCelula(tdB);
    if (a.data !== null && b.data !== null) return a.data < b.data ? -1 : a.data > b.data ? 1 : 0;
    const num = (s) => { const m = (s || '').match(/-?[\d.,]+/); return m ? parseFloat(m[0].replace(/\./g, '').replace(',', '.')) : NaN; };
    const na = num(a.t), nb = num(b.t);
    if (!isNaN(na) && !isNaN(nb)) return na - nb;
    return a.t.localeCompare(b.t, locale, { numeric: true, sensitivity: 'base' });
  }
  function makeSortable(table) {
    if (table.dataset.sortable === '1') return;
    const ths = table.querySelectorAll('thead th');
    ths.forEach((th, idx) => {
      if (th.textContent.trim() === '#') return;
      th.classList.add('sortable');
      if (!th.querySelector('.sort-ind')) {
        const ind = document.createElement('span'); ind.className = 'sort-ind'; ind.textContent = '⇅'; th.appendChild(ind);
      }
      th.addEventListener('click', () => {
        const tbody = table.querySelector('tbody'); if (!tbody) return;
        const rows = Array.from(tbody.querySelectorAll('tr'));
        const dir = th.classList.contains('sort-asc') ? 'desc' : 'asc';
        ths.forEach((t) => { t.classList.remove('sort-asc', 'sort-desc'); const i = t.querySelector('.sort-ind'); if (i) i.textContent = '⇅'; });
        th.classList.add(dir === 'asc' ? 'sort-asc' : 'sort-desc');
        const ind = th.querySelector('.sort-ind'); if (ind) ind.textContent = dir === 'asc' ? '▲' : '▼';
        rows.sort((a, b) => {
          const c = compararCelulas(a.children[idx], b.children[idx], 'es');
          return dir === 'asc' ? c : -c;
        });
        rows.forEach((r) => tbody.appendChild(r));
      });
    });
    table.dataset.sortable = '1';
  }

  return { render: render, montarCharts: montarCharts, makeSortable: makeSortable };
});
