# Changelog

Mudanças relevantes nas skills do Agente Inhouse.

Cada skill é versionada de forma independente, no campo `version` do frontmatter de seu `SKILL.md`. O esquema é semver simplificado:

- **MAJOR** — muda interface (parâmetros, comandos) ou comportamento de forma incompatível.
- **MINOR** — adiciona capacidade preservando compatibilidade.
- **PATCH** — correção, ajuste de tom, refinamento de prompt sem mudar comportamento esperado.

**Como atualizar:** ao alterar uma skill, bumpe a `version` no frontmatter e adicione uma entrada nova na seção da skill correspondente abaixo, no mesmo PR. Datas em ISO (`YYYY-MM-DD`).

---

## CSP dos guarda-chuvas — liberar Google Ads e Google Signals
### 2026-08-06 — vercel.json dos 5 domínios + `vercel.template.json` (lp-publicar 5.1.3, PATCH)

O `connect-src` cobria `*.google-analytics.com` mas não os outros hosts que o gtag/GTM usa,
então o navegador bloqueava em runtime — sem sintoma na página, só no console. Achado ao
inspecionar `content.buzzmonitor.com/buzz-academy-experience`; o mesmo buraco existia nos
**5 guarda-chuvas e no template**, ou seja, em toda LP servida por eles.

Bloqueado até aqui (`Refused to connect`):

- `analytics.google.com/g/collect` e `www.google.com/g/collect` — Google Signals do GA4.
- `www.google.com/ccm/collect`, `www.google.com/rmkt/collect` e `ad.doubleclick.net/ccm/s/collect`
  — conversão e remarketing do Google Ads (`AW-832709839`).

Adicionados ao `connect-src`: `analytics.google.com`, `*.googletagmanager.com`,
`*.doubleclick.net`, `www.google.com`, `www.google.com.br`. Wildcard em doubleclick em vez de
enumerar `ad.`/`stats.g.`/`td.` — Google troca de subdomínio sem aviso. Nenhuma outra directive
mudou; `img-src` já era `https:`, então pixel-como-imagem nunca esteve bloqueado.

**Limitação conhecida:** o ping de audiência do Ads bate em TLD regional (`www.google.es`,
`www.google.com.mx`…). Cobrimos `.com` e `.com.br`; LP em outra região pode ver o mesmo bloqueio
pro TLD dela. Enumerar todos os TLDs do Google não compensa — tratar caso a caso se aparecer.

**Fora do CSP, não corrigido aqui:** o Meta Pixel `705678789565591` responde *"unavailable on
this website due to it's traffic permission settings"*. É allowlist de domínio no Events Manager
da Meta, não header — só resolve no painel.

## Infra LP — OG image: nome único `og-{slug}.png` (fim da duplicata `og-image.png`)
### 2026-08-05 — GUIDELINES §18 + lp-gerar 1.8.2 · lp-revisar 1.8.2 · lp-publicar 5.1.2 (PATCH)

31 LPs tinham em `assets/` um `og-image.png` que era **cópia byte-a-byte** (mesmo sha1) do `og-{slug}.png` irmão, sem nenhuma referência: 4,49 MB de peso morto no repo. Causa raiz: contradição dentro da própria GUIDELINES §18 — o comando de render mandava o screenshot pra `og-{slug}.png` (linha 290) enquanto a "convenção de path no source" declarava `og-image.png` (linha 297). Quem gerava OG produzia um dos dois, descobria que o `build_umbrella.py` só resolve `og-{slug}.png` (linha 53) e fazia a segunda cópia pra garantir — em vez de renomear.

- **Convenção única: o nome do arquivo no source é `og-{slug}.png`, no source e no deploy, zero rename.** GUIDELINES §18 reescrita com a proibição explícita de `og-image.png`, mais a exceção legítima (variantes irmãs que reusam de propósito a OG da LP-mãe — `banimento-whatsapp{,-pt,-latam,-comercial}` — referenciam o arquivo por path literal, com uma só cópia física).
- **`lp-gerar` 1.8.2** — path final anotado no README agora é `og-{slug}.png`; guard explícito contra as duas cópias; checklist do README template ganhou a linha da OG com o nome canônico. `og-template.html`: comando de render aponta pra `og-{slug}.png`.
- **`lp-revisar` 1.8.2** — o check §3.7.e passa a validar `og-{slug}.png` e ganhou um check novo (`OG-IMAGE-DUPLICATE`) que acusa `og-image.png` sobrando como CRÍTICO. Impede a regressão na porta de entrada.
- **`lp-publicar` 5.1.2** — §1.4.1 sem rename nos dois modos (o sufixo já vem do source) + aviso se achar duplicata legada; `{{OG_IMAGE_PATH}}` em modo solo resolve `assets/og-{slug}.png`.
- **Removidas as 31 duplicatas** (`git rm`). Auditoria prévia LP-por-LP: cada arquivo só saiu depois de confirmar hash idêntico ao OG irmão de fato referenciado. Os 5 guarda-chuvas buildam com **0 avisos de OG** depois da limpeza (o único aviso remanescente, `case-ia-de-voz/beatriz.jpg`, é pré-existente e vem de uma ref dentro de comentário HTML).
- **`buzzmonitor/plataforma-completa-social-media-latam`** — caso oposto: tinha só `og-image.png` (nenhum irmão), e o HTML usa `{{OG_IMAGE_PATH}}`, que resolveria pra um arquivo inexistente. **Renomeado** (não apagado) pra `og-plataforma-completa-social-media-latam.png` — a LP não está em nenhum manifesto, então o `og:image` quebrado nunca chegou a produção.
- **`cxpress/atendimento-sem-metrica/assets/render_og.py`** — output derivado da pasta da LP (`og-{slug}.png`), pra rerodar o script não recriar o órfão.
- 33 README/REVISAO de LP que citavam o path antigo atualizados pro nome canônico.

## Infra LP + fluxo de commit — anti-PR-stale
### 2026-08-03 — pull seguro antes de commit, `pr_check` por merge-base, `launch.json` des-versionado

Motivado pela PR #168, que caiu na revisão humana por dois falsos gatilhos do merge-bot: (1) `.claude/launch.json` (dev server local) arrastado no commit e (2) "3 slugs removidos" no manifesto — falso-positivo de branch desatualizada. O merge 3-way real preservava tudo; o alarme era só do detector.

- **`pr_check.py` — detecção de remoção de slug agora compara pelo merge-base** (ponto onde a branch divergiu), não pela ponta de `origin/main`. Uma branch velha não tem os slugs que entraram na main depois que ela saiu; comparar contra a ponta acusava esses slugs como "despublicação" e travava o auto-merge por engano. `changed` já usava three-dot (merge-base) — a detecção fica consistente. Validado reproduzindo o cenário da #168 (lógica antiga: 3 falsos "removidos" → nova: 0). Despublicação real continua sendo detectada (branch que de fato remove um slug presente no merge-base).
- **`.claude/launch.json` deixou de ser versionado** (`git rm --cached` + `.gitignore`). É registro de dev servers locais gerado por `preview_start`, variava por colaborador e vinha sendo commitado junto das LPs — gatilho nº1 que tirava PR de LP do auto-merge (`.claude/**` = mecânica). Agora é per-colaborador; `preview_start` recria sob demanda.
- **`/commit` v2.1.0** — novo Passo 0.4: estando em `main`, roda `git pull --rebase --autostash origin main` antes de criar a branch, pra ela não nascer de base velha (a raiz do PR stale). `--autostash` guarda o trabalho não-commitado e devolve (não apaga). Regra inviolável ajustada pra abrir exceção a esse pull de sincronização.
- **`lp-preparar` 1.4.1 · `lp-gerar` 1.8.1 · `lp-revisar` 1.8.1 · `lp-integrar-form` 1.4.1 · `lp-publicar` 5.1.1** — o `git pull --rebase` do passo de sync ganhou `--autostash`, pra não travar (nem exigir stash manual) quando há trabalho não-commitado na working tree.
- **OG image de `cxpress/atencion-clinicas-latam`** gerada (1200×630, template Cxpress, Chrome headless) e colocada no source da LP (`assets/og-atencion-clinicas-latam.png`) — o `og:image` apontava pra arquivo inexistente (404 no preview social). Servida pelo build padrão, sem `extra_files`.

## Infra LP — 5º guarda-chuva: `content.buzzmonitor.com`
### 2026-07-21 — novo guarda-chuva CI + migração de 2 LPs ES

Novo guarda-chuva `content.buzzmonitor.com` (conteúdo Buzzmonitor ES-LATAM — social listening; equivalente Buzzmonitor do `content.cxpress.io`). Nasceu direto no CI: `landing-pages/dominios/content-buzzmonitor-com/` (manifest + vercel.json espelhando o do material, com Termly/Ads/LinkedIn no CSP) + `content.buzzmonitor.com` em `MIGRADOS.json` + opção no dispatch de `lp-deploy.yml`. Projeto Vercel `buzzmonitor-content` criado via API (domínio já apontado no Route 53).

As LPs `ia-para-social-listening-es` e `la-mejor-plataforma-social-listening-es` saíram de `material.buzzmonitor.com` (removidas do manifesto do material; os paths antigos fazem **301 permanente** pra `content.buzzmonitor.com/{mesmo-slug}` via `redirects` do vercel.json do material).

Regras/docs atualizadas pra prever o novo guarda-chuva: `lp-preparar/CONTEXT.md` (tabelas de subdomínio e projeto Vercel), `landing-pages/CONTEXT.md` (§tabela de guarda-chuvas ativos + contagem), `lp-publicar/SKILL.md` (exemplo), `lp-pr.yml` (comentário count-agnóstico), `PLANO-MIGRACAO-CI.md` (addendum). `lp-health-check` descobre o domínio sozinho (discover.py é dinâmico — sem mudança). Merge-bot: build por glob já cobre o novo manifesto; PR entra como mecânica (revisão do Victor).

**Fix `deploy_ci.py` (robô de deploy) — primeiro deploy de guarda-chuva novo:** o script assumia que sempre há um deploy de produção anterior pra usar como alvo de rollback; num projeto Vercel recém-criado (zero deploys) o fallback `["deployments"][0]` estourava `IndexError` **antes de publicar**. Agora trata `prev = None` (primeiro deploy): publica normalmente e, se o smoke falhar, sai com erro sem tentar rollback (não havia estado anterior a restaurar). Caso normal (com deploy anterior) inalterado. Pego ao subir a 1ª LP de `content.buzzmonitor.com`.

## Gate de GTM×região no deploy (novo) + lp-revisar/lp-publicar
### 2026-07-17 — check_gtm_region.py + lp-revisar v1.8.0 + lp-publicar v5.1.0 (MINOR)

Fecha o buraco do "traduz LP sem skill e esquece de trocar o pixel" (container GTM da
unidade de origem — incidente 2026-04-20, reaberto pelo caminho sem-skill). A correção
saiu da skill e foi pro chokepoint que não dá pra pular (o deploy/CI).

- **Novo** `landing-pages/build/check_gtm_region.py`: resolve a região (CONTEXT §5.1),
  lê o container esperado em `brand/{marca}/tracking.json` e compara com o GTM do HTML.
  Determinístico, stdlib-only. Só `wrong` (container ≠ região) bloqueia; `absent`/
  `no_expected` só avisam. Selo `.tracking.lock` por LP dá skip (título trocado não
  re-dispara — fingerprint = região+esperado+encontrado) e grandfathering de estados
  pré-existentes.
- **deploy_ci.py**: roda o gate antes do `vercel deploy` — bloqueio aborta com o live intacto.
- **pr_check.py**: LP tocada no diff com container errado não auto-mergeia (fica pro Victor).
- **lp-revisar v1.8.0**: Passo 3.5 agora delega ao script (determinístico, ~zero token) em
  vez de auditar "no olho" e grava o selo; ganhou `Bash` no allowed-tools.
- **lp-publicar v5.1.0**: gate no Passo 0.0.c (fluxo CI, pré-commit) e §2.5 (solo, pré-deploy).
- **CONTEXT.md §5.4** documenta gate + selo + grandfathering; §5.2 ganhou a linha do CI.
- Grandfathered nesta leva: `buzzmonitor/webinar-territorios-marca-mundial-junho-2026`
  (declara pt-PT, dispara o container LATAM) — decisão de conteúdo pendente do Victor.

## lp-publicar — CI vira o fluxo padrão; clássico rebaixado a modo solo
### 2026-07-15 — v5.0.0 — Fase 5 da migração (MAJOR)

Com os 4 guarda-chuvas migrados (MIGRADOS.json completo), o Passo 0.0 passa a rotear:
guarda-chuva → fluxo CI; solo → fluxo clássico (segue válido — sem vizinhas, sem corrida);
guarda-chuva NOVO nasce direto no CI (manifesto + MIGRADOS, nunca sibling). Descrição do
frontmatter atualizada. Documentação: CONTEXT.md §1/§2.2/§4.3 (seção histórica) e CLAUDE.md.

## lp-sync — DESATIVADA
### 2026-07-15 — movida para `.claude/skills-desativadas/lp-sync/`

Era a ferramenta de "sibling fresh" do modelo aposentado. Pra inspecionar o ar de um
guarda-chuva hoje: `dominios/{dom}/manifest.json` + `build_umbrella.py` (o build É o deploy);
auditoria contra o live: `paridade_check.py`.

## lp-publicar — fluxo CI completo pra domínios migrados
### 2026-07-15 — v4.0.0 — Passo 0.0 vira o fluxo novo (MAJOR)

Fase 3 da migração LP→CI. Para domínio em `MIGRADOS.json`, a skill não usa mais NADA do
fluxo sibling — o Passo 0.0 agora conduz o fluxo completo: `git pull --rebase` → source +
manifesto (`landing-pages/dominios/{dom}/manifest.json`) → validação local com
`build_umbrella.py` → entrega (colaborador via `/commit` + merge-bot; admin direto na main)
→ acompanhar o run do `lp-deploy.yml` (smoke + rollback automático) → relatório Notion.
Domínios não migrados seguem no fluxo clássico v3.9.x intacto. MAJOR porque muda o
comportamento da interface pro piloto content.cxpress.io.

## lp-preparar v1.4.0 · lp-gerar v1.8.0 · lp-revisar v1.7.0 · lp-integrar-form v1.4.0 — sync do repo
### 2026-07-15 — Passo 0.0: `git pull --rebase` antes de editar

Com o deploy via CI, colaboradores publicam por PR direto na main — editar em cima de
working tree velha vira conflito evitável. As 4 skills de edição ganham Passo 0.0 que
sincroniza o repo (e aborta com aviso se o rebase conflitar) antes de tocar em arquivo.

## lp-publicar — gate de domínio migrado pro CI
### 2026-07-15 — v3.10.0 — Passo 0.0: recusa domínio listado em MIGRADOS.json

Fase 2 da migração LP→CI (`landing-pages/PLANO-MIGRACAO-CI.md`). Domínios guarda-chuva
migrados pro deploy via GitHub Actions (`.github/workflows/lp-deploy.yml` + manifestos em
`landing-pages/dominios/`) não podem mais ser deployados pela skill — o caminho local
sibling é exatamente a corrida que a migração elimina. Novo Passo 0.0 lê
`landing-pages/dominios/MIGRADOS.json` e aborta com instrução do fluxo novo quando o
domínio-alvo está na lista. Domínios não migrados seguem no fluxo v3.9.x sem mudança.

## convites-moderador — só dias úteis
### 2026-07-13 — v1.2.1 — Help do `--force` honesto

O help do `--force` prometia "envia mesmo em sáb/dom", mas o flag só destrava o dia do run — o filtro de dia útil dentro de `next_session_for_series()` continua ativo (por design: sessão de fim de semana roda sem vendedor de propósito, decisão da v1.2.0). Num sábado, `--force` termina em SKIP geral porque a única sessão futura materializada pelo ClickMeeting é a do próprio fim de semana. Achado Importante #1 do review do PR #58.

- Corrigido o texto (docstring, help do argparse, mensagem de `SKIP TOTAL` e SKILL.md) para dizer o que o flag realmente faz: roda em sáb/dom, mas nunca convida pra sessão de fim de semana. Comportamento intacto — PATCH, só texto.

### 2026-07-13 — v1.2.0

Convites de moderador (vendedores) passam a sair **apenas em dias úteis** — decisão do Victor: o ClickMeeting não permite pular fim de semana na recorrência, e bloquear a inscrição na LP seria pior que a sessão rodar sem vendedor. As LPs seguem intactas (inscrição livre sáb/dom); a gestão é toda no lado dos convites.

- **n8n (produção)**: Code node "Montar plano de convites" ganhou trava dupla — (a) sáb/dom em America/Sao_Paulo o run retorna vazio (`SKIP TOTAL`, nada enviado); (b) a escolha da próxima sessão nunca cai em sessão de fim de semana (dia local da sessão via `Intl` no timezone da própria conferência). Aplicado no workflow vivo (`1TFA4xHvFEZQ5lns`) via API em 2026-07-13 e espelhado em `integracoes/n8n/convites-moderador-clickmeeting.json`.
- **`send_invites.py` (fallback manual)**: mesma trava dupla + flag `--force` pra ignorar a trava de fim de semana quando for intencional. America/Sao_Paulo como offset fixo -3 (sem DST desde 2019 — evita depender de tzdata no Windows); o dia da sessão usa o offset do próprio `starts_at`.
- Sem convite duplicado: sexta convida a sessão de sexta (futura no run das 07:00), sáb/dom não envia, segunda convida a de segunda. MINOR — comportamento novo compatível (interface só ganha `--force`).

## dashboard-atualizar — multi-dashboard
### 2026-07-08 — v3.0.0

A skill deixou de ser single-purpose (Buzzmonitor Brasil) e passou a atualizar **qualquer uma das 3 dashboards CM dinâmica-estáticas** no Vercel — `buzz-br` | `cxpress` | `latam` — escolhida por argumento (`/dashboard-atualizar cxpress`) ou, sem arg, por chip (AskUserQuestion). Toda decisão específica de dashboard (pasta-fonte, sibling, URL, JSON de dados, arquivos a copiar, marcador do index, se roda a auditoria de 3 superfícies) virou um bloco de config `case "$DASH"` no topo; os passos (pre-flight, export, sanity, cópia, deploy, validação) são genéricos.

- **Contexto:** as dashboards Cxpress BR e Buzzmonitor LATAM foram convertidas de snapshot estático pra dinâmica-estática (mesmo modelo do Buzz BR), com fonte em `dashboard-cxpress-vercel/` e `dashboard-latam-vercel/`. Faltava um comando único pra atualizá-las — antes só o Buzz BR tinha.
- **Novo:** Passo A (resolver dashboard) + Passo 1.5 (paridade número-a-número opcional, obrigatória se mexeu no motor/render/queries). Sanity do JSON parametrizado (`$MAIN` = `leads`/`deals`). Validação confirma o marcador certo do index (`MotorCM`/`MotorCxpress`/`MotorLatam`) e que a senha fraca antiga (`inhouse@77`) dá 401.
- **Específico do buzz-br preservado:** a auditoria de sincronia do filtro CM em 3 superfícies (Passo 0.2b) só roda pra ele (`AUDIT3=1`); cxpress/latam têm superfície única de queries.
- MAJOR pela mudança de interface (novo argumento `[dashboard]`). Chamada antiga `/dashboard-atualizar` sem arg continua válida (agora pergunta qual).

## Família social-* multi-marca (cross-skill)
### 2026-07-08 — social-pipeline v1.0.0, social-plan v4.0.0, social-analytics v1.0.0, social-canva v1.0.0

As 4 skills de redes sociais deixaram de ser single-purpose Buzzmonitor e passaram a aceitar **as 4 marcas do grupo** (`buzzmonitor` | `cxpress` | `buzzcreators` | `elife`). Toda decisão específica de marca que vivia hardcoded nas skills foi extraída pra um arquivo novo de identidade de marca, **`brand/{marca}/social-media.json`** — handles das contas (Instagram/LinkedIn), contas secundárias de cross-check, modelo de rede (primária + réplica), cadência/dias/horários, pilares base de conteúdo, nicho, perfis de referência e queries de tendência. As skills leem de lá; concorrentes continuam vindo de `conhecimento/produto/{marca}/concorrentes.md` e o blog do `brand-manifest.json` (campo `blog`).

- **Configs criadas nas 4 marcas**: Buzzmonitor = migração 1:1 do que estava nas skills (modelo de referência, `status: ativo`); Cxpress e Buzzcreators = `rascunho` (pilares/referências derivados do brand-manifest, validar no 1º ciclo); Elife = `esqueleto` (brand-manifest da marca está vazio). Campos `null` (ex: handle do IG da Cxpress) não travam: a skill pergunta na primeira execução e **salva a resposta de volta no JSON**.
- **Notion multi-marca**: `conhecimento/config/notion-ids.md` ganhou a regra de título de hub por marca — Buzzmonitor mantém `{Mês Ano}` (compat com histórico); demais marcas usam `{Mês Ano} — {Marca}`. Hub sem sufixo é sempre da Buzzmonitor; nunca reaproveitar hub de outra marca.
- **`social-analytics`**: agora aceita `[marca] [YYYY-MM]` (ordem livre); separação próprios × secundárias × UGC vem da config, não mais de `buzzmonitorbr`/`buzzcreatorsbr` fixos. `_gen_report.py` ganhou `--marca`/`--handle`/`--secundarias` (defaults = valores antigos, retrocompatível).
- **`social-plan`**: agora aceita `[marca] [mes]`; pilares/referências/nicho/queries/cadência vêm da config; lista de concorrentes vem do `concorrentes.md` da marca (antes hardcoded Sprinklr/Brandwatch/etc); blog do manifest. Nova exceção ao gate do relatório anterior: **primeiro ciclo da marca** pode seguir sem baseline (com registro explícito). MAJOR pela mudança de assinatura (`[mes]` → `[marca] [mes]`), mas chamadas antigas só com mês continuam funcionando (marca default buzzmonitor).
- **`social-canva`**: deriva a marca do caminho do arquivo de copies (`social-media/{marca}/...`); lê `brand/{marca}/canva-template-ids.json`. A especificação `brand/buzzmonitor/canva-brand-templates.md` vale como modelo pra qualquer marca (usar o brand kit da marca).
- **`social-pipeline`**: valida a config da marca no Passo 0.5 (arquivo ausente = para com orientação; campos null = pergunta e persiste; status rascunho = avisa sem bloquear); Etapa C carrega também `brand-manifest.json` (nameUsage/tom) e `conhecimento/produto/{marca}/{marca}.md` antes das copies.
- MAJOR/versões 1.0.0 marcam a promoção da família de "v0.x Buzzmonitor-only" pra interface multi-marca estável. Interfaces antigas (sem marca) seguem aceitas com default buzzmonitor.

## Regra de copy — a primeira linha carrega a dor (cross-skill)
### 2026-07-07 — copy-criar v1.3.0; fundamentos-copy §0; GUIDELINES de LP e de criativos

Nova boa prática de copy, **prioritária sobre as demais**: a primeira linha de qualquer peça (H1 de LP, headline de criativo, subject + abertura de e-mail, hook de vídeo/webinar, título de post) lidera com a **dor/problema** do público, não com a solução/método/oferta. Padrão **H1 = dor · H2 = solução + método**, com o método das 2 perguntas antes de escrever a headline. Calibrada por funil: default forte em ToFu/MoFu; BoFu/público quente pode abrir pelo ganho.

- **Fonte de verdade:** `conhecimento/copywriting/fundamentos-copy.md` **§0** — nova seção no topo, numerada 0 para sinalizar "vem antes de todas" sem renumerar as seções existentes nem quebrar as referências a "seção 3.1/4.2". Cobre automaticamente toda skill que lê o arquivo (família copy-*, `roteiro-webinar-perpetuo`, `pauta-quente`, `news-criar-post`, e os docs de tipo email/estático/vídeo/blog/linkedin/funil).
- **Ponteiros onde a fonte não é lida:** `landing-pages/GUIDELINES.md` §3 (Hero) e §5 (Copy) — a família LP não lê fundamentos; postura conservadora (sinaliza H1 que abre pela solução, não reescreve tom). `criativos/GUIDELINES.md` §4 — capa/hook lidera com a dor sem inventar hook novo (respeita a §9).
- **Reforço na geração:** `copy-criar` ganhou a "Regra 0" nas regras universais do Passo 4 (cobre os 3 formatos de uma vez) + nota no campo Headline do estático. MINOR — nova diretriz preservando a interface da skill.

## convites-moderador
### 2026-07-08 — v1.1.1 — Série Atención LATAM: 17544 → 17701

A série `17544` (Buzzmonitor Atención al Cliente, ES-LATAM) esgotou as sessões e foi recriada como `17701` em 2026-07-08. Atualiza o `recurring_config_id` no `config.json` e na tabela SERIES espelhada no `SKILL.md`, além dos espelhos fora da skill (workflow n8n `convites-moderador-clickmeeting.{json,md}` e o `next-webinar.js` + `README.md` da `_clickmeeting-api` das LPs). Sem isso, o convite diário apontava pra série morta e o webinar Atención ficava sem moderador. PATCH — só troca de dado (ID da série), sem mudança de comportamento nem interface.

### 2026-07-07 — v1.1.0 — Gatilho diario migrado pro GitHub Actions

O disparo diario dos convites de moderador saiu do remote-trigger da claude.ai e passou a rodar em **GitHub Actions** (`.github/workflows/convites-moderador.yml`, cron `17 11 * * *` UTC = 08:17 America/Sao_Paulo). Motivo: a ClickMeeting **bloqueou o IP** do harness da nuvem, entao o cron agendado falhava todo dia — mesma classe de problema que ja tinha levado o `lp-health-check` pro Actions. O workflow le `CLICKMEETING_API_KEY` de um secret do repo (setado nesta mudanca) e faz `checkout`, entao **editar `config.json` continua exigindo commit + push** pra valer no proximo run. Tem `workflow_dispatch` com opcao **Dry-run** pra teste manual sem enviar email. O `send_invites.py` nao mudou (ja lia `os.environ` antes do `.env.local`). MINOR — nova forma de acionar preservando a interface (script + `/convites-moderador` local seguem iguais). Config tambem ganhou a serie **17671** (Cxpress Vozxpress, moderadora Lilian) no mesmo passe.

## Resiliência ao shim Python do Windows — resolver `$PYBIN` estendido (cross-skill)
### 2026-07-02 — convites-moderador v1.0.1, lp-health-check v1.1.1, social-analytics v0.1.1, lp-revisar v1.6.1, lp-gerar v1.7.1, pull-request-review v1.0.2, bunzzai v1.1.1, criativo v1.1.1, commit v2.0.1

Extensão da convenção `$PYBIN` (criada hoje em `lp-publicar` Passo 0.4 — ver entrada `lp-publicar, lp-sync`) para **todas as demais skills que chamavam `python` literal** em snippets bash. No Windows, o `python`/`python3` do PATH costuma ser o shim da Microsoft Store: o arquivo existe, mas falha com exit 49. O resolver testa **execução** e fica com o 1º interpretador que roda de verdade (Windows → `py`; macOS/Linux → `python3`/`python`), inlinado por bloco (não persiste entre execuções de shell).

- **Por que agora — e por que NÃO era urgente:** a investigação da `convites-moderador` (que roda agendada e funciona) mostrou que **execuções em background alcançam o Python real por trás do shim** (`AppData\Local\Python\bin\python.exe`); só sessões **interativas** batem no shim. Logo isto é **blindagem/determinismo**, não conserto de quebra ativa nas agendadas — mas fecha o buraco em qualquer uso interativo (foi o que travou a recuperação de LP em 2026-07-02) e remove a dependência do quirk interativo-vs-background.
- **Deps já cobertas:** o `py` (3.14) desta máquina tem **Pillow 12.2.0 + Playwright**, então os checks de OG image (`lp-gerar`, `lp-revisar`) e o `render.py` (`criativo`) rodam sob `$PYBIN` sem `uv`. Skills com pandas/psycopg (`dashboard-*`, `auditar-deals-cm`) seguem em `uv run --python 3.12` (não adotam `$PYBIN`).
- **`commit`** era o pior caso: só trocava pra `python3` no Mac/Linux (via `uname`) — **no Windows continuava chamando o shim**. Agora resolve `$PYBIN` nos blocos 5.4/5.5 (foi preciso fazer isso à mão nesta própria sessão pra abrir o PR).
- **Heredocs e here-strings** (`bunzzai` `- <<EOF`, `pull-request-review` `<< PYEOF`, `commit` `-c … <<< $VAR`) validados sob o resolver — todos OK.
- PATCH em todas (portabilidade; sem mudança de interface). **Não tocados de propósito:** docstrings internas dos `.py` (usage genérico), a doc legada `bunzzai/AUDITORIA-vs-meta-ads.md` (scripts `meta-ads/` arquivados) e o probe de detecção do `setup-agencia` (`python --version` — precisa de tratamento próprio: preferir `py` no Windows; fica pra passe separado).

## blog-publicar
### 2026-07-28 — v1.3.0 — Capa Pexels on-theme: prioriza resultado real (alt) + modo `--candidates`

Corrige a capa que saía **fora do tema**. O `search_photo_ids` extraía IDs com um regex sobre **todo** o HTML da página de busca, então capturava thumbnails **decorativas** (trending/relacionadas/promo) que o Pexels injeta **antes** da grade real de resultados — e essas costumam vir com `alt` **vazio**. A 1ª foto baixada era, na prática, uma dessas: publicando `como-trabalhar-com-micro-e-nano-influenciadores` (2026-07-28), as duas primeiras queries devolveram "homem sentado no mar" e "pegadas na areia"; só resolveu forçando `--id` de uma foto vetada à mão.

- **`search_photo_ids` → `search_photo_candidates(query)`**: parseia **só as `<img>` com `src` do CDN do Pexels** e devolve pares `(id, alt)` com as de **`alt` não-vazio (resultados reais) na frente** e as sem `alt` (decorativas) no fim, como fallback. Se nenhuma `<img>` casar (mudança de markup), cai no scan solto do HTML inteiro — comportamento antigo — pra não travar a publicação. No caso normal a ordem é **idêntica à antiga** (sem regressão — provado em teste hermético + live nas queries do incidente).
- **A linha `OK` agora imprime o `alt` que o Pexels dá pra foto escolhida** — dá pra checar se bate com o tema sem abrir o `.jpg`. Se a foto escolhida veio do fim sem `alt` (fallback decorativo), imprime **WARN** sugerindo trocar via `--id`.
- **Novo modo `--candidates "query"`** (read-only, não baixa nada): lista os candidatos `id :: alt` na ordem em que o script tentaria, marcando decorativas (`<sem alt — decorativa, evite>`) e já-usadas (`[JA USADA]`, lê o COVERS-FONTES.md). Substitui o trial-and-error cego que forçava vetar `--id` na mão — agora dá pra espiar e escolher um `id` on-theme antes de gerar.
- **Passo 0.6 do SKILL.md** atualizado (comportamento de priorização + helper `--candidates` no fluxo). MINOR — interface preservada (`--list`/geração/`--id` inalterados); só adiciona `--candidates` e o alt no log.

### 2026-07-07 — v1.2.0 — Capa padrão vira foto Pexels (Passo 0.6); gen_cover.py rebaixado a fallback

Os sócios rejeitaram o estilo HTML→PNG do `gen_cover.py` (as 20 capas existentes foram trocadas por fotos do Pexels em 2026-07-07). O Passo 0.6 agora usa o novo `pexels_cover.py`: para cada post sem `cover:`, o agente escolhe uma query de busca em inglês (cena concreta do tema) + `coverAlt` em PT-BR, e o script busca no Pexels (scrape keyless da página de busca com User-Agent de browser — sem API key), pula fotos já usadas em outras capas, baixa recortada 1200×630 direto pelo CDN (`?w=1200&h=630&fit=crop`) em `public/assets/covers/{slug}.jpg`, preenche `cover`/`coverAlt` no frontmatter e registra a proveniência na tabela de `COVERS-FONTES.md` (criando o arquivo se não existir). Depois o agente confere a foto (Read no .jpg) e ajusta o alt se a cena vier diferente. Segue **idempotente** (post com `cover:` é pulado; re-rodar um slug atualiza a linha da tabela em vez de duplicar).

- **`gen_cover.py` vira fallback explícito**: só quando a busca falha (rede/bloqueio/zero resultados após 2–3 queries), pra não travar a publicação — e a skill manda sinalizar no relatório que a capa saiu no estilo rejeitado e precisa ser trocada por foto.
- **Sem Playwright no caminho feliz**: o fluxo Pexels só usa curl (nativo) + urllib; browser só é necessário no fallback.
- **Pegadinha Windows documentada no script**: `subprocess.run(["curl", ...])` resolve pelo CreateProcess, que olha System32 **antes** do PATH — e a curl do Windows leva 403/1010 do Cloudflare do pexels.com (fingerprint TLS banido), enquanto a curl do Git (mingw64) passa. O script resolve o caminho absoluto via `shutil.which` e ainda tenta a curl do Git como candidato seguinte. O CDN de imagens não tem o bloqueio (urllib direto).
- MINOR — interface da skill inalterada; muda o estilo/fonte da capa gerada. No mesmo passe: `blog-diario` v1.0.1 (nota no Passo 8: artefato Astro-ready fica **sem** `cover`/`coverAlt` de propósito — é o que aciona o fluxo de foto na publicação) e seção "Posts novos" do `COVERS-FONTES.md` atualizada (fluxo automatizado em vez de manual).

### 2026-07-02 — v1.1.0 — Capas OG automáticas (Passo 0.6)

Antes do build, a skill agora gera a **capa/OG de qualquer post sem `cover:`** via `gen_cover.py` (Playwright, template HTML→PNG 1200×630) e preenche `cover`/`coverAlt` no frontmatter. Assets 100% da marca (off-white + gradiente assinatura + mascote + logo raster) — zero risco de copyright. **Idempotente** (pula quem já tem capa). A imagem serve como capa no topo do post, card da home e `og:image` de compartilhamento. MINOR (nova capacidade; publicar seguia funcionando sem). As 20 primeiras capas do blog foram geradas com o mesmo template.

### 2026-07-02 — v1.0.0 — Deploy governado do blog Astro no Vercel

Primeira versão. Publica o blog estático (`blog/{marca}`, hoje Buzzcreators) no projeto Vercel: pré-flight (auth + resolve URL de produção com fallback `.vercel.app`), build local como **gate de meta tags** (o `content.config.ts` falha o build se um post violar os limites), deploy `--prod` com `PUBLIC_NOINDEX=false`, validação da versão no ar (posts/sitemap/rss/llms + sem noindex) e relatório. Sem sibling (blog é estático, sem middleware/PII/vizinhas). Contexto sancionado da trava de deploy Vercel (`guard_vercel_deploy.py`).

## dashboard-atualizar
### 2026-07-02 — v2.0.2 — `HERANCA_SOURCES_INTERNAS` no check de sincronia (Passo 0.2b)

A constante nova de `queries.py` (sources internas que não bloqueiam a herança de atribuição — criada na mudança de atribuição por contato de 2026-07-02) entrou na lista de constantes auditadas entre oficial × espelho. Sem isso, uma divergência futura nela passaria batida (o check só compara o que está na lista — foi assim que o ECHEF ROBOT voltou em 2026-07-01). PATCH.

A mudança de regra em si (atribuição 90d por **contato** em vez de conta + guarda de origem + blacklist/whitelist nos eventos via `predicado_evento()`) vive em `dashboard/queries.py` + `dashboard-pessoal/lib/queries.py` + `dashboard-buzz-br-vercel/exportar_dados.py` e está documentada em `dashboard/MAPEAMENTO-CAMPOS.md` §3 — não é versionada por esta skill.

### 2026-07-02 — v2.0.1 — Nota de re-validação de paridade roda via `uv` (evita o shim Python do Windows)

Ajuste pontual: a nota de manutenção "re-validar após mudar motor/queries" chamava `python paridade_gerar_esperado.py` direto. No Windows, esse `python` é o shim da Microsoft Store (exit 49), e o script importa `psycopg` (C-extension) — então precisa mesmo de `uv`. Alinhado ao padrão do resto da skill: `uv run --python 3.12 --with "psycopg[binary]" python …`, que provisiona o próprio 3.12 com wheels. O **fluxo principal já rodava em `uv`** (Passos 0.2b/1) e não muda. PATCH. Contexto do shim: entrada `lp-publicar, lp-sync` de 2026-07-02 + `landing-pages/CONTEXT.md` §6.

### 2026-07-01 — v2.0.0 — Dash dinâmica-estática no Vercel (date-picker + dados 2026), substitui o snapshot

A dashboard no link do Vercel deixou de ser o snapshot semanal fixo e passou a ser a **dash dinâmica** (date-picker de intervalo livre + todos os dados de 2026), servida **estática** — sem o Vercel tocar no Supabase (o pooler IPv4 não aceita `looker_readonly`). Contexto e arquitetura em `dashboard-buzz-br-vercel/PLANO-VERCEL.md`.

- **Arquitetura:** exportador Python (`dashboard-buzz-br-vercel/exportar_dados.py`) reusa `dashboard-pessoal/lib/queries.py` (lógica CM = fonte única) → `dados-2026.json` (~290KB). O navegador (`motor.js`) deriva os 4 períodos + agrega por intervalo, entregando ao `render()` o mesmo formato de antes. `index.html` adaptado da dash local (fetch à API → motor local); visual/gráficos inalterados.
- **Paridade validada:** `paridade_gerar_esperado.py` (dash local, fonte da verdade) × `paridade_check.mjs` (motor) → **916 checagens, 0 divergências** em intervalos variados (1 dia, cross-month, mês, ano). Cobre KPIs, listas (dedup por e-mail no range), rankings (inclusive o quirk do `JOIN USING` que zera dimensão NULL).
- **Skill reescrita:** fluxo = exportar → copiar 3 arquivos (index.html + motor.js + dados-2026.json) pra sibling → deploy → validar (401 sem senha, 200 nos 3 arquivos, noindex, index referencia MotorCM). Sem o gate de EXPECTED do snapshot (dados vêm do export; sanity check no lugar). Bump MAJOR (muda o que a skill faz).
- **Segurança reaproveitada:** mesma sibling protegida (senha forte + noindex + SSO Standard). Troca de filtro ~150ms (vs ~14s da local).
- **Guarda de sincronia (Passo 0.2b):** a skill agora audita, no pré-flight, se o filtro CM do espelho (`dashboard-pessoal/lib/queries.py`, que o exportador usa) bate com o oficial (`dashboard/queries.py`) — o ECHEF ROBOT (deal 186199) reapareceu na 1ª subida porque a blacklist estava só no oficial; sincronizado em `dashboard-pessoal/lib/queries.py` e a guarda evita repetição.
- **Tabela "Leads Perdidos"** passou a seguir o período do filtro (era fixa no mês corrente — ficava vazia no início do mês e não acompanhava o date-picker); título ajustado pra "no período". Consistente com as demais listas. Motor + validador de paridade atualizados juntos.
- **Funil inclui deals que fecharam (Causa 1 da auditoria de reuniões):** as queries de funil (lead/CE/RA/RR/Prop, rankings, série, proporção) passaram a ler de `deals_comercial_prod` **+** `deals_contratos_prod` via o helper `fonte_deals_funil()` (dedup por id, prioriza comercial). Antes, quando um deal fechava e migrava pra contratos, todo o funil dele sumia da contagem — só o fechamento restava. Perdidos (coorte) e a CTE `conversoes_cm` não mudam. Efeito 2026: RA +5, RR +5, CE +5, leads +5, prop +6 (a fatia CM dos fechados). Paridade revalidada: 916 checagens, 0 divergências. **Nota:** `dashboard/queries.py` (snapshot aposentado + `/auditar-deals-cm`) NÃO recebeu essa mudança estrutural; a guarda 0.2b compara constantes, não a fonte — replicar lá se quiser consistência total.
- Snapshot antigo (`dashboard/gerar_relatorio.py`) aposentado; mantido no repo para auditoria.

### 2026-06-30 — v1.1.0 — Credencial Basic Auth sai do código versionado; SSO Standard + senha forte + noindex

Reforço de segurança da dashboard CM Buzzmonitor BR no Vercel (pedido do Victor — blindar contra acesso de terceiros).

- **Credencial Basic Auth deixou de ser hardcoded** na skill (era `inhouse:inhouse@77`, exposta no git). A skill agora resolve `DASHBOARD_BASIC_AUTH_USER`/`_PASS` de `.env.local` (gitignored — novo Passo 0.6) e usa nos curls de validação (§4.1, §4.4). A senha **forte** real vive só no `.env.local` + no `middleware.js` da sibling (fora do repo), sincronizados. Senha antiga `inhouse@77` aposentada.
- **Contexto da decisão (medido, não suposto):** o Vercel Authentication (Standard Protection, ligado no painel) cobre só as URLs internas de deploy (`*-elife-group.vercel.app` → `302 vercel.com/sso-api`), **NÃO** o domínio principal `dashboard-buzzmonitor-brasil.vercel.app` (responde direto com o Basic Auth do middleware). Proteger o domínio via SSO exigiria o add-on pago "All Deployments" (vetado pelo custo). Logo, a tranca real do domínio público é a senha forte do middleware; o SSO Standard fica como camada extra grátis.
- **Anti-descoberta** (na sibling, não-versionada): `vercel.json` ganhou `X-Robots-Tag: noindex, nofollow, noarchive, nosnippet`; criado `robots.txt` com `Disallow: /`.
- Sem mudança de args nem de fluxo. Bump MINOR pela nova dependência de env (`.env.local`).

## blog-diario
### 2026-07-07 — v1.0.1 — Nota no Passo 8: artefato sem `cover`/`coverAlt` (capa entra na publicação)

O frontmatter Astro-ready do artefato local fica **sem** `cover`/`coverAlt` de propósito: a capa (foto Pexels) é gerada na publicação pelo Passo 0.6 da `blog-publicar` (`pexels_cover.py`), que só atua em post sem `cover:`. Detalhes na entrada blog-publicar v1.2.0 desta mesma data. PATCH — só documentação do contrato entre as duas skills.

### 2026-06-30 — v1.0.0 — Skill inicial: blogpost SEO/GEO diário autônomo, multi-marca

Skill standalone que gera **1 blogpost otimizado para SEO + GEO** por execução, a partir dos clusters de tema da marca, e publica rascunho no Notion (`SEO > {Marca} > Conteúdos complementares`). Pensada pra rodar diariamente via `/schedule` ou `/loop 1d`.

- **Autônoma** (decisão do Victor): sem pausa de aprovação — escolhe o tema pelo score e segue. Arg opcional `[tema]` força um tema e pula a seleção.
- **Seleção = bake-off de volume multi-fonte:** monta 3–4 candidatos dos clusters × 2–3 variações de keyword, mede volume no **Semrush** (`execute_report`/`keyword_research`) cruzado com **fontes grátis** (Google autocomplete/PAA via WebSearch, Trends, GSC) que **corroboram ou refutam** o Semrush, e escolhe o melhor match: `0.30·volume_validado + 0.25·gap + 0.20·prioridade_cluster + 0.15·relação_produto + 0.10·equilíbrio_funil`.
- **Anti-duplicação:** Passo 1 carrega e atualiza o inventário de posts existentes (blog-cache.md + crawl do sitemap vivo + rascunhos Notion + state) antes de selecionar; dedupe por **intenção**, não só keyword.
- **Saída SEO/GEO:** bloco METADADOS completo (slug, title, meta description, keywords, cluster, categoria, links internos) + artigo resposta-primeiro com TOC, H2 em pergunta, FAQ (FAQPage), `tldr` e links internos só reais.
- **CTA por funil:** ToFu sem CTA duro; MoFu/BoFu com CTA inline + final pra 1 módulo (grafia exata do BRANDBOOK) + LP do catálogo + UTM `utm_source=blog-{marca}&utm_campaign={campaign}&utm_content={slug}`.
- **Anti-IA MÍNIMO** (decisão do Victor): só precisão factual (zero stat/case inventado, stat com fonte) + grafia exata + correção linguística regional; **não** roda a varredura de `regras-anti-ia.md`.
- **Multi-marca/região:** corpo neutro; tudo específico vem de arquivo chaveado por marca/região. **v1 pronto: Cxpress BR** (Buzzmonitor BR e demais acendem quando o Victor enviar os clusters).
- **Entrega:** rascunho Notion hoje; artefato local Astro-ready (`blog-seo/{marca}/{regiao}/{DATA}-{slug}.md`) pra posting via API no futuro.

Arquivos: `.claude/skills/blog-diario/{SKILL,CONTEXT}.md`; conhecimento `conhecimento/copywriting/blog-seo-copy.md`, `conhecimento/editorial/geo-checklist.md`, `conhecimento/editorial/metadados-seo-spec.md`; dados `conhecimento/produto/cxpress/seo/clusters-brasil.md`, `landing-pages/catalogo/lps-{cxpress,buzzmonitor,buzzcreators,elife}.md`; nova chave `seo` em `conhecimento/config/notion-ids.md`.

## lp-publicar, lp-sync
### 2026-07-02 — lp-publicar v3.9.3 + lp-sync v1.0.3: resolver de interpretador Python (`$PYBIN`), resiliente ao shim da Microsoft Store no Windows

Num recovery de LP em 2026-07-02, `python sync_sibling.py` (e os demais `python -c` das skills) falharam com **exit 49** (`Python was not found; run without arguments to install from the Microsoft Store`). Causa: no Windows, o `python`/`python3` no PATH do Git Bash é o **shim da Microsoft Store** — o arquivo existe (`command -v` acha), mas quebra ao rodar de verdade. O launcher `py` aponta pro Python real. Foi preciso trocar `python`→`py` à mão pra concluir o sync; esta mudança automatiza isso.

- **Convenção nova (lp-publicar Passo 0.4):** cada snippet bash resolve o interpretador testando **execução** (não só existência — o shim passa no `command -v` e só falha ao rodar) e usa `$PYBIN`: `PYBIN=""; for _c in py python3 python; do command -v "$_c" … && "$_c" -c '' … && { PYBIN="$_c"; break; }; done; PYBIN="${PYBIN:-python}"`. Windows → `py`; macOS/Linux (sem `py`) → `python3`/`python`. Single-token de propósito: os scripts (`sync_sibling.py`, `csp_drift_check.py`) são stdlib-only e rodam em qualquer versão.
- **Aplicado em todas as fronteiras com o Python:** lp-publicar 0.5.d.ii (`projectId`/`orgId` + parse do RESPONSE), 0.5.d.iii (`sync_sibling.py`), 1.6 (`csp_drift_check.py`) e 2.4 (REDIRECT_COUNT/MAP); lp-sync Passos 4 e 5. Inlinado por bloco (o `PYBIN` não persiste entre execuções de shell), junto do `to_win_path` — as duas convenções são ortogonais e complementares (`$PYBIN` = **qual** interpretador; `to_win_path` = normalização do **path** que chega nele).
- **Não confundir com as skills de C-extension:** `dashboard-*` e `auditar-deals-cm` usam pandas/psycopg e continuam em `uv run --python 3.12` (que provisiona o próprio Python 3.12 com wheels; o `py -3.12` nem sempre está instalado) — não adotam `$PYBIN`.
- Doc de troubleshooting em `landing-pages/CONTEXT.md` §6. No-op em máquinas onde `python` já é o Python real. PATCH (correção de portabilidade; sem mudança de interface ou comportamento esperado).

### 2026-06-30 — lp-publicar v3.9.2 + lp-sync v1.0.2: normalizar path Windows pro Python + não silenciar a leitura do REDIRECT_MAP

Ao republicar `que-es-mcp` em `webinar.buzzmonitor.com`, o smoke test 3.4.b deu **2 falsos positivos de "REGRESSAO"** (`agentes-automacao-junho-2026` e `webinar-territorios-marca-mundial-junho-2026`) — ambos slugs que são `source` de redirect 308 no `vercel.json`. Causa-raiz (Windows/Git Bash): o `python -c` do Passo 2.4 recebeu o path do `vercel.json` em forma **MSYS** (`/c/Users/...`), que o **Python do Windows não entende** → `FileNotFoundError`. O `2>/dev/null` no comando **mascarou** o erro, `REDIRECT_MAP` ficou **vazio em silêncio**, e a lógica de redirect da v3.9.0 (que validaria essas vizinhas por `Location` em vez de hash) nunca carregou — então elas caíram no baseline-por-hash e o `curl` sem `-L` do 308 nunca bateu. Risco maior do que o ruído: um falso positivo recorrente pode mascarar uma regressão **real** numa vizinha.

- **Convenção nova e obrigatória (Passo 0.3):** todo path passado ao Python — `python -c` inline **ou** env var consumida por helper `.py` — é normalizado para formato Windows (`C:/...`, via `cygpath -m` com fallback `sed`) antes de chegar ao Python. As ferramentas bash entendem as duas formas; o Python do Windows só entende a Windows. No-op em macOS/Linux. Helper `to_win_path()` inlinado em cada snippet que toca o Python (não persiste entre execuções de shell).
- **Aplicado em todas as fronteiras com o Python:** Passo 0.5.d.ii (`projectId`/`orgId` + guarda de leitura vazia), 0.5.d.iii (`SIBLING` exportado pro `sync_sibling.py` — que **escreve** arquivos; path MSYS gravaria em `C:\c\Users\...` em silêncio), 1.6 (env vars do `csp_drift_check.py`) e 2.4 (REDIRECT_MAP).
- **REDIRECT_MAP deixou de silenciar a leitura:** removido o `2>/dev/null`; sonda de `REDIRECT_COUNT` antes do mapa — se a leitura falhar (saída não-numérica) **aborta** com a causa provável; e se o `vercel.json` declara `redirects` mas o mapa sai vazio, **aborta** em vez de seguir e gerar falso positivo no 3.4.b.
- **Defesa em profundidade nos helpers:** `sync_sibling.py` e `csp_drift_check.py` normalizam o path internamente (MSYS → Windows) também — protege invocação standalone, idempotente para path já Windows e no-op em Unix/relativo.
- **`lp-sync` v1.0.2 (mesma correção):** o Passo 4 do `lp-sync` tem o `python -c` idêntico (lê `projectId`/`orgId` do `.vercel/project.json`) e o Passo 5 exporta `SIBLING` pro mesmo `sync_sibling.py` — ambos ganharam normalização Windows-style + guarda de leitura vazia. Era o mesmo bug latente; corrigido junto pra não deixar a skill irmã quebrando no Windows.
- Mesma família de pegadinha já documentada na memória do agente (Python lê/grava `/tmp` em `C:\tmp`, bash usa o `/tmp` do MSYS). Incidente em `landing-pages/CONTEXT.md` §7.2 (2026-06-30) + linha de troubleshooting no §6. Sem mudança de interface.

### 2026-06-25 — lp-publicar v3.9.1 + lp-sync v1.0.1: detecção de guarda-chuva pagina `vercel alias ls`

Ao restaurar a LP `mcp-na-pratica-p` (`webinar.buzzmonitor.com`), a detecção de modo do `lp-publicar` Passo 0.5.b retornou vazio e cairia em **modo solo por engano** — criaria projeto Vercel duplicado que não serve o domínio. Causa: `vercel alias ls` pagina (~20 aliases/página, mais recentes primeiro) e imprime `... --next <token>` no rodapé; o domínio guarda-chuva, antigo, estava na **página 2**, e o `awk` só lia a primeira página.

- **lp-publicar Passo 0.5.b** e **lp-sync Passo 1** agora iteram as páginas via token `--next` (teto de 50 páginas) até achar o domínio ou esgotar. Match na coluna 2 (`$2 == d`); de quebra, o lp-sync deixou de usar `$0 ~ d` (que casava substring na source URL) e passou a `$2 == d`. Sem mudança de interface.
- Bug latente desde que cada guarda-chuva passou de ~20 aliases — afetaria **qualquer** domínio antigo da org, não só este. Os 4 incidentes históricos de regressão em `webinar.buzzmonitor.com` (CONTEXT §7.2) reforçam o peso de a detecção de guarda-chuva ser confiável.

## meta-campanha
### 2026-06-24 — v1.1.0 — Calibrar defaults pela auditoria de uma campanha REMKT real da conta

Comparei o 1o teste (MOFU-VRJ-0626) com campanhas de remarketing reais da Buzzmonitor BR (`[BR][CONVERSAO][Remarketing-IA]` etc.) e ajustei os defaults da skill pra espelhar a casa:

- **Conversao por padrao, nao trafego.** A conta roda `OFFSITE_CONVERSIONS` (com pixel) em quase tudo — inclusive MoFu e remarketing. Tabela funil->objetivo revista + nova linha MoFu. So usar `OUTCOME_TRAFFIC`/`LANDING_PAGE_VIEWS` quando NAO ha pixel/evento.
- **Pixel obrigatorio em conversao:** `promoted_object={"pixel_id","custom_event_type"}` via `ads_get_datasets`.
- **UTM padrao de TODAS marcas/regioes** (decisao do Victor) embutido no `link_url`, com macros dinamicos da Meta: `utm_source=meta&utm_medium={{placement}}&utm_campaign={{campaign.name}}&utm_content={{ad.name}}&adset={{adset.name}}&campaignid={{campaign.id}}&adsetid={{adset.id}}&adid={{ad.id}}`. A casa cruza UTM com deals; sem isso a atribuicao cega.
- **Esclarecido:** pixel (`promoted_object`) e targeting (geo/idade/custom audiences) sao setaveis na criacao E edicao (write); a limitacao do MCP e so de LEITURA (nao clona de campanha existente). Furo unico: interesse-por-ID (sem tool de busca).
- **Orcamento default ABO** (a casa usa adset R$20-70/dia), nao CBO.
- **Idade default 28-50**; **nao excluir idade desconhecida** por padrao (esp. WhatsApp) — decisao do Victor.
- **CTA por funil** (SEE_DETAILS/SIGN_UP/BOOK_NOW/GET_QUOTE no fundo), nao `LEARN_MORE` cego.
- **Nome de campanha na convencao da casa** `[BR][CONVERSAO][Tema]`; nota que a Meta acrescenta ` YYYY-MM-DD-<hash>` ao nome do criativo.
- **Limitacao de leitura do MCP documentada:** nao expoe pixel/destination/targeting/url_tags -> nao da pra clonar de campanha existente; perguntar ao Victor.

### 2026-06-24 — v1.0.0 — Skill inicial: criar e gerir campanhas Meta Ads via MCP oficial (escrita real)

Primeira skill de **escrita** no Meta Ads (ate entao so leitura via /bunzzai). Usa o MCP oficial da Meta (`mcp__<id>__ads_*`, OAuth) e atua como gestor de trafego senior.

- **6 acoes:** criar campanha/adset/ad · editar (publico/posicionamento/orcamento/link) · pausar/religar · renomear.
- **Seguranca em 2 camadas:** a skill forca briefing completo e mostra o plano pra confirmar; o hook novo `guard_meta_activate.py` (molde do guard do Vercel) trava **ativacao/religacao** e **orcamento acima do teto** (`meta-ads/data/budget-guardrails.json` — conservador R$50/$12/EUR12 por adset/dia). Tudo nasce PAUSADO; nada gasta sem aprovacao. Por defesa, o hook cobre tambem as tools de escrita do BunzzAI.
- **Gestor expert:** classifica funil (tabela do /bunzzai) -> objetivo ODAX + optimization_goal coerentes; sanity-check de publico vs ICP da marca (questiona incoerencia); benchmarks de CpL/CTR de `meta-ads/data/benchmarks.json`.
- **Criativo (3 fontes):** post/acervo existente (`object_story_id`/`image_hash`) ou arquivo novo (PC/Drive/repo `/criativo`) auto-hospedado via Vercel -> `image_url` (o MCP da Meta nao sobe arquivo local).
- **Anti-ban:** so MCP da Meta, requisicoes minimizadas (1 leitura de contas/sessao + cache + log local pra edicoes). Hook **uuid-agnostico** (casa por sufixo `ads_*`, nao depende do id do server).

Arquivos: `.claude/skills/meta-campanha/{SKILL,CONTEXT}.md`, `.claude/hooks/guard_meta_activate.py`, `meta-ads/data/budget-guardrails.json`, matcher novo em `.claude/settings.json`, ponteiro em `.claude/skills/anuncios/SKILL.md`.

## seo-report
### 2026-07-02 — v1.0.1 — Resolver de interpretador Python (`$PYBIN`) nos blocos PowerShell + nota anti-shim

Os pré-checks e a execução do coletor Google chamavam `python` direto (PowerShell, Windows). No Windows, esse `python`/`python3` é o shim da Microsoft Store (exit 49) — o mesmo problema das skills lp-*. Adicionado um resolver PowerShell (`$PYBIN`) em cada bloco Python do Passo 2 (pré-condições, `pip install`, execução do script), que testa execução e prefere `py` (Python real), caindo em `python3`/`python` fora do Windows. A nota de troubleshooting "Python não instalado" deixou de recomendar a Microsoft Store (é justamente o alias que falha) e passou a apontar python.org (registra o launcher `py`); adicionada linha explícita pro erro exit 49. PATCH (portabilidade; sem mudança de fluxo). Nota: o probe usa `-c 'import sys'` (não-vazio) porque o PowerShell descarta o argumento `''` do operador de chamada.

### 2026-06-23 — v1.0.0 — Skill inicial: dashboard SEO Buzzmonitor BR (GSC + GA4 + Semrush), sem chave de API no repo

Skill nova (base no PR #24 da Bárbara) que gera um dashboard HTML de SEO cruzando Google Search Console, Google Analytics 4 e Semrush. Reescrita para ser **universal e segura** antes de entrar:

- **Semrush via MCP, sem chave hardcoded.** A versão original trazia `SEMRUSH_API_KEY` em texto puro no script (secret commitado). Agora a parte Semrush é buscada pela skill via MCP do Semrush (`domain_rank` para overview + `domain_organic` para top keywords, `database=br`). Zero chave de API no repositório.
- **Script Python só Google (GSC + GA4), credenciais locais.** OAuth2 com `client_secret.json`/`token.json` por usuário, num diretório de trabalho fora do repo (`~/.seo-report-buzzmonitor/` ou `SEO_REPORT_DIR`). Nada de caminho de máquina hardcoded (a versão original apontava para `D:\Meus documentos\...`). `.gitignore` da pasta protege credenciais e saída.
- **Entrega real.** O passo final salva o HTML no diretório de trabalho e abre no navegador (`Start-Process`), no lugar da tool inexistente `Artifact` da versão original.
- **Frontmatter no padrão do repo:** `allowed-tools` (incl. tools do MCP Semrush) + `argument-hint` (no lugar de `trigger:`/`args:`).

## roteiro-webinar-perpetuo
### 2026-06-23 — v1.4.0 — Acoplar a skill a base de conhecimento (persuasao + anti-IA), sem hardcodar

Auditoria da skill contra toda a base de conhecimento + skills irmas (copy-criar, copy-revisar, pauta-quente, trad-revisar). A skill citava tecnicas de copy sem operacionaliza-las, e o passo anti-IA era o mais fraco de todos os revisores irmaos. Principio do PR: a skill **referencia e aplica** tecnicas por nome de secao (lidas do doc em runtime), nunca transcreve conteudo — melhorar um doc de copy melhora o roteiro sem tocar na skill.

**Persuasao (faz o roteiro converter) — tudo via ponteiro pra `conhecimento/copywriting/`:**
- **Cadeia de premissas (Ladeira)** virou campo obrigatorio do plano (Passo 2): monta a escada de 3-4 premissas usando "Premissas para {TOFU|MOFU|BOFU}" + "Temperatura de publico" do `funil-copy.md`. E o esqueleto logico do Bloco A.
- **Hook com barra de qualidade + 2-3 candidatos** (Passo 2): rascunha multiplos, aplica o "teste do comeco forte" de `fundamentos-copy.md`, escolhe 1 com justificativa. Antes era "escolhe 1 do menu".
- **Open-loops + callback** (regra 8): planta no hook, paga na demo/recap — "Gere expectativa" + "Expectativa e misterio" (`fundamentos-copy.md` / `video-curto-organico.md`). Retencao num formato sem Q&A.
- **Postura de fala** (regra 9): "3 erros invisiveis" + lo-fi/conversacional — antidoto pra "locucao corporativa".
- **Demo = prova, nao tour** (regra 10): "Mostrar vale 10x" (antes/depois ou numero na tela) + "De comandos a sua audiencia" (1 comando/bloco = micro-compromisso). Novos campos no template de cada demo.
- **Dor pelo storytelling** (regra 11): 5 passos de `fundamentos-copy.md` com objeto tangivel recorrente.
- **Quebra de objecao antes do CTA** (Bloco C, novo beat): "Tratamento de objecoes" do `funil-copy.md`. Antes ia recap→CTA frio.
- **CTA com beneficio + reducao de risco** (regra 12): secao "CTA em e-mail" do `email-copy.md`.
- **Titulo/Slide 1 com gancho de curiosidade**: "Subject line" do `email-copy.md`.

**Anti-IA + fidelidade (Passo 5 reescrito — fecha a lacuna vs copy-revisar):**
- **Contagens obrigatorias + re-check em loop (5.4):** apos corrigir, roda as contagens do `regras-anti-ia.md` (em-dash via Grep = 0; antitese; filler 2.0; ritmo) e refaz ate 2 rodadas — porque a propria correcao reintroduz IA. Limites ficam no `regras-anti-ia.md` (fonte unica), nao recopiados na skill.
- **Guarda de deriva de dialeto (5.5):** se `idioma` != `pt-br`, rele o texto corrigido vs `padrao-linguistico.md` (brasileirismo volta na reescrita).
- **Varredura de fato (5.6):** numero/case/feature rastreia pro BRANDBOOK ou leva `[VERIFICAR]`; Slide 4 sem Fonte vazia; case Cxpress sempre `[VERIFICAR com Victor]`.
- **`samplePhrases.do/dont` virou check (5.2):** era carregado e nunca usado.
- **REVISAO-LOG com tabela de contagens + severidade + nota de naturalidade (5.8)**, alimentando o gate `requer-atencao-humana`.

**Carga:** Passo 1 agora tambem le `video-curto-organico.md` + `email-copy.md`. **NAO** foram wirados `RESUMO-COPY.md` (arquivos inexistentes no repo) nem swipe-file (1 entrada, so newsletter) — seriam galhos mortos. Atualizados: SKILL.md (Passos 1-5 + regras universais + templates), CONTEXT.md (pilar boas-praticas), frontmatter 1.3.0 → 1.4.0.

### 2026-06-23 — v1.3.0 — Idioma opcional, inferencia de marca e brandbook completo

Tres aprimoramentos pedidos pelo Victor, todos retrocompativeis (chamadas antigas `[marca] [regiao] [duracao] [tema]` seguem funcionando).

- **`idioma` como input opcional, no mesmo eixo que `regiao` (1:1).** Aceita `pt-br`/`pt-pt`/`es-latam` (e os atalhos `br`/`pt`/`es`). O usuario pode passar so a regiao, so o idioma, os dois ou nenhum — a skill deriva o que faltar (Passo 0.1). Se passar os dois e forem inconsistentes, o idioma manda na copy e avisa no plano. O `idioma` resolvido (nao mais a regiao) passa a dirigir TODO o pilar linguistico: pasta `conhecimento/linguistico/`, terminologia de produto localizada, anexo anti-IA por idioma e o campo `idioma:` no frontmatter de roteiro, slides e INDICE. Gate reforcado: idioma != pt-br sem `padrao-linguistico.md` carregado → PARA.
- **Inferencia de marca.** `marca` virou opcional. Se omitida, a skill infere do tema por uma tabela de sinais (buzzmonitor=social listening, cxpress=atendimento/WhatsApp, buzzcreators=influencia, elife=consultoria/social intelligence), declara a inferencia no plano e no resumo final pro Victor corrigir, e PARA em caso de empate. Unico argumento obrigatorio agora e o `tema`. Parsing por vocabulario disjunto (marca/regiao/idioma/duracao reconhecidos pelo valor, em qualquer ordem).
- **BRANDBOOK completo.** Passo 1 agora le o `brand/{marca}/BRANDBOOK.md` INTEIRO (nao so secoes extraidas), com atencao a secao "Adaptacao por Regiao" (artigo gramatical + subsecao do idioma) — alinhado com a geracao idioma-aware.
- Atualizados: SKILL.md (Passo 0 reescrito + 0.1/0.2, Passo 1, plano, regras universais, frontmatter de slides, resumo final, Regras Criticas), CONTEXT.md (marcas+inferencia, eixo regiao⟺idioma, pilar linguistico) e CLAUDE.md (secao Webinar). Frontmatter bump 1.2.0 → 1.3.0.

### 2026-06-23 — v1.2.0 — Remover etapa de notas de producao

Decisao do Victor: a skill nao gera mais o `notas-producao.md`. A v1.1.0 ja tinha enxugado o arquivo so pra tabela "Telas a capturar/preparar"; agora a etapa sai por completo.

- **Passo 5 (Notas de Producao) removido** e os passos seguintes renumerados: Revisao Anti-IA 6→5, Salvar Arquivos 7→6, Publicar no Notion 8→7, Resumo Final 9→8 (subsecoes e referencias cruzadas ajustadas junto).
- **Tirado de todos os pontos que citavam o arquivo:** intro (lista de entregaveis agora e 2 — roteiro + deck), arvore de arquivos do Passo 6, template do INDICE, toggle "Notas de producao" da pagina Notion (Passo 7) e o resumo final (Passo 8).
- **Nenhuma informacao perdida:** o que ia pra tabela de telas ja vive dentro do `roteiro.md` — cada momento de demo tem "O que mostrar" + "Recursos necessarios". Preparar telas/contas continua sendo decisao de quem grava, fora do escopo do roteirista.
- **Entregaveis agora (4 arquivos):** `roteiro.md`, `slides-abertura.md`, `INDICE.md`, `REVISAO-LOG.md`.
- **Entrega de exemplo atualizada** (Buzzmonitor BR · "Seu primeiro listening em 5 passos"): `notas-producao.md` apagado, referencias removidas do INDICE e do REVISAO-LOG.

### 2026-06-22 — v1.1.0 — Notas de producao enxutas + features em ingles parafraseadas

Dois ajustes pedidos pela Catharina no primeiro uso da skill (Buzzmonitor BR · "Seu primeiro listening em 5 passos").

- **`notas-producao.md` para apos "Telas a capturar/preparar".** Cortadas as secoes Dados sensiveis, Dependencias de feature, Equipamento, Vestuario, Pos-producao e Checklist pre-gravacao. Motivo: essas decisoes ficam com o time de producao, nao com o roteirista — entregar so isso evita atravessar a sua zona de decisao. Template do Passo 5 simplificado, regra explicita ("REGRA — `notas-producao.md` para aqui").
- **Features em ingles parafraseadas na 1a mencao.** Adicionada regra 7 nas "Regras universais" do Passo 3: a grafia oficial (Theme Monitoring, Sentiment Classification, Buzz Pills, Auto Tag Suggestions etc — tabela `### Features de IA` do BRANDBOOK) continua obrigatoria, mas na 1a mencao o speaker explica em PT-BR/PT-PT/ES-LATAM em 5-10 palavras, integrado a fala (ex: "Aqui dentro do Theme Monitoring — que e onde voce cria os temas que vai monitorar"). Sem isso, o lead leigo trava no nome em ingles. Vale tambem pra deck: preferir descricao em PT-BR no slide e citar o nome oficial entre parenteses se necessario.

### 2026-06-22 — v1.0.0 — Nova skill: roteiro de webinar perpetuo + slides de abertura

Criada a partir de pedido para roteirizar um webinar perpetuo de 10 min ("Seu primeiro listening em 5 passos") da Buzzmonitor. O `/copy-criar` so cobre `video-curto | estatico | email` — roteiro de webinar (talking head longo + demo da plataforma + deck de abertura) nao cabia em nenhum molde existente.

- **Estrutura padrao:** Hook → Quem fala → Promessa → Contexto + Dor → Ponte → Demo (3 momentos, 40-50% do tempo) → Resumo + Prova → CTA repetido 2x. Distribuicao de tempo dimensionada para 5/10/15/20/30 min.
- **Talking head com demo:** roteiro entrega timestamps, falas-modelo (70% do tempo) + bullets de fallback (30% mais livre), indicacoes cenicas entre colchetes e mudancas de tela (slide ↔ compartilhamento da plataforma). Aplica esqueleto T·MAES·A/N dentro de cada bloco.
- **Demo lastreada no BRANDBOOK:** as 3 telas/features da demo usam grafias exatas do `brand/{marca}/BRANDBOOK.md` (ex: `Buzzmonitor Social Listening`). Se a marca nao tem mockup para uma feature, marca `[VERIFICAR COM PRODUTO]` em vez de inventar.
- **Deck de abertura:** 5-7 slides PPT/Keynote (capa, quem fala, promessa, dado, dor, ponte, CTA final), 1 ideia por slide, com notas visuais — sem clipart generico.
- **Notas de producao:** terceiro arquivo da entrega lista telas a capturar, dados a anonimizar, dependencias de feature, equipamento sugerido e checklist de pos-producao.
- **3 pilares carregados:** padrao linguistico (se regiao != brasil), fundamentos-copy + funil + video-curto-talking-head, regras-anti-ia + anexo do idioma. Revisao anti-IA dedicada pos-geracao (Passo 6) com lista especifica de anti-patterns de webinar ("Bem-vindos ao nosso webinar", "Voces estao prontos?", "saiba mais" como CTA).
- **Publicacao Notion:** subpasta `Webinars — {NomeDaMarca}` dentro de Entregas (cria se nao existir, icone 🎤). Gate automatico: arquivos marcados `requer-atencao-humana` apos 2 rodadas de revisao nao sao publicados.
- Arquivos: `.claude/skills/roteiro-webinar-perpetuo/SKILL.md` + `.claude/skills/roteiro-webinar-perpetuo/CONTEXT.md`. Registro em `CLAUDE.md` (fluxo + nova secao "Webinar Perpetuo" na lista de comandos).

---

## Pipeline de Meta Ads (cross-skill: anuncios, bunzzai, setup-agencia + CLAUDE.md)
### 2026-06-22 — Substituicao do pipeline `meta-ads-*` por `/bunzzai` + `/bunzzai-geral`

Decisao do Victor: analises de Meta Ads passam a rodar **somente via MCP Bunzzai**, eliminando dependencia de token Meta que expirava a cada ~60 dias (e que precisava ser renovado por cada colaborador, com risco de quebrar fluxo). Bunzzai e MCP em tempo real, sem setup local.

- **5 skills desativadas** → movidas pra `.claude/skills-desativadas/`: `meta-ads`, `meta-ads-fetch`, `meta-ads-report`, `meta-ads-trends`, `meta-ads-geral`. Claude Code nao carrega skills fora de `.claude/skills/`, entao saem do registry automaticamente. Pra reativar: `git mv` de volta (ver `.claude/skills-desativadas/README.md`).
- **Scripts arquivados** → `meta-ads-legacy/` (raiz do repo): pipeline Python original (`fetch_*.py`, `full_analysis.py`, `trend_analyzer.py`, `report_generator.py`, `audit_vs_bunzzai.py`, etc.), `SETUP.md` do token Meta, requirements.txt, relatorios historicos e cache. Continua rodavel pra auditoria pontual (especialmente `audit_vs_bunzzai.py` quando precisar cross-checar Bunzzai vs Meta API direta).
- **Pasta `meta-ads/` enxuta** → ficou so com `data/benchmarks.json` (thresholds CpL/CTR/Conv.LP por moeda × tipo de campanha — reaproveitados pelo bunzzai) + README explicando o estado novo. `.env` e `.env.example` preservados pra auditoria pontual.
- **`/bunzzai` v1.0.0 → v1.1.0** — autossuficiente: removeu refs a `/meta-ads-trends` como cross-check, embutiu Python embed sem `cd meta-ads/scripts`, consolidou benchmarks + matriz de cenarios + classificacao de campanhas dentro do proprio `CONTEXT.md` (em vez de referenciar o CONTEXT.md do meta-ads). Cross-check passa a ser manual via `meta-ads-legacy/scripts/audit_vs_bunzzai.py`.
- **`/bunzzai-geral` v1.0.0 (NOVA)** — substituto direto do `/meta-ads-geral`: consolidado das 6 contas (Buzzmonitor BRL/USD/EUR + Cxpress BRL/USD/EUR), drill-down Conta→Funil→Adset→Ad, publica no Notion. Itera as 6 contas via MCP Bunzzai em ~2-4min, sem rate limit de token Meta.
- **`/anuncios` (advisor)** — simplificado: pergunta so 1-3 questoes (escopo: conta especifica vs consolidado; depois marca + moeda se conta) e dispara `/bunzzai` ou `/bunzzai-geral`. Fast-path `geral`/`consolidado`/`todas` vai direto pro `/bunzzai-geral`.
- **`/setup-agencia` v0.5.0 → v0.6.0** — passo 3 reescrito: removeu fluxo de geracao de token Meta no Business Manager, geracao de `.env`, instalacao de `requirements.txt` e execucao de `check_setup.py`. Substituido por: (1) verificar se MCP Bunzzai esta conectado via `claude mcp list | grep bunzzai`; (2) se nao estiver, fallback `bunzzai-mcp-falhou` direciona pro Victor. Fallbacks `token-falhou`/`token-rejeitado`/`conta-sem-acesso` foram removidos.
- **`CLAUDE.md`** — Tabela de fluxos: `Meta Ads:` agora lista so `/bunzzai` + `/bunzzai-geral`. Diretorios: `meta-ads/` documentado como enxuto, `.claude/skills-desativadas/` adicionado. Secao "Setup" perdeu o sub-passo de Meta Ads. Secao "Meta Ads (SOMENTE LEITURA)" reescrita como "Meta Ads — via Bunzzai".
- **`.gitignore`** — entradas de `meta-ads/data/meta_ads.db`, `meta-ads/data/cache/`, `meta-ads/data/reports/*.md`, `meta-ads/credentials-snapshot.md` movidas para `meta-ads-legacy/...` correspondente.

**Por que manter `meta-ads-legacy/` em vez de apagar:** os scripts ainda compilam e ficam disponiveis pra auditoria de discrepancia entre Bunzzai e Meta API direta. Particularmente util pra decisoes de budget grande (>R$ 1.000) — `audit_vs_bunzzai.py` casa entidades por `meta_id` e compara metricas.

**Migracao de jobs/loops agendados:** se voce tinha `/loop` ou `/schedule` rodando `/meta-ads*`, troque por `/bunzzai [conta]` ou `/bunzzai-geral`. Nao ha equivalente para `/meta-ads-fetch` (Bunzzai e tempo real) nem `/meta-ads-report` (Bunzzai nao tem banco local separado).

---

## Protocolo de Copy (cross-skill: copy-*, trad-*, lp-preparar, criativo + CLAUDE.md)
### 2026-06-15 — Split núcleo/pesquisa dos padrões linguísticos (corte de custo + curadoria)

Otimização do custo de token e da qualidade do padrão linguístico, depois de medir que o `padrao-linguistico.md` PT-PT custava ~5k tokens por leitura — e que as regras que mais definem o idioma ("está a + infinitivo", "utilizador") estavam enterradas no log de pesquisa, não nas tabelas do topo.

- **Split em 2 arquivos por idioma:** `padrao-linguistico.md` vira o **núcleo** (só regra acionável, ~2–2,5k tokens) e `padrao-pesquisa.md` (novo) recebe a proveniência (sites, headlines, leads coletados pelo `/trad-calibrar`). Corte de ~50% no custo de leitura em trabalho PT-PT/ES; o caso PT-BR continua em zero.
- **Curadoria (Regras de Ouro):** regras de alto impacto que viviam só no log foram promovidas pro núcleo — PT-PT: "está a + infinitivo", "precisa de + infinitivo", "utilizador", faturação/retalho/mil milhões; ES-LATAM: México = tuteo (nunca voseo), monitoreo, "Ingresa" (login), CTAs em 1ª pessoa, traduzir pipeline/leads/deals. O núcleo ficou menor **e** mais completo.
- **Blast radius zero nas consumidoras:** as 11 skills que leem o padrão (`copy-*`, `trad-traduzir`, `trad-revisar`, `lp-preparar`, `criativo`, `pauta-quente`, `news-*`) **não mudam** — mesmo path (`padrao-linguistico.md`), arquivo mais leve.
- **`trad-calibrar` v1.0.0 → v1.1.0** — único skill alterado: lê os 2 arquivos; Fase 3 grava proveniência no `padrao-pesquisa.md`; Fase 4 (agora "Promoção para o Núcleo", obrigatória) promove regras duráveis pro núcleo via Edit + guardrail anti-bloat (núcleo < ~250 linhas, nunca proveniência nele).
- Arquivos de padrão (PT-PT e ES-LATAM) bumped para **Versão 1.0** (núcleo).

### 2026-06-15 — 3 pilares obrigatórios em toda skill que gera ou altera copy

Resposta a um incidente: copy PT-PT criada por colaboradora brasileira saiu cheia de brasileirismo porque a skill usada não carregava o padrão linguístico. Auditoria das portas de entrada de copy mostrou que o rigor existe (`padrao-linguistico.md`, `regras-anti-ia.md`) mas não era carregado de forma consistente — e que, sem skill, nada carregava. Correção: contrato global no `CLAUDE.md` + fechamento das lacunas skill a skill, replicando o padrão que `news-gerar` / `pauta-quente` / `social-*` já faziam certo.

**Os 3 pilares** (carregados ANTES de escrever): (1) linguístico — `padrao-linguistico.md` do idioma quando regiao != brasil; (2) boas práticas — `fundamentos-copy.md`; (3) anti-IA — `regras-anti-ia.md` + anexo do idioma (fonte única; `estilo-newsletter.md` é só estrutura de newsletter).

- **`CLAUDE.md`** — nova seção "Protocolo de Copy (OBRIGATORIO)" no topo: os 3 pilares + regra "sem skill = pare e use a skill certa". Cobre o caso de chat sem skill (efetivo apenas dentro do Claude Code neste repo; chat fora do repo depende de processo/treino).
- **`copy-criar` v1.1.0 → v1.2.0** — anti-IA passa a apontar para `regras-anti-ia.md` (+ anexo do idioma), não mais `estilo-newsletter.md` (Passo 1 #9 e Passo 4 regra 3).
- **`copy-revisar` v1.1.0 → v1.2.0** — novo arg opcional `regiao` + detecção de idioma; carrega `padrao-linguistico.md` quando regiao != brasil; nova **Dimensão 4 (fidelidade nativa)** que flagra brasileirismo em copy PT-PT/ES; fonte anti-IA corrigida (Passo 1 #6); check de deriva de dialeto no loop pós-correção (Passo 4.5 #5). Era o caminho mais provável do incidente — revisar copy estrangeira sem nunca checar o idioma.
- **`lp-preparar` v1.2.1 → v1.3.0** — detecção de idioma da fonte (Passo 2); se != PT-BR carrega `padrao-linguistico.md` + anexo (Passo 1 #6) e roda marcação de fidelidade nativa conservadora (Passo 4.3).
- **`criativo` v1.0.0 → v1.1.0** — carrega `padrao-linguistico.md` antes de adaptar/enxugar copy quando regiao != brasil; anexo do idioma no anti-IA; confere a copy final contra o padrão (Passo 1).
- **`trad-traduzir` v1.0.0 → v1.1.0** — carrega `regras-anti-ia.md` + anexo do idioma no Passo 1 (antes só havia ~2 padrões de memória inline); Passo 5 roda contagens reais (em-dash = 0, antítese ≤ 2, filler, anexo).
- **`trad-revisar` v1.0.0 → v1.1.0** — anexo do idioma explícito na Passada 1; nova **Passada 4 (re-contagem anti-IA pós-correção + deriva de dialeto)** — corrigir não pode reintroduzir IA nem voltar pro PT-BR.
- **CONTEXT.md (copy + trad)** — callout dos 3 pilares no topo; tabela anti-IA do copy de-ambiguada (`regras-anti-ia.md` = fonte única SEMPRE; `estilo-newsletter.md` = só newsletter).

Pendente (P2, fora deste PR): hook `UserPromptSubmit` (único backstop determinístico pro chat sem skill), linter de brasileirismo, rollout do hard-stop universal nas demais skills. `copy-pesquisar` não foi alterada (gera relatório PT-BR, não publica copy).

---

## social-* (família: pipeline, analytics, canva + social-plan v2)
### 2026-06-12 — Sistema de automação de redes sociais Buzzmonitor (PR #14)

Três skills novas + upgrade do social-plan fecham o ciclo mensal de redes sociais da Buzzmonitor (Instagram, por enquanto): analytics do mês anterior → planejamento → copies em lote → designs no Canva.

- **`social-pipeline` v0.1.0 (nova)** — orquestrador do ciclo mensal. Diagnóstico de estado pelo filesystem (idempotente, retoma de onde parou), pausas com chips entre etapas, zero auto-post. Etapa C (copies em lote) carrega **obrigatoriamente** `conhecimento/editorial/regras-anti-ia.md` + `fundamentos-copy.md` e roda auto-checagem (zero em-dash, sem antítese-por-negação em série) antes de salvar.
- **`social-analytics` v0.1.0 (nova)** — relatório mensal de performance orgânica a partir dos CSVs do Meta Business Suite (enviados via chat; a skill organiza e normaliza). Helper `parse_csvs.py` lida com UTF-16/BOM e multi-line cells; `_gen_report.py` gera esqueleto mecânico opcional (estrutura canônica é a do SKILL.md). Publica no Notion (chave `redes-sociais-relatorios`).
- **`social-canva` v0.1.0 (nova)** — preenche brand templates do Canva slide a slide a partir das copies aprovadas (create + editing transaction; rollback em falha). Regra inegociável de layout: texto novo dentro de ±20% do original. Config em `brand/buzzmonitor/canva-template-ids.json` (aguardando dataset fields — a skill para e orienta enquanto incompleto).
- **`social-plan` v2.0.0** — MAJOR: calendário muda de formato. Passo 0.5 consome `relatorio.md` do mês anterior (dado próprio > tendência externa); Passo 0.7 obrigatório pergunta 4 alavancas do mês (novidade/case/dashboard/sazonal) com chips; **vídeos saem do calendário** (viram seção "Sugestões de vídeos pra produzir"); campo **Justificativa** obrigatório por post; Passo 1 passa a carregar `regras-anti-ia.md` (hooks são texto publicável).

Nota de versionamento: as 3 skills novas nascem em **0.1.0** (exceção consciente à convenção 1.0.0) — sinalizam beta; `social-canva` em particular não roda até os dataset fields do Canva serem configurados.

Ajustes de review (mesmo PR): UUID do MCP Notion padronizado com o restante do repo (`d23bd62b-…`), `AskUserQuestion` adicionada aos `allowed-tools` das skills que pausam com chips, referências a memórias pessoais (`[[feedback-social-*]]` e path absoluto de máquina) substituídas por regras inline, rodapé do social-plan sem versão hardcoded.

Arquivos:
- `.claude/skills/social-pipeline/SKILL.md` · `.claude/skills/social-analytics/{SKILL.md,parse_csvs.py,_gen_report.py}` · `.claude/skills/social-canva/SKILL.md` · `.claude/skills/social-plan/SKILL.md`
- `brand/buzzmonitor/{canva-brand-kit.md,canva-brand-templates.md,canva-template-ids.json}`
- `conhecimento/config/notion-ids.md` (chave `redes-sociais-relatorios`) · `CLAUDE.md` (seção Redes Sociais) · entregas em `social-media/buzzmonitor/2026-0{5,6}/`

---

## dashboard/queries.py (Dashboard CM Buzzmonitor Brasil)
### 2026-06-15 — Atribuição CM 90d: granularidade ::date + auto-atribuição p/ account_id NULL

Correção de **subcontagem** em eventos pós-conversão (Contato Efetivo, Reunião Agendada, Reunião Realizada, Proposta). Disparada por investigação do Victor: a dashboard reportava **0 reuniões** na semana 06–12/jun, mas havia deals legítimos de CM com reunião agendada/realizada na janela. Duas causas-raiz na regra dos 90 dias (`EXISTS` contra `conversoes_cm`), ambas centralizadas agora no novo helper `_atrib_cm_90d(col, alias)`:

1. **Granularidade `::date`.** As colunas de evento são gravadas à meia-noite (`data_agendamento_auto = 'YYYY-MM-DD 00:00:00'`) enquanto `cdate` carrega hora real (`timestamptz`). A comparação em timestamp cru (`cdate 07:39 <= agendamento 00:00` = falso) derrubava silenciosamente o evento que cai **no mesmo dia** da conversão. Passa a comparar em `::date` nos dois lados — alinhado ao §6 do MAPEAMENTO. Sozinha, recupera ~26 reuniões agendadas YtD 2026 (RA tem hora 00:00; RR já gravava hora real, então não era afetada).
2. **Auto-atribuição para `account_id IS NULL`.** Deals sem empresa no CRM (leads individuais — ex.: campanha Monitoramento Político: pré-candidatos, jornalistas) têm `account_id` nulo. A CTE `conversoes_cm` exige `account_id NOT NULL` e o `EXISTS` casa por conta, então esses deals **nunca** contavam CE/RA/RR/Proposta — só Leads (que não usa conta). Quando o próprio row é CM, o deal passa a se auto-atribuir dentro da janela 90d.

`filtro_cm()` e `_sql_exclusao_deals()` ganharam parâmetro `alias` opcional (default `''` gera SQL byte-idêntico ao anterior) para o branch de auto-atribuição prefixar colunas (`d.`/`ct.`). Os 16 blocos `EXISTS` inline (count/lista de evento, propostas, fechamentos, rankings, série 12m, proporção 12m) foram trocados pelo helper.

**Impacto medido (YtD 2026), só pelas 2 correções de critério:** RA ~41→69, RR ~55→58, CE ~82→92, Proposta ~45→50. **Fechamentos permanecem 7 · R$ 19.270 (gate §7 intacto)** — verificado: o fix não recupera nenhum fechamento novo (`account_id` nulo CM em contratos = 0; nenhum fechamento same-day muda de lado). Perdidos também não mudam (já usavam filtro CM no próprio row, sem join por conta).

**Override nominal `CM_DEALS_FORCADOS` (mesmo PR):** lista de `deal_id` que o Victor confirma como CM mas que nenhuma regra automática pega — ex.: *Assembleia Legislativa do MA* (189715), lead que converteu na **página de oferta webinar** mas teve deal novo criado sem UTM, em conta diferente, 108d depois. Força os **eventos** do deal (CE/RA/RR/Proposta) a contarem, ignorando account-join e janela 90d; **não** toca Leads (lead original já conta) nem Fechamentos (só `deals_comercial_prod`; fechamento via `EMAIL_WHITELIST`). Mesma filosofia da `EMAIL_WHITELIST`/`RECONVERSOES_MANUAIS`. Com 189715 incluído: semana 06–12/jun RA=3 / CE=8; YtD RA=70 / CE=93. Gate de fechamentos segue 7 · R$ 19.270.

**Pendente (não tocado neste PR):** `queries_latam.py` e `queries_cxpress.py` compartilham o mesmo padrão de `EXISTS` 90d e provavelmente o mesmo viés — avaliar replicar o helper (LATAM tem peculiaridades de schema: sem `account_id` na base).

Arquivos: `dashboard/queries.py`, `dashboard/MAPEAMENTO-CAMPOS.md` (§3).

---

## dashboard/queries_latam.py (Dashboard CM LATAM)
### 2026-06-06 — Fechamento (cierre) ampliado + valor pela coluna `value`

- **Fechado deixa de exigir `status='Ganho'`.** Esse campo quase não é mantido no AC LATAM (no stage 176
  do pipeline Contratos, 84 de 96 deals estão `Aberta` apesar de fee + contrato + data de cierre). Nova
  constante `FECHADO_LATAM` = `status='Ganho'` OU `primer_pago_realizado_automatico` OU
  `fecha_de_inicio_de_contrato` OU `fecha_de_cierre_de_negocio`.
- **Valor do contrato passa de `fee_mensual` para `value` (USD).** `fee_mensual` é inconsistente (às vezes
  `value`×100, às vezes não — ex.: value=1615/fee=90000); o renderer mostrava 100× a mais. Cast defensivo
  texto→numeric (`VALOR_USD`).
- **Datação do cierre** ganha 3º fallback `fecha_de_primer_pago_automatico` (`DATA_FECHO`); segue **sem `mdate`**.
- Aplicado em `q_count_fechamentos`, `q_lista_fechamentos`, `q_ranking`, `q_serie_12m`. Renderer
  (`render_helpers_latam.py`/`gerar_relatorio_latam.py`) inalterado — consome os aliases `valor`/`currency`.
- **Impacto (cierres CM):** all-time **2 → 34** (USD 18.334) · 2026 **1 → 7** (USD 3.049). Ex.: La Firma
  (deal 43258), fechado 25/05 com pagamento automático mas `status='Aberta'`, agora aparece.
- ⚠️ Mudança só reflete no dashboard live após regenerar + redeployar (não há skill de deploy LATAM ainda).

## .claude/skills/auditar-deals-cm + dashboard/auditar_deals_cm.py
### 2026-06-02 — v1.0.0 — Skill nova (auditoria de deals CM nao mapeados por falha de UTM)

Acha deals de Content Marketing que a dashboard CM nao conta porque chegaram ao Supabase com
`utm_source`/`url_conversao` vazios (falha da automacao AC->Supabase, ja sintomatizada em
`MAPEAMENTO-CAMPOS.md` §8/§9). Harness **read-only** que recupera a UTM **localmente** (nunca grava no
banco) e re-roda o filtro CM **reaproveitado** de `queries.py`.

- **3 niveis de confianca:** doador por **email** (mesmo contato) = NET-NEW alta confianca; doador por
  **conta** (mesma empresa) e **titulo/inbound** = revisao. So o email entra no headline.
- **Reuso, nao reimplementacao:** importa `filtro_cm`, `EMAIL_WHITELIST/BLACKLIST`, `_sql_email_list`,
  `q_lista_leads`. Anti-drift validado: ANTES == `q_count_leads` da dashboard (287 YtD 2026).
- **Saidas gitignored** (PII: emails + ids) em `dashboard/auditoria/`: relatorio MD + CSVs por nivel.
- **Remediacao so proposta:** bloco de `EMAIL_WHITELIST` se N pequeno; senao recomenda corrigir a
  automacao AC->Supabase / popular `cm_email_whitelist`. Nunca auto-edita `queries.py`; nunca toca no Supabase.
- **Fase 2 (AC) desenhada, nao implementada** (decisao Victor 2026-06-02 "so Supabase por ora"):
  `enrich_from_ac()` no-op + mapa AC validado (deal.id==AC id, contato/notas, campos 845–851) documentado
  em `dashboard/AUDITORIA-DEALS-CM.md`.
- Baseline 1a rodada (YtD 2026): 287 leads CM hoje contados -> **+43 net-new alta confianca (+15%)**;
  ~1.148 em revisao (573 mesma empresa + 575 titulo/inbound).

## .claude/skills/criativo + criativos/GUIDELINES.md
### 2026-05-27 — v1.0.0 — Skill nova (gerador de criativos ponta a ponta) — co-desenhada com o Victor

Formaliza em skill o pipeline de criativo estatico que ate entao era a POC `criativos/render_poc.py`
(usada no teste do webinar 2026-05-22 e no carrossel Cxpress "10→4" de 2026-05-26). Arquitetura,
engines e GUIDELINES **decididos ponto a ponto com o Victor** (sessao 2026-05-27) — nao foi build solo.

- **`/criativo` = skill unica ponta a ponta:** adapta a copy → carrega brandbook + GUIDELINES → gera →
  **revisa as imagens** → entrega numa pasta local. Sem args, pergunta com chips. (Decisao: skill unica,
  nao pipeline modular.)
- **Duas engines independentes** (decisao do Victor): **HTML/CSS + Playwright** (padrao, texto
  pixel-perfect, DPR=1) e **Bloom** (IA, peca inteira, opt-in). Bloom e **desligavel** — sem MCP/assinatura,
  a opcao nao aparece e tudo vai por HTML (degrada sem erro). Escolha: HTML por padrao, Bloom sob pedido.
- **Margem de seguranca por `uso` (organico|anuncio) × `formato` (1x1|4x5|9x16).** `base.css` deriva
  `--safe-top/-bottom/-x` de dois data-attributes; `render.py` injeta uso/formato no `.canvas` (um HTML
  serve todos os formatos). Anuncio 9:16 reserva topo 250 / base 340 / lados 64 (UI do Stories/Reels).
  Em `anuncio`: gera `-guia.png` (overlay das zonas reservadas) + avisa se a peca tiver texto demais.
  **Nao** ha auto-containment de mascote/decorativo (decisao: a recomposicao e humana; o guia sinaliza).
- **`criativos/GUIDELINES.md` (novo, versionado):** 11 secoes co-desenhadas — formatos, safe-zones,
  escolha de engine, estrutura (a copy dita), tipografia, cor (auto-AA), decorativos, mascote (so quando
  agrega), fidelidade da copy (adaptativo: copy boa → literal; copy crua → adapta + anti-IA), revisao
  (auto-corrige e re-renderiza), entrega. E a fonte de regras; o SKILL.md so descreve o processo.
- Scaffold em `.claude/skills/criativo/assets/` (`base.css` + `render.py`), copiado pra pasta da peca.
  Output em `criativos/{marca}/{regiao}/{slug}/` — entrega por caminho no chat, upload manual.
- Lembretes embutidos: contraste WCAG auto-corrigido (branco sobre laranja Cxpress/Buzzmonitor REPROVA),
  cases Cxpress pendentes (prova social), artigo via `nameUsage`, tipografia reforcada no Bloom.
- `.gitignore`: ignora `criativos/*` (era `criativos/`) + excecao `!criativos/GUIDELINES.md` — assim o
  GUIDELINES versiona e os outputs (PNGs) ficam de fora. (Negacao so funciona ignorando o conteudo, nao a pasta.)

---

## dashboard/queries.py + dashboard-pessoal/lib/queries.py
### 2026-05-26 — Exclusao de deals por URL (+ opcionalmente data) (`DEALS_EXCLUIDOS_URL_DATA`)

Nova estrutura pra remover deals **sem** banir o email globalmente (como faria a `EMAIL_BLACKLIST`). Cada entrada e `{url_like, datas?}` — `datas` opcional: com datas, exclui so naqueles dias; sem datas, exclui qualquer data que case a URL. O helper `_sql_exclusao_deals()` gera `NOT ((url ILIKE ... [AND cdate IN (...)]) OR ...)` injetado no topo do `filtro_cm()`.

**Primeiro caso — webinar Analise Preditiva:** inscricoes em `webinar.buzzmonitor.com/analise-preditiva-maio-2026` nunca devem virar lead CM (e topo de funil — pagina de inscricao, nao oportunidade). Decisao do Victor 2026-05-26 apos investigar: a falha comecou como lote em 25/05 (34 deals) e 06/03 (19 deals), mas havia inscricoes pingadas em ~24 outros dias — todas a mesma URL. Optou-se por excluir **todas** (regra de URL sem data) em vez de so os lotes. A OFERTA (`conteudo.buzzmonitor.com.br/oferta-webinar-analise-preditiva-na-pratica`) tem URL distinta e **continua contando** (3 leads). Vantagem sobre blacklist por email: os emails voltam a contar em conversoes futuras por outras campanhas.

**Impacto:** Leads CM YtD 2026 caiu de 323 (so com fix NULL) pra 255 (−68 acumulado: −34 inscricoes + dedupe de emails que so vinham do webinar). Fechamentos inalterados (7 · R$ 19.270 — nenhuma inscricao tinha fechado). Aplicado nos dois queries.py (paridade validada).

### 2026-05-26 — Fix do bug NULL no filtro CM + 4 emails na blacklist

**Bug:** a primeira regra do `filtro_cm()` era `NOT (utm_source = 'google' AND utm_medium = 'cpc')`. Em SQL, `NULL = 'google'` retorna `NULL`, `NOT NULL` retorna `NULL`, e `NULL` no `WHERE` descarta a linha. Resultado: **todo lead com `utm_source NULL` era silenciosamente excluido da dashboard CM**, mesmo com `url_conversao` batendo numa whitelist legitima (blog, oferta-*, gestao-de-crises, buzztalk-, etc.). 14-19 leads YtD 2026 estavam sumindo.

**Fix:** `NOT (COALESCE(utm_source, '') = 'google' AND COALESCE(utm_medium, '') = 'cpc')`. Aplicado nos dois arquivos (oficial + pessoal) pra manter paridade. Descoberto investigando por que a LP `oferta-webinar-analise-preditiva-na-pratica` (que ja estava na whitelist via prefix `oferta-`) so contava 1 dos 3 leads.

**Blacklist:** +4 emails apos o fix expor leads que nao deviam contar:
- `stella.santana@parceiros-npx.com.br` (contrato NUPIXEL — lead original era Google CPC; mantem fech YtD em 7 · R$ 19.270)
- `teste@teste.com` (teste)
- `thamires.oliveira@buzzmonitor.com.br`, `albali@elife.com.br` (emails internos)

**Impacto:** fechamentos YtD inalterados (7 · R$ 19.270). Leads CM YtD agora 323 (antes excluia ~16 leads NULL/CM legitimos). Doc atualizada em `dashboard/MAPEAMENTO-CAMPOS.md` §2 e §7.

---

## .claude/skills/dashboard-atualizar
### 2026-06-02 — v1.0.2 — Fix: `url_conversao` NULL derrubava leads CM (cláusula de exclusão)

`_sql_exclusao_deals()` em `dashboard/queries.py` gerava `NOT (url_conversao ILIKE '<webinar>')`
sem guarda de NULL. Com `url_conversao` NULL (lead de `utm_source` válido — ex: `meta` — mas sem
URL de conversão capturada), `NULL ILIKE '...'` vira NULL, o `NOT (...)` propaga NULL no WHERE e o
lead some de **todo** o filtro CM (leads, eventos 90d, rankings, série 12m). Regressão introduzida
junto com a exclusão do webinar Análise Preditiva.

- **Fix:** `COALESCE(url_conversao, '') ILIKE '...'` nas duas cláusulas (com/sem `datas`). Mesma
  classe do bug `google/cpc` corrigido em 2026-05-25/26.
- **Impacto:** passa a contar leads CM com source válido e URL vazia. YtD 2026: +6 deals (5 `meta`,
  1 `chatgpt.com`); +3 no gráfico 12m (2025). Auditado com o Victor (deals conferidos no AC) antes de aplicar.
- Detectado investigando lote de leads "Monitoramento Político" 26/05 que não apareciam na dash mesmo
  após o time preencher `utm_source` no ActiveCampaign.
- **Twin local sincronizado:** `dashboard-pessoal/lib/queries.py` (dashboard local com seletor de
  período, porta 8000) tinha a mesma cláusula — corrigido no mesmo fix (o README pede manter as duas
  cópias iguais). Precisa reiniciar o `run_local.py` pra pegar a mudança. LATAM e Cxpress não têm o
  construto — não afetadas.

### 2026-05-25 — v1.0.1 — Fixes do smoke test inicial (3 bugs)

Bugs descobertos rodando a skill pela primeira vez em 2026-05-25:

- **§2.1 threshold**: era `> 100KB`, HTML real ~72KB → falsa-fail. Baixado pra `> 50KB`.
- **§3.3 regex**: buscava `dpl_[a-zA-Z0-9]+` no output de `vercel ls`, mas `vercel ls` lista URLs (subdomain) — nao `dpl_id`. Trocado pra match no padrao `https://dashboard-buzzmonitor-brasil-[a-z0-9]+-elife-group\.vercel\.app`. Adicionado atalho: se `vercel deploy` ja imprimiu "Aliased", pular `vercel ls` direto.
- **§4.3 grep data**: buscava `$TODAY` no formato ISO (`2026-05-25`), HTML do gerador escreve PT-BR (`25 Mai 2026`). Trocado pra extrair `LOCAL_DATA` no §2.2 e comparar com `REMOTE_DATA` (mesma extracao) no §4.3.

### 2026-05-25 — v1.0.0 — Skill nova

Encapsula o fluxo semanal de atualizacao da dashboard CM Buzzmonitor Brasil (https://dashboard-buzzmonitor-brasil.vercel.app) que antes era prosa em `dashboard/DEPLOY.md`. Manual-trigger sem args. Orquestra:

- Geracao do HTML via `dashboard/gerar_relatorio.py` (consome Supabase).
- Gate de regressao do smoke test (fechamentos novos): lista os deltas via `AskUserQuestion` com 3 chips ("Sim — atualizar e deployar" / "Atualizar mas pular deploy" / "Investigar antes — abortar"). Se aprovado, auto-patcha `EXPECTED_FECH_YTD_2026` e `EXPECTED_FECH_VALOR_YTD_2026` em `dashboard/gerar_relatorio.py:48-58` (backup em `tmp/gerar_relatorio.py.bak-{data}` antes do edit).
- Divergencia negativa (fech sumiu do banco) aborta sem perguntar — evita esconder regressao.
- Aviso no bloco textual do gate quando `dashboard/queries.py` mudou nos ultimos 7 dias (commit recente em filtro CM pode explicar fech "novos").
- Deploy via pasta sibling em `{DASHBOARD_SIBLING_BASE}/dashboard-buzzmonitor-brasil/` (mesma convencao das LPs — sibling tem middleware Basic Auth + vercel.json + package.json).
- Auto-promove deploy se alias principal nao atualizou (defesa pos-rollback).
- Verificacao: HTTP 200 + Basic Auth + tamanho bate vs sibling + grep da data "gerado em".

Configuracao: `DASHBOARD_SIBLING_BASE` em `.env.local` (mesmo padrao do `LP_SIBLING_BASE`).

Motivacao: incidente 2026-05-25 — `vercel deploy` saiu de `dashboard/` direto (sem middleware Basic Auth nem `index.html`), site retornou 404, restaurado via rollback em ~30s. Skill force-feeds o padrao sibling pra evitar repeticao.

Padrao reusado: `lp-publicar` (estrutura step-by-step + envvar sibling), `news-pipeline` (pausa de aprovacao com chips).

---

## brand/buzzmonitor
### 2026-05-21 — Buzzmonitor: `websites` → `regions` (com Instagram, htmlLang, hreflang, ogLocale) + `socials.linkedin`

Refatoração estrutural do `brand-manifest.json` para suportar geração SEO localizada. O bloco antigo `websites: {brasil, latam, portugal}` virou `regions: {brasil, latam, portugal}.{home, instagram, htmlLang, hreflang, ogLocale}` + `socials.linkedin` único. As home URLs foram corrigidas:

- BR: `https://buzzmonitor.com.br` → `https://buzzmonitor.com/`
- LATAM: `https://buzzmonitor.com/` → `https://getbuzzmonitor.com/es/`
- PT: `https://buzzmonitor.com/` → `https://getbuzzmonitor.com/pt/`

Instagram por região: `buzzmonitorbr`, `getbuzzmonitor.es`, `buzzmonitor.pt`. LinkedIn global: `linkedin.com/company/buzzmonitor`. Esses dados são consumidos por `lp-gerar` (bloco SEO + JSON-LD + logo header/footer) e `lp-revisar` (validação).

Outras marcas (cxpress, buzzcreators, elife) ainda usam o formato antigo `websites` — migrar caso a caso quando precisar de SEO localizado.

---

## landing-pages/GUIDELINES.md
### 2026-05-27 — §19 nova: logo SVG com `<text>` vivo proibido (serifa no browser)

SVG de logo com `<text>` vivo (fonte não embarcada) cai no fallback serifado do browser — a logo sai com tipografia errada (ex.: "BUZZ" sans + "CREATORS" serifada). §19 adiciona validação obrigatória (`grep -c '<text'` deve ser 0) e tabela de estado por marca: Buzzcreators serifa (usar `logo-color.png` ou o raster do deploy), Buzzmonitor já é raster, Cxpress/Elife são outline. Origem: LP `buzzcreators-estado-arte-influencia` foi ao ar 2× com "CREATORS" serifada porque a review trocou o raster pelo "vetor limpo".

---

### 2026-05-21 — §15-§18 novos: SEO obrigatório, hreflang, logo regional, OG image

Quatro seções novas codificam padrões descobertos na sessão MCP (`material.buzzmonitor.com/mcp`, `/mcp-es`, `/mcp-pt`):

- **§15 SEO obrigatório** — pacote completo no `<head>`: meta description + robots + 8 OG tags + 4 Twitter Card + JSON-LD (Organization + WebPage + SoftwareApplication/Article/Event). Inclui templates, regras de URL absoluta vs relativa, regras de encoding e comandos de validação local (grep counts + parse JSON-LD).
- **§16 hreflang + canonical** — quando há LPs irmãs multi-idioma, cada uma lista todas as variantes + `x-default`; cada LP tem `canonical` próprio (não para o default). Códigos válidos: `pt-BR`, `pt-PT`, `es-419`. Inválidos: `es-LA`, `pt-LATAM`.
- **§17 Logo header/footer regional** — `href` aponta para `regions.{regiao}.home` do manifest (NÃO `/`), com `target="_blank" rel="noopener"`. Justificativa: em guarda-chuva `/` resolve para raiz do domínio sem LP (link quebrado).
- **§18 OG image 1200×630** — geração via template HTML + Chrome headless. Convenção de path: solo `assets/og-image.png`, guarda-chuva `assets/{marca}/og-{slug}.png` (sufixo de slug evita colisão entre LPs irmãs no mesmo namespace de marca).

---

## lp-gerar
### 2026-05-27 — v1.7.0: validar logo web-safe (sem `<text>` vivo, GUIDELINES §19)

Passo 1 valida cada SVG de wordmark com `grep -c '<text'` e passa só os logos web-safe no briefing. Briefing do Passo 3 ganha "REGRA DE LOGO WEB-SAFE". Passo 4.1.2 ganha check de `<text>` no logo referenciado. Previne logo serifada no browser (Buzzcreators: usar `logo-color.png` ou o raster do deploy).

---

### 2026-05-21 — v1.6.0: gerar bloco SEO completo + ler `regions` do manifest

Passo 0.1 e 0.2 novos para ler `brand/{marca}/brand-manifest.json#regions.{regiao}` + `#socials.linkedin` e identificar LPs irmãs (multi-idioma). Briefing do Passo 3 expandido para instruir `frontend-design` a gerar o bloco SEO completo conforme GUIDELINES §15-§17, usando placeholders `{{DOMAIN}}` / `{{OG_IMAGE_PATH}}` / `{{BRAND_LOGO_PNG_PATH}}` que `lp-publicar` resolve no deploy.

Novas validações no Passo 4:
- 4.1.1 — checklist SEO (1 description, ≥8 og, ≥4 twitter, JSON-LD parseia, canonical presente)
- 4.1.2 — checklist header/footer regional (href = manifest.home, target=_blank, aria-label localizado)
- 4.1.3 — sinalizar OG image pendente no README

Fallback documentado para marcas com manifest antigo (formato `websites`): cair pra `Organization` sem `sameAs` e anotar migração pendente.

---

## lp-revisar
### 2026-05-27 — v1.6.0: Passo 3.7.d audita logo web-safe (sem `<text>` vivo, §19)

3.7.d (logo regional) agora também checa que os SVG de logo do header/footer não têm `<text>` vivo (serifa no browser) — CRÍTICO. Rede de segurança independente do `lp-gerar`.

---

### 2026-05-21 — v1.5.0: Passo 3.7 — auditoria SEO + multi-idioma + logo regional + OG image

Novo Passo 3.7 trata vazamentos SEO como CRÍTICOS (mesma prioridade de GTM e fidelidade de copy). Subpassos:

- **3.7.a** — counts de meta description, robots, og:, twitter:, JSON-LD, canonical (thresholds por GUIDELINES §15).
- **3.7.b** — JSON-LD parseia e `Organization.url` + `sameAs[]` batem com `brand/{marca}/brand-manifest.json#regions.{regiao}`. Detecta URL hardcoded.
- **3.7.c** — multi-idioma: detecta LPs irmãs por sufixo de slug (`-es`/`-pt`), exige hreflang completo + `x-default`, rejeita códigos inválidos (`es-LA`, `pt-LATAM`).
- **3.7.d** — logo regional: zero `href="/"` em `navbar__logo`/`footer__logo`; URL deve bater com manifest.
- **3.7.e** — OG image: URL absoluta, arquivo existe no source, dimensões 1200×630 (validado com PIL).

Cada achado vai pro bucket de críticos com formato `SEO-MISSING:`, `I18N-HREFLANG-MISSING:`, `LOGO-BAD-HREF:`, `OG-IMAGE-DIMENSIONS:`, etc.

---

## lp-publicar
### 2026-06-16 — v3.9.0: smoke test 3.4.b reconhece vizinha que é SOURCE de redirect (corta falso "REGRESSAO")

Durante o recovery de `webinar.buzzmonitor.com` (incidente CONTEXT §7.2 2026-06-16: colaborador deployou fora da skill e derrubou 6 LPs), o smoke test 3.4.b acusou **falso "REGRESSAO"** na vizinha `agentes-automacao-junho-2026` — slug que é `source` de um redirect `308 → /mcp-para-social-listening` no `vercel.json`. O live serve 3xx, mas o smoke test comparava hash de conteúdo via `curl` sem `-L`, pegando o corpo do 308 — que nunca bate com o hash do `index.html` da pasta. Esse guarda-chuva tem 3 redirects, então o falso-alarme dispararia em todo deploy — risco de habituar o operador a ignorar o alerta e mascarar uma regressão real.

- **Passo 2.4** lê o array `redirects` do `vercel.json` e separa as vizinhas que são `source` de redirect numa lista própria (`REDIRECT_OTHERS`, formato `slug:destino`), em vez de capturar hash de conteúdo delas.
- **Passo 3.4.b** valida essas vizinhas por `curl -sI` (status 3xx + `Location` == destino esperado), não por hash. Vizinhas normais seguem no smoke test de hash, inalterado.
- **CONTEXT.md §6** ganha linha de troubleshooting; **§7.2** registra o incidente. Mudança aditiva — `BASELINES_OTHERS` continua igual, `REDIRECT_OTHERS` é novo. Sem mudança de interface.

### 2026-06-09 — v3.8.0: cobertura do padrão bare `assets/X` (sem `./`) em descoberta, rewrite e drift-check

Durante a publicação batch `conheca-a-cxpress,conheca-a-cxpress-confirmado` (bridge page de confirmação do webinar ClickMeeting), o drift-check 1.0 acusou divergência falsa: o HTML da LP referencia o speaker como `src="assets/enrico-chiari.jpg"` (bare, sem `./`), padrão que a simulação de rewrite e as tabelas dos Passos 1.3/1.5 não cobriam — o live estava idêntico ao HEAD, e a única diferença era exatamente esse rewrite não simulado. Mudanças: (a) nota nova no 1.3 documenta o padrão bare como equivalente a `./assets/X`, com a regra de ordem do sed (brand antes de bare, ancorado em `src="assets/`) e o namespace por slug do precedente (`/assets/cxpress/conheca-a-cxpress/...` — evita colisão entre LPs irmãs da mesma marca; ao re-publicar, manter o namespace vigente no live); (b) lista de rewrite do 1.5 (modo guarda-chuva) ganha a substituição correspondente. Sem mudança de interface.

### 2026-06-08 — v3.7.0: liberação CSP para TikTok Pixel (Events JS + Events API)

Template CSP (`vercel.template.json`) ganha `https://analytics.tiktok.com` em `script-src`/`connect-src` e `https://ads.tiktok.com` em `connect-src`. Motivação: campanhas TikTok via GTM precisam do pixel `https://analytics.tiktok.com/i18n/pixel/events.js` carregar + enviar eventos para `analytics.tiktok.com` (web pixel) e `ads.tiktok.com` (Events API server-side). Sem isso, browser bloqueia em runtime — `Refused to load https://analytics.tiktok.com/...` no DevTools.

**Mesma estrutura do Meta Pixel (v3.2.0):** `analytics.tiktok.com` em script-src (carregar events.js) + connect-src (enviar eventos via fetch/xhr). `ads.tiktok.com` em connect-src apenas (server-side Events API, sem JS para carregar).

**Sibling drift:** as 5 siblings guarda-chuva vivas no momento da bump (buzzcreators-lp-vendendo-com-creators, buzzmonitor-evento, buzzmonitor-lp-monitoramento-concorrentes, buzzmonitor-material, cxpress-lp-playbook-whatsapp2026) receberam patch no `vercel.json` local — `csp_drift_check.py` valida que todas zeraram (extra_in_sibling=={} antes do patch, sem decisão a tomar). Mudança só vale em produção após re-deploy de cada sibling (Vercel serve `vercel.json` como header de origem).

**Bonus colateral (buzzcreators-lp-vendendo-com-creators):** CSP dessa sibling estava em pre-v3.2.0 (sem `connect.facebook.net` nem `www.facebook.com`). Patch sincronizou tudo de uma vez — Meta Pixel **e** TikTok Pixel agora cobertos. O drift acumulado era invisível porque a LP única daquele projeto não dispara nem fbq nem ttq hoje, mas seria buraco silencioso se uma campanha futura adicionasse pixel via GTM.

**Check proativo no Passo 1.6 (SKILL):** grep no HTML procura `ttq(`, `ttq.`, `analytics.tiktok.com`, `tiktok-pixel` — espelha o check existente do Meta Pixel.

### 2026-05-21 — v3.6.0: modo batch (CSV de slugs) + namespace OG image + substituição de placeholders SEO

Suporte nativo a publicar N LPs irmãs num único deploy (`/lp-publicar buzzmonitor mcp,mcp-es,mcp-pt material.buzzmonitor.com`). Motivação: sessão MCP de 2026-05-18 fez essa orquestração manualmente (3 LPs em 1 deploy), o padrão virou primitiva.

**Modo batch (só em guarda-chuva):** sync 1×, drift-check N×, copy+rewrite N×, deploy 1×, smoke test 1× cobrindo os N alvos + vizinhas. Tabela detalhada no Passo 0 documenta quais passos rodam 1× vs N×.

**Convenção OG image (Passo 1.4.1 novo):**
- solo: `landing-pages/{marca}/{slug}/assets/og-image.png` → `{sibling}/assets/og-image.png`
- guarda-chuva: `landing-pages/{marca}/{slug}/assets/og-image.png` → `{sibling}/assets/{marca}/og-{slug}.png` (com rename — sufixo de slug evita colisão entre LPs irmãs).

`logo-primary.png` também é copiado explicitamente (JSON-LD `Organization.logo` referencia ele via URL absoluta — heurística de grep não pega referência dentro de `<script type="application/ld+json">`).

**Substituição de placeholders SEO (Passo 1.5):** `{{DOMAIN}}`, `{{OG_IMAGE_PATH}}`, `{{BRAND_LOGO_PNG_PATH}}` são resolvidos com base no modo (solo/guarda-chuva) + domínio efetivo. Verificação obrigatória pós-substituição: grep procura qualquer `{{...}}` sobrando — se aparecer, abortar.

Restrições do batch: todos slugs mesma marca, todos com fonte em `landing-pages/{marca}/{slug}/`, modo guarda-chuva obrigatório.

---

## bunzzai
### 2026-05-19 — v1.0.0 nova: análise de tendências via MCP Bunzzai (snapshots cumulativos)

Skill nova `/bunzzai` que espelha o `/meta-ads-trends` mas usando o MCP do Bunzzai como fonte. Aceita apenas contas Buzzmonitor e Cxpress (mesma lista do `/meta-ads`), faz drill-down `Conta → Campanha → Adset → Ad`, calcula janelas 7d/15d/30d via **diff de snapshots cumulativos** (não dados diários como a Meta API), aplica diagnóstico cruzado (CpL × CTR × Conv. LP) e detecta `cron travado` (snapshots consecutivos idênticos indicando que o coletor do Bunzzai parou de atualizar).

Características chave:

- **Fonte alternativa, mesma cobertura** — Buzzmonitor + Cxpress nas 3 moedas (BRL/USD/EUR). Útil para cross-check quando o token Meta expirou, validação cruzada, ou auditoria do cron Bunzzai.
- **Diff de snapshots** — `janela(X dias) = snapshot(ontem) − snapshot(ontem − X dias)`. Reconstitui agregados sem precisar de cache local. Validado pelo `stress_test_bunzzai.py` (2026-05-19).
- **Detecção de cron travado** — se 2+ snapshots consecutivos têm acumulado idêntico, badge `[CRON TRAVADO: N dias congelados desde YYYY-MM-DD]` aparece ao lado do ad afetado. Janela 7d contaminada vira `N/A` e o diagnóstico usa 15d como recente.
- **Benchmarks reaproveitados** — `meta-ads/data/benchmarks.json` (mesmos thresholds CpL/CTR/Conv.LP por moeda × tipo de campanha). CONTEXT.md alerta para a inflação esperada (Bunzzai conta cliques totais e conversões amplas, então CTR vem maior e CpL menor que os benchmarks calibrados em link_clicks + leads custom — sugerir cross-check com `/meta-ads-trends` quando a decisão de budget passar de R$ 1.000).
- **Sem setup local** — zero arquivos Python novos, zero SQLite. Tudo via tools `mcp__bunzzai__tool_find_company`, `list_campaigns`, `list_campaign_ads`, `tool_get_ad_performance`. Python embed inline só para o diff e classificação de tendência.
- **Publicação no Notion** — chave `entregas` em `conhecimento/config/notion-ids.md`.

Arquivos:
- `.claude/skills/bunzzai/SKILL.md` (skill principal — fluxo de 9 passos)
- `.claude/skills/bunzzai/CONTEXT.md` (contas válidas, diferenças métricas Bunzzai vs Meta API, matriz de diagnóstico)
- `CLAUDE.md` (nova seção "Bunzzai (fonte alternativa via MCP — SOMENTE LEITURA)")
- `conhecimento/config/notion-ids.md` (adicionado `bunzzai` aos consumers de `entregas`)

---

## meta-ads-fetch
### 2026-05-19 — v1.1.0 fix: auto-popular tabela `ads` antes da coleta nível ad

Corrigido bug silencioso onde `fetch_insights.py --include-ads` salvava `leads = 0` para todos os ads de campanhas com pixel custom (`offsite_conversion.custom.*`) quando a tabela `ads` do banco estava vazia ou parcial. Sem ela, `get_ad_campaign_map()` retornava `{}`, `ad_indicators` ficava vazio, e `extract_primary_conversions` caía em fallback (`extract_leads`) que procura apenas `lead` ou `offsite_conversion.fb_pixel_lead` — não acertando o pixel custom da campanha.

A coleta seguia sem erro, gerando dados aparentemente válidos mas com leads zerados — o pior tipo de bug, pois quem usasse `meta-ads-trends` ou `meta-ads-report` tomaria decisão de budget em cima de dados falsos.

Fix:

- **Auto-populate em `fetch_all_insights`** quando `include_ads=True`: chama `fetch_campaigns.fetch_all(include_ads=True)` automaticamente se detectar que a tabela `ads` precisa atualização. Três gatilhos: (a) tabela vazia para a conta; (b) campanhas com `results_indicator` custom sem nenhum ad mapeado; (c) último fetch da estrutura há mais de 24h.
- **Validação final** após carregar `ad_indicators`: imprime AVISO claro se ainda houver campanhas com indicator custom sem ads mapeados (caso de campanhas pausadas há +30d, fora da janela de fetch_campaigns). Não aborta — coleta segue nos demais níveis.
- **3 helpers novos em `cache_manager.py`**: `count_ads_for_account`, `count_adsets_for_account`, `adsets_in_campaigns_with_indicator`.

Reproduzido durante stress test de comparação com Bunzzai MCP (2026-05-19) para a campanha Webinar-Analise-Preditiva (buzzmonitor_brl). Após o fix, todos os 6 ads da campanha tem leads > 0; antes do fix, todos tinham leads = 0.

Arquivos:
- `meta-ads/scripts/fetch_insights.py` (`_ads_table_is_stale`, `_ensure_ads_populated`, chamada em `fetch_all_insights`, validação final)
- `meta-ads/scripts/cache_manager.py` (3 helpers novos)
- `.claude/skills/meta-ads-fetch/SKILL.md` (seção nova "Coleta nível ad — pré-requisito automático")

---

## social-plan
### 2026-07-03 — v3.2.0: relatório do mês anterior vira pré-requisito bloqueante, não mais best-effort

Passo 0.5 mudou de "tente ler o relatório, se não existir segue especulativo" para **bloqueante**: sem `relatorio.md` do mês anterior, a skill para antes de pesquisar ou montar calendário, avisa a Catharina que precisa do relatório primeiro, roda `social-analytics` pra gerá-lo (pedindo os CSVs do Meta Business Suite) e só then retoma o planejamento. Decisão da Catharina: planejamento sem aprendizado real do mês anterior é a raiz de calendários especulativos (o mesmo padrão que gerou os 5 planejamentos de junho divergentes entre si, cada um "inventando" contexto diferente sem dado real).

Também explicitado: usar o relatório **ativamente** na síntese e no calendário — descartar formato/tema que não funcionou (citando por quê) e insistir no que funcionou — em vez de só mencionar o relatório de passagem no resumo estratégico.

Arquivos: `.claude/skills/social-plan/SKILL.md` (v3.2.0, Passo 0.5)

---

## social-plan
### 2026-07-03 — v3.1.0 + social-pipeline v0.2.0 + social-analytics v0.2.0: Facebook fora, LinkedIn réplica-first, 1 página por mês no Notion

Revisão pedida pela Catharina depois do primeiro planejamento de julho. Dois incidentes motivaram mudança de regra permanente (não só ajuste pontual deste mês):

- **Facebook sai do calendário.** Só Instagram + LinkedIn de agora em diante. Instagram é a rede primária (todo post nasce ali, 3x/semana); LinkedIn replica a maioria dos temas com tom mais executivo e só ganha post **exclusivo** quando o ângulo é puramente textual e não converte pra carrossel (ex: reação a evento do dia, retrospectiva de mês). Tabela de formato por rede e template do calendário atualizados (Passo 3.3, Passo 4).
- **Regra "posts prontos, não categorias vazias".** Todo item do calendário precisa vir com tema e ângulo fechados — nunca um placeholder tipo "post de case" sem dizer qual case. Slots de oportunidade (antes 2-3 por padrão) caem pra 0-2, reservados só pra temas genuinamente reativos (ex: "novidade de plataforma — avaliar toda segunda"), sempre com instrução de ativação escrita, nunca `(a definir)` vazio.
- **Incidente de duplicação no Notion:** rodadas anteriores de `/social-plan` (algumas de testes exploratórios, nunca comunicadas como tal) tinham criado **5 páginas de planejamento diferentes pra junho** e **2 pra julho**, soltas como irmãs dentro de `redes-sociais`, nenhuma marcada como "a válida" — a Catharina não conseguia saber qual conteúdo estava em vigor. Correção: `conhecimento/config/notion-ids.md` ganha a seção "Padrão de página por mês", regra fixa pras 3 skills da família — **1 página-hub por mês** (`{Mês} {Ano}`, ex: `Julho 2026`) dentro de `redes-sociais`, com `Planejamento`, `Copies`, `📅 Calendário` (database) e `Relatório de Performance` como children dela. Antes de criar qualquer coisa, `notion-fetch` no hub pra checar se já existe; se existe, **atualiza em vez de criar**. `social-plan` (Passo 5), `social-pipeline` (Etapa C.2) e `social-analytics` (Passo 6) apontam pro mesmo padrão. Chave antiga `redes-sociais-relatorios` fica só como arquivo histórico pré-junho/2026 (Maio pra trás).
- **`allowed-tools` completado pras 3 skills:** como o padrão acima exige *atualizar* páginas existentes (não só criar), `social-plan`, `social-pipeline` e `social-analytics` passaram a declarar `notion-update-page` no `allowed-tools` (e `social-plan` também `notion-update-view`, pro rename da view do calendário no Passo 5.4). Sem isso, ao reencontrar o hub do mês a skill não conseguiria atualizar e cairia de volta no `create` — recriando a duplicata que a regra existe justamente pra evitar.
- Limpeza feita manualmente nesta sessão: as 5+2 páginas soltas de junho/julho foram arquivadas; as páginas reais (a que efetivamente virou copy e foi publicada) foram movidas pra dentro dos novos hubs `Junho 2026` e `Julho 2026`.

Arquivos: `.claude/skills/social-plan/SKILL.md` (v3.1.0) · `.claude/skills/social-pipeline/SKILL.md` (v0.2.0) · `.claude/skills/social-analytics/SKILL.md` (v0.2.0) · `conhecimento/config/notion-ids.md` (seção "Padrão de página por mês") · `social-media/buzzmonitor/2026-07/{planejamento.md,copies/copies-julho.md}`

---

## social-plan
### 2026-05-19 — v1.0.0 nova: planejamento editorial mensal de redes sociais Buzzmonitor

Skill nova `/social-plan` que gera planejamento editorial mensal para LinkedIn, Instagram e Facebook da Buzzmonitor. Fluxo: parsing do mês → leitura do brand-manifest + produto + concorrentes → 4 agentes de pesquisa em paralelo (concorrentes nas redes, perfis de referência B2B SaaS, tendências do nicho, blog Buzzmonitor reutilizável) → síntese (pilares, temas de oportunidade, formato por rede) → calendário com 3 posts/semana por rede + 2-3 slots de oportunidade em aberto → publicação no Notion (página principal + database com calendar view).

Características chave:

- **Pesquisa real, dados próprios primeiro** — agentes pesquisam concorrentes (Sprinklr, Brandwatch, mLabs, Etus, Stilingue), referências (HubSpot, Sprout Social, Buffer, RD Station) e tendências do nicho. A pesquisa do blog Buzzmonitor é obrigatória para ancorar conteúdo em posts existentes.
- **Adaptação por rede obrigatória** — mesmo tema pode aparecer nas 3 redes na mesma semana, mas com formato e linguagem diferentes (LinkedIn técnico/dados, Instagram visual/leve, Facebook comunitário).
- **Publicação no Notion estruturada** — cria página principal com resumo estratégico, pilares, insights e calendário detalhado; abaixo, uma database de posts com propriedades (Tema, Data, Rede, Formato, Pilar, Hook, Tipo) e visualização em calendário.
- **Conector com /copy-criar** — cada post no planejamento já vem com hook, briefing e referência de blog; copy real é gerada chamando `/copy-criar buzzmonitor brasil [tipo] [estagio] "[tema]"` quando o momento de produzir chegar.
- **Notion ID** — chave `redes-sociais` em `conhecimento/config/notion-ids.md` (3603934026fd8158876dd38d432aceef).

Arquivos:
- `.claude/skills/social-plan/SKILL.md` (v1.0.0)
- `social-media/{marca}/{YYYY-MM}/planejamento.md` (output local)
- `social-media/{marca}/{YYYY-MM}/pesquisa/*.md` (4 docs de pesquisa)
- `CLAUDE.md` raiz (linha `/social-plan` na tabela Redes Sociais)
- `conhecimento/config/notion-ids.md` (chave `redes-sociais` + mapping da skill)

Não-objetivos v1: outras marcas além de Buzzmonitor, agendamento automático de publicação, geração de copy/criativo (delegado a `/copy-criar`).

---

## lp-health-check
### 2026-05-27 — v1.1.0 — drift determinístico (corta falso-positivo no relatório)

O drift detection da v1.0.0 era prosa no `SKILL.md` (o agente rodava `find` e compunha a lista à mão), e **qualquer** item de drift disparava email. Resultado: relatório diário cheio de ruído benigno — o placeholder estrutural do guarda-chuva (`_placeholder`) aparecia sempre, LPs no ar só em `*.vercel.app` apareciam como "fonte sem deploy", e uma mesma LP com nome de pasta ≠ nome do path no deploy aparecia 2× (uma de cada lado). Victor abriu a questão ao receber um relatório com 9 entradas estando todas as páginas no ar.

- **Novo `drift.py` determinístico** — lê o output do `discover.py` (stdin) + escaneia `landing-pages/` no disco. Substitui a composição manual em prosa. Classifica cada item num `kind`:
  - `fonte_sem_deploy` (ACIONÁVEL) — source no repo sem deploy em lugar nenhum.
  - `deploy_orfao` (ACIONÁVEL) — slug deployado no guarda-chuva sem source no repo.
  - `vercel_app_only` (INFORMATIVO) — source deployado só em `*.vercel.app` (cross-ref com `skipped` do discover). Estado legítimo; **não dispara email**.
- **Slugs com prefixo `_` ignorados dos dois lados** — `_placeholder` (raiz de guarda-chuva) e similares são estruturais, não LPs. Param de aparecer.
- **`ACTIONABLE_KINDS` é fonte única de verdade** — definido em `drift.py`, importado por `notify.py` e pelo gate do `SKILL.md`. Só drift acionável conta pra decidir enviar email; `vercel_app_only` vai numa seção "Informativo" separada no corpo.
- Resultado no estado atual: de 9 entradas ruidosas → 0 acionáveis + 2 informativas (`pocket-events`, `hallmark-stat-led-...`), email não dispara.

Arquivos: novo `drift.py`; `SKILL.md` (Passo 2 chama o script, Passo 4 conta acionável, relatório/troubleshooting atualizados, v1.0.0→v1.1.0); `notify.py` (importa `ACTIONABLE_KINDS`, assunto+gate+corpo por categoria).

### 2026-05-13 — v1.0.0 nova: rotina diária de health check com descoberta dinâmica

Skill nova `/lp-health-check` que cobre o gap entre o smoke test do `lp-publicar` (no momento do deploy) e a detecção de incidente em produção (LP cai dias depois — rollback parcial, cert lapsa, deploy de outra LP no mesmo guarda-chuva quebra vizinha, drift entre repo e Vercel). Antes desta skill, Victor só descobria LP fora do ar quando o tráfego começava a reclamar; com `/schedule` cron diário rodando `/lp-health-check`, agora chega email assim que algo cai.

Características chave:

- **Descoberta dinâmica zero-manutenção** via Vercel API — lista todos projetos da org `elife-group`, filtra os que têm FQDN custom (ignora `*.vercel.app`), pega último deploy READY, walk no file tree pra identificar todas LPs (solo `index.html` na raiz; guarda-chuva subpastas com `index.html`). Reusa endpoints e padrão de token resolution do `lp-publicar` §0.5.d.i (env → `.env.local` → `auth.json` CLI → validação `/v2/user`).
- **HTTP check paralelo** (até 5 simultâneos) com HEAD method e fallback GET pra CDNs que retornam 405. Timeout 10s, retry 1× em 5xx, classificação ok/warning/fail.
- **Drift detection bonus** cross-check com source no repo (`landing-pages/{marca}/{slug}/index.html`): alerta como warning (não falha) quando há LP no repo sem deploy ou deploy órfão sem source. `--no-drift` desliga.
- **Silenciosa por design** — 0 falhas e 0 drift = exit 0 sem arquivo nem email. Reduz ruído.
- **Email via Resend** quando há falha — free tier 100/dia (suficiente). Configurar `RESEND_API_KEY` em `.env.local`. Sem a key, skill ainda roda mas só salva relatório local em `landing-pages/health-checks/INCIDENT-YYYY-MM-DD-HHMM.md`.
- **Modo `--dry-run`** descobre + checa + imprime no console, sem salvar arquivo nem enviar email — pra debug.
- **Pra agendar:** `/schedule create "Health check diário LPs" --cron "0 9 * * *" --tz "America/Sao_Paulo" --command "/lp-health-check"`. Roda no cloud Anthropic — independente da máquina do Victor estar ligada.

Arquivos:
- `.claude/skills/lp-health-check/SKILL.md` (orquestra, v1.0.0)
- `.claude/skills/lp-health-check/discover.py` (Vercel API → lista de URLs)
- `.claude/skills/lp-health-check/check.py` (HTTP checks paralelos)
- `.claude/skills/lp-health-check/notify.py` (email via Resend)
- `landing-pages/health-checks/` (pasta de relatórios — gitkeep)
- `landing-pages/CONTEXT.md` §11 nova (documenta a rotina + matriz de ação por sintoma)
- `CLAUDE.md` raiz (linha `/lp-health-check` na tabela Landing Pages)

Não-objetivos v1: validação de conteúdo (só status), PageSpeed (já no `lp-publicar`), auto-remediação, dashboard histórico.

---

## lp-publicar
### 2026-05-18 (tarde) — v3.5.1: sync_sibling.py usa `slug=` em vez de `teamId=` na API V6/V7 files

Ao publicar as LPs `mcp-es` e `mcp-pt` em `material.buzzmonitor.com`, o Passo 0.5.d.iii (sync via Vercel API) falhou com `HTTP 403 missingToken` no endpoint `/v6/deployments/{id}/files?teamId=team_nC991VqUuSU2jXZN152xqqEg`. Estranho porque o mesmo token (resolvido de `auth.json` do CLI) validava 200 em `/v2/user` e o endpoint `/v13/deployments/{id}` retornava metadata sem problema.

Causa-raiz: tokens OAuth do CLI Vercel (gerados via `vercel login`) **não autorizam** os endpoints V6/V7 de files quando o team scope é passado como `teamId=team_xxx` — exigem `slug=elife-group`. Access Tokens manuais (Settings → Tokens) aceitam ambos. Diferença não documentada na referência da API. Validado empiricamente:

```
# Falha:
curl -H "Authorization: Bearer $TOKEN_OAUTH" \
  "https://api.vercel.com/v6/deployments/.../files?teamId=team_xxx"
# {"error":{"code":"forbidden","message":"missingToken","missingToken":true}} HTTP 403

# Funciona:
curl -H "Authorization: Bearer $TOKEN_OAUTH" \
  "https://api.vercel.com/v6/deployments/.../files?slug=elife-group"
# Retorna tree JSON normalmente
```

Mudança: `sync_sibling.py` ganhou env var opcional `ORG_SLUG` (default `elife-group`) e usa `?slug=...` nos dois endpoints (`/v6/deployments/{id}/files` e `/v7/deployments/{id}/files/{uid}`). `ORG_ID` continua aceito mas só seria usado se `ORG_SLUG` for explicitamente vazio (fallback para Access Tokens em workspaces hipotéticos sem slug conhecido). Para qualquer execução normal no repo, o default `elife-group` resolve.

Por que default hardcoded e não obrigatoriamente via env: o repo serve uma única org Vercel (`elife-group`). Forçar declaração explícita em todas as máquinas adicionaria atrito sem ganho — mantemos `ORG_SLUG` como override para o caso (improvável) de migração futura.

Sem o fix, primeiro deploy guarda-chuva em qualquer máquina que use `vercel login` (em vez de Access Token manual em `.env.local`) aborta no Passo 0.5.d.ii com mensagem genérica "forbidden — token sem permissão de read", levando o operador a regerar token desnecessariamente. Encontrado e corrigido durante o deploy desta sessão; validado em seguida (sync das 11 arquivos do guarda-chuva `buzzmonitor-material`, integridade OK, deploys de `mcp-es` e `mcp-pt` concluídos sem regressão em vizinhas).

### 2026-05-18 — v3.5.0: patch CSP automatico quando nao ha decisao real a tomar

Ao publicar a LP `mcp` em `material.buzzmonitor.com` hoje, o Passo 1.6 (drift-check ativo de CSP, v3.4.0) detectou que o sibling estava com CSP antigo — faltava `connect.facebook.net`/`www.facebook.com` para liberar Meta Pixel via GTM (pendente documentado em §7.2 2026-05-08). A skill pausou via `AskUserQuestion` oferecendo 3 opcoes (patch / deixar / abortar), e o usuario respondeu pra patchar automaticamente E ajustar a skill para nao perguntar mais nesse caso.

Mudanca: Passo 1.6 separa em dois casos baseado em `extra_in_sibling` (saida do `csp_drift_check.py`):

- **`extra_in_sibling == {}` (caso comum)** — patch automatico, sem `AskUserQuestion`. Sibling esta apenas atrasado em relacao ao template; nao ha decisao real (sem dominio custom para preservar). Skill reporta em uma frase o que vai adicionar, substitui o CSP via `Edit replace_all: false` cirurgico, re-roda drift-check pos-patch e segue. A acao fica logada no relatorio Notion em "Mudancas desta entrega".

- **`extra_in_sibling != {}` (raro, decisao real)** — mantem o fluxo v3.4.0 com `AskUserQuestion` e 3 opcoes. Aqui ha dominios custom no sibling fora do template que poderiam ser apagados em silencio se o patch fosse cego.

Por que esta separacao: depois da v3.4.0, todo deploy guarda-chuva em sibling defasado pagava o custo de uma pergunta extra que sempre tinha a mesma resposta ("patch recomendado") porque era o unico caminho que destravava o pixel sem perder customizacoes (que naquele caso nao existiam). Automatizamos o caminho-sem-decisao mantendo a pausa onde ela ainda agrega seguranca.

Validacao: o proprio deploy desta sessao (`dpl_ED9nkC1NHwVB3L9EtWbWu6p642JD` em `material.buzzmonitor.com`) executou o patch manual; proxima execucao em `webinar.buzzmonitor.com` ou `evento.buzzmonitor.com` (que tambem estao com CSP pre-v3.2.0 conforme §7.2 2026-05-08) deve rodar pelo novo Caso 1 e patchar sozinha. Sem mudanca em `csp_drift_check.py` nem em `vercel.template.json` — toda logica fica no SKILL.md.

### 2026-05-13 (noite) — Hardening contra bypass da skill: lp-sync v1.0.0 nova + anti-padrão "deploy manual" + doc §7.2

Reação ao incidente 2026-05-13 (LP `latam-webinar-atencionalcliente` 404 por ~1h40min — diagnóstico completo em [Notion 35f3934026fd815ab641cd00714cfcbc](https://www.notion.so/35f3934026fd815ab641cd00714cfcbc)). Causa-raiz: outra colaboradora bypassou `lp-publicar` e fez 4 deploys consecutivos com `vercel deploy --force` direto, usando lista hardcoded de vizinhas via `curl + grep` que nunca incluiu a LATAM. Skill `lp-publicar` v3.4.0 já protegia o cenário desde v3.1.0 (sync via Vercel API descobre vizinhas dinamicamente) — não houve bug de skill, houve bypass.

Hardening em 3 níveis para tornar o bypass mais difícil e o caminho-skill mais óbvio:

- **Nova skill `lp-sync` v1.0.0** — standalone read-only que popula sibling local com snapshot do último deploy production READY via Vercel API. Reusa o helper `sync_sibling.py` canônico de `lp-publicar`. Caso de uso: fluxo manual inevitável (debug, inspeção, recovery, primeira sessão numa máquina nova) — em vez de inventar `curl` hardcoded, rodar `/lp-sync [dominio]` antes para garantir sibling fresh. Cobre Passos 0.5.a/b/c/d.i/ii/iii/iv da `lp-publicar`, sem nenhum deploy. Argumento único `[dominio]` FQDN do guarda-chuva. Não cobre modo solo (re-publicação solo via `lp-publicar` já faz sync desde v3.3.0).

- **landing-pages/CONTEXT.md** (sem bump — só doc):
  - **§7.1 anti-padrões**: 2 anti-padrões novos. (a) "Rodar `vercel deploy` direto na sibling sem usar `lp-publicar` (fluxo manual)" — explica que mata as 4 camadas de defesa e referencia §7.2 (2026-05-13). (b) "Preservar vizinhas em deploy manual com lista hardcoded (`curl live > sibling/X` para slugs conhecidos)" — subset crítico do anterior; sublinha que descoberta de vizinhas deve vir da Vercel API, não de inferência humana.
  - **§7.2 histórico**: entrada nova 2026-05-13 documentando a janela 14:12-15:51 UTC, os 4 deploys (`dpl_DAV2`, `dpl_3299`, `dpl_63nL`, `dpl_BCzc`) e o recovery via `dpl_DruoX...`. Cita explicitamente que skill já cobria o cenário e o problema foi bypass — sem bump de skill, hardening organizacional.
  - **§2.2 matriz fluxo de alteração**: nova linha "Inspeção / debug local sem deploy" mapeando para `/lp-sync`. Parágrafo novo de regra geral logo após a tabela.
  - **§8 checklist pré-deploy**: bullet novo "Nunca rodar `vercel deploy` direto na sibling" — referência cruzada para §7.1 e §7.2.

- **CLAUDE.md raiz** (sem bump — só doc):
  - **Fluxo no topo**: linha LP ganha `| /lp-sync (standalone — snapshot sibling)`.
  - **Seção Landing Pages**: parágrafo "Regra inegociável" novo logo abaixo do parágrafo introdutório, antes da tabela — define que toda alteração/deploy roda por `lp-publicar`, fluxo manual é anti-padrão, `/lp-sync` é a saída quando só precisa snapshot. Tabela de comandos LP ganha linha `/lp-sync [dominio]` + bullet `[dominio]` na legenda.

**Não há bump em `lp-publicar`** — comportamento dela continua idêntico, hardening é em torno (skill nova + docs). Próxima sessão de qualquer colaborador entra com sinalização tripla (CLAUDE.md raiz + CONTEXT §7.1/§7.2 + ferramenta `/lp-sync` à mão).

### 2026-05-13 (tarde) — Em-dash bloqueado em todo o pipeline LP (lp-preparar v1.2.1, lp-revisar v1.4.1)

Colaboradora publicou LP com em-dash (`—`) na copy ao ar. Em-dash tem tolerância zero por `conhecimento/editorial/regras-anti-ia.md` — é o tique de IA mais identificável em PT-BR. Auditoria revelou **3 contradições internas** na cadeia de skills LP que permitiram o vazamento:

1. **`landing-pages/GUIDELINES.md` §5 linha 48** instruía literalmente "Usar aspas curvas, ellipsis e em-dash (`&mdash;`) corretos" — ordem direta de USAR em-dash, contradizendo `regras-anti-ia.md`.
2. **`.claude/skills/lp-preparar/SKILL.md` Passo 3 (Regras)** mandava "Preservar aspas curvas, en-dash, pontuação original" — se a copy bruta vinha com em-dash, a skill preservava. Passo 4 (anti-IA conservadora) **não listava em-dash** entre os itens a marcar.
3. **`.claude/skills/lp-revisar/SKILL.md` Passo 3.6 bucket (c) Cosmético permitido** autorizava explicitamente "substituir `--` por `—`" como cosmética OK — a skill de revisão liberava a injeção.

Resultado: 11 LPs ativas com 202 em-dashes em produção (não retrofitadas neste PR — apenas barrar novos casos, decisão do Victor).

**Correções:**

- **landing-pages/GUIDELINES.md §5** (sem bump — só doc): linha de em-dash invertida para "**Em-dash (`—` / `&mdash;`) PROIBIDO** — tolerância zero, ver `conhecimento/editorial/regras-anti-ia.md`. Substituir por vírgula, ponto ou parênteses conforme função. Vale para copy bruta, copy estruturada e HTML renderizado. Validação: `grep -c "—" index.html` deve retornar 0".

- **lp-preparar 1.2.0 → 1.2.1 (PATCH — correção de bug)**:
  - Passo 3 (Regras): "preservar en-dash" virou "preservar en-dash (`–`)" explícito (não em-dash) + linha nova "Em-dash (`—`) NUNCA é preservado".
  - **Passo 4 reestruturado** com subseção 4.1 (em-dash) e 4.2 (resto anti-IA). 4.1 é exceção à regra "apenas marque" — em-dash **substitui direto** (contagem obrigatória `grep -c "—" copy.txt` antes e depois, esperado 0). Tabela de substituição por função (pausa curta → vírgula, pausa forte → ponto, aparte → parênteses, atribuição de citação → vírgula/nova linha).

- **lp-revisar 1.4.0 → 1.4.1 (PATCH — correção de bug)**:
  - **Passo 3.6 bucket (c) Cosmético permitido**: removido "substituir `--` por `—`" da lista. Inserida linha explícita: "**`--` (hífen duplo) NUNCA vira `—` (em-dash) — isso é VAZAMENTO, não cosmética.**"
  - **Passo 3.6.5 Auditoria de em-dash**: mudou de **relativa** (HTML > copy.txt = crítico) para **absoluta** (qualquer ocorrência no HTML = crítico, independe de copy.txt). Se copy.txt também tem em-dash, registrar para corrigir no mesmo passo — o gap está upstream (lp-preparar 4.1 falhou). Tabela de substituição embutida na auditoria.
  - **Tabela de severidade**: linha "Em-dash adicionado" virou "Em-dash (`—` ou `&mdash;`) presente no HTML | CRITICO (tolerancia zero)" — ação inclui corrigir copy.txt no mesmo passo se também contaminada.

**Não retrofitado nesta passada:** as 11 LPs ativas com 202 em-dashes ficam como estão até alguém editar/re-publicar cada uma (decisão do Victor: corrigir cadeia agora, limpeza retroativa em outro momento). A próxima execução de `/lp-revisar {marca}/{slug}` em qualquer LP existente vai detectar e oferecer fix automático.

### 2026-05-13 — GUIDELINES §10 reescrita + numeração corrigida em skills LP

§10 trocou vocabulário de "dobra" (posição visual ao scroll) por contagem de seções (hero = §1, blocos subsequentes = §2, §3, ...) — mais determinístico para quem gera e para quem revisa, sem julgamento subjetivo de "isso é meio da página?". Cobertura expandida de 2 para 3 buckets de tráfego, com **remarketing** entrando explicitamente no mesmo grupo de tráfego quente/qualificado. Default forte com override justificado mantido.

- **landing-pages/GUIDELINES.md** (sem bump — só doc):
  - **§10 reescrita**: ToFu (webinar, material rico, lead frio) → form na **2ª seção** (logo após o hero); MoFu/BoFu/Remarketing (material avançado, comparativos, demo, vendas, retargeting) → form na **4ª ou última seção** (meio/fim da página, após prova social e diferencial); CTA visível no hero (§1) em todos os casos. Override permitido se briefing pedir, lead já quente, ou A/B test provar — justificar no PR / REVISAO.md.
  - **Título trocado** de "Posicionamento do formulário (sugestão, não obrigação)" para "Posicionamento do formulário por tipo de LP" — força ("default forte") agora aparece no corpo, não no título.
  - **§6 (Estrutura mínima)**: referência cruzada à §10 alinhada ao novo vocabulário (substituído "2ª dobra, meio ou fim" por "2ª seção para ToFu; 4ª ou última para MoFu/BoFu/Remarketing").

- **5 skills LP — correção de numeração de referência cruzada (sem bump — só doc):**
  - `lp-pipeline/SKILL.md`, `lp-preparar/SKILL.md`, `lp-integrar-form/SKILL.md`, `lp-gerar/SKILL.md` (2 lugares): 5 referências a "GUIDELINES §10" que apontavam para mock form / integração tardia agora apontam para **§11** (a numeração havia ficado quebrada em algum momento quando §10 — posicionamento do form — foi inserida e empurrou integração tardia para §11). `lp-preparar/SKILL.md` ganhou referência explícita a §10 (posicionamento) na lista de seções a ler.
  - `lp-preparar/CONTEXT.md`: range "§1 a §10" no diagrama de árvore atualizado para "§1 a §14" (GUIDELINES tem 14 seções hoje).

### 2026-05-11 — Padrão `<img>` em grid container documentado em GUIDELINES §14

Victor reportou no iPhone que o mascote da LP `analise-preditiva-maio-2026` renderizava em tamanho gigante, sobrepondo a seção `.speakers`. Diagnóstico: `<img>` com dimensões intrínsecas (`width="810" height="1080"`) dentro de grid item com `min-height: auto` (default) e pai com `aspect-ratio: 1/1` quebra em Safari iOS — Chrome/Firefox aplicam `max-width: 100%` como cap retroativo, Safari iOS faz fallback para a altura intrínseca da imagem. Mesmo padrão presente em outras 2 LPs Buzzmonitor (`monitoramento-concorrentes-maio-2026-pt`, `social-listening-mayo-2026-latam`) — bug latente, ainda não relatado mas confirmado por leitura do CSS idêntico.

- **landing-pages/GUIDELINES.md** (sem bump — só doc): **§14 nova** documenta a regra inegociável `min-height: 0` em `<img>` filho de grid item com `aspect-ratio` no pai, além de defesa em profundidade com `overflow: hidden` em seções que contêm imagens decorativas vazáveis. Histórico do incidente registrado.
- **3 LPs corrigidas em `landing-pages/buzzmonitor/{slug}/index.html`** (`analise-preditiva-maio-2026`, `monitoramento-concorrentes-maio-2026-pt`, `social-listening-mayo-2026-latam`): adicionado `min-height: 0` em `.for-visual .mascot` e `overflow: hidden` em `.for`. Re-deploys via `/lp-publicar` no guarda-chuva `webinar.buzzmonitor.com`.

### 2026-05-08 (noite) — Drift-check ativo de CSP em modo guarda-chuva (lp-publicar v3.4.0)

Hardening preventivo motivado por feedback que Victor recebeu de equipe externa: depois da v3.2.0 atualizar o template para liberar Meta Pixel via Facebook (`connect.facebook.net` + `www.facebook.com` em `script-src`/`connect-src`/`frame-src`), apenas o sibling guarda-chuva redeployado em seguida (`cxpress-lp-playbook-whatsapp2026`) recebeu o patch. Os 3 guarda-chuvas Buzzmonitor (`webinar.buzzmonitor.com`, `evento.buzzmonitor.com`, `material.buzzmonitor.com`) continuaram servindo CSP antigo por ~24h — pixel Meta era bloqueado em runtime via `Refused to load https://connect.facebook.net` mas a skill nao detectava porque o `diff` generico do Passo 1.6 era ignoravel (CR/LF + multiplas linhas). Verificacao manual via `curl -sI` em todos os deploys confirmou o gap em 5 LPs ativas. Correcao pos-fato: 2 deploys com patch cirurgico de CSP (`dpl_BGADTQUh963ZsC62Qqa2eTx5jh9p` em evento, `dpl_qnvc2iyfy...` em webinar; 5/5 vizinhas intactas, 2/2 redirects 308 preservados). Material ficou pendente (sem LP ativa).

- **lp-publicar 3.3.1 → 3.4.0 (MINOR — capacidade nova retro-compat)**:
  - **Novo helper `csp_drift_check.py`**: extrai CSP do sibling e do template, parseia por directive (`script-src`, `connect-src`, `frame-src`, etc.), compara conjuntos de dominios. Exit 0 = OK, exit 1 = DRIFT (template tem dominio que sibling nao tem), exit 2 = erro. Stdout em JSON com `missing_in_sibling` (lista por directive — drift que precisa de patch) e `extra_in_sibling` (customizacoes do sibling a preservar). Stdlib so (~110 linhas, testavel isolado via env vars).
  - **Passo 1.6 reestruturado** em modo guarda-chuva: `diff` generico substituido pelo helper. Quando exit 1, pausa via `AskUserQuestion` com 3 opcoes — (a) **Patch CSP no sibling com versao do template (Recomendado)** preservando `redirects` + `extra_in_sibling`; (b) **Deixar como esta** e anotar em pendencias do relatorio Notion; (c) **Abortar e investigar manualmente**. Modo solo nao muda (continua sobrescrevendo template).
  - **Sem mudanca em interface ou comportamento de happy-path** (sibling ja sincronizado com template). Skill so se comporta diferente quando ha drift de CSP — pausa em vez de seguir silencioso.

- **landing-pages/CONTEXT.md** (sem bump — so doc):
  - **§6 Troubleshooting**: 2 atualizacoes — linha existente "Pixel Meta via GTM nao dispara" agora menciona que v3.4.0 detecta automaticamente; linha nova "lp-publicar Passo 1.6 emite 'DRIFT — CSP do sibling guarda-chuva esta atras do template'" com instrucao das 3 opcoes.
  - **§7.2 Historico**: linha 2026-05-08 (noite) documentando o feedback Meta Pixel, patch manual nos 2 deploys (smoke test 5/5 LPs intactas + 2/2 redirects 308 + 9/9 endpoints com Facebook coverage), e o hardening v3.4.0.

- **`.claude/skills/lp-publicar/csp_drift_check.py` (NOVO)**: helper Python invocado pelo Passo 1.6 (modo guarda-chuva). Le `SIBLING_VERCEL_JSON` e `TEMPLATE_VERCEL_JSON` por env var. Testavel isolado: `SIBLING_VERCEL_JSON=foo.json TEMPLATE_VERCEL_JSON=bar.json python csp_drift_check.py`. Validado contra 3 cenarios pre-merge: sibling patcheado (exit 0 OK), sibling com CSP antigo (exit 1 DRIFT com lista exata de 3 dominios faltantes em 3 directives), env vazio (exit 2 ERROR).

### 2026-05-08 (tarde) — Validacao de integridade pos-sync (lp-publicar v3.3.1)

Re-incidente JSON wrapper em `webinar.buzzmonitor.com` (mesma causa-raiz do incidente 2026-05-07 tarde 2: outra colaboradora rodou versao antiga do `sync_sibling.py` sem `base64.b64decode`). 3 das 4 LPs vizinhas ficaram servindo JSON wrapper. Durante o recovery manual, Victor levantou: "tem algum bug na skill que atrapalhou isso?" — e tinha.

**Bug descoberto na propria v3.3.0:** se o operador rodasse `lp-publicar` para fazer recovery, o sync 0.5.d teria baixado as 3 LPs corrompidas do live e sobrescrito as integras na sibling local — propagando o bug. Validacao 0.5.d.iv so checava **presenca** (`index.html` existe?), nao **integridade** (e HTML valido?). Drift-check 1.0 (v3.3.0) so compara a LP que esta sendo publicada, nao vizinhas. Baseline 2.4 + smoke test 3.4.b confirmariam que live mantem o hash do JSON wrapper = false positive. O que evitou propagacao em 2026-05-08 foi intuicao do operador (Victor interrompeu pedindo recovery manual), nao a skill.

- **lp-publicar 3.3.0 → 3.3.1 (PATCH — bug fix puro)**:
  - **Passo 0.5.d.iv reestruturado** em 2 checks independentes:
    - **Check 1 — presenca** (existente): cada slug vivo no live tem `index.html` na sibling pos-sync. Aborta se algum esta faltando (token sem read, bug no sync recursivo).
    - **Check 2 — integridade (NOVO)**: cada `index.html` na sibling pos-sync comeca com `<!doctype html>` ou `<html>` (case-insensitive, ignora whitespace). Aborta se algum nao bate, com mensagem orientando recovery manual ("NAO rode lp-publicar enquanto live estiver corrompido — propagaria o bug. Use sibling integra de outra maquina e deploy direto via npx vercel deploy").
  - Validacao usa `head -c 100 | tr A-Z a-z | grep -qE '^[[:space:]]*<(!doctype|html)'` — robusto contra line-ending, caps de tag, e BOM ASCII. Falso positivo previsto so com BOM UTF-8 (`\xEF\xBB\xBF`); lp-gerar nao gera BOM.
  - Sem mudanca em interface ou comportamento de happy-path. Skill so se comporta diferente quando o live esta de fato corrompido — nesse caso, aborta cedo em vez de propagar.

- **landing-pages/CONTEXT.md** (sem bump — so doc):
  - **§6 Troubleshooting**: 2 atualizacoes — linha existente do "JSON wrapper" agora menciona que v3.3.1 detecta automaticamente; linha nova "lp-publicar aborta em 0.5.d.iv com 'Sync trouxe LP(s) corrompida(s)'" com instrucao de recovery manual.
  - **§7.2 Historico**: linha 2026-05-08 (tarde) documentando o re-incidente, o bug descoberto na v3.3.0, recovery manual (`dpl_Bn9NmxFpJU8SSLAVokRk28mH9HjA` em 6s) e fix v3.3.1.

- **Mitigacao operacional permanente:** garantir `git pull` antes de qualquer deploy guarda-chuva. Versao antiga do `sync_sibling.py` continua sendo a causa-raiz nas maquinas que nao atualizaram, e o fix v3.3.1 e detector pos-fato — nao impede a corrupcao original. So `git pull` (ou treinamento da equipe) resolve na origem.

### 2026-05-08 — Drift-check pre-overwrite + sync em solo re-publicacao + bug fix de diagnostico de token (lp-publicar v3.3.0)

Hardening preventivo motivado por revisao de Victor — nenhum incidente novo, mas dois buracos simetricos ao caso JSON wrapper de 2026-05-07 ainda existiam:

1. **Buraco 1 — drift na propria LP em guarda-chuva**: o sync 0.5.d (v3.1.0) baixava todas as LPs do live para a sibling, mas o Passo 1.2 imediatamente sobrescrevia `sibling/{slug}/index.html` com o source local sem comparar. Se outra pessoa publicou a mesma LP de outra maquina sem commitar (cenario do incidente JSON wrapper), o trabalho era apagado em silencio.

2. **Buraco 2 — modo solo sem sync**: Passo 0.5.d explicitamente dizia "Pular em modo solo". Re-publicacao solo de maquina diferente da ultima sobrescrevia o live sem rede de protecao. Probabilidade real subiu apos a equipe crescer (varios colaboradores rotativos).

3. **Bug menor de UX em 0.5.d.ii**: se o token Vercel era valido mas sem permissao de read no projeto-alvo, `DEPLOY_ID` ficava vazio e a skill emitia "projeto recem-criado" — confundia debugging.

- **lp-publicar 3.2.0 → 3.3.0 (MINOR — capacidade nova retro-compat + bug fix)**:
  - **Passo 0.5.d ampliado** para guarda-chuva **e solo re-publicacao**. Pre-check no inicio do passo: se `[ ! -f "$SIBLING/.vercel/project.json" ]`, pular sync com mensagem clara ("Solo, primeira publicacao — sem deploy anterior para sincronizar"). Caso contrario, executar 0.5.d.i a 0.5.d.iv normalmente.
  - **Novo Passo 1.0 "Drift-check pre-overwrite"** entre 0.5.d e 1.1. So roda se sibling pos-sync ja contem `{slug}/index.html` (= re-publicacao). Logica: copia source local pra temp, simula a reescrita do Passo 1.5 (modo solo OU guarda-chuva), normaliza line-endings, calcula md5 dos dois lados. Se divergem, **pausa e pergunta ao usuario via `AskUserQuestion`** com 3 opcoes (Continuar / Abortar / Pull primeiro). Nao decide por conta — drift e sinal forte de que outra pessoa pode ter publicado.
  - **Bug fix em 0.5.d.ii**: case statement com 4 branches distinguindo `ERR:forbidden|not_found` (token sem read — aborta com mensagem acionavel pra regerar token), `ERR:*` (erro inesperado da API — aborta), `EMPTY:` (caso legitimo de projeto sem deploy — pula sync), `OK:*` (tem deploy — segue normal). Antes, qualquer branch caia silenciosamente em "projeto recem-criado".
  - **Comentarios atualizados** no 0.5.d.v explicando que re-publicacao agora passa pelo drift-check do 1.0 antes de sobrescrever.
  - Sem mudanca em interface, args ou comandos invocaveis.

- **landing-pages/CONTEXT.md** (sem bump — so doc):
  - **§4.3 reescrita** explicitando 4 camadas de defesa em 2 eixos: vizinhas em guarda-chuva (sync + baseline + smoke test) e propria LP em qualquer modo (drift-check). Documenta historico das camadas (v3.1.0 fechou buraco de vizinhas, v3.3.0 fechou buraco de propria LP + sync em solo).
  - **§6 Troubleshooting**: 3 linhas atualizadas/novas — "Sync incompleto" reformulada (token sem read agora detectado mais cedo); nova "VERCEL_TOKEN nao tem permissao de read no projeto"; nova "AVISO: a versao de '{slug}' no Vercel NAO bate com o que seu source local geraria" (drift-check do 1.0).
  - **§7.2 Historico**: linha 2026-05-08 documentando o hardening preventivo + motivacao (varios colaboradores rotativos = disciplina humana nao escala).

- **`.env.local.example`**: secao "Vercel API" promovida de "(opcional)" para "(recomendado)". `VERCEL_TOKEN=` descomentado para sinalizar que e variavel ativa, nao opcional. Comentario explicativo expandido cobrindo solo re-publicacao.

- **Nao requer mudanca em `sync_sibling.py`**: helper continua igual — recebe `DEPLOY_ID`/`ORG_ID`/`VERCEL_TOKEN`/`SIBLING` por env vars e baixa recursivamente. So o codigo que decide *quando* invocar o helper mudou.

---

## lp-publicar, setup-agencia (+ docs LP)
### 2026-05-07 (tarde 2) — Recovery `webinar.buzzmonitor.com` (JSON wrapper bug) + LP `buzzcreators-webinar-junho` recuperada (sem bump — só doc)

Segundo incidente real do dia, em `webinar.buzzmonitor.com`. Deploy `dpl_AVT1U37u4ZDMQpyTLQVTsxTrK9pv` foi feito por colaboradora rodando versão antiga do `sync_sibling.py` (anterior à v3.1.0, ou implementação manual da API). Em vez de decodificar o `data` base64 do response `/v7/deployments/{id}/files/{uid}`, o helper escreveu o JSON cru (`{"data":"<base64>"}`) direto em cada `index.html` na sibling DELA. O deploy publicou esse JSON como HTML — visitante recebia 200 OK + Content-Type `text/html` mas o conteúdo era literalmente `{"data":"PCFkb2N0eXBlIGh0bWw+..."}`.

Diagnóstico: `curl https://webinar.buzzmonitor.com/analise-preditiva-maio-2026 | head -c 30` retornava `{"data":"PCFkb2N0eXBlIGh0bWw+`. As 3 LPs vizinhas estavam corrompidas; a LP nova (`buzzcreators-webinar-junho`) era a única íntegra porque foi copiada direto do filesystem da colaboradora, não baixada do live.

**Correção em 1 sessão:**
1. Discovery: validar Vercel CLI/token, listar últimos 10 deploys (todos os 4 de hoje afetados), inspecionar árvores via API V6 — confirmar que todas as 4 LPs aparecem na árvore (estrutura existe, conteúdo é que está errado).
2. Curl em cada LP no live → confirmar que 3 servem JSON, 1 serve HTML.
3. Confirmar sibling local da máquina do Victor ainda tem as 3 vizinhas íntegras (HTML puro, intactas pré-incidente — a colega não rodou da máquina dele).
4. Baixar `buzzcreators-webinar-junho/` do `dpl_AVT1U...` via `sync_sibling.py` v3.1.0 (decodifica base64 corretamente). Promover `logo-color.png` (PNG, 2.6KB) ao brand. Reverter paths absolutos `/assets/buzzcreators/...` para padrão source `../../brand/buzzcreators/assets/...`. Salvar em `landing-pages/buzzcreators/buzzcreators-webinar-junho/` com README documentando origem e débito técnico.
5. Adicionar a LP nova ao sibling local com paths reescritos guarda-chuva. Validar isolamento + capturar baseline MD5.
6. Deploy unificado `dpl_5RvZD27rGojJn3Xdifibc46WjAcb` — restaura as 3 LPs corrompidas (do sibling local íntegro) + preserva LP nova. Smoke test pós-deploy: 4/4 status 200, 4/4 MD5 batem com sibling, 4/4 começam com `<!doctype html>` (HTML puro, fim do JSON wrapper). Headers 7/7 ativos.

**Não requer bump de skill** — v3.1.0 do `sync_sibling.py` já faz `base64.b64decode(data, validate=True)`. Causa-raiz é máquina rodando versão antiga do helper. Mitigação operacional documentada: alinhar versão do repo (`git pull`) antes de delegar deploys guarda-chuva.

- **landing-pages/CONTEXT.md** (sem bump — só doc):
  - §6 (Troubleshooting): linha nova "LP responde 200 mas conteúdo começa com `{\"data\":\"<base64>\"}`" — sintoma, causa, solução.
  - §7.2 (Histórico): linha 2026-05-07 (tarde) documentando o **segundo incidente real** do dia + recovery.
- **`landing-pages/buzzcreators/buzzcreators-webinar-junho/` (NOVA)**: source recuperado do live. `index.html` (~46KB) com paths revertidos pro padrão (`../../brand/buzzcreators/...`) + README documentando origem + débito técnico (sem `copy.txt`, sem `REVISAO.md`, dependência cross-domain de `bruno-filho.png`).
- **`brand/buzzcreators/assets/logos/logo-color.png` (NOVO)**: versão PNG do logo color que só existia no deploy. Promovido ao brand para reuso futuro por outras LPs Buzzcreators.

### 2026-05-07 (tarde 1) — CSP libera Meta Pixel via GTM (lp-publicar v3.2.0)

LP `webinar-tecnologia-maio2026` (Cxpress) tinha GTM `GTM-T4XDWHL3` carregando, mas o pixel Meta nao disparava: CSP em producao recusava `connect.facebook.net` (onde mora o `fbevents.js`) e `www.facebook.com` (endpoint `/tr/` que recebe os eventos). Como o pixel e disparado pelo GTM em runtime, nem sempre aparece grep-avel no HTML — entao precisa estar coberto **por padrao** no template, nao caso-a-caso.

- **lp-publicar 3.1.0 → 3.2.0 (MINOR — capacidade nova retro-compat)**:
  - **`vercel.template.json`**: CSP ganha `https://connect.facebook.net` em `script-src` e `connect-src`; `https://www.facebook.com` em `connect-src` e `frame-src`. `img-src` ja permitia `https:` global, entao pixel GIF estava coberto.
  - **Passo 1.6**: nova checagem proativa antes do deploy — `grep -oE "fbq\(|connect\.facebook\.net|fbevents\.js|www\.facebook\.com/tr"` no HTML do sibling, alertando quando aparece (caso CSP do sibling guarda-chuva ainda esteja no template antigo).
  - **Passo 1.6**: descritivo do CSP padrao atualizado para mencionar Meta Pixel via GTM como provedor coberto.
  - Sibling de producao `cxpress-lp-playbook-whatsapp2026` ja recebeu o patch e foi redeployada (`dpl_9E2xEQdbWU2ocg47RpPCidgifV8g`). Smoke test 4/4 LPs intactas (livraria, playbook-whatsapp2026, latam-webinar-atencionalcliente, webinar-tecnologia-maio2026).

- **`landing-pages/CONTEXT.md` §6** (sem bump — so doc): nova linha de troubleshooting "Pixel Meta via GTM nao dispara" → CSP nao cobre Facebook → cobertura default a partir do template v3.2.0.

### 2026-05-07 — Sync sibling via Vercel API + LP `webinar-tecnologia-maio2026` recuperada (lp-publicar v3.1.0, setup-agencia v0.5.0)

Hardening de modo guarda-chuva apos **incidente real** que apagou `/livraria` da production por ~2h. Causa-raiz: deploy feito de maquina sem `livraria/` na sibling local, `BASELINES_OTHERS` (Passo 2.4) vazio, smoke test 3.4.b iterou sobre lista vazia e nao detectou regressao. Production foi substituida por snapshot que tinha apenas `playbook-whatsapp2026` + LP nova.

**O fluxo da correcao em 1 sessao:**
1. Investigacao do 404 reportado pelo Victor leva ao deploy `dpl_3rKKvvAfdinBXbQB1MeFFdJP51Au` (criado ~11h, 1.35h antes do diagnostico).
2. Plano: hardenizar `lp-publicar` com sync via Vercel API antes de modificar sibling.
3. Implementacao do Passo 0.5.d.
4. Primeiro teste em producao (`/lp-publicar cxpress livraria content.cxpress.io`): sync baixa playbook + webinar do live, sibling local mantem livraria, deploy preserva as 3 LPs. **livraria restaurada com sucesso**.
5. 4 bugs descobertos durante o teste foram corrigidos no mesmo PR.
6. LP `webinar-tecnologia-maio2026` recuperada do live pro repo (estava no Vercel mas sem source — foi publicada de outra maquina sem commit).

- **lp-publicar 3.0.0 → 3.1.0 (MINOR — capacidade nova retro-compat)**:
  - **Novo Passo 0.5.d "Sync sibling com ultimo deploy production"** entre 0.5.c e Passo 1, executado SO em modo guarda-chuva.
  - **0.5.d.i**: resolve `VERCEL_TOKEN` em 4 camadas — env var > `.env.local` no CWD > `.env.local` no repo principal (suporta worktrees via `git rev-parse --git-common-dir`) > parse de `auth.json` do CLI Vercel (sempre em `com.vercel.cli/Data/auth.json`, com `/Data/` no meio do path; cross-platform Linux/macOS/Windows). Token resolvido **sempre validado** via `curl /v2/user` antes de usar — descarta tokens expirados que o CLI renova internamente mas a API REST direta nao tem fallback.
  - **0.5.d.iii**: logica de download recursivo extraida pra arquivo helper `.claude/skills/lp-publicar/sync_sibling.py` (em vez de heredoc Python inline na skill). Heredoc combinado com escape de backslash em paths Windows + redirecionamento de stdin gerava bugs sutis. Script externo isola tudo, le env vars com `os.environ`, da pra testar isolado.
  - **0.5.d.iv**: validacao pos-sync cruza slugs vivos no dominio (curl 200) com `landing-pages/{*}/{*}/` no repo. Se algum slug vivo NAO esta na sibling pos-sync, aborta com mensagem clara — sem isso, deploy apagaria a vizinha.
  - **Edge case re-publicacao**: se o slug atual ja existe na sibling pos-sync, deixa — Passo 1.2 sobrescreve com a versao do source.
  - **Passo 0.1**: tambem ganhou fallback worktree pro `.env.local` (mesma logica do 0.5.d.i).
  - **Comentarios em 2.4 e 3.4.b**: explicitando 3 camadas de defesa (sync, baseline, smoke test).
  - Sem mudanca em interface, args ou comandos invocaveis.

- **setup-agencia 0.4.0 → 0.5.0**:
  - **Novo Passo 4.5 "Vercel API token (opcional)"** depois de 4.4. Recomendado pra colaboradores que vao publicar em guarda-chuva. Pulavel — fallback continua sendo `auth.json` do CLI.
  - Novo fallback `vercel-token-falhou` (mensagem hardcoded com instrucao manual).

- **`.claude/skills/lp-publicar/sync_sibling.py` (NOVO)**: script helper invocado pelo Passo 0.5.d.iii. Le env vars (`DEPLOY_ID`, `ORG_ID`, `VERCEL_TOKEN`, `SIBLING`), faz GET na arvore de arquivos do deploy, baixa cada folha via V7 e grava em `$SIBLING/`. Descarta o wrapper top-level `src/` que o Vercel envelopa.

- **landing-pages/CONTEXT.md** (sem bump — so doc):
  - §4.3 reescrita pra explicitar 3 camadas de defesa (sync, baseline, smoke test) e referenciar §7.2.
  - §6 (Troubleshooting): 2 linhas novas — "vizinhas viraram 404" e "Sync incompleto".
  - §7.2 (Historico): linha 2026-05-07 documentando o **incidente real** (livraria apagada e restaurada na mesma sessao via v3.1.0) + recuperacao da LP webinar.

- **`landing-pages/cxpress/webinar-tecnologia-maio2026/` (NOVA)**: source recuperado do live (deploy production atual). Contem `index.html` (~42KB) + `README.md` documentando origem + debito tecnico (sem `copy.txt`, sem `REVISAO.md`). Paths revertidos de absolutos (`/assets/...`) pra padrao source (`../../brand/cxpress/assets/...`).

- **`.env.local.example`**: nova secao "Vercel API (opcional)" documentando `VERCEL_TOKEN` e como gerar.

### 2026-05-04 — `.env.local` central + auto-invoke setup-agencia em fallback (v3.0.0)

Iteração de DX em cima da v2.0.0. Reduz precedência de `SIBLING_BASE` de 4 caminhos para 2, elimina branching do sanity check OneDrive/iCloud (vira responsabilidade do setup-agencia) e fecha o loop entre as skills: se config falta, lp-publicar invoca setup-agencia automaticamente.

- **`.env.local.example` (novo, raiz, versionado)**: template KEY=VALUE com `LP_SIBLING_BASE`. Documento auto-explicativo do formato pra colaboradores. Por enquanto só essa chave; preparado pra crescer com outras configs cross-skill per-máquina.

- **`.env.local` (gitignored)**: arquivo real escrito pelo setup-agencia. Substitui o `landing-pages/.lp-config.local.json` da v2.0.0 (removido do `.gitignore`).

- **lp-publicar 2.0.0 → 3.0.0 (MAJOR — comportamento muda)**:
  - Passo 0.1 simplificado de 4 caminhos → 2: env var `LP_SIBLING_BASE` no shell > linha em `.env.local`. Fim do fallback "parent-do-repo + sanity check OneDrive/iCloud/Dropbox" (v2.0.0). Config é responsabilidade do setup-agencia.
  - **Auto-invoke setup-agencia em fallback**: se nem env var nem `.env.local` resolverem, lp-publicar usa o tool `Skill` para invocar `setup-agencia` com argumento `"so lp"`, espera ele escrever `.env.local`, e re-resolve. Loop fechado, zero "rode X primeiro depois volte".
  - `allowed-tools` ganhou `Skill` para o auto-invoke acima.
  - **Migração necessária**: colaboradores existentes (Victor) precisam rodar `/setup-agencia` uma vez em modo `"so lp"` pra criar `.env.local`. Sem isso, primeira chamada de `/lp-publicar` automaticamente dispara o setup. Sem quebra silenciosa — só uma pergunta extra na primeira vez.

- **setup-agencia 0.3.0 → 0.4.0**:
  - Passo 4.4 reescrito: ao invés de instruir o user a rodar `setx`/`export` no shell (com fricção cross-platform: reabrir terminal, escolher entre bashrc/zshrc/etc), agora pergunta o path com `AskUserQuestion` (sugerindo parent-do-repo se não for sync-watched) e escreve `.env.local` direto via `Write`/`Edit`.
  - Validação de path: rejeita pasta dentro do repo, dentro de OneDrive/iCloud/Dropbox; pede outra.
  - Novo fallback `lp-sibling-falhou`.

- **landing-pages/CONTEXT.md §1**: precedência atualizada para 2 caminhos. Menciona auto-invoke do setup-agencia.

- **lp-preparar/CONTEXT.md** (sem bump — só doc): atualizada referência de precedência.

- **landing-pages/cxpress/livraria/README.md**: instrução manual de cópia atualizada para ler `.env.local` em vez do fallback `${LP_SIBLING_BASE:-../}` da v2.0.0. Mensagem clara "rode /setup-agencia primeiro" se faltar.

- **`.gitignore`**: substituído `landing-pages/.lp-config.local.json` por `.env.local`.

- **Motivação de DX**: o ponto crítico do Victor depois da v2.0.0 era que cada execução de `/lp-publicar` recomputava o ambiente (`git rev-parse` + `dirname` + sanity check). Custo em tokens marginal mas a complexidade era real — 4 caminhos pra entender e debugar. v3.0.0 troca essa complexidade por um arquivo de config persistente, mais alinhado com `meta-ads/.env` que já existe há tempo.

---

## news-gerar, news-revisar, template-newsletter.md, estilo-newsletter.md
### 2026-05-04 — Enxugamento + pergunta-eixo INTERNA (v2.1.0)

Feedback do Victor pos primeiro teste end-to-end com Cxpress BR: NL "muito grande, estrutura feia". Pediu reducao pela metade dos caracteres + remocao da pergunta-eixo do output visivel ("deixe como algo interno, que so nos vemos na hora de construir, mas que nao aparece de forma explicita para o cliente").

- **news-gerar 2.0.0 → 2.1.0**:
  - Limite do corpo: ≤600 → **≤300 palavras**
  - Bloco "## A pergunta da semana" no template **REMOVIDO** — pergunta-eixo agora vive como comentario HTML interno no topo do arquivo local (`<!-- Pergunta-eixo (planejamento interno, NAO publicar): "..." -->`) e em `dor-semana.md`. NUNCA aparece como bloco visivel ao leitor.
  - Mini-blocos da resposta encurtados: 95-115 → 35-55 palavras cada (total 110-170 vs 280-340 antes)
  - Abertura encurtada: 40-60 → 30-50 palavras
  - "Mais pra explorar": 1-2 bullets → 1 bullet (15-25 palavras)
  - Estrutura visivel: 2 blocos obrigatorios (Abertura + Resposta em capitulos) + 3 opcionais (era 3 obrigatorios + 3 opcionais)

- **news-revisar 2.0.0 → 2.1.0**:
  - Validar limite ≤300 palavras no corpo
  - Adicionar checagem: pergunta-eixo **NAO** aparece como bloco visivel (sem `> ## A pergunta da semana`, sem callout/blockquote com a pergunta literal). Se aparecer, REMOVER e absorver no assunto/abertura
  - Atualizar criterios de aprovacao

- **template-newsletter.md** (em news-gerar):
  - Reescrito conforme nova anatomia
  - Bloco "Pergunta da semana" removido como elemento visivel — vira nota explicativa de que a pergunta-eixo e elemento INTERNO de planejamento

- **conhecimento/editorial/estilo-newsletter.md**:
  - Anatomia atualizada: 2 blocos obrigatorios + 3 opcionais (em vez de 3 + 3)
  - Limite ≤300 palavras no corpo
  - Checklist atualizada: "Pergunta-eixo NAO aparece como bloco visivel"

- **Cxpress 2026-W19** (newsletter ja gerada): reescrita do corpo aplicando v2.1.0 (~376 → ~185 palavras), bloco da pergunta-eixo removido, Notion atualizado via `notion-update-page` (`replace_content`).

- **Sem mudanca em**: news-pesquisar (continua gerando `dor-semana.md` com a pergunta-eixo), news-pipeline, news-criar-post.

---

## news-* (familia) + estilo-newsletter.md + CLAUDE.md
### 2026-05-04 — Newsletter semanal noticiosa com eixo no blog proprio (v2.0.0)

- **Migracao da familia news-* de 5 NLs/mes formato campanha → 1 NL/semana formato curadoria editorial.**
- **Feedback de origem:** Alessandro (socio) leu as 4 NLs do mes e disse "esta com muita cara de campanha de email marketing", pediu formato mais noticioso, 90% conteudo do blog proprio (oportunidade de revisar centenas de posts antes de divulgar), 10-20% clipping de imprensa, foco em dores, linguagem jornalistica e direta, sugestao de "uma pergunta por edicao", edutainment (educacao + entretenimento). Benchmark: a propria newsletter Buzzmonitor.

- **news-pesquisar 1.0.0 → 2.0.0 (MAJOR):**
  - Foco totalmente reorientado: mapear dores (BRANDBOOK §Publico-Alvo) + indexar blog proprio em profundidade + clipping PR (mencoes da marca em imprensa, data ≤ 7 dias).
  - Removidos da news: noticias gerais de mercado e analise de concorrentes (concorrentes.md preservado para outras skills).
  - Cache cumulativo `conhecimento/produto/{brand}/blog-cache.md` indexa posts ja conhecidos (nao deleta entre semanas).
  - Versionamento de pasta: `pesquisa/atual/` (semana corrente) + `pesquisa/arquivo/YYYY-WW/` (historico).
  - Novos outputs: `dores-candidatas.md`, `indice-blog.md`, `dor-semana.md`, `pauta-sugerida.md` (condicional), `clipping-pr.md`, `RESUMO.md`.
  - Detecta lacuna: dor com cobertura <3 posts gera pauta sugerida.
  - Argumento `foco` removido (era engessante).

- **news-criar-post 1.0.0 (NOVO):**
  - Skill manual-trigger invocada pelo `news-pipeline` apos aprovacao explicita da pauta.
  - Le `pesquisa/atual/pauta-sugerida.md`, escreve post completo (1500-2500 palavras) seguindo `conhecimento/copywriting/blog-copy.md` com edutainment + tom jornalistico.
  - Salva local em `newsletter/{brand}/posts-sugeridos/post-{slug}-{semana}.md` e publica draft no Notion sob `Entregas > Drafts de Blog > {Marca} > [{semana}] {H1}`.
  - Atualiza `dor-semana.md` adicionando o novo post como ancora 1, e `_state.json` registrando a pauta consumida.
  - Time editorial revisa, publica no blog real e atualiza dor-semana.md com URL final antes do disparo da news.

- **news-gerar 1.0.0 → 2.0.0 (MAJOR):**
  - Output: 1 NL em `newsletter/{brand}/entregas/newsletter-{semana}.md` (sem subpasta YYYY-WW — direto na pasta `entregas/`).
  - Le `dor-semana.md`, `clipping-pr.md`, `_state.json` e (se existir) swipe-file Buzzmonitor.
  - Estrutura nova: 3 blocos obrigatorios (Abertura jornalistica + Pergunta da semana + Resposta em capitulos) + 3 opcionais (Mais pra explorar + Na imprensa + Bloco extra).
  - Limites: ≤600 palavras no corpo, 3-6 links contextuais (≥3 blog proprio, ≤1 clipping, ≤1 extra).
  - Notion: 1 pagina por edicao (nao toggle), titulo `[{semana}] {Assunto}`.
  - Atualiza `_state.json` com pergunta-dor e links da edicao para dedupe (6 semanas pergunta, 4 semanas links).

- **news-revisar 1.0.0 → 2.0.0 (MAJOR):**
  - Argumento `[todas|N]` removido (sempre 1 NL).
  - Novas validacoes: ≥3 links blog proprio, 3-6 links totais, ≤1 clipping PR, ≤1 extra, 0 noticias gerais de mercado, dedupe vs `_state.json`.
  - Linguagem jornalistica: rejeita aberturas "imagine que...", "no mundo atual...", frases medias ≤22 palavras.
  - Tom nao-vendedor: max 1 mencao a marca fora dos links de blog; alerta se >40% links forem para dominio proprio fora do blog.
  - Edutainment: cada mini-bloco da resposta valida ter analogia, dado, exemplo ou definicao.
  - Limite mantido em 600 palavras (corpo).

- **news-pipeline 1.0.0 → 2.0.0 (MAJOR):**
  - Novo fluxo: pesquisa → (pausa explicita: aprovar pauta sugerida?) → news-criar-post (se aprovada) → news-gerar → news-revisar.
  - Argumento `foco` removido.
  - Adicionada nota de cadencia semanal (loop ou schedule).
  - Relatorio final consolida estado da edicao + draft de blog (se houver) + pendencias do time editorial.

- **template-newsletter.md (em news-gerar):** reescrito completo. Estrutura espelha a anatomia: Abertura jornalistica (40-60 palavras) + Pergunta da semana (15-20 palavras em destaque) + Resposta em tres tempos (3 mini-blocos, 280-340 palavras, 3 links) + opcionais.

- **conhecimento/editorial/estilo-newsletter.md (in-place):**
  - Referencia de estilo: YouScan → newsletter oficial Buzzmonitor (com pointer para swipe-file a popular com amostras reais).
  - Adicionadas secoes: Anatomia da newsletter semanal, Linguagem jornalistica e direta, Edutainment, Criterios de selecao de post proprio, Criterios de clipping PR, Bloco extra (sem cadencia fixa).
  - Demovidos: "Tipos de Gancho (10 tipos)" → "Aberturas jornalisticas (referencia opcional)" — tipos viram inspiracao para abertura curta, nao eixo da NL. "Tipos de CTA" → removido (sem cadencia fixa).
  - Checklist pre-publicacao reescrita.

- **CLAUDE.md:** fluxo `Newsletters` atualizado (inclui pausa de aprovacao + news-criar-post). Tabela de comandos news-* expandida (5 comandos). Nota de cadencia semanal via `/loop` ou `/schedule`.

- **Conhecimento sustentado:** `conhecimento/copywriting/swipe-file/buzzmonitor-newsletter.md` sera populado com 3-5 edicoes reais da newsletter Buzzmonitor (Victor envia). Sem o swipe, news-gerar usa fallback editorial baseado em estilo-newsletter.md.

- **Migracao:** sem modo legacy. Pesquisas e entregas mensais antigas ficam em `entregas/YYYY-MM/` e `pesquisa/arquivo/` como historico. Primeira execucao da v2.0 cria `entregas/newsletter-{semana}.md`, `_state.json` zerado e `blog-cache.md` zerado.

- **BREAKING:** argumento `foco` removido de news-pipeline e news-pesquisar; argumento `[todas|N]` removido de news-revisar; pesquisa nao gera mais `noticias-mercado.md` nem `analise-concorrentes.md` para a news.

- Plano de implementacao em `~/.claude/plans/n-s-rodamos-a-skill-eventual-token.md`.

---

## lp-publicar, lp-preparar, setup-agencia, landing-pages/CONTEXT.md
### 2026-05-04 — Cross-platform: paths sibling e auth Vercel parametrizados

- **lp-publicar 1.7.0 → 2.0.0 (MAJOR — comportamento muda por máquina):**
  - Novo Passo 0.1: `SIBLING_BASE` resolvido em runtime em ordem de precedência: env var `LP_SIBLING_BASE` > `landing-pages/.lp-config.local.json` (campo `siblingBase`, gitignored) > pasta-mãe do repo (`dirname(git rev-parse --show-toplevel)`). Sanity check aborta se default cair em pasta sync-watched (OneDrive/iCloud/Dropbox/node_modules/.git/worktrees) — exige `LP_SIBLING_BASE` explícita.
  - Passo 0.5 reescrito em 3 sub-passos: pre-flight do CLI Vercel (`vercel --version` + `vercel whoami --scope $TEAM`, abortando com erro claro se faltar instalação ou auth), detecção de guarda-chuva via `vercel alias ls` + awk (CLI cuida de auth internamente — zero dependência de filesystem cross-platform), garantia de `.vercel/project.json` no sibling de guarda-chuva (auto-link via `vercel link` se ausente — destrava primeira execução em outra máquina).
  - **Por que `alias ls` em vez de `curl + Python lendo auth.json` (escolha original do plano):** verificação descobriu que Python da Microsoft Store (caso comum no Windows) roda em sandbox AppContainer e não consegue acessar paths absolutos em `AppData/Roaming/`, mesmo com paths corretos. Validado: `Path('auth.json').exists()` no CWD = True; `Path(os.environ['APPDATA']) / '...'` = False. Pivot para CLI nativo elimina toda essa categoria de bug. Bônus: `alias ls` cobre o caso "domínio atribuído mas projeto sem deploy custom-domain" (cenário "guarda-chuva em popularização" — `material.buzzmonitor.com` hoje), que `vercel projects ls` não pega.
  - Removidas todas as menções a `C:/Users/titof/Downloads/Claude/{nome}/` no SKILL.md (substituídas por `${SIBLING_BASE}/{nome}/`).
  - Removida a leitura direta de `$APPDATA/com.vercel.cli/Data/auth.json` (Windows-only e quebrava com Python sandboxed).
  - **Migração para Victor:** comportamento default (parent-do-repo) já bate com o setup atual (`Downloads/Claude` é o parent de `Agente Inhouse/`). Verificação end-to-end confirmou que SIBLING_BASE resolve igual ao path antes hardcoded. Nenhuma ação necessária.

- **lp-preparar 1.1.0 → 1.2.0:**
  - Tabela "Projetos Vercel correspondentes" no `CONTEXT.md` perdeu coluna "Sibling local" (derivada em runtime, era redundante). Restaram subdomínio + projeto Vercel.
  - Seção "Pasta sibling (deploy artifact)" agora documenta `${SIBLING_BASE}/{nome}/` em vez de path absoluto.

- **landing-pages/CONTEXT.md:**
  - §1 (Mapa mental): adicionada linha sobre resolução de `SIBLING_BASE` em runtime.
  - §4.1, §4.2, §6 (troubleshooting): paths absolutos `C:/Users/titof/...` substituídos por `${SIBLING_BASE}/...`.

- **setup-agencia 0.2.0 → 0.3.0:**
  - Passo 1.2 ganhou opção 5 — "Landing Pages (/landing-page)" — que dispara o novo Passo 4.
  - Novo **Passo 4** (Vercel CLI) com sub-passos: validar CLI via `npx vercel --version`, login via `npx vercel login`, validar org com `vercel whoami --scope team_nC991VqUuSU2jXZN152xqqEg`, e configuração opcional de `LP_SIBLING_BASE`. Explicita que **MCP Vercel ≠ CLI Vercel**.
  - Passo 4 antigo (Test drive) renumerado para 5; Passo 5 (Resumo) para 6 — agora inclui `/landing-page` e o checkmark de Vercel.
  - Novos fallbacks: `vercel-cli-falhou`, `vercel-login-falhou`, `vercel-org-falhou`.

- **landing-pages/cxpress/livraria/README.md:** instrução manual de cópia atualizada para usar `LP_SIBLING_BASE` com fallback a parent-do-repo + auto-link via `vercel link` se `.vercel/project.json` ausente. Funciona cross-máquina.

- **`.gitignore`:** adicionado `landing-pages/.lp-config.local.json` (config pessoal por colaborador).

- **Motivação:** colega tentou rodar `/lp-pipeline` em máquina nova e falhou em 2 frentes — sibling apontando pra `C:/Users/titof/...` inexistente, e leitura de auth Vercel via `$APPDATA` falhando porque ela autenticou só o MCP Vercel (não o CLI). Pós-mortem em `~/.claude/plans/uma-colega-rodou-lp-pipeline-staged-biscuit.md`.

---

## landing-pages/GUIDELINES.md
### 2026-04-30 — §10 Posicionamento do formulário (sugestão)
- Nova seção §10 com defaults de posicionamento por tipo de LP, válidos para todas as marcas:
  - **Webinar / material rico** → form na 2ª dobra (lead frio, otimizar volume).
  - **BoFu (demo, falar com vendas)** → form no meio da página (scroll filtra intenção, otimiza qualificação).
  - Sempre manter CTA visível na 1ª dobra que rola suave até o form.
- Sugestão, não obrigação. Override permitido com justificativa no PR/REVISAO.md.
- §6 (Estrutura mínima) ajustada: "CTA final com formulário" → "CTA final", desacoplando posição do form da estrutura narrativa (a §10 decide onde o form aparece).
- §§ 11-13 renumeradas (antigas §§ 10-12: integração tardia, favicon, performance).
- Base de pesquisa: CXL (long vs short form), MarketingExperiments (Sierra Tucson +220% com form abaixo da dobra), Unbounce Conversion Benchmark Report, Clearbit (lead form quality).

---

## meta-ads (benchmarks)
### 1.1.0 — 2026-04-30 — Threshold único nos benchmarks
- `meta-ads/data/benchmarks.json` simplificado: removida a tier "bom"/"aceitável", agora é **um threshold só = mínimo aceitável**. Status binário `[OK]` / `[RUIM]` (antes 3-tier).
- Valores atualizados conforme padrão atual da agência:
  - **CTR link** (cliques/impressões): Topo ≥ 1,0% / Remarketing ≥ 0,6%.
  - **Taxa de conversão LP** (leads/cliques): Topo ≥ 15% / Remarketing ≥ 5%.
  - **CpL** (gasto/leads):
    - BRL: Webinar ≤ R$ 18 / Material rico ≤ R$ 12 / Remarketing ≤ R$ 220.
    - USD (Latam): Webinar ≤ US$ 5 / Material rico ≤ US$ 3 / Remarketing ≤ US$ 60.
    - EUR (Portugal): Webinar ≤ € 6 / Material rico ≤ € 6 / Remarketing ≤ € 60.
  - **Frequência** (global): ≤ 7,0.
- `benchmark_checker.py` adaptado: `get_metric_status()` retorna `[OK]` ou `[RUIM]` (sem `[OK] Aceitável`).
- `full_trends_report.py` `_benchmarks_for()` adaptado para nova estrutura: `_bom` e `_ruim` apontam ao mesmo threshold (matriz de cenários CpL × CTR × Conv.LP segue funcionando como classificação binária).
- Skill `meta-ads/SKILL.md` (1.0.0 → 1.1.0): seção "Status dos Benchmarks" reescrita com tabela explícita por etapa de funil e moeda. `meta-ads/CONTEXT.md` ganha tabela de referência idêntica para colaboradores consultarem.

---

## lp-preparar (CONTEXT.md), landing-pages/CONTEXT.md
### 2026-04-28 — Documentação dos guarda-chuvas Buzzmonitor (3 subdomínios) + Cxpress
- Tabela de marcas em `lp-preparar/CONTEXT.md` ampliada: Buzzmonitor agora tem 3 subdomínios guarda-chuva (`evento.*`, `material.*`, `webinar.*`) com convenção de uso por tipo de LP. Cxpress documentado com `content.cxpress.io` (subdomínio único, qualquer tipo de LP).
- `landing-pages/CONTEXT.md` §4.2 ganhou tabela "Guarda-chuvas ativos hoje" com mapping subdomínio→projeto Vercel→LPs ativas, mais regra editorial: LPs novas devem priorizar subdomínio mais específico.
- Argument-hint de `lp-pipeline` e `lp-publicar` atualizado: exemplo agora usa `evento.buzzmonitor.com` (mais alinhado com convenção atual). PageSpeed example em `lp-publicar` Passo 5.1 também atualizado.
- **Comportamento das skills inalterado** — `lp-publicar` Passo 0.5 já era genérico, detecta qualquer guarda-chuva via API Vercel. Mudança é puramente documentacional.
- **Migração concomitante:** LP `vendendo-com-creators` (Buzzcreators, evento presencial) movida de `webinar.buzzmonitor.com` → `evento.buzzmonitor.com`. Redirect 301 ativo no antigo para preservar URLs já compartilhadas. Detalhes em `landing-pages/buzzcreators/vendendo-com-creators/REVISAO.md` Iteração 2.5.

---

## pauta-quente
### 1.1.0 — 2026-06-02 — Doc de roteiro falado à câmera (Triângulo do Yap) no tipo video-curto
- **Liga o doc** `conhecimento/copywriting/video-curto-talking-head.md` (framework **T · MAES · A/N**) ao tipo `video-curto`, espelhando o que foi feito na `copy-criar` v1.1.0 (mesma sessão 2026-06-02).
- **Carregamento:** Passo 3 (Copy — por tipo) passa a ler o doc quando `tipo = video-curto`; tabelas "Tipos de Conteúdo" e "Base de Conhecimento" do `CONTEXT.md` atualizadas.
- **Aplicação:** Passo 5 (template Video-Curto) instrui a estruturar o áudio pelo esqueleto T·MAES·A/N quando for talking head, **mapeado na ancoragem jornalística da skill**: T = HOOK (fato/dado), MAES = CONTEXTO+INSIGHT num exemplo/analogia concreto, A/N = CONECTOR+CTA. Preserva a regra dura "conector + CTA sempre ao final".
- Não-breaking: nenhum parâmetro, template ou tipo (carrossel/blog/linkedin/email) mudou; só adiciona fonte e orientação para video-curto.

### 1.0.0 — 2026-04-24
- Skill nova `/pauta-quente` para transformar noticia recente em conteudo multi-formato x multi-idioma por marca. Orientada a evento externo (URL obrigatoria), complementar a `/copy-criar` (standalone).
- Inputs: `[url] [marca] [tipos-csv] [idiomas-csv]`. Tipos: `carrossel`, `video-curto`, `blog`, `linkedin`, `email`. Idiomas: `br` (PT-BR), `pt` (PT-PT), `es` (ES-LATAM). Combinacoes cartesianas tipos x idiomas numa unica execucao.
- Pipeline de 10 passos: parsing -> fingerprint URL (primaria/imprensa-com-fonte/agregador) -> pesquisa expandida ate fonte primaria (ate 3 queries WebSearch quando necessario + 1 query de contexto) -> carregar base de conhecimento (brand + copy + anti-ia + linguistico por idioma) -> definir angulo edutainment + conector com produto -> **gerar pecas** (em memoria) -> **revisao anti-IA pos-geracao dedicada** (varre frases tipicas, filler words, anti-patterns estruturais; corrige em lugar; log em REVISAO-LOG.md) -> salvar local -> publicar Notion (gate: so publica pecas sem `requer-atencao-humana`) -> resumo final.
- Diretrizes editoriais obrigatorias: edutainment (educacao + entretenimento), fontes primarias rastreadas (nunca "noticia da noticia"), conector com produto ao final com feature especifica + beneficio concreto, CTA focado em beneficio por canal.
- Output local em `pauta-quente/{marca}/YYYY-MM-DD-{slug-noticia}/` (pasta raiz nova, versionada, espelhando `newsletter/` e `traducao/`).
- Output Notion em `Entregas > Pauta Quente {Marca} > YYYY-MM-DD — {tema}` com toggles organizados por tipo primeiro, idioma dentro (corte natural para distribuidor por canal). Icon 🔥.
- **Docs novos criados junto:** `conhecimento/copywriting/blog-copy.md` (9 secoes — titulo, estrutura, lead, corpo, fontes, conector, CTA, extensao, checklist) e `conhecimento/copywriting/linkedin-copy.md` (10 secoes — hook, estruturas por tamanho, ritmo visual, storytelling, tom, conector, CTA, hashtags, anti-padroes, checklist). Ambos espelham o padrao de `email-copy.md`.
- Gate automatico: pecas marcadas `revisao: requer-atencao-humana` apos 2 rodadas de revisao ficam so em disco local, nao sao publicadas no Notion — evita vazamento de IA em entrega oficial.

---

## pull-request-review
### 1.0.1 — 2026-04-23
- **Fix Windows:** `/tmp/` não persiste entre bash calls no Claude Code no Windows (shell state some). Passo 2 agora salva em `reviews/.tmp/` (dentro do repo, persiste).
- **Fix encoding:** Python 3 no Windows usa `cp1252` por padrão em `open()` — quebra ao ler JSON da API com unicode (→, ≤, emojis). Todas as chamadas de `open()` agora passam `encoding='utf-8'` explicitamente.
- **Fix SHA vazio:** `check-runs` chamava a API com `$SHA` vazio porque estava em bash call separado. Agora extração de SHA e call de check-runs ficam no mesmo bash da coleta de meta/files/commits, reusando `$TOKEN`.
- **Novo:** Passo 3.1 — salvar patches em arquivos individuais (`reviews/.tmp/patches/{path}.patch`) pra poder ler via `Read` tool, contornando problema de encoding no stdout do terminal Windows.
- Descoberto durante auto-review do PR #1; memory feedback `feedback_skill_improvement.md` aplicado (bug em skill durante uso → atualizar a skill antes de fechar).

### 1.0.0 — 2026-04-23
- Skill nova `/pull-request-review` para o Victor revisar PRs localmente — recebe URL ou número do PR, coleta diff + metadata + CI status via API do GitHub (reusa token do Git Credential Manager, mesmo padrão do `/commit`), analisa em 3 dimensões (genérico, domain-specific do Agente Inhouse, PR meta) e gera relatório em `reviews/pr-{N}-YYYY-MM-DD.md` com achados em 3 níveis de severidade (🔴 CRÍTICO, 🟡 IMPORTANTE, 🟢 NICE-TO-HAVE).
- Domain-specific checks: skills (frontmatter, CHANGELOG sync, version bump), brand tokens (W3C DTCG), LPs (GUIDELINES, favicon absoluto, 2-3 cores, Cxpress cases pendentes), meta-ads (read-only, sem secrets), conhecimento (duplicação), CLAUDE.md (manter enxuto), CHANGELOG (ISO dates, ordem).
- Relatório local apenas — skill NUNCA posta, aprova, fecha ou mergea o PR. Veredicto automático: Aprovar / Aprovar com ressalvas / Pedir ajustes / Rejeitar.
- Suporta PR de repo externo com degradação graciosa (só roda Dimensão A genérica, avisa que domain checks não aplicam).

## commit
### 2.0.0 — 2026-04-23
- **Reescrita completa do Passo 5 para via única: API direta do GitHub.** Remove dependência de `gh` CLI e remove o fallback via navegador.
- A skill agora extrai o token do **Git Credential Manager** (o mesmo que autentica `git push`) via `git credential fill` com `GIT_TERMINAL_PROMPT=0` e chama `POST /repos/{owner}/{repo}/pulls` via `curl`. Zero cliques, zero dependências externas (nem `gh`, nem navegador).
- Breaking change vs v1.x: Passo 0.3 (detecção de `gh auth`) removido; Passo 5 deixa de bifurcar por `GH_AUTH_OK`. Comportamento anterior via `gh pr create` ou URL compare no browser não existe mais.
- Detecção de PR duplicado mantida via `GET /pulls?head={owner}:{branch}&state=open`; 401/403 aborta com instrução pro usuário abrir PR manualmente (copiando título e body já prontos).
- Mensagem de erro de push auth atualizada pra guiar `git pull` manual (pra o credential helper salvar o token), em vez de `/setup-agencia`.

### 1.0.0 — 2026-04-23
- Skill nova `/commit` para colaboradores entregarem alterações ao Victor sem commitar direto em main.
- Fluxo autônomo: pre-flight checks (repo git, sem rebase/merge pendente, `gh` logado, há algo pra commitar) → inspeção com detecção de arquivos sensíveis (`.env`, credentials, tokens, keys) → branch `claude/{slug}` (infere do path dominante do diff, fallback random estilo `claude/vibrant-elgamal`) → commit PT-BR imperativo → push → `gh pr create` com base=main → retorna URL para revisão.
- Reusa branch atual se já estiver fora da main; aborta limpo se PR já existe (OPEN), se push falha non-fast-forward, se hook pre-commit bloqueia, ou se detecta arquivo sensível.
- Regras invioláveis hardcoded: nunca commita em main, nunca usa `--force`/`--no-verify`/`--amend`, nunca mergea, nunca adiciona `Co-Authored-By`.
- PR body em PT-BR com seções `## Resumo` + `## Arquivos alterados`, sem assinatura de IA.

## setup-agencia
### 0.2.0 — 2026-04-23
- Resumo final (Passo 5) agora menciona `/commit` como comando pós-alterações, com instrução clara de que nunca commita em main.
- Nenhum passo de setup adicional foi introduzido — `/commit` v2.0.0 funciona com a credencial do Git Credential Manager que todos já têm do clone HTTPS.

## landing-page (advisor) + familia lp-*
### 1.9.0 — 2026-04-30 (lp-integrar-form: card-dentro-de-card)

Round de fix a partir de incidente visual durante integracao do form Jotform na LP `buzzmonitor/social-listening-mayo-2026-latam`. Foco: garantir que o wrapper do embed nao herde o card visual do form mock.

#### Sintoma observado
Apos `/lp-integrar-form` substituir o `<form>` mock pelo embed Jotform, o live mostrou **dois cards aninhados**: o card branco com `padding: 40px`, `border` e `box-shadow` do `.form` (estilo do mock no `lp-gerar`) envolvendo outro card branco que o Jotform renderiza por padrao em volta dos campos.

#### Causa-raiz
- `lp-integrar-form` Passo 2 instruia: `<div class="form jotform-embed">{snippet}</div>`. A classe `form` foi mantida com a intencao de "preservar tamanho/contexto" do mock.
- Mas `.form` no `lp-gerar` e um **card visual completo** (`background: #fff; padding: 40px; border: 1px solid; box-shadow`) — nao so estilos de campo. Provedores externos (Jotform, RD Station, HubSpot) ja vem com card proprio. Resultado: dois cards.
- O CSS canonico `.form.jotform-embed { padding: 16px; overflow: hidden }` (Passo 3 da v1.2.0) so sobrescrevia o padding — nao desligava background/border/shadow herdados.

#### Mudancas
- **`lp-integrar-form` 1.2.0 → 1.3.0** — Passo 2 atualizado: wrapper agora usa apenas `<div class="jotform-embed">` (sem `form`). Passo 2 explicita "NAO herdar a classe `form` do mock" com referencia ao incidente. Passo 3 reduzido: `.jotform-embed iframe { width: 100% !important; ... }` (sem padding/background/overflow no wrapper — o provedor cuida do card). Passo 3 inclui regra de migracao: se LP antiga tem `.form.jotform-embed` (v<=1.2.0), substituir pelo novo seletor.
- **CHANGELOG entry** (este) — registra incidente para referencia futura, conforme `feedback_skill_improvement.md` (bug em skill durante uso → atualizar a skill antes de fechar caso pontual).

#### Skills bumpadas
- `lp-integrar-form` 1.2.0 → 1.3.0 (wrapper limpo, sem heranca de card mock)

#### Skills nao tocadas
- `lp-gerar`, `lp-revisar`, `lp-preparar`, `lp-publicar`, `lp-pipeline`, `landing-page` (advisor) — nao envolvidas. O `.form` no `lp-gerar` continua sendo card visual valido para o mock; mudanca foi apenas no que `lp-integrar-form` faz na transicao mock → embed.

#### Como impacta a LP afetada
A LP `buzzmonitor/social-listening-mayo-2026-latam` foi consertada in-place no mesmo round: `index.html` ajustado (classe `form` removida do wrapper, CSS reduzido) e re-deploy via `/lp-publicar`. Skill atualizada previne o cenario na proxima integracao.

### 1.8.0 — 2026-04-29 (guard anti-vazamento de copy)

Round de fixes a partir de incidente de geracao da LP `buzzmonitor/social-listening-mayo-2026-latam`. Foco: prevenir o gerador de inventar texto novo durante `lp-gerar` quando o briefing pede componentes visuais ricos (pull-quotes, kickers, tags rotacionadas, art cards).

#### Sintoma observado
Auditoria pos-`lp-gerar` (modo review) detectou **5 vazamentos CRITICOS** no HTML gerado:
- Frase-ancora do CIERRE truncada: `"...sino las que mejor entienden lo que se dice de ellas"` virou `"...sino las que mejor escuchan"`.
- Pull-quote inventado em `<aside class="for-quote">` na secao Para Quien (frase nao existia em `copy.txt`).
- Question inventada na secao Cierre (`"Sobran datos. Falta lectura. Vamos a leer juntos el 28 de Mayo."` — nao em `copy.txt`).
- Punchline de marketing inventada: `"Sin spam, sin enredos."` no CTA final.
- 5 em-dashes adicionados ao body durante expansao de bullets em `<h3>+<p>` (regras-anti-ia.md tem tolerancia zero para em-dash).

Plus: sinonimos cosmeticos (hero h1 `"utilizar"` -> `"usar"`), virgula+conjuncao reescrita como ponto+frase no hero sub.

#### Causa-raiz
- `lp-gerar` Passo 3 (briefing) instruia "estrutura solicitada" descrevendo elementos visuais (`card visual`, `tag rotacionada`, `pull-quote`) sem amarrar o texto desses elementos a uma linha especifica de `copy.txt`. O gerador interpretou "tem espaco visual aqui" como permissao para inventar.
- `lp-gerar` Passo 4 (validacao) so checava contagem de itens e emoji — nao fazia diff textual entre `copy.txt` e strings do HTML.
- `lp-revisar` tinha auditoria de GTM (Passo 3.5) mas nao tinha equivalente para fidelidade da copy.
- Incentivo composicional perverso: `frontend-design` e otimizada para gerar UIs "memoraveis" — quando ve um art card com slot vazio, preenche com texto criativo, nao com decoracao geometrica.

#### Mudancas
- **`lp-gerar` 1.4.0 -> 1.5.0** — Passo 3 (briefing pra `frontend-design`) ganhou bloco **REGRA DE FIDELIDADE DA COPY** explicitando: (a) todo texto visivel vem literal de `copy.txt`, (b) lista do que NAO inventar (pull-quotes, kickers, taglines, disclaimers punchy), (c) regra de nao truncar nem reescrever cosmeticamente, (d) whitelist exata do que pode aparecer fora da copy (5 categorias), (e) instrucao explicita "se componente visual pede texto e copy nao tem, fazer sem texto OU repetir literal frase relevante da copy". Passo 4 dividido em 4.1 (checklist tecnico — adicionado item de fallback robusto de reveal-on-scroll via `<noscript>`) e 4.2 (auditoria de fidelidade — diff textual em 4 buckets, busca dos 4 padroes mais comuns de vazamento, contagem de em-dash, validacao da frase-ancora, deteccao de sinonimos).
- **`lp-revisar` 1.3.0 -> 1.4.0** — novo **Passo 3.6: Auditoria de Fidelidade da Copy (CRITICO)**. Defesa em camadas: roda independente da auditoria que a `lp-gerar` ja faz. Procedimento de 7 etapas: carregar `copy.txt`, extrair textos do HTML, classificar em 4 buckets (literal/whitelist/cosmetica/vazamento), procurar 4 padroes (pull-quote, kicker, tag rotacionada, punchline), auditar em-dash com grep, validar frase-ancora, detectar sinonimos. Tabela de severidade-acao mapeia cada tipo de achado. Vazamentos sao tratados com mesma prioridade do GTM — CRITICOS, nao opcionais.
- **CHANGELOG entry** (este) — registra incidente para referencia futura, conforme `feedback_skill_improvement.md` (bug em skill durante uso -> atualizar a skill antes de fechar caso pontual).

#### Skills bumpadas
- `lp-gerar` 1.4.0 -> 1.5.0 (regra de fidelidade no briefing + checklist auditoria de fidelidade no Passo 4.2 + fallback robusto de reveal Passo 4.1)
- `lp-revisar` 1.3.0 -> 1.4.0 (novo Passo 3.6 — auditoria de fidelidade da copy)

#### Skills nao tocadas
- `lp-preparar`, `lp-publicar`, `lp-integrar-form`, `lp-pipeline`, `landing-page` (advisor) — nao envolvidas no path de geracao do HTML.

#### Como impacta a LP afetada
A LP `buzzmonitor/social-listening-mayo-2026-latam` foi consertada in-place no mesmo round (5 criticos + 4 melhorias aplicados via `Edit` em `index.html`, documentados em `REVISAO.md`). Nao precisa re-rodar `lp-gerar` — fix cirurgico foi suficiente. Skills atualizadas previnem o cenario na proxima LP.

### 1.7.0 — 2026-04-28 (consolidacao pos-revisao critica)

Round de fixes a partir de revisao critica das skills LP + CONTEXT/GUIDELINES (3 alta + 5 media + 4 baixa severidade). Foco: eliminar contradicoes, deduplicar regras espalhadas, fonte unica para regras canonicas (cascata GTM, snippet GTM, anti-padroes, wrapper CSS form).

#### Alta severidade (bugs reais)
- **`landing-pages/CONTEXT.md` §5.1:** documentar explicitamente que `lp-gerar` pula o passo 2 da cascata (HTML ainda nao existe) — antes essa diferenca nao estava em lugar nenhum, gerava confusao entre lp-gerar (2 passos) vs lp-revisar (3 passos).
- **`landing-pages/CONTEXT.md` §3.7 (validacao favicon):** `curl` de exemplo trocou `{path}` (variavel inexistente — favicon resolve em `/` absoluto) por paths corretos solo (`/assets/logos/...`) e guarda-chuva (`/assets/{marca}/logos/...`).
- **`landing-page` (advisor) v1.1.0 → v1.2.0:** Q1 reduzida de 7 → 3 opcoes (LP nova / Alterar / Etapa especifica) — AskUserQuestion suporta no maximo 4. Q1b expande "Etapa especifica" se necessario. Fluxo: Alterar agora delega decisao fina a `landing-pages/CONTEXT.md` §2.2 em vez de duplicar a tabela.

#### Media severidade (deduplicacao)
- **Cascata de regiao centralizada em `landing-pages/CONTEXT.md` §5.1.** Removida de `lp-gerar` e `lp-revisar` (substituida por ref) e do brand CONTEXT (`.claude/skills/lp-preparar/CONTEXT.md`). Antes vivia em 4 lugares — qualquer mudanca exigia atualizar 4 arquivos com risco de divergir.
- **Snippet GTM canonico em `landing-pages/CONTEXT.md` §5.3.** Removido de `lp-gerar` Passo 3 (briefing) e `lp-revisar` Passo 3.5. Skills agora apontam pro snippet em §5.3. Se Google atualizar o snippet, 1 lugar pra atualizar.
- **Wrapper CSS `.form.jotform-embed` so em `lp-integrar-form` Passo 3.** Removido de GUIDELINES §10 e do brand CONTEXT — esses agora referenciam.
- **Anti-padroes consolidados em `landing-pages/CONTEXT.md` §7** (categoria + historico). `lp-publicar` substituiu sua lista propria por referencia a §7.1. CONTEXT §2.3 (anti-padroes de fluxo) tambem virou ref para §7.1.
- **Fluxo de alteracao alinhado:** `landing-page` advisor agora delega 100% a `landing-pages/CONTEXT.md` §2.2 (matriz canonica de 11 linhas) em vez de manter tabela propria com 6 categorias incompletas.

#### Baixa severidade (polish)
- **Adicionada `landing-pages/CONTEXT.md` §5.2 — ownership chain:** `lp-gerar` injeta inicial, `lp-revisar` audita+corrige, `lp-publicar` valida no live. Antes essa cadeia ficava implicita em 3 SKILL.md sem visao consolidada.
- **PageSpeed endpoint movido** do brand CONTEXT (.claude/skills/lp-preparar/CONTEXT.md) — so `lp-publicar` Passo 5.1 usa, ja tinha duplicado la. Brand CONTEXT e shared entre todas skills lp-* — endpoint de validacao pos-deploy nao pertencia ali.
- **Brand CONTEXT "Pasta sibling" atualizada** pra refletir solo + guarda-chuva (antes so descrevia formato solo `{marca}-lp-{slug}/` — desatualizado desde lp-publicar v1.5.0). Detalhes operacionais redirecionam pra `landing-pages/CONTEXT.md` §4.
- **Refs "CONTEXT.md" agora sempre com path completo** nas skills lp-* (`landing-pages/CONTEXT.md` ou `.claude/skills/lp-preparar/CONTEXT.md`). Tira ambiguidade entre os dois CONTEXT.

#### Skills bumpadas
- `lp-gerar` 1.3.0 → 1.4.0 (cascata removida, snippet GTM removido, ref pro CONTEXT §5.1/§5.3)
- `lp-revisar` 1.2.0 → 1.3.0 (idem)
- `lp-publicar` 1.6.0 → 1.7.0 (anti-padroes removidos, ref pro CONTEXT §7)
- `landing-page` (advisor) 1.1.0 → 1.2.0 (Q1 enxuta, Fluxo Alterar delegado)
- Brand CONTEXT (`.claude/skills/lp-preparar/CONTEXT.md`) — sem campo version, mas reescrita

#### Skills nao tocadas neste round
- `lp-preparar` (carga ja correta em 1.1.0)
- `lp-integrar-form` (carga ja correta em 1.2.0; agora e fonte canonica do wrapper CSS)
- `lp-pipeline` (carga ja correta em 1.1.0)

### 1.6.0 — 2026-04-28
- **Novo `landing-pages/CONTEXT.md`** — runbook operacional unificado para todas as skills lp-*. Cobre: mapa mental (fonte-verdade vs sibling), fluxo padrao de LP nova, **matriz de alteracao pós-deploy** (§2.2 — "o que mudou → o que rodar", endereça problema recorrente do Victor de não saber qual skill rodar quando pede ajuste numa LP já viva), convenção unificada de assets/imagens (brand vs LP-local, paths source vs deploy, namespace solo vs guarda-chuva, formatos por tipo, regra do favicon, mascotes por marca), modos de deploy, cascata de detecção de região (deduplicada — antes em 3 skills), **troubleshooting** (sintoma → causa → solução cobrindo favicon 404, mascote 404, colisão de assets, CSP bloqueando form, GTM ausente/errado, FetchError CLI, smoke test divergente, sibling apagada/divergente, vazamento de path interno, conflito de domínio), anti-padrões documentados (linkados aos incidentes que motivaram cada versão), checklist pré-deploy, quando-não-usar-este-pipeline, e referências cruzadas. Complementar a `landing-pages/GUIDELINES.md` (que segue como regras de **design** — paleta, hero, motion, copy, seções-tipo, favicon §11). CONTEXT cobre o "como operar"; GUIDELINES cobre o "como deve ser".
- **Skills bumpadas** (todas adicionam `landing-pages/CONTEXT.md` ao Passo 0/1 de carga de insumos):
  - `lp-preparar` 1.0.0 → 1.1.0
  - `lp-gerar` 1.2.0 → 1.3.0
  - `lp-revisar` 1.1.0 → 1.2.0
  - `lp-integrar-form` 1.1.0 → 1.2.0
  - `lp-publicar` 1.5.0 → 1.6.0
  - `lp-pipeline` 1.0.0 → 1.1.0 (novo bloco "Contexto comum" que carrega GUIDELINES + CONTEXT antes da validação de argumentos; e detecção de pedido de alteração vs LP nova com redirect para CONTEXT.md §2.2)
  - `landing-page` (advisor) — adicionado `version: 1.1.0` ao frontmatter (não tinha versionamento antes); nova opção "Alterar LP existente" no Q1 + novo Fluxo: Alterar com sub-pergunta sobre o que mudou (copy/visual/asset/form/tracking/dominio) que dispara a skill correta conforme a matriz §2.2 do CONTEXT
- **Motivo (do Victor):** "toda vez que peço alterações numa LP, o agente tem dificuldade em deploy correto, em qual passo seguir quando é alteração, e em tratar imagens (logos, ilustrações, onde guardar, como evitar 404)". A exploração confirmou que a base é sólida mas o conhecimento operacional estava disperso em 6 SKILL.md + CHANGELOG + READMEs por LP. Agora 1 doc canonico e carregado pelas 6 skills cobre fluxo de alteração, assets e troubleshooting num lugar só.
- **Não-mudancas (intencionais):** `landing-pages/GUIDELINES.md` segue identico (regras de design não mudaram). `.claude/skills/lp-preparar/CONTEXT.md` segue como compartilhado para convenções de marca/IDs Notion (papel diferente do CONTEXT operacional recém-criado). LPs existentes em `landing-pages/{marca}/{slug}/` não foram tocadas. `brand/` não tocado.

### 1.5.0 — 2026-04-27
- `lp-publicar` (v1.5.0): novo **modo guarda-chuva** para LPs que compartilham domínio. Quando `[dominio]` é fornecido, o **Passo 0.5** consulta a API da Vercel (`GET /v9/projects?teamId=...`) checando se algum projeto já tem esse domínio nos aliases. Se sim, a skill anexa a LP nova como subpasta do sibling existente em vez de criar projeto novo. Comportamento default (modo solo) inalterado.
- **Namespace de assets por marca em multi-LP:** no modo guarda-chuva, paths são reescritos para `/assets/{marca}/X` em vez de `/assets/X`, evitando colisão de filename entre marcas (ex: Buzzmonitor e Buzzcreators têm ambos `logo-icon.png`). Source pode usar `../../brand/{marca}/...` ou `./assets/...` que a skill faz a conversão correta.
- **Validação de regressão zero (§2.4 + §3.4.b):** antes do deploy guarda-chuva, capture-se hash MD5 do `index.html` de cada LP vizinha (baseline). Pós-deploy, smoke test refaz o hash via URL pública — qualquer divergência aborta o relatório (algo da entrega quebrou vizinhas, investigar antes de publicar).
- **Não-sobrescrever `vercel.json` e `README.md` em modo guarda-chuva (§1.6 + §1.8):** o sibling já está configurado para multi-LP; sobrescrever pode mudar CSP/headers e quebrar form/script de vizinhas. Skill compara com template e avisa em vez de aplicar silenciosamente.
- **Anti-padrões documentados:** nova seção no fim do SKILL.md tabula 5 anti-padrões com motivo e quando aconteceram (criar projeto duplicado em vez de guarda-chuva, sobrescrever vercel.json, copiar asset com filename igual sem namespace, path relativo sobrando, misturar entregas no mesmo deploy).
- **Incidente que motivou:** 2026-04-27, LP Buzzcreators `vendendo-com-creators` foi inicialmente publicada em projeto Vercel separado (`buzzcreators-lp-vendendo-com-creators`) em vez de usar o guarda-chuva já existente para `webinar.buzzmonitor.com` (`buzzmonitor-lp-monitoramento-concorrentes`). Consolidação manual + 2 deploys + projeto órfão. v1.5.0 evita o cenário desde a primeira execução.

### 1.4.0 — 2026-04-27
- `lp-publicar` (v1.4.0): §1.3-1.5 reescritos para suportar **assets LP-locais** além de assets do `brand/`. Antes, §1.4 só sabia copiar de `brand/{marca}/assets/` — assets em `landing-pages/{marca}/{slug}/assets/` (ex: mascot específico de uma LP) não eram copiados ao sibling, e o redeploy quebrava. Agora classifica cada referência por padrão (`../../brand/...` → brand, `./assets/...` → LP-local, `/assets/...` → checa brand primeiro, senão LP-local) e copia da origem certa. §1.5 ganhou verificação obrigatória pós-rewrite (grep por `../assets/`, `./assets/`, `../../brand/` remanescente — se sobrar, aborta).
- **Fix:** LP `buzzmonitor/monitoramento-concorrentes-maio-2026` (BR + PT) com mascot.png 404 no live — caminho relativo `./assets/mascot.png` resolvendo para `/assets/mascot.png` (raiz vazia) por causa de `cleanUrls: true` + `trailingSlash: false` no Vercel. Path corrigido para absoluto, mascot levado pro sibling root e redeployado.

### 1.3.0 — 2026-04-23
- `lp-revisar` (v1.1.0): novo **Passo 3.5 — Auditoria de GTM (CRITICO)**. Resolve regiao via cascata (sufixo slug `-pt`/`-latam`/`-br` → `<html lang>` → fallback `brasil`), resolve GTM esperado em `tracking.json` e audita os 2 snippets no HTML. GTM ausente ou com ID errado vira CRITICO e eh corrigido automaticamente no Passo 4; caso "tracking.json null mas LP tem GTM" vira MELHORIA em `REVISAO.md`.
- `lp-gerar` (v1.2.0): Passo 1 agora detecta regiao explicitamente por cascata (sufixo slug → fallback `brasil`). Antes dependia de "briefing ou CTX regional", sem mecanismo deterministico — motivo pelo qual LPs PT recebiam GTM BR.
- `lp-integrar-form`: nota em `## Notas` delega auditoria de GTM para `lp-revisar` (Passo 3.5). Skill continua focada so em trocar form mock por embed real, sem auditoria duplicada.
- **Tracking.json atualizado com IDs reais por regiao:**
  - Buzzmonitor: BR `GTM-WFJVK858` (ja existia), LATAM `GTM-MKQBX2MG` (novo), PT `GTM-NCFT22CW` (novo).
  - Cxpress: BR `GTM-T4XDWHL3`, LATAM `GTM-WRQ47B9R`, PT `GTM-NW6V5KBM` (antes tudo `null`).
- **Cascata de deteccao de regiao documentada em CONTEXT.md:** sufixo do slug → `<html lang>` → fallback `brasil`. Fonte unica usada por `lp-gerar` e `lp-revisar`.
- **Fix:** LP `buzzmonitor/monitoramento-concorrentes-maio-2026-pt` estava com GTM BR (`GTM-WFJVK858`) em vez de PT (`GTM-NCFT22CW`) — bug causado pela regiao implicita antes desta versao. Trocado nos 2 lugares (script e noscript).

### 1.2.0 — 2026-04-20
- `lp-gerar` (v1.1.0): injeta automaticamente **Google Tag Manager** no HTML gerado, lendo o container id de `brand/{marca}/tracking.json` (`gtm.regions[{regiao}]` > `gtm.default`; se ambos `null`, omite).
- Novo arquivo canonico **`brand/{marca}/tracking.json`** — schema `tracking/v1` com `gtm.default` + `gtm.regions.{brasil,latam,portugal}`. Buzzmonitor preenchido (`GTM-WFJVK858` cobre BR/LATAM/PT); Cxpress/Buzzcreators/Elife ficam como stubs `null` ate IDs oficiais.
- `lp-publicar` (v1.2.0): novo passo 5.3 valida via `curl` que ambos snippets GTM (`<script>` + `<noscript>`) estao servidos na URL final. Relatorio Notion passa a listar GTM container e status `2/2 | 1/2 | 0/2`.
- LP `buzzmonitor/monitoramento-concorrentes-maio-2026` recebeu GTM injetado e foi redeployada.

### 1.1.0 — 2026-04-20
- `lp-publicar`: template `vercel.template.json` agora inclui header **Content-Security-Policy (CSP)** — cobre Jotform, RD Station, HubSpot, Google Fonts, GA/GTM, YouTube e Vimeo por default.
- `lp-publicar`: passo 1.6 documenta quando ajustar o CSP (scripts externos nao-default); passo 5.2 valida a presenca do header pos-deploy; relatorio Notion passa a listar 7 headers ativos.
- `lp-integrar-form`: novo passo 2.5 remove o JS placeholder do form quando se troca mock por embed real — evita `TypeError: Cannot read properties of null (reading 'addEventListener')` no console da LP publicada.

### 1.0.0 — 2026-04-18
- Familia nova de skills para automatizar criacao de LPs ponta-a-ponta: `lp-preparar`, `lp-gerar`, `lp-revisar`, `lp-integrar-form`, `lp-publicar`, `lp-pipeline` + advisor `/landing-page`.
- Marca-agnostica: funciona para Buzzmonitor, Buzzcreators, Cxpress e Elife.
- CONTEXT.md compartilhado em `.claude/skills/lp-preparar/CONTEXT.md`.
- `landing-pages/GUIDELINES.md` enriquecido com §8 (secoes-tipo), §9 (copy dita estrutura), §10 (integracao tardia de form).
- `lp-publicar` usa pasta sibling isolada + validacao de isolamento pre-deploy, PageSpeed Insights API pos-deploy e relatorio Notion.
- LPs existentes migradas para `landing-pages/buzzmonitor/{slug}/`.

## anuncios (advisor)
### 1.0.0 — 2026-04-14
- Reescrita completa: SKILL.md cortado de 156 para ~65 linhas (~58% menor).
- Removido step de confirmação (2 turnos LLM a menos por invocação).
- Adicionado fast-path: `/anuncios performance buzzmonitor_brl mes_atual` dispara em 1 turno.
- Removidas seções Princípios, Fallback e Passo 0 (aviso inline).

## escrever (advisor)
### 1.0.0 — 2026-04-14
- Reescrita completa: SKILL.md cortado de 206 para ~75 linhas (~64% menor).
- Removido step de confirmação. Adicionado fast-path para os 4 sub-fluxos.
- Removidas seções Princípios e Fallback.

## newsletter (advisor)
### 1.0.0 — 2026-04-14
- Reescrita completa: SKILL.md cortado de 122 para ~50 linhas (~59% menor).
- Removido step de confirmação. Adicionado fast-path.
- Removidas seções Princípios e Fallback.

## traduzir (advisor)
### 1.0.0 — 2026-04-14
- Reescrita completa: SKILL.md cortado de 122 para ~50 linhas (~59% menor).
- Removido step de confirmação. Adicionado fast-path.
- Removidas seções Princípios e Fallback.

---

## copy-criar
### 1.1.0 — 2026-06-02 — Doc de roteiro falado à câmera (Triângulo do Yap)
- **Novo doc de conhecimento** `conhecimento/copywriting/video-curto-talking-head.md`: estrutura da fala para vídeo de uma pessoa falando direto à câmera (Reels/TikTok/Shorts/UGC). Framework **T · MAES · A/N** (Tópico → Metáfora/Analogia/Exemplo/Story → Aplicação/Próximo passo), adaptado ao método da casa (Ladeira/Light Copy) e cruzado com `fundamentos-copy.md`, `video-curto-ads.md`, `video-curto-organico.md` e `funil-copy.md`. Inclui template, exemplo mapeado, anti-padrões e checklist.
- **Carregamento ligado:** Passo 1 (item 2) passa a ler o doc quando `tipo = video-curto`; Passo 4 (formato Video-Curto) instrui a estruturar o áudio pelo esqueleto T·MAES·A/N quando for talking head. Tabela de `CONTEXT.md` atualizada.
- Não-breaking: nenhum parâmetro ou saída mudou; só adiciona fonte e orientação.

### 1.0.0 — 2026-04-13
- Baseline após refactor `f580823` (eliminação de duplicação, criação de CONTEXT.md compartilhado).

## copy-pesquisar
### 1.0.0 — 2026-04-13
- Baseline após refactor `f580823`.

## copy-revisar
### 1.1.0 — 2026-04-27
- **Novo Passo 4.5 obrigatório — re-revisão sobre as próprias correções.** Disparado por feedback do Victor após revisão da Copy LP do evento Vendendo com Creators (Buzzcreators), onde a v2 publicada no Notion vazou 3 padrões de IA introduzidos *durante* a correção: (a) antítese-por-negação ("X, não Y") repetida 6× em ~400 palavras, (b) 6 em-dashes de ênfase em texto que tinha zero, (c) substitutos decorativos no lugar dos fillers removidos ("planilha mágica", "com achismo" para "de forma clara").
- O Passo 4.5 roda 4 contagens no texto **corrigido**: antítese-por-negação (max 2 / peça), **em-dash (tolerância zero — qualquer `—` no output vaza IA)**, substitutos decorativos (filler 2.0 — palavras que dão ritmo sem trazer info), ritmo sintático repetitivo (2+ frases consecutivas com mesma forma).
- Causa-raiz documentada: a skill antes terminava em "aplicar correções → apresentar resultado", sem loop sobre o output. Os erros de IA mais previsíveis são introduzidos *durante* o conserto (especialmente quando o revisor tenta dar "punch" no lugar de filler removido).
- Atualização paralela em `conhecimento/editorial/regras-anti-ia.md`: nova seção "Estruturas Viciadas" com 3 sub-regras (antítese-por-negação, **em-dash com tolerância zero**, filler 2.0); regra "de forma X" adicionada à lista de filler words; "Teste Final de Naturalidade" agora inclui re-checagem pós-correção como obrigatória; "Não é X, é Y" tirado da lista de frases (era específico demais) e absorvido pela nova regra estrutural mais ampla.
- **Em-dash com tolerância zero (decisão do Victor 2026-04-27):** "nenhum ser humano usa isso". Regra ficou absoluta — Ctrl+F por `—` no texto final, esperado 0 ocorrências. Substitutos: vírgula (pausa curta), ponto (pausa forte), parênteses (aparte), nova linha (atribuição de citação). Única exceção é separador de seção markdown `---` (três hifens, vira `<hr>`, não é em-dash).

### 1.0.0 — 2026-04-13
- Baseline após refactor `f580823`.

## copy-swipefile
### 1.0.0 — 2026-04-13
- Baseline após refactor `f580823`.

## meta-ads
### 1.0.0 — 2026-04-13
- Baseline: pipeline completo (fetch + report) consolidado após refactor `f580823`.

## meta-ads-fetch
### 1.0.0 — 2026-04-13
- Baseline após refactor `f580823`.

## meta-ads-report
### 1.0.0 — 2026-04-13
- Baseline após refactor `f580823`.

## meta-ads-trends
### 1.0.0 — 2026-04-13
- Baseline após commit `8eb3ca9` (diagnóstico cruzado, criativos de referência e métricas de vídeo).

## news-pipeline
### 1.0.0 — 2026-04-13
- Baseline após refactor `f580823`.

## news-pesquisar
### 1.0.0 — 2026-04-13
- Baseline após refactor `f580823`.

## news-gerar
### 1.0.0 — 2026-04-13
- Baseline após refactor `f580823`.

## news-revisar
### 1.0.0 — 2026-04-13
- Baseline após refactor `f580823`.

## trad-pipeline
### 1.0.0 — 2026-04-13
- Baseline após refactor `f580823`.

## trad-traduzir
### 1.0.0 — 2026-04-13
- Baseline após refactor `f580823`.

## trad-revisar
### 1.0.0 — 2026-04-13
- Baseline após refactor `f580823`.

## trad-calibrar
### 1.0.0 — 2026-04-13
- Baseline após refactor `f580823`.

## setup-agencia
### 0.1.0 — 2026-04-13
- Skill nova: guia interativo de primeiro setup (Python, Notion MCP, token Meta) para newbies. Acompanha `meta-ads/SETUP.md` e `meta-ads/scripts/check_setup.py`.

## meta-ads (módulo Python)
### 2026-04-13
- IDs das 6 contas hardcoded em `cache_manager.py` (`ACCOUNTS[*]["account_id"]`); `get_account_id` simplificado. `.env.example` reduzido a token + data + API version (de 36 para ~24 linhas, sem `META_ACCOUNT_*`).
- `scripts/check_setup.py` novo: valida `.env`, expiração do token e acesso a cada uma das 6 contas via `AdAccount.api_get`. Exit 0/1.
