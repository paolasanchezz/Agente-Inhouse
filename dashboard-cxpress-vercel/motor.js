/* motor.js — Cxpress: agregacao CM no navegador (paridade com a dashboard-cxpress local).
 *
 * Recebe dados-cxpress.json (uma linha por deal no escopo CM, com as 7 datas de etapa) e,
 * pra um intervalo [ini,fim], produz o MESMO objeto `d` que o colher() Python devolvia —
 * pro render (port de render_html) consumir sem mudanca de estrutura.
 *
 * A logica CM (filtro_cm calibrado, escopo) NAO esta aqui — ja veio resolvida no export.
 * Aqui so: derivar periodos + filtrar por data de etapa + contar/agrupar. Sem dedup por email
 * (a tabela Cxpress nao tem e-mail — conta por deal, igual as q_count_* de queries_cxpress.py).
 * Espelha dashboard-cxpress/server.py::calcular_periodos_range e dashboard/queries_cxpress.py.
 *
 * UMD: funciona como <script> no browser (window.MotorCxpress) e via require no Node (paridade).
 */
(function (root, factory) {
  if (typeof module !== 'undefined' && module.exports) module.exports = factory();
  else root.MotorCxpress = factory();
})(typeof self !== 'undefined' ? self : this, function () {
  'use strict';

  // ---------- datas (comparacao por string ISO YYYY-MM-DD; aritmetica em UTC) ----------
  function _d(iso) { return new Date(iso + 'T00:00:00Z'); }
  function _iso(d) { return d.toISOString().slice(0, 10); }
  function _addDays(iso, n) { const d = _d(iso); d.setUTCDate(d.getUTCDate() + n); return _iso(d); }
  function _diffDays(a, b) { return Math.round((_d(a) - _d(b)) / 86400000); } // a - b
  function _inRange(dt, ini, fim) { return dt != null && dt >= ini && dt <= fim; }
  function _cmp(a, b) { return a < b ? -1 : a > b ? 1 : 0; }

  // Espelha dashboard-cxpress/server.py::calcular_periodos_range
  function calcularPeriodos(ini, fim, hoje, periodoNome) {
    const dias = _diffDays(fim, ini) + 1;
    const fimD = _d(fim);
    const y = fimD.getUTCFullYear(), m = fimD.getUTCMonth();
    const mtd_ini = _iso(new Date(Date.UTC(y, m, 1)));
    const ytd_ini = _iso(new Date(Date.UTC(y, 0, 1)));
    const diasYtd = _diffDays(fim, ytd_ini) + 1;
    return {
      hoje: hoje,
      ini_atual: ini, fim_atual: fim,
      ini_ant: _addDays(ini, -dias), fim_ant: _addDays(ini, -1),
      mtd_ini: mtd_ini, mtd_fim: fim,
      ytd_ini: ytd_ini, ytd_fim: fim,
      dias_periodo: dias,
      // render_html usa 'semanas_decorridas_ytd' como divisor da media (== server.py local)
      semanas_decorridas_ytd: Math.max(1, Math.floor(diasYtd / dias)),
      periodo_nome: periodoNome || 'Período',
    };
  }

  // Perdido = coorte: lead criado no periodo + lost preenchido + motivo + status 'Perdido'
  // (espelha q_count_kpis / q_lista_perdidos).
  function _isPerd(r) {
    return r.d_lost != null &&
      r.motivo != null && String(r.motivo).trim() !== '' &&
      r.status === 'Perdido';
  }

  // ---------- KPIs (espelha q_count_kpis) ----------
  function contarKpis(deals, ini, fim) {
    const k = { leads: 0, triagem: 0, agendamento: 0, demo: 0, proposta: 0, fechamento: 0, perd: 0 };
    for (const r of deals) {
      if (_inRange(r.d_lead, ini, fim)) k.leads++;
      if (_inRange(r.d_triagem, ini, fim)) k.triagem++;
      if (_inRange(r.d_agendamento, ini, fim)) k.agendamento++;
      if (_inRange(r.d_demo, ini, fim)) k.demo++;
      if (_inRange(r.d_proposta, ini, fim)) k.proposta++;
      if (_inRange(r.d_fechamento, ini, fim)) k.fechamento++;
      if (_inRange(r.d_lead, ini, fim) && _isPerd(r)) k.perd++;
    }
    return k;
  }

  // ---------- listas de exibicao (periodo atual) ----------
  function listaLeads(deals, ini, fim) {
    return deals.filter((r) => _inRange(r.d_lead, ini, fim))
      .map((r) => ({ id: r.id, deal: r.deal, utm_source: r.utm_source, utm_content: r.utm_content, responsavel: r.responsavel, data_evento: r.d_lead }))
      .sort((a, b) => _cmp(a.data_evento, b.data_evento)); // ORDER BY cdate ASC
  }
  function listaAgend(deals, ini, fim) {
    return deals.filter((r) => _inRange(r.d_agendamento, ini, fim))
      .map((r) => ({ id: r.id, deal: r.deal, utm_source: r.utm_source, utm_content: r.utm_content, responsavel: r.responsavel, data_evento: r.d_agendamento, data_demo: r.d_demo }))
      .sort((a, b) => _cmp(a.data_evento, b.data_evento));
  }
  function listaDemo(deals, ini, fim) {
    return deals.filter((r) => _inRange(r.d_demo, ini, fim))
      .map((r) => ({ id: r.id, deal: r.deal, utm_source: r.utm_source, utm_content: r.utm_content, responsavel: r.responsavel, data_evento: r.d_demo, data_proposta: r.d_proposta }))
      .sort((a, b) => _cmp(a.data_evento, b.data_evento));
  }
  function listaProp(deals, ini, fim) {
    return deals.filter((r) => _inRange(r.d_proposta, ini, fim))
      .map((r) => ({ id: r.id, deal: r.deal, utm_source: r.utm_source, utm_content: r.utm_content, responsavel: r.responsavel, data_evento: r.d_proposta, valor_text: r.valor_text, currency: r.currency }))
      .sort((a, b) => _cmp(a.data_evento, b.data_evento));
  }
  function listaFech(deals, ini, fim) {
    return deals.filter((r) => _inRange(r.d_fechamento, ini, fim))
      .map((r) => ({ id: r.id, deal: r.deal, utm_source: r.utm_source, utm_content: r.utm_content, responsavel: r.responsavel, data_evento: r.d_fechamento, valor_text: r.valor_text, currency: r.currency }))
      .sort((a, b) => _cmp(a.data_evento, b.data_evento));
  }
  // Perdidos: coorte por d_lead, ORDER BY d_lost DESC (espelha q_lista_perdidos)
  function listaPerdidos(deals, ini, fim) {
    return deals.filter((r) => _inRange(r.d_lead, ini, fim) && _isPerd(r))
      .map((r) => ({
        id: r.id, deal: r.deal, utm_source: r.utm_source, utm_content: r.utm_content,
        motivo: r.motivo, etapa: r.etapa, data_evento: r.d_lost,
        ultima_conversao: r.d_demo || r.d_agendamento || r.d_triagem || r.d_lead, // COALESCE
      }))
      .sort((a, b) => _cmp(b.data_evento, a.data_evento));
  }

  // ---------- rankings (espelha q_ranking: COALESCE(dim,'(vazio)'), conta por data de etapa) ----------
  const _RK_MET = ['leads', 'triagem', 'agendamento', 'demo', 'proposta', 'fechamento'];
  function ranking(deals, dimField, ini, fim) {
    const acc = new Map();
    const ensure = (k) => { if (!acc.has(k)) acc.set(k, { dim: k, leads: 0, triagem: 0, agendamento: 0, demo: 0, proposta: 0, fechamento: 0 }); return acc.get(k); };
    for (const r of deals) {
      const dv = (r[dimField] == null) ? '(vazio)' : r[dimField]; // COALESCE (null CONTA como '(vazio)')
      if (_inRange(r.d_lead, ini, fim)) ensure(dv).leads++;
      if (_inRange(r.d_triagem, ini, fim)) ensure(dv).triagem++;
      if (_inRange(r.d_agendamento, ini, fim)) ensure(dv).agendamento++;
      if (_inRange(r.d_demo, ini, fim)) ensure(dv).demo++;
      if (_inRange(r.d_proposta, ini, fim)) ensure(dv).proposta++;
      if (_inRange(r.d_fechamento, ini, fim)) ensure(dv).fechamento++;
    }
    // HAVING (>0 em alguma metrica) — garantido pois so criamos entry quando alguma data cai no range
    const rows = [...acc.values()].filter((r) => _RK_MET.some((m) => r[m] > 0));
    rows.sort((a, b) => b.leads - a.leads || b.fechamento - a.fechamento || b.demo - a.demo);
    return rows;
  }

  // src_map: por content (chave crua), o utm_source do lead mais recente no YtD (q_source_por_content).
  function srcMap(deals, ini, fim) {
    const best = new Map(); // content -> {source, ts}
    for (const r of deals) {
      if (!_inRange(r.d_lead, ini, fim)) continue;
      const c = (r.utm_content == null) ? '(vazio)' : r.utm_content;
      const cur = best.get(c);
      if (!cur || r.d_lead > cur.ts) best.set(c, { source: r.utm_source, ts: r.d_lead });
    }
    const map = {};
    for (const [c, v] of best) map[c] = v.source;
    return map;
  }

  // ---------- montar o objeto `d` do render (espelha colher()) ----------
  function montar(D, ini, fim, hoje, periodoNome) {
    const p = calcularPeriodos(ini, fim, hoje || D.gerado_em, periodoNome);
    const deals = D.deals;
    const per = {
      semana: [p.ini_atual, p.fim_atual],
      sem_ant: [p.ini_ant, p.fim_ant],
      mtd: [p.mtd_ini, p.mtd_fim],
      ytd: [p.ytd_ini, p.ytd_fim],
    };
    const d = { periodos: p };
    for (const key in per) d[key] = contarKpis(deals, per[key][0], per[key][1]);
    d.leads_semana = listaLeads(deals, p.ini_atual, p.fim_atual);
    d.agend_semana = listaAgend(deals, p.ini_atual, p.fim_atual);
    d.demo_semana = listaDemo(deals, p.ini_atual, p.fim_atual);
    d.prop_semana = listaProp(deals, p.ini_atual, p.fim_atual);
    d.fech_semana = listaFech(deals, p.ini_atual, p.fim_atual);
    d.perdidos_periodo = listaPerdidos(deals, p.ini_atual, p.fim_atual);
    for (const key in per) {
      d['rk_src_' + key] = ranking(deals, 'utm_source', per[key][0], per[key][1]);
      d['rk_ct_' + key] = ranking(deals, 'utm_content', per[key][0], per[key][1]);
    }
    d.src_map = srcMap(deals, p.ytd_ini, p.ytd_fim);
    d.serie = D.serie;
    d.proporcao = D.proporcao;
    return d;
  }

  return { calcularPeriodos: calcularPeriodos, contarKpis: contarKpis, ranking: ranking, montar: montar };
});
