/* motor.js - agregacao CM no navegador (paridade com dashboard-pessoal Python).
 *
 * Recebe o dados-2026.json (eventos CM ja carimbados pela queries.py) e, pra um
 * intervalo [ini,fim], produz o MESMO objeto `data` que o coletar()/api Python
 * devolvia - pra o render() do index.html consumir sem mudanca.
 *
 * A logica CM (filtro, regra 90d, coorte) NAO esta aqui - ja veio resolvida no
 * export. Aqui so ha: derivar periodos + filtrar por data + contar/dedup/agrupar.
 * Espelha lib/datas.py (calcular_periodos) e lib/queries.py (counts/listas/rankings).
 * Validado por paridade_check.mjs (916 checagens, 0 divergencias).
 *
 * UMD: funciona como <script> no browser (window.MotorCM) e via require no Node.
 */
(function (root, factory) {
  if (typeof module !== 'undefined' && module.exports) module.exports = factory();
  else root.MotorCM = factory();
})(typeof self !== 'undefined' ? self : this, function () {
  'use strict';

  // ---------- datas (comparacao por string ISO YYYY-MM-DD; aritmetica em UTC) ----------
  function _d(iso) { return new Date(iso + 'T00:00:00Z'); }
  function _iso(d) { return d.toISOString().slice(0, 10); }
  function _addDays(iso, n) { const d = _d(iso); d.setUTCDate(d.getUTCDate() + n); return _iso(d); }
  function _diffDays(a, b) { return Math.round((_d(a) - _d(b)) / 86400000); } // a - b
  function _inRange(dt, ini, fim) { return dt != null && dt >= ini && dt <= fim; }
  function _email(e) { return (e || '').trim().toLowerCase(); }
  // Chave de dedup de Leads/Perdidos — espelha queries.py::_chave_lead: deal sem email vira lead proprio pelo id.
  function _chaveLead(r) { return _email(r.email) || ('id:' + r.id); }

  // Espelha lib/datas.py::calcular_periodos
  function calcularPeriodos(ini, fim, hoje) {
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
      periodos_decorridos_ytd: Math.max(1, Math.floor(diasYtd / dias)),
    };
  }

  // ---------- KPIs (espelha q_count_*) ----------
  function contarKpis(D, ini, fim) {
    const leadEmails = new Set();
    for (const r of D.leads) if (_inRange(r.data, ini, fim)) leadEmails.add(_chaveLead(r)); // distinct email (sem email: id), cdate efetivo
    const cnt = (arr) => { let n = 0; for (const r of arr) if (_inRange(r.data, ini, fim)) n++; return n; };
    const perdEmails = new Set();
    for (const r of D.perdidos) if (_inRange(r.cdate, ini, fim)) perdEmails.add(_chaveLead(r)); // coorte por cdate
    return {
      leads: leadEmails.size,
      ce: cnt(D.ce), ra: cnt(D.ra), rr: cnt(D.rr), prop: cnt(D.prop), fech: cnt(D.fech),
      perd: perdEmails.size,
    };
  }

  // ---------- listas de exibicao ----------
  // Leads: dedup por email (mais recente por cdate cru - espelha DISTINCT ON ... ORDER BY d.cdate DESC)
  function listaLeads(D, ini, fim) {
    const byEmail = new Map();
    for (const r of D.leads) {
      if (!_inRange(r.data, ini, fim)) continue;
      const e = _chaveLead(r);
      const cur = byEmail.get(e);
      if (!cur || r.cdate_cru > cur.cdate_cru) byEmail.set(e, r);
    }
    return [...byEmail.values()]
      .map((r) => ({ id: r.id, deal: r.deal, email: r.email, utm_source: r.utm_source, utm_content: r.utm_content, data_conversao: r.data, bd: r.bd, _ts: r.ts }))
      .sort((a, b) => (a._ts < b._ts ? -1 : a._ts > b._ts ? 1 : 0));
  }

  // ce/ra/rr/prop/fech: filtra por data, renomeia data->data_evento (mantem extras: valor, valor_text, data_realizada, data_proposta)
  function listaEvento(arr, ini, fim) {
    return arr.filter((r) => _inRange(r.data, ini, fim))
      .map((r) => Object.assign({}, r, { data_evento: r.data }))
      .sort((a, b) => (a.data < b.data ? -1 : a.data > b.data ? 1 : 0));
  }

  // Perdidos: coorte por cdate, dedup por email (mais recente por data_perda)
  function listaPerdidos(D, ini, fim) {
    const byEmail = new Map();
    for (const r of D.perdidos) {
      if (!_inRange(r.cdate, ini, fim)) continue;
      const e = _chaveLead(r);
      const cur = byEmail.get(e);
      if (!cur || r.data_perda > cur.data_perda) byEmail.set(e, r);
    }
    return [...byEmail.values()]
      .map((r) => ({ id: r.id, deal: r.deal, email: r.email, utm_source: r.utm_source, utm_content: r.utm_content, ultima_conversao: r.ultima_conversao, motivo: r.motivo }))
      .sort((a, b) => (a.data_perda < b.data_perda ? 1 : a.data_perda > b.data_perda ? -1 : 0));
  }

  // ---------- rankings (espelha q_ranking) ----------
  // src_map: por utm_content, o utm_source mais frequente entre leads no periodo (cdate cru) - q_source_por_content
  function srcMap(D, ini, fim) {
    const counts = new Map(); // content -> Map(source -> n)
    for (const r of D.leads) {
      if (!_inRange(r.cdate_cru, ini, fim)) continue;
      if (r.utm_content == null) continue;
      if (!counts.has(r.utm_content)) counts.set(r.utm_content, new Map());
      const inner = counts.get(r.utm_content);
      inner.set(r.utm_source, (inner.get(r.utm_source) || 0) + 1);
    }
    const map = {};
    for (const [content, srcs] of counts) {
      let best = null, bestN = -1;
      for (const [s, n] of srcs) if (n > bestN) { bestN = n; best = s; }
      map[content] = best;
    }
    return map;
  }

  function ranking(D, dimField, ini, fim, srcMapObj) {
    const acc = new Map();
    const ensure = (k) => { if (!acc.has(k)) acc.set(k, { dim: k, leads: 0, ce: 0, ra: 0, rr: 0, prop: 0, fech: 0 }); return acc.get(k); };
    // dim NULL some do ranking - espelha o LEFT JOIN USING(dim) da dash (NULL nao casa em JOIN)
    const add = (arr, field, dateField) => {
      for (const r of arr) {
        const dv = r[dimField];
        if (dv == null) continue;
        if (_inRange(r[dateField], ini, fim)) ensure(dv)[field]++;
      }
    };
    add(D.leads, 'leads', 'cdate_cru'); // leads: cdate cru, count(*)
    add(D.ce, 'ce', 'data');
    add(D.ra, 'ra', 'data');
    add(D.rr, 'rr', 'data');
    add(D.prop, 'prop', 'data');
    add(D.fech, 'fech', 'data');
    const rows = [...acc.values()].sort((a, b) => b.leads - a.leads || b.ra - a.ra); // ORDER BY leads DESC, ra DESC
    if (srcMapObj) for (const r of rows) r.source = srcMapObj[r.dim] || null;
    return rows;
  }

  // ---------- motivos de perda (graficos de pizza) ----------
  // Top 8 motivos + "Outros"; deal sem motivo vira categoria propria (nao some do total).
  const MOTIVOS_TOP = 8;
  function agruparMotivos(lista) {
    const acc = new Map();
    for (const r of lista) {
      const m = (r.motivo != null && String(r.motivo).trim()) || '(sem motivo)';
      acc.set(m, (acc.get(m) || 0) + 1);
    }
    const rows = [...acc.entries()].map(([motivo, n]) => ({ motivo, n }))
      .sort((a, b) => b.n - a.n || (a.motivo < b.motivo ? -1 : 1));
    if (rows.length <= MOTIVOS_TOP + 1) return rows;
    const resto = rows.slice(MOTIVOS_TOP);
    return rows.slice(0, MOTIVOS_TOP).concat([{ motivo: `Outros (${resto.length})`, n: resto.reduce((t, r) => t + r.n, 0) }]);
  }
  // Janela fixa do grafico de tendencia: 52 semanas fechadas na segunda (== colher_serie do export) ate hoje.
  function janelaSerie(hoje) {
    const dow = (_d(hoje).getUTCDay() + 6) % 7; // 0 = segunda
    return [_addDays(hoje, -dow - 51 * 7), hoje];
  }

  // ---------- montar o objeto `data` do render() ----------
  function montarData(D, ini, fim) {
    const p = calcularPeriodos(ini, fim, D.gerado_em);
    const per = { atual: [p.ini_atual, p.fim_atual], ant: [p.ini_ant, p.fim_ant], mtd: [p.mtd_ini, p.mtd_fim], ytd: [p.ytd_ini, p.ytd_fim] };
    const kpis = {}, rSource = {}, rContent = {};
    const sm = srcMap(D, p.ytd_ini, p.ytd_fim);
    const j12 = janelaSerie(p.hoje);
    for (const k in per) {
      kpis[k] = contarKpis(D, per[k][0], per[k][1]);
      rSource[k] = ranking(D, 'utm_source', per[k][0], per[k][1], null);
      rContent[k] = ranking(D, 'utm_content', per[k][0], per[k][1], sm);
    }
    return {
      periodos: p,
      kpis: kpis,
      listas: {
        leads: listaLeads(D, p.ini_atual, p.fim_atual),
        ra: listaEvento(D.ra, p.ini_atual, p.fim_atual),
        rr: listaEvento(D.rr, p.ini_atual, p.fim_atual),
        prop: listaEvento(D.prop, p.ini_atual, p.fim_atual),
        fech: listaEvento(D.fech, p.ini_atual, p.fim_atual),
        perdidos_mtd: listaPerdidos(D, p.ini_atual, p.fim_atual), // segue o periodo do filtro (nao so o MtD) — Victor 2026-07-01
      },
      rankings: { source: rSource, content: rContent },
      janela_12m: j12,
      motivos_periodo: agruparMotivos(listaPerdidos(D, p.ini_atual, p.fim_atual)),
      motivos_12m: agruparMotivos(listaPerdidos(D, j12[0], j12[1])),
      serie_12m: D.serie_12m,
      _meta: { estatico: true, gerado_em: D.gerado_em },
    };
  }

  return { calcularPeriodos: calcularPeriodos, montarData: montarData };
});
