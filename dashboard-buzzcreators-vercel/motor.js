/* motor.js — Buzzcreators: agregacao CM no navegador.
 *
 * Recebe dados-buzzcreators.json (uma linha por deal no escopo CM, com as datas de etapa) e,
 * pra um intervalo [ini,fim], produz o objeto `d` que o render consome.
 *
 * A logica CM (whitelist de utm_source, join deal->contato pra recuperar a atribuicao) NAO esta
 * aqui — ja veio resolvida no export (dashboard/queries_buzzcreators.py). Aqui so: derivar
 * periodos + filtrar por data de etapa + contar/agrupar.
 *
 * Funil: Lead · Agendamento · Reuniao realizada · Fechamento (+ Perdidos). Sem etapa Proposta —
 * o Pipedrive nao registra data de entrada em Proposta (decisao Victor 2026-08-26).
 * Sem dedup por e-mail: conta por deal (1 deal = 1 negociacao no pipeline Vendas Buzzcreators).
 *
 * UMD: funciona como <script> no browser (window.MotorBuzzcreators) e via require no Node (paridade).
 */
(function (root, factory) {
  if (typeof module !== 'undefined' && module.exports) module.exports = factory();
  else root.MotorBuzzcreators = factory();
})(typeof self !== 'undefined' ? self : this, function () {
  'use strict';

  // ---------- datas (comparacao por string ISO YYYY-MM-DD; aritmetica em UTC) ----------
  function _d(iso) { return new Date(iso + 'T00:00:00Z'); }
  function _iso(d) { return d.toISOString().slice(0, 10); }
  function _addDays(iso, n) { const d = _d(iso); d.setUTCDate(d.getUTCDate() + n); return _iso(d); }
  function _diffDays(a, b) { return Math.round((_d(a) - _d(b)) / 86400000); } // a - b
  function _inRange(dt, ini, fim) { return dt != null && dt >= ini && dt <= fim; }
  function _cmp(a, b) { return a < b ? -1 : a > b ? 1 : 0; }

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
      // divisor da media YtD: quantos periodos do tamanho escolhido cabem no ano corrido
      semanas_decorridas_ytd: Math.max(1, Math.floor(diasYtd / dias)),
      periodo_nome: periodoNome || 'Período',
    };
  }

  // Perdido = coorte: lead criado no periodo + lost preenchido + status 'lost'.
  // O motivo (lost_reason) NAO entra na condicao: 2.302 dos 2.409 deals perdidos tem motivo,
  // e exigir motivo esconderia ~4% das perdas reais. Ele so aparece na coluna da lista.
  function _isPerd(r) {
    return r.d_lost != null && r.status === 'lost';
  }

  // ---------- KPIs ----------
  function contarKpis(deals, ini, fim) {
    const k = { leads: 0, agendamento: 0, reuniao: 0, fechamento: 0, perd: 0 };
    for (const r of deals) {
      if (_inRange(r.d_lead, ini, fim)) k.leads++;
      if (_inRange(r.d_agendamento, ini, fim)) k.agendamento++;
      if (_inRange(r.d_reuniao, ini, fim)) k.reuniao++;
      if (_inRange(r.d_fechamento, ini, fim)) k.fechamento++;
      if (_inRange(r.d_lead, ini, fim) && _isPerd(r)) k.perd++;
    }
    return k;
  }

  // ---------- listas de exibicao (periodo atual) ----------
  function _base(r) {
    return {
      id: r.id, deal: r.deal, utm_source: r.utm_source, utm_content: r.utm_content,
      url_conversao: r.url_conversao, responsavel: r.responsavel, funil: r.funil,
    };
  }
  function listaLeads(deals, ini, fim) {
    return deals.filter((r) => _inRange(r.d_lead, ini, fim))
      .map((r) => Object.assign(_base(r), { data_evento: r.d_lead, data_agendamento: r.d_agendamento }))
      .sort((a, b) => _cmp(a.data_evento, b.data_evento));
  }
  function listaAgend(deals, ini, fim) {
    return deals.filter((r) => _inRange(r.d_agendamento, ini, fim))
      .map((r) => Object.assign(_base(r), { data_evento: r.d_agendamento, data_reuniao: r.d_reuniao }))
      .sort((a, b) => _cmp(a.data_evento, b.data_evento));
  }
  function listaReuniao(deals, ini, fim) {
    return deals.filter((r) => _inRange(r.d_reuniao, ini, fim))
      .map((r) => Object.assign(_base(r), {
        data_evento: r.d_reuniao, data_fechamento: r.d_fechamento, etapa_atual: r.etapa_atual,
      }))
      .sort((a, b) => _cmp(a.data_evento, b.data_evento));
  }
  function listaFech(deals, ini, fim) {
    return deals.filter((r) => _inRange(r.d_fechamento, ini, fim))
      .map((r) => Object.assign(_base(r), { data_evento: r.d_fechamento, valor: r.valor, currency: r.currency }))
      .sort((a, b) => _cmp(a.data_evento, b.data_evento));
  }
  // Perdidos: coorte por d_lead, ORDER BY d_lost DESC
  function listaPerdidos(deals, ini, fim) {
    return deals.filter((r) => _inRange(r.d_lead, ini, fim) && _isPerd(r))
      .map((r) => Object.assign(_base(r), {
        motivo: r.motivo, etapa_atual: r.etapa_atual, data_evento: r.d_lost,
        ultima_etapa: r.d_reuniao || r.d_agendamento || r.d_lead,
      }))
      .sort((a, b) => _cmp(b.data_evento, a.data_evento));
  }

  // ---------- rankings (COALESCE(dim,'(vazio)'), conta por data de etapa) ----------
  const _RK_MET = ['leads', 'agendamento', 'reuniao', 'fechamento'];
  function ranking(deals, dimField, ini, fim) {
    const acc = new Map();
    const ensure = (k) => {
      if (!acc.has(k)) acc.set(k, { dim: k, leads: 0, agendamento: 0, reuniao: 0, fechamento: 0 });
      return acc.get(k);
    };
    for (const r of deals) {
      const dv = (r[dimField] == null || r[dimField] === '') ? '(vazio)' : r[dimField];
      if (_inRange(r.d_lead, ini, fim)) ensure(dv).leads++;
      if (_inRange(r.d_agendamento, ini, fim)) ensure(dv).agendamento++;
      if (_inRange(r.d_reuniao, ini, fim)) ensure(dv).reuniao++;
      if (_inRange(r.d_fechamento, ini, fim)) ensure(dv).fechamento++;
    }
    const rows = [...acc.values()].filter((r) => _RK_MET.some((m) => r[m] > 0));
    rows.sort((a, b) => b.leads - a.leads || b.fechamento - a.fechamento || b.reuniao - a.reuniao);
    return rows;
  }

  // src_map: por content (chave crua), o utm_source do lead mais recente no YtD.
  function srcMap(deals, ini, fim) {
    const best = new Map();
    for (const r of deals) {
      if (!_inRange(r.d_lead, ini, fim)) continue;
      const c = (r.utm_content == null || r.utm_content === '') ? '(vazio)' : r.utm_content;
      const cur = best.get(c);
      if (!cur || r.d_lead > cur.ts) best.set(c, { source: r.utm_source, ts: r.d_lead });
    }
    const map = {};
    for (const [c, v] of best) map[c] = v.source;
    return map;
  }

  // ---------- montar o objeto `d` do render ----------
  function montar(D, ini, fim, hoje, periodoNome) {
    const p = calcularPeriodos(ini, fim, hoje || D.gerado_em, periodoNome);
    const deals = D.deals;
    const per = {
      semana: [p.ini_atual, p.fim_atual],
      sem_ant: [p.ini_ant, p.fim_ant],
      mtd: [p.mtd_ini, p.mtd_fim],
      ytd: [p.ytd_ini, p.ytd_fim],
    };
    const d = { periodos: p, cobertura: D.cobertura || null };
    for (const key in per) d[key] = contarKpis(deals, per[key][0], per[key][1]);
    d.leads_semana = listaLeads(deals, p.ini_atual, p.fim_atual);
    d.agend_semana = listaAgend(deals, p.ini_atual, p.fim_atual);
    d.reuniao_semana = listaReuniao(deals, p.ini_atual, p.fim_atual);
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
