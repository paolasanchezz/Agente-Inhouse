# Dashboard Content Marketing Cxpress Brasil — dinâmica (LOCAL)

Versão **interativa** do dashboard de Content Marketing da Cxpress, com **seletor de data**
(presets 7d/15d/30d/90d/MtD/YtD + intervalo livre) e consulta ao Supabase **ao vivo**.

> **Por que local?** O Vercel não consegue conectar no Supabase com o user `looker_readonly`
> (pooler IPv4 — mesmo motivo da `dashboard-pessoal` e da `dashboard-latam`). Então esta versão
> roda **na sua máquina**. A versão **publicada** (snapshot semanal estático, sem seletor) fica
> em `dashboard/relatorio-semanal-cxpress-brasil.html` → sibling Vercel (ver `dashboard/DEPLOY-cxpress.md`).
> As duas usam o mesmo visual/critério.

## Como rodar

```bash
uv run --python 3.12 --with "psycopg[binary]" python dashboard-cxpress/server.py
# abre http://127.0.0.1:8020
```

(ou pelo `/run` / preview do Claude Code — config `dashboard-cxpress` no `.claude/launch.json`)

## Como funciona

- `server.py` serve a **shell** (barra com presets + date-picker) em `/` e um endpoint
  `/render?preset=…` ou `/render?ini=YYYY-MM-DD&fim=YYYY-MM-DD`.
- O `/render` **reaproveita o `render_html` do dashboard estático** (`dashboard/gerar_relatorio_cxpress.py`)
  para o período escolhido — mesmos blocos, funil de 6 etapas + Perdido, PT-BR, BRL. O seletor troca o
  conteúdo via `fetch` (iframe `srcdoc`), sem recarregar a página.
- **Cache em memória** por intervalo (botão ↻ ignora o cache e re-consulta o banco).
- Lê `SUPABASE_PG_URL` de `dashboard/.env` (read-only).

## Funil (mesma estrutura do BR/LATAM, etapas da Cxpress)

Lead → **Triagem → Agendamento → Demo realizada** → Proposta → Fechamento (+ Perdido).
Fonte: `cxpress_deals_funil_principal_prod`. Escopo = **só o filtro de canal CM** (funil_auto NÃO
filtra — AC marca leads de mídia como Outbound; mesma decisão do Buzz BR): exclui Google Ads,
whatsapp, youtube e inscrições de webinar; inclui Meta/IG/FB/LinkedIn/Email/Blog/TikTok/Newsletter/
Linktree + LP `atendimento-para-clinicas` + `content.cxpress.io`. Critério completo em
`dashboard/MAPEAMENTO-CAMPOS-cxpress.md` §2.

**Baseline YtD 2026 (2026-06-09):** 490 leads · 35 triagem · 21 agend · 18 demo · 12 propostas ·
5 fechamentos · 419 perdidos (coorte: criados no período e perdidos, igual Buzz BR). 15d = 9 leads,
batendo com o Meta Ads. Nome do deal linka pro AC (`elife.activehosted.com/app/deals/{id}`).

## Limitações / pendências (ver `dashboard/MAPEAMENTO-CAMPOS-cxpress.md`)

- **Datas das etapas** vêm como texto ISO do ActiveCampaign (lidas via `_d()`); confirmadas em 2026-06-06.
- **Escopo:** Inbound + Content Marketing calibrado (decisão Victor 2026-06-09).
- **Sem dedup por pessoa** (a tabela não tem e-mail) — conta por deal.

Nada aqui depende de deploy — é uso interno local.
