# LP Cxpress — planos

**Gerado em:** 2026-08-27
**Copy-fonte:** `copy.txt` (output de `/lp-preparar`)
**Notion (copy):** https://app.notion.com/p/3c93934026fd81668a43f8a4b64f04a1
**No ar em:** https://content.cxpress.io/planos (guarda-chuva migrado pro CI)
**Relatorio de entrega:** https://app.notion.com/p/3c93934026fd8183a186c020d7a12937
**Form provider:** Jotform `261034073026647` (integrado em 2026-08-27). Mesmo formulário da LP
`institucional`; a página de agradecimento é config do Jotform, não do embed. Trocar = 1 linha
via `/lp-integrar-form`.

Página de pricing da Cxpress no Brasil. Dois planos: **Basic** (a plataforma completa,
a partir de R$ 1.290/mês com 5 acessos de operador) e **Enterprise** (tudo do Basic mais
canais, agentes de IA, escala, integrações e serviços gerenciados com a Elife, com
precificação sob demanda).

## Fonte do conteúdo

| Bloco | Fonte |
|---|---|
| Pacote de entregas do Basic + valor mensal + 5 operadores | planilha de proposta comercial Cxpress (print enviado no chat, 2026-08-27) |
| Itens do Enterprise (TikTok, GMB, agentes extras, Concierge, Voice Agent, integrações) | linha "Incrementos estratégicos" da mesma planilha + lista de recursos adicionais enviada no chat |
| Serviços gerenciados com a Elife | lista enviada no chat (criação/gestão de agentes, gestão de qualidade, equipe humana, social listening) |
| Estrutura visual (fontes, paleta, botões, footer, reveal on scroll) | `landing-pages/cxpress/institucional/` |
| Distribuição de informação (cards + tabela comparativa + FAQ) | referência pedida: octadesk.com/precos |

### Decisões de conteúdo registradas

- **Preço do Basic:** "A partir de R$ 1.290 por mês", com nota de que o valor corresponde ao
  pacote de 5 acessos. A fala do briefing mencionava também "a partir de 990 com 3 licenças";
  prevaleceu a instrução final ("para o plano basic considerar primeira imagem"), que traz
  R$ 1.290,00 / 5 operadores humanos.
- **Preços unitários dos incrementos ficaram fora da página** (R$ 120 por operador, R$ 300 por
  agente de IA, R$ 300 por Concierge, R$ 100 por número, R$ 1.290 por Voice Agent). O Enterprise
  foi definido como precificação sob demanda, então esses valores seguem com o comercial.
- **Nada de "sem fidelidade / cancele quando quiser"** — o item aparece riscado na referência
  visual enviada, então não entrou em nenhuma forma.
- **Central telefônica no plano base:** o Basic declara o canal de telefone com URA inteligente
  (encaminhamento de chamados), como na planilha. A IA de voz (Voice Agent) fica no Enterprise.
  Isso resolve o item sublinhado na referência visual.
- **Sem seção de urgência/escassez** (GUIDELINES §8). Página de pricing perene não tem escassez
  real; inventar uma seria copy fora da fonte.

## Estrutura

1. **HERO** — logo, overline, H1, subtítulo, CTA duplo (`#planos` e `#proposta`), faixa de 8 canais
2. **PLANOS** (`#planos`) — H2 + subtítulo + 2 cards (Basic branco com borda royal, Enterprise em gradiente escuro) + nota de rodapé do valor
3. **COMPARATIVO** — tabela item por item, 7 grupos (Canais, IA e automação, Dados e CRM, Gestão e operação, Serviços gerenciados, Suporte, Investimento)
4. **PROVA** — faixa de clientes (desktop e mobile)
5. **PERGUNTAS** — FAQ com 6 itens em `<details>` nativo
6. **PROPOSTA** (`#proposta`) — embed do Jotform + 3 bullets do que o lead recebe
7. **FOOTER** — igual ao da LP institucional

## Estado

- [x] HTML gerado
- [x] OG image 1200×630 → `assets/og-planos.png` (arquivo único, sem `og-image.png`)
- [x] Revisão aplicada — ver `REVISAO.md`
- [x] Formulário integrado — Jotform `261034073026647` (2026-08-27)
- [x] Publicado em https://content.cxpress.io/planos (2026-08-27, PR #389, run 33084579231)

## Desvios deliberados das GUIDELINES

Todos motivados pelo briefing "100% baseada na estrutura da página institucional":

| Regra | Desvio | Motivo |
|---|---|---|
| §2 (respiro mín. 120px desktop) | seções com 80px | é o ritmo da LP `institucional`, que esta página precisa espelhar para as duas lerem como o mesmo site |
| §1 (alternar branco ↔ neutral-100) | usa também o lilás `#D7E2FF` na seção de planos | mesmo tint de marca já usado na `institucional`; a paleta segue com 3 cores (royal, navy, lilás) e 1 gradiente |
| §3 (hero texto à esquerda + visual à direita) | hero centralizado | idem `institucional`, que tem hero centralizado |
| Passo 3 do `lp-gerar` (invocar `frontend-design`) | HTML escrito reaproveitando o CSS da `institucional` | o pedido era clonar a estrutura existente; gerar design novo produziria outra linguagem visual |
| §17 (logo no header) | não há header (sem menu) | a `institucional` teve o header removido a pedido; o logo abre a home regional a partir do hero |

## Assets referenciados

Brand:
- `../../brand/cxpress/assets/logos/logo-icon.png` (favicon)

LP-local (`./assets/`, todos portados da LP `institucional`):
- `logo-header-1.png` (logo do hero)
- `Group-1707478254.png` (check verde de item incluído)
- `icon-home-2-2.png`, `icon-home-2-3.png`, `icon-home-2-4.png`, `icon-home-2-5.png`, `icon-home-2-7.png`, `icon-home-2-8.png`, `icon-facebook.png`, `icon-wechat-2-1.png` (faixa de canais)
- `Clientes_Cxpress.webp` (clientes, desktop) e `Group-1707478259.png` (clientes, mobile)
- `Cxpress_icons_social-scaled.png`, `icon-footer-1.png`, `whatsapp-icon.png`, `imgi_1_3433378_1_176476463169302bd7a5301467666886-1.png` (footer)
- `og-planos.png` + `og-template.html` + `render_og.py` (OG image)

## Validação

- em-dash: `grep -c "—" index.html` = **0**
- SEO: 1 description, 10 `og:`, 4 `twitter:`, 1 JSON-LD (parseia), canonical com `{{DOMAIN}}`
- `check_gtm_region.py`: 1 OK, 0 bloqueios (GTM-T4XDWHL3, brasil)
- `bump_mobile_type.py`: aplicado (11 regras px no mobile)
- `check_mobile_type.py` a 375px: `h1=34 corpo=16 min=14`, único achado de overflow é o
  `.skip-link` em `left:-9999px` (fora de tela por construção, mesmo achado da `institucional`)
- imagens sem `alt`: 0 · form: embed Jotform no wrapper canônico `.jotform-embed`
