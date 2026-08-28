# LP Cxpress — whatsapp-business

**Gerado em:** 2026-08-28
**Copy-fonte:** `copy.txt` (briefing colado pelo Victor + restauração pontual da LP irmã `whatsapp-business-smb`)
**Região:** brasil (pt-BR) · **Domínio alvo:** `content.cxpress.io` (guarda-chuva migrado pro CI)
**Form provider:** Jotform `261027639617663` (compartilhado com a LP irmã `whatsapp-business-smb`) — integrado em 2026-08-28

## Estrutura

1. Hero — categoria + H1 (variante B, ganho operacional) + subtítulo + CTA duplo + tela real do produto
2. Prova rápida — 2 métricas (85% de redução de SLA · +220% de interações) + grade de logos
3. Dores — lista vertical com X vermelhos, 5 itens (GUIDELINES §8)
4. Plataforma — 5 funcionalidades alternando lado, cada uma com a tela real correspondente
5. Integrações — 7 chips (HubSpot, Buzzmonitor, RD Station Marketing, Pipedrive, TOTVS, ActiveCampaign, Jira)
6. Quem somos — faixa escura (única da LP), 2 parágrafos + badges API oficial WhatsApp / ChatGPT / elifegroup
7. CTA final — embed do Jotform + WhatsApp + e-mail comercial
8. FAQ — acordeão `<details>` com 4 perguntas
9. Footer

Ordem conforme o template modular do guia: Hero → Prova rápida → Dores → Como funciona → Integrações → CTA → FAQ.

## Estado

- [x] HTML gerado (`index.html`, 978 linhas, 52 KB)
- [x] OG image 1200×630 → `assets/og-whatsapp-business.png` (arquivo único, sem `og-image.png`)
- [x] Revisão (frontend-design + web-design-guidelines + auditorias determinísticas) → `REVISAO.md`, 10 críticos aplicados
- [x] Conteúdo aprovado (copy das dores + decisões das 5 lacunas)
- [x] Formulário integrado — Jotform `261027639617663` (embed `jsform`), 28/08
- [ ] Publicado — rodar `/lp-publicar cxpress whatsapp-business content.cxpress.io`

## Tracking

| Item | Valor |
|---|---|
| GTM | `GTM-T4XDWHL3` (Cxpress brasil, de `brand/cxpress/tracking.json`) — `<head>` + `<noscript>` |
| GA4 | **Sem `gtag.js` no HTML.** Decisão do Victor em 2026-08-28: o GA4 é disparado pela tag configurada dentro do container GTM. Hardcodar um segundo snippet duplicaria a contagem de pageview. |
| Gate de CI | `check_gtm_region.py` → `status=ok`, selo `.tracking.lock` gravado |

Se um dia esta LP precisar de um GA4 próprio fora do GTM, o padrão está na `evite-banimento-whatsapp` (que usa container e GA próprios por briefing específico, com selo de grandfathering).

## Assets referenciados

**Brand (`../../brand/cxpress/assets/`)**
- `logos/logo-primary.svg` — navbar (validado §19: 0 `<text>`, vetor outline)
- `logos/logo-reversed.svg` — footer (idem)
- `logos/logo-icon.png` — favicon
- `plataforma/clientes-cxpress.png` — grade de logos de clientes

**LP-local (`./assets/`)**
- `telas/tela-tickets.svg` — hero (painel de tickets)
- `telas/tela-chatbot-whatsapp.svg` — feature 01 (IA)
- `telas/tela-distribuicao.svg` — feature 02 (tickets por setor)
- `telas/tela-canais.svg` — feature 03 (canais integrados)
- `telas/tela-principal.svg` — feature 04 (cadastro unificado)
- `telas/tela-dashboard.svg` — feature 05 (dashboards)
- `onda-decorativa.png` — ornamento do hero (da home atual)
- `elife-logo-badge.png` — badge "elifegroup"
- `og-whatsapp-business.png` + `og-template.html` + `render_og.py`

## Formulário

Embed `jsform` do Jotform `261027639617663`, o mesmo da LP irmã `whatsapp-business-smb`, dentro de `<div class="jotform-embed reveal">` com o wrapper CSS canônico da skill (sem padding/borda/fundo próprios: o Jotform já traz card).

**O mock de 2 etapas foi removido junto**, com todo o CSS e JS dele (a LP encolheu de 978 para 797 linhas). O que o form real entrega, medido no embed ao vivo:

| Campo do Jotform | Cobre o quê do guia §4 |
|---|---|
| Seu nome · Sua empresa · Seu e-mail da empresa · Seu WhatsApp | Etapa 1 (captura) completa |
| Site da empresa | Extra — casa com o pré-requisito da FAQ ("ter um site ativo") |
| O que você gostaria de resolver na sua operação? | Etapa 2: maior dor |
| Quantidade de colaboradores | Etapa 2: porte da empresa |
| (não tem) | Etapa 2: principal canal · volume de atendimentos/mês |

Ou seja, o form compartilhado já qualifica quase tudo. Faltam só 2 dos 8 campos que o mock tinha, e ele ainda traz opt-out de newsletter e dois CTAs de saída (Falar pelo WhatsApp / Receber uma ligação). Se um dia quiserem os 2 campos que faltam, é edição no Jotform, não na LP.

**Telas não usadas** (copiadas mas sem lugar na copy atual, disponíveis se algum bloco novo entrar): `tela-agentes.svg`, `tela-disparo-ativo.svg`.

### Nota sobre os SVGs de tela

Os arquivos vieram de `D:\Elife\174 - LP ClaudeCode\03 - App WhatsApp\telas\` (export Figma de 2023). Cada um tinha de 1 a 4 nós `<text>` vivos com `font-family="Montserrat, ..."` **sem fallback genérico** — em navegador sem Montserrat instalada isso cai na fonte serifada padrão, e rótulos como "Email:" a 32px na tela de canais sairiam serifados (mesma armadilha do GUIDELINES §19, aqui aplicada a screenshot em vez de logo).

Corrigido na cópia local: cada `font-family` ganhou `Open Sans, Helvetica, Arial, sans-serif` no fim da pilha. Renderização validada com Chrome headless antes de entrar na LP. **Se estes SVGs forem re-exportados do Figma, refazer o patch.**

## Decisões de conteúdo que precisam do seu aval

Estão detalhadas em `REVISAO.md`. Em uma linha cada:

1. **Copy das 5 dores: APROVADA em 28/08.** Escrita nesta sessão sob o protocolo (fundamentos + anti-IA), não veio do briefing. Texto integral no `REVISAO.md`.
2. **Atribuição dos 2 números (85% de SLA, +220% de interações): adiada em 28/08**, por decisão do Victor. Vão ao ar sem nota de fonte. Não é bloqueante; quando quiser resolver, é uma linha de nota abaixo dos cards.
3. **Perguntas do FAQ foram restauradas** da LP irmã `whatsapp-business-smb` (transcrição da página viva), casando resposta por resposta — o briefing trouxe as respostas com os títulos como "[Inserir Pergunta N]". Você aprovou antes da geração.
4. **Descrições das 5 funcionalidades** também vieram da irmã pelo mesmo motivo (o briefing só trouxe os títulos). Nada inventado.
5. **Bloco "Casos de uso" adiado** para uma 2ª rodada, por decisão sua. Entra entre a plataforma e as integrações sem mexer no que já existe.

### Decisões registradas em 2026-08-28

| Lacuna | Decisão | Status |
|---|---|---|
| Dores resolvidas | (b) eu escrevo, você aprova | **Aplicada e aprovada** |
| Headline do hero | Variante B (ganho operacional) | Aplicada |
| Prova com números | (b) métricas próprias | **Aplicada**; atribuição adiada de propósito |
| Casos de uso | Adiar | Pendente, 2ª rodada |
| Integrações | 7 sistemas informados | Aplicada |
