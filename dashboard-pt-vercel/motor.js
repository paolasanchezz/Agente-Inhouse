/* motor.js — Portugal: agrega a coorte no navegador. Sem banco, sem rede.
 *
 * Espelha o papel do motor.js das outras dashboards, mas com uma diferenca de
 * fundo que vem da auditoria (dashboard/AUDITORIA-PORTUGAL.md):
 *
 *   Em PT nenhum marco de funil tem data. Nao ha data de reuniao, de proposta
 *   nem de fecho, e nao existe historico de mudanca de etapa. A unica data
 *   confiavel e a de CRIACAO do deal.
 *
 * Por isso o periodo escolhido define uma COORTE (deals criados no intervalo) e
 * tudo o que se mostra e o estado ATUAL dessa coorte. Nao existe conversao entre
 * etapas aqui — seria inventar uma progressao que o dado nao registra.
 */
const MotorPT = (function () {
  'use strict';

  let DADOS = null;

  function carregar(d) { DADOS = d; return d; }

  function noIntervalo(deal, ini, fim) {
    const d = deal.d;
    return d && d >= ini && d <= fim;
  }

  function vazioRanking() { return []; }

  /** Agrega a coorte criada entre `ini` e `fim` (YYYY-MM-DD, inclusivos). */
  function agregar(ini, fim) {
    if (!DADOS) throw new Error('MotorPT: dados nao carregados');
    const coorte = DADOS.deals.filter((x) => noIntervalo(x, ini, fim));

    const terminais = new Set(DADOS.terminais || []);
    const ganhas = new Set(DADOS.ganhas || []);

    const kpis = {
      total: coorte.length,
      cm: 0, nao_cm: 0, sem_rastreio: 0,
      aberto: 0, ganho: 0, perdido: 0,
      inbound: 0, outbound: 0,
      valor_ganho: 0,
    };

    const porEtapa = new Map();
    const porFonte = new Map();
    const porPagina = new Map();
    const porMes = new Map();

    for (const x of coorte) {
      kpis[x.c] += 1;
      kpis[x.o] += 1;

      // Ganho: a etapa manda (o campo `status` quase nunca sai de 'Aberta' em PT —
      // 1 unico deal marcado 'Perdido' em toda a base), mas quando o status diz
      // 'Ganho' isso e informacao positiva e vale.
      const ehGanho = ganhas.has(x.e) || x.e === 'fecho' || x.s === 'Ganho';
      if (ehGanho) { kpis.ganho += 1; kpis.valor_ganho += x.v || 0; }
      else if (terminais.has(x.e)) kpis.perdido += 1;
      else kpis.aberto += 1;

      porEtapa.set(x.e, (porEtapa.get(x.e) || 0) + 1);

      const f = x.f || '(sem UTM)';
      const rf = porFonte.get(f) || { fonte: f, n: 0, cm: 0 };
      rf.n += 1; if (x.c === 'cm') rf.cm += 1;
      porFonte.set(f, rf);

      if (x.dom) {
        const chave = x.dom + (x.pa && x.pa !== '/' ? x.pa : '');
        const rp = porPagina.get(chave) || { pagina: chave, dom: x.dom, n: 0 };
        rp.n += 1;
        porPagina.set(chave, rp);
      }

      const mes = x.d.slice(0, 7);
      const rm = porMes.get(mes) || { mes, cm: 0, nao_cm: 0, sem_rastreio: 0, total: 0 };
      rm[x.c] += 1; rm.total += 1;
      porMes.set(mes, rm);
    }

    const rotulos = new Map(DADOS.etapas);
    const etapas = DADOS.etapas
      .map(([chave, rotulo]) => ({
        chave, rotulo,
        n: porEtapa.get(chave) || 0,
        pct: coorte.length ? (100 * (porEtapa.get(chave) || 0)) / coorte.length : 0,
      }))
      .filter((e) => e.n > 0);

    return {
      periodo: { ini, fim },
      gerado_em: DADOS.gerado_em,
      nome: DADOS.nome,
      moeda: DADOS.moeda || 'EUR',
      escopo: DADOS.escopo,
      kpis,
      etapas,
      rotuloEtapa: (c) => rotulos.get(c) || c,
      serie: [...porMes.values()].sort((a, b) => (a.mes < b.mes ? -1 : 1)),
      fontes: [...porFonte.values()].sort((a, b) => b.n - a.n),
      paginas: [...porPagina.values()].sort((a, b) => b.n - a.n),
      deals: coorte,
    };
  }

  /** Menor e maior data de criacao presentes — pra travar o date-picker. */
  function limites() {
    if (!DADOS || !DADOS.deals.length) return { min: null, max: null };
    const ds = DADOS.deals.map((x) => x.d).filter(Boolean);
    return { min: ds[0], max: ds[ds.length - 1] };
  }

  return { carregar, agregar, limites, vazioRanking };
})();

if (typeof module !== 'undefined' && module.exports) module.exports = MotorPT;
