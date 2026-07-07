/* motor.js — LATAM: agregacao CM no navegador (paridade com a dashboard-latam local).
 *
 * Recebe dados-latam.json (leads[] de inbound∪outbound + fech[] de contratos, ja no escopo CM)
 * e, pra um intervalo [ini,fim], produz o MESMO objeto `d` que o colher() Python devolvia.
 *
 * Funil de 5 fases: Leads -> Primer contacto (pc) -> Reunion -> Cierre (+ Perdido).
 * Sem regra 90d, sem dedup por pessoa. Fechamentos vem de tabela separada (fech[]).
 * dim do ranking = lower(coalesce(dim,'(vacío)')) — espelha queries_latam.q_ranking.
 * Perdidos: status='Perdido' + mdate no periodo; a LISTA de perdidos segue o MtD (== dash local).
 *
 * UMD: <script> no browser (window.MotorLatam) e require no Node (paridade).
 */
(function (root, factory) {
  if (typeof module !== 'undefined' && module.exports) module.exports = factory();
  else root.MotorLatam = factory();
})(typeof self !== 'undefined' ? self : this, function () {
  'use strict';

  function _d(iso) { return new Date(iso + 'T00:00:00Z'); }
  function _iso(d) { return d.toISOString().slice(0, 10); }
  function _addDays(iso, n) { const d = _d(iso); d.setUTCDate(d.getUTCDate() + n); return _iso(d); }
  function _diffDays(a, b) { return Math.round((_d(a) - _d(b)) / 86400000); }
  function _inRange(dt, ini, fim) { return dt != null && dt >= ini && dt <= fim; }
  function _cmp(a, b) { return a < b ? -1 : a > b ? 1 : 0; }
  function _norm(v) { return (v == null) ? '(vacío)' : String(v).toLowerCase(); } // lower(coalesce(dim,'(vacío)'))

  // Espelha dashboard-latam/server.py::calcular_periodos_range
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
      semanas_decorridas_ytd: Math.max(1, Math.floor(diasYtd / dias)),
      periodo_nome: periodoNome || 'Período',
    };
  }

  // ---------- KPIs (espelha q_count_kpis + q_count_perdidos + q_count_fechamentos) ----------
  function contarKpis(D, ini, fim) {
    const k = { leads: 0, pc: 0, reunion: 0, cierre: 0, valor: 0, perd: 0 };
    for (const r of D.leads) {
      if (_inRange(r.d_lead, ini, fim)) k.leads++;
      if (_inRange(r.d_ce, ini, fim)) k.pc++;
      if (_inRange(r.d_reunion, ini, fim)) k.reunion++;
      if (r.status === 'Perdido' && _inRange(r.d_mdate, ini, fim)) k.perd++;
    }
    for (const r of D.fech) {
      if (_inRange(r.d_fech, ini, fim)) { k.cierre++; k.valor += Number(r.valor) || 0; }
    }
    return k;
  }

  // ---------- listas ----------
  function listaLeads(D, ini, fim) {
    return D.leads.filter((r) => _inRange(r.d_lead, ini, fim))
      .map((r) => ({ id: r.id, deal: r.deal, utm_source: r.utm_source, utm_content: r.utm_content, pais: r.pais, responsable: r.responsable, data_conversao: r.d_lead }))
      .sort((a, b) => _cmp(a.data_conversao, b.data_conversao));
  }
  function listaReuniones(D, ini, fim) {
    return D.leads.filter((r) => _inRange(r.d_reunion, ini, fim))
      .map((r) => ({ id: r.id, deal: r.deal, utm_source: r.utm_source, utm_content: r.utm_content, pais: r.pais, responsable: r.responsable, data_evento: r.d_reunion }))
      .sort((a, b) => _cmp(a.data_evento, b.data_evento));
  }
  function listaCierres(D, ini, fim) {
    return D.fech.filter((r) => _inRange(r.d_fech, ini, fim))
      .map((r) => ({ id: r.id, deal: r.deal, utm_source: r.utm_source, utm_content: r.utm_content, pais: r.pais, responsable: r.responsable, valor: r.valor, currency: r.currency, data_fech: r.d_fech }))
      .sort((a, b) => _cmp(a.data_fech, b.data_fech));
  }
  // Perdidos: status='Perdido' + mdate no periodo, ORDER BY mdate (== q_lista_perdidos)
  function listaPerdidos(D, ini, fim) {
    return D.leads.filter((r) => r.status === 'Perdido' && _inRange(r.d_mdate, ini, fim))
      .map((r) => ({ id: r.id, deal: r.deal, utm_source: r.utm_source, utm_content: r.utm_content, pais: r.pais, data_evento: r.d_mdate }))
      .sort((a, b) => _cmp(a.data_evento, b.data_evento));
  }

  // ---------- ranking (espelha q_ranking: leads/pc/reunion da base + cierre de contratos) ----------
  function ranking(D, dimField, ini, fim) {
    const acc = new Map();
    const ensure = (k) => { if (!acc.has(k)) acc.set(k, { dim: k, leads: 0, pc: 0, reunion: 0, cierre: 0 }); return acc.get(k); };
    for (const r of D.leads) {
      const dv = _norm(r[dimField]);
      if (_inRange(r.d_lead, ini, fim)) ensure(dv).leads++;
      if (_inRange(r.d_ce, ini, fim)) ensure(dv).pc++;
      if (_inRange(r.d_reunion, ini, fim)) ensure(dv).reunion++;
    }
    for (const r of D.fech) {
      if (_inRange(r.d_fech, ini, fim)) ensure(_norm(r[dimField])).cierre++;
    }
    const rows = [...acc.values()];
    rows.sort((a, b) => b.leads - a.leads || b.cierre - a.cierre || b.reunion - a.reunion);
    return rows;
  }

  function srcMap(D, ini, fim) {
    const best = new Map(); // content(lower) -> {source, ts}
    for (const r of D.leads) {
      if (!_inRange(r.d_lead, ini, fim)) continue;
      const c = _norm(r.utm_content);
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
    const per = {
      semana: [p.ini_atual, p.fim_atual],
      sem_ant: [p.ini_ant, p.fim_ant],
      mtd: [p.mtd_ini, p.mtd_fim],
      ytd: [p.ytd_ini, p.ytd_fim],
    };
    const d = { periodos: p };
    for (const key in per) d[key] = contarKpis(D, per[key][0], per[key][1]);
    d.leads_semana = listaLeads(D, p.ini_atual, p.fim_atual);
    d.reuniones_semana = listaReuniones(D, p.ini_atual, p.fim_atual);
    d.cierres_semana = listaCierres(D, p.ini_atual, p.fim_atual);
    // A lista de perdidos segue o MtD (== dashboard-latam local: q_lista_perdidos(mtd_ini, mtd_fim)).
    d.perdidos_mtd = listaPerdidos(D, p.mtd_ini, p.mtd_fim);
    for (const key in per) {
      d['rk_src_' + key] = ranking(D, 'utm_source', per[key][0], per[key][1]);
      d['rk_ct_' + key] = ranking(D, 'utm_content', per[key][0], per[key][1]);
    }
    d.src_map = srcMap(D, p.ytd_ini, p.ytd_fim);
    d.serie = D.serie;
    d.proporcao = D.proporcao;
    return d;
  }

  return { calcularPeriodos: calcularPeriodos, contarKpis: contarKpis, ranking: ranking, montar: montar };
});
