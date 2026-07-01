/* paridade_check.mjs — roda o motor.js sobre dados-2026.json nos mesmos intervalos
 * do paridade_esperado.json (gerado pela dash local) e compara numero a numero.
 * Sai com codigo 1 se houver qualquer divergencia.
 *
 * Uso:  node dashboard-buzz-br-vercel/paridade_check.mjs
 */
import fs from 'node:fs';
import path from 'node:path';
import { createRequire } from 'node:module';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const require = createRequire(import.meta.url);
const M = require(path.join(HERE, 'motor.js'));
const D = JSON.parse(fs.readFileSync(path.join(HERE, 'dados-2026.json'), 'utf8'));
const E = JSON.parse(fs.readFileSync(path.join(HERE, 'paridade_esperado.json'), 'utf8'));

let checks = 0, fails = 0;
const diff = (ctx, a, b) => { checks++; if (a !== b) { fails++; console.log(`  DIFF ${ctx}: motor=${a} esperado=${b}`); } };
const KPIS = ['leads', 'ce', 'ra', 'rr', 'prop', 'fech', 'perd'];

function cmpRank(nome, tag, got, exp) {
  const byDim = (arr) => Object.fromEntries(arr.map((r) => [r.dim, r]));
  const g = byDim(got), e = byDim(exp);
  for (const dim of new Set([...Object.keys(g), ...Object.keys(e)]))
    for (const k of ['leads', 'ce', 'ra', 'rr', 'prop', 'fech'])
      diff(`${nome} ${tag}[${dim}].${k}`, (g[dim] || {})[k] || 0, (e[dim] || {})[k] || 0);
}

for (const nome of Object.keys(E)) {
  const e = E[nome];
  const data = M.montarData(D, e.ini, e.fim);
  // KPI do intervalo = kpis.atual do motor
  for (const k of KPIS) diff(`${nome} kpi.${k}`, data.kpis.atual[k], e.kpis_atual[k]);
  // extras (so no ytd): listas e rankings
  if (e.listas_len)
    for (const k of Object.keys(e.listas_len)) diff(`${nome} listas.${k}.len`, data.listas[k].length, e.listas_len[k]);
  if (e.rank_source) cmpRank(nome, 'rank_source', data.rankings.source.atual, e.rank_source);
  if (e.rank_content) cmpRank(nome, 'rank_content', data.rankings.content.atual, e.rank_content);
}

console.log(`\n${'='.repeat(52)}`);
console.log(`Paridade: ${checks} checagens · ${fails} divergencia(s)`);
console.log('='.repeat(52));
process.exit(fails ? 1 : 0);
