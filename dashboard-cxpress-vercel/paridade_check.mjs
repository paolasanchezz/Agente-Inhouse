/* paridade_check.mjs — Cxpress: roda o motor.js sobre dados-cxpress.json nos mesmos
 * intervalos do paridade_esperado.json (gerado pela dash local) e compara numero a numero.
 * Sai com codigo 1 se houver qualquer divergencia.
 *
 * Uso:  node dashboard-cxpress-vercel/paridade_check.mjs
 */
import fs from 'node:fs';
import path from 'node:path';
import { createRequire } from 'node:module';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const require = createRequire(import.meta.url);
const M = require(path.join(HERE, 'motor.js'));
const D = JSON.parse(fs.readFileSync(path.join(HERE, 'dados-cxpress.json'), 'utf8'));
const E = JSON.parse(fs.readFileSync(path.join(HERE, 'paridade_esperado.json'), 'utf8'));

let checks = 0, fails = 0;
const diff = (ctx, a, b) => { checks++; if (a !== b) { fails++; console.log(`  DIFF ${ctx}: motor=${a} esperado=${b}`); } };
const KPIS = ['leads', 'triagem', 'agendamento', 'demo', 'proposta', 'fechamento', 'perd'];
const RK_MET = ['leads', 'triagem', 'agendamento', 'demo', 'proposta', 'fechamento'];
const LISTA_KEY = { leads: 'leads_semana', agend: 'agend_semana', demo: 'demo_semana', prop: 'prop_semana', fech: 'fech_semana', perdidos: 'perdidos_periodo' };

function cmpRank(nome, tag, got, exp) {
  const byDim = (arr) => Object.fromEntries(arr.map((r) => [r.dim, r]));
  const g = byDim(got), e = byDim(exp);
  for (const dim of new Set([...Object.keys(g), ...Object.keys(e)]))
    for (const k of RK_MET)
      diff(`${nome} ${tag}[${dim}].${k}`, (g[dim] || {})[k] || 0, (e[dim] || {})[k] || 0);
}

for (const nome of Object.keys(E)) {
  const e = E[nome];
  const d = M.montar(D, e.ini, e.fim); // KPI do intervalo = d.semana (periodo atual)
  for (const k of KPIS) diff(`${nome} kpi.${k}`, d.semana[k], e.kpis_atual[k]);
  if (e.listas_len)
    for (const k of Object.keys(e.listas_len)) diff(`${nome} listas.${k}.len`, d[LISTA_KEY[k]].length, e.listas_len[k]);
  if (e.rank_source) cmpRank(nome, 'rank_source', d.rk_src_semana, e.rank_source);
  if (e.rank_content) cmpRank(nome, 'rank_content', d.rk_ct_semana, e.rank_content);
}

console.log(`\n${'='.repeat(52)}`);
console.log(`Paridade Cxpress: ${checks} checagens · ${fails} divergencia(s)`);
console.log('='.repeat(52));
process.exit(fails ? 1 : 0);
