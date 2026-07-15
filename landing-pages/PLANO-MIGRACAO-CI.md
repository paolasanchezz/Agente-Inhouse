# PLANO — Migração do deploy de LPs para Git + CI

> **Status:** proposta aprovada em conceito por Victor (2026-07-15), aguardando execução.
> **Objetivo:** eliminar por construção a classe de incidente "deploy de uma pessoa apaga a LP de outra" (§7.2 do CONTEXT.md — 2026-05-07, 05-08, 05-11, 05-13, 06-16), trocando o modelo *sibling local → deploy da máquina* pelo modelo *Git como fonte de verdade → deploy exclusivo via GitHub Actions*.
> **Escopo v1:** guarda-chuvas Vercel (`content.cxpress.io`, `webinar.buzzmonitor.com`, `evento.buzzmonitor.com`, `material.buzzmonitor.com`). Projetos solo e Webflow ficam fora (ver §9).

---

## 1. Arquitetura alvo

```
Pessoa (marketing) ──► skill lp-* edita source ──► /lp-publicar v4:
                                                     1. git pull --rebase
                                                     2. atualiza manifesto do domínio
                                                     3. abre PR (branch claude/{slug})
                                                     └─► GitHub Actions:
                                                           a. valida (build + isolamento + paths)
                                                           b. deploy PREVIEW → comenta URL no PR
                                                           c. paths só-LP + checks OK → merge-bot mergeia
                                                           d. push na main → build da MAIN INTEIRA
                                                           e. vercel deploy --prebuilt --prod (token só no CI)
                                                           f. smoke test em TODAS as URLs do manifesto
                                                           g. falhou → rollback automático + alerta
```

Componentes novos (todos no repo atual — **não** há repo separado):

| Componente | Caminho | Papel |
|---|---|---|
| Manifesto por domínio | `landing-pages/dominios/{dominio}.json` | Estado declarado do ar: slugs ativos, marca de cada um, redirects, CSP extra, projeto Vercel. Publicar = entrar no manifesto; despublicar = sair. |
| Script de build | `landing-pages/build/build_umbrella.py` | Determinístico, stdlib-only: manifesto + sources → `dist/{dominio}/`. Absorve os Passos 1.3–1.6 da lp-publicar (cópia seletiva de assets, namespace `/assets/{marca}/`, rewrite de paths, placeholders `{{DOMAIN}}`/`{{OG_IMAGE_PATH}}`/`{{BRAND_LOGO_PNG_PATH}}`, remoção de sufixos `[REVISADO]`/`[TESTE]`/`[DRAFT]`, geração do `vercel.json` = template + redirects/CSP-extra do manifesto). |
| Workflow de deploy | `.github/workflows/lp-deploy.yml` | Trigger: push na main tocando `landing-pages/**` ou `brand/*/assets/**`. Detecta domínios afetados, builda, deploya `--prebuilt`, smoke-testa, rollback se falhar. `concurrency: lp-deploy-{dominio}` serializa. |
| Workflow de PR | `.github/workflows/lp-pr.yml` | Trigger: PR. Roda validações + deploy preview + comenta URL. Se todos os arquivos do diff ∈ paths livres e checks verdes → auto-merge (squash) via `gh pr merge`. Senão, rotula `precisa-revisao-victor` e para. |
| Secret | `VERCEL_TOKEN` (GitHub Actions secret) | Token org elife-group. Ao final da migração, é a ÚNICA credencial Vercel de deploy existente. |

### 1.1 Schema do manifesto (proposta)

```json
{
  "dominio": "content.cxpress.io",
  "projeto_vercel": "cxpress-lp-playbook-whatsapp2026",
  "lps": [
    { "slug": "playbook-whatsapp2026", "marca": "cxpress", "source": "landing-pages/cxpress/playbook-whatsapp2026" },
    { "slug": "livraria",              "marca": "cxpress", "source": "landing-pages/cxpress/livraria" }
  ],
  "redirects": [
    { "source": "/exemplo-antigo", "destination": "/exemplo-novo", "permanent": true }
  ],
  "csp_extra": { "frame-src": ["https://provedor-custom.example"] }
}
```

Regras: `slug` único no domínio; `source` precisa existir com `index.html` (o build aborta senão); `redirects`/`csp_extra` capturam as customizações que hoje vivem soltas no `vercel.json` da sibling.

### 1.2 Paths livres vs paths que exigem revisão do Victor

| Regra | Paths |
|---|---|
| **Auto-merge** (checks verdes bastam) | `landing-pages/{marca}/**`, `landing-pages/dominios/*.json`, `brand/*/assets/**` |
| **Exige aprovação do Victor** | Todo o resto — `.claude/**`, `.github/**`, `landing-pages/build/**`, `landing-pages/GUIDELINES.md`, `landing-pages/CONTEXT.md`, `brand/*/tokens.json`, `brand/*/generation-rules.json`, `conhecimento/**`, etc. |

Nota: `landing-pages/build/**` e `.github/**` ficam do lado "exige revisão" de propósito — são o próprio mecanismo de deploy; mudança ali sem revisão seria escalada de privilégio.

**Limitação de plano GitHub (repo privado em conta pessoal Free):** branch protection, CODEOWNERS-required-review, auto-merge nativo e merge queue não estão disponíveis. O merge-bot via Actions substitui tudo isso funcionalmente (a serialização vem do `concurrency` do workflow de deploy; o gate de paths vem da lógica do bot). O que NÃO dá pra impedir tecnicamente nesse plano é um humano commitando direto na main pelo GitHub — mas o time é não-técnico e opera só via skills, e o guard-rail que importa (token Vercel só no CI) não depende de plano. **Opcional:** GitHub Pro (usuário owner) habilita branch protection em repo privado; migrar o repo pra uma org com Team habilita merge queue nativa. Avaliar na Fase 0; não é bloqueador.

---

## 2. Princípios de segurança da migração

1. **Nada muda no ar até a paridade fechar.** O build novo tem que reproduzir byte-a-byte (ou com diff explicado e aprovado) o que está em produção hoje, domínio por domínio, ANTES de qualquer cutover.
2. **Cutover por domínio, seco e exclusivo.** A partir do momento em que um domínio migra, o caminho antigo é bloqueado para ele (lp-publicar v3.x recusa e aponta o fluxo novo). Nunca dois caminhos de deploy ativos pro mesmo domínio — convivência recriaria a corrida que estamos matando.
3. **Rollback do plano sempre disponível.** Em qualquer fase, reverter = remover o domínio da lista de migrados + redeployar via lp-publicar clássica (skills v3.x ficam intactas até a Fase 5).
4. **Piloto no domínio de maior dor e menor superfície** (`content.cxpress.io`), observação de 1–2 semanas de uso real antes do rollout.
5. **Reconciliação antes de tudo:** LP no ar sem source no repo (`deploy_orfao` do lp-health-check) precisa ser trazida pro repo ANTES da migração do seu domínio — no modelo novo, o que não está no Git não vai pro ar.

---

## 3. Fases

### Fase 0 — Preparação (meia sessão; zero risco)

- [x] 0.1 Criar secret `VERCEL_TOKEN` no repo GitHub — feito 2026-07-15. Validação dentro de um workflow fica pra Fase 2 (workflows entram via PR e só rodam a partir da main).
- [x] 0.2 Checar recursos do plano GitHub — **Free em conta pessoal**, branch protection 403 em repo privado. Decisão: merge-bot via Actions; upgrade Pro opcional.
- [x] 0.3 Reconciliação repo × live — **19 LPs órfãs** encontradas e importadas pro repo (detalhes em `dominios/INVENTARIO-2026-07-15.md`).
- [x] 0.4 Snapshots dos `vercel.json` live em `dominios/snapshots-2026-07-15/` — 3 redirects encontrados (webinar ×2, material ×1); achado extra: assets legados na raiz de content.cxpress.io (ver inventário §3.2 — exige `legacy_root_assets` no manifesto da Fase 1).
- [x] 0.5 Decisão do Victor (2026-07-15): paths livres = proposta do §1.2 aceita sem ajustes (conteúdo livre, mecânica protegida); ordem de rollout confirmada = content.cxpress.io → webinar → evento → material.

**Critério de aceite:** secret validado; inventário repo×live 100% reconciliado nos 4 guarda-chuvas; decisões registradas neste doc.

### Fase 1 — Manifestos + build script + prova de paridade (1–2 sessões; zero risco — nada deploya)

- [x] 1.1 Manifestos gerados a partir do live em `dominios/{dominio}/manifest.json` (+ `vercel.json` verbatim do live — decisão de desenho: mais simples que template+extras, ver PARIDADE.md).
- [x] 1.2 `build_umbrella.py` escrito com todas as validações previstas (+ tolerância a BOM e refs bare já namespaceadas, descobertas na prova).
- [x] 1.3 **Prova de paridade EXECUTADA e FECHADA (2026-07-15): 0 diferentes / 0 faltando / 0 sobrando nos 4 guarda-chuvas.** 14 LPs tinham drift source≠live (live adotado como verdade, sources re-importados). Relatório completo em `build/PARIDADE.md`. Re-rodar fresh antes do cutover da Fase 2 (`build/paridade_check.py`).
- [x] 1.4 Cobertura de teste = a própria prova contra 66 LPs reais (todos os casos do plano exercitados); testes unitários ficam como melhoria futura (justificativa em PARIDADE.md).

**Critério de aceite:** paridade 100% (ou diffs aprovados) nos 4 domínios ✓; build roda em <60s no Actions (validar na Fase 2 — localmente roda em segundos).

### Fase 2 — Piloto: `content.cxpress.io` (1 sessão + 1–2 semanas de observação)

> **Achado da Fase 1 que afeta o desenho do workflow:** `webinar.buzzmonitor.com` contém uma
> **função serverless** (`api/clickmeeting-register.js`, registro ClickMeeting — lê
> `CLICKMEETING_API_KEY` do env do projeto Vercel). `vercel deploy --prebuilt` NÃO builda
> funções a partir de `api/` — o workflow deve usar `vercel deploy` normal (a CLI builda
> `api/` como function e serve o resto como estático) ou montar `.vercel/output`. Decidir/testar
> na Fase 2 antes de migrar o webinar; o piloto content.cxpress.io é 100% estático e não é afetado.

- [x] 2.1 `lp-deploy.yml` criado (2026-07-15): `workflow_dispatch` (qualquer domínio, validação supervisionada) + push na main gated por MIGRADOS.json. Smoke testa TODAS as URLs do manifesto (200/redirect + hash newline-normalizado vs build). `deploy_ci.py` validado em dry-run nos 4 domínios antes do 1º run.
- [x] 2.2 Rollback automático implementado E ENSAIADO DE VERDADE (input `force_fail`): deploy real no piloto → falha simulada → promote do deploy anterior → 30/30 URLs ok, run vermelho. O ensaio achou e corrigiu bug real: alvo de rollback agora é o deploy que o ALIAS serve (não o "último READY" — errado após rollback anterior). Alerta por email/issue fica de melhoria (o run vermelho já notifica pelo GitHub).
- [x] 2.3 Cutover do piloto (2026-07-15): `content.cxpress.io` em MIGRADOS.json; `lp-publicar` v3.10.0 recusa domínios migrados (Passo 0.0). Pendência menor: mensagem específica no hook `guard_vercel_deploy.py` (o gate da skill já cobre o fluxo normal).
- [ ] 2.4 Criar `lp-pr.yml` (validações + preview em PR) — junto do merge-bot na Fase 3.
- [x] 2.5 **Substituído por bateria de testes sintéticos** (decisão do Victor 2026-07-15 — sem tempo pra observação passiva): (1) build quebrado em PR → reprovou sem merge (PR #68 ✓); (2) concorrência real — 2 PRs quase simultâneos em LPs distintas → ambos mergearam, deploys enfileiraram, os 2 marcadores no ar (PRs #69/#70 ✓); (3) LP nova via manifesto + guarda de despublicação (PRs #71/#72); (4) rollback — já ensaiado na 2.2 ✓. Dúvidas reais do time serão tratadas conforme aparecerem.

**Critério de aceite:** ≥3 publicações reais sem incidente; rollback testado de verdade (simular deploy quebrado num sábado de manhã, não descobrir em produção); nenhuma vizinha afetada (por construção + smoke test).

### Fase 3 — Merge-bot + skills v4 (1–2 sessões)

- [x] 3.1 `lp-pr.yml` criado (2026-07-15): valida (build dos 4 domínios + `pr_check.py` — classificação de paths + guarda de despublicação), auto-mergeia diff 100%-conteúdo via GITHUB_TOKEN e dispara `lp-deploy` por `workflow_dispatch` (push do GITHUB_TOKEN não dispara workflow — regra anti-recursão). Diff com mecânica → label `precisa-revisao-victor` + comentário com motivos. **Preview deploy adiado:** URLs de preview do Vercel são SSO-protected (memória 2026-07-09) — inúteis pro time sem bypass token; fica como melhoria.
- [x] 3.2 `lp-publicar` v4.0.0: Passo 0.0 conduz o fluxo CI completo (pull → manifesto → validação local via build → entrega → acompanhar run → Notion). Fluxo clássico intacto pros não migrados.
- [x] 3.3 `lp-preparar` v1.4.0, `lp-gerar` v1.8.0, `lp-revisar` v1.7.0, `lp-integrar-form` v1.4.0: Passo 0.0 `git pull --rebase` + branch check.
- [x] 3.4 Conflito: instrução de rebase/reaplicação no Passo 0.0 das skills (a pessoa de marketing não vê Git — a skill resolve e segue).
- [x] 3.5 CONTEXT.md §2.6 (fluxo CI) + regra geral com gate; CLAUDE.md seção LP; CHANGELOG (v4.0.0 + 4 skills de edição).

**Critério de aceite — VALIDADO 2026-07-15:** PR #66 (só conteúdo) mergeou e publicou sozinho, marcador confirmado no live com SMOKE OK; PR #67 (misto conteúdo+mecânica) travou com label `precisa-revisao-victor` e sem merge. ✓

### Fase 4 — Rollout + revogação de credenciais (1 sessão + observação)

- [x] 4.1 Migração completa em 2026-07-15 (Victor autorizou acelerar — a bateria de testes sintéticos do item 2.5 substituiu a observação): webinar (27 LPs, SMOKE OK + função serverless `api/clickmeeting-register` validada contra baseline 405/JSON — o `vercel deploy` não-prebuilt builda `api/` normalmente), evento (4 LPs) e material (6 LPs) deployados via dispatch supervisionado e adicionados ao MIGRADOS.json. **Os 4 guarda-chuvas agora deployam exclusivamente via CI.**
- [ ] 4.2 Com os 4 migrados: **remover `VERCEL_TOKEN` dos `.env.local` de todas as máquinas e revogar os tokens antigos na Vercel UI**. A partir daqui o incidente clássico é fisicamente impossível — nenhuma máquina tem credencial de deploy.
- [ ] 4.3 `lp-health-check` v2: além do HTTP check, comparar live × manifesto (fica trivial: o manifesto É o estado esperado). Mantém como vigia diário.
- [ ] 4.4 `content.elife.com` (1ª LP Elife) já nasce no modelo novo — criar manifesto, sem sibling nunca.

**Critério de aceite:** 4 domínios no CI; zero tokens Vercel fora do GitHub Actions; health-check verde 7 dias seguidos.

### Fase 5 — Aposentadoria do legado (quando estiver confortável; sem pressa)

- [ ] 5.1 Mover `lp-sync` e o corpo v3.x da `lp-publicar` pra `.claude/skills-desativadas/` (mesmo tratamento do meta-ads-*). Manter `sync_sibling.py` acessível pra recovery/auditoria.
- [ ] 5.2 Simplificar `guard_vercel_deploy.py`: qualquer `vercel deploy` manual em domínio de LP → bloquear (não só confirmar), exceto contextos sancionados restantes (dashboards, blog-publicar).
- [ ] 5.3 Limpar seções obsoletas do CONTEXT.md (sibling, drift, JSON wrapper) movendo para um `LEGADO.md` de referência histórica.

---

## 4. Riscos e mitigação

| Risco | Mitigação |
|---|---|
| Build novo diverge do live no cutover | Fase 1.3 (paridade por hash) é gate obrigatório; cutover só com paridade provada |
| Actions fora do ar / lento na hora de publicar | Raro; fallback documentado: disparar `lp-deploy.yml` via `workflow_dispatch` quando voltar. Deploy de emergência manual continua possível pelo Victor (admin) com token pessoal temporário |
| PR só-LP com conteúdo ruim indo pro ar sem revisão | Igual a hoje (deploy já é sem revisão) — mas ganha as validações automáticas do CI que hoje não existem no caminho manual |
| Duas pessoas editando a MESMA LP | Conflito de Git detectado no PR; skill resolve reaplicando por cima da main (3.4). Hoje isso é sobrescrita silenciosa |
| Manifesto editado errado (slug removido sem querer) | Validação no PR: slug removido do manifesto sem remoção da pasta → o bot NÃO auto-mergeia, marca "despublicação intencional?" pra revisão |
| Colaborador com repo desatualizado | `git pull` automático no Passo 0 das skills (3.3); e mesmo sem ele, produção não é afetada — vira no máximo conflito de PR |
| Segredo VERCEL_TOKEN vazar via workflow | Workflows de deploy só rodam na main (não em PR de fork; repo privado sem forks); paths do build exigem revisão do Victor (§1.2) |

## 5. O que muda pra cada perfil

**Marketing:** nada perceptível — roda as mesmas skills; a LP vai pro ar em minutos sem aprovação de ninguém, como hoje. Some: instalação de Vercel CLI/token no setup, prompts de drift, incidentes.

**Victor:** revisa exatamente o que já revisa (skills/config); LPs continuam sem passar por você. Ganha: auditoria completa (todo estado do ar = um commit), rollback por revert, e o fim dos chamados de "LP sumiu".

## 6. Fora de escopo v1 (decidir depois)

- **Projetos solo** (1 LP = 1 projeto): risco de corrida ~zero (não há vizinhas). Migram na Fase 5 se valer a simplificação, ou permanecem no fluxo v3.x.
- **Webflow:** rota independente (CONTEXT §2.4), não é afetada.
- **Dashboards CM** (`dashboard-atualizar`): mesmo padrão sibling, mas single-operator e com PII — avaliar migração análoga só depois das LPs estabilizarem.

---

*Doc vivo — atualizar checkboxes e decisões conforme a execução. Dúvidas de desenho: ver conversa de 2026-07-15 com o Victor.*
