# Revisao LP — buzzmonitor/black-friday-alta-performance-outubro-2026

**Data:** 2026-08-27
**Auditores:** frontend-design (review mode) + web-design-guidelines (Vercel Web Interface Guidelines)

> ⚠️ **Nota (2026-08-27, mesma data):** este relatório auditou o design "corporativo" original. Logo em seguida o usuário pediu para reaproveitar a estrutura de `buzztalk-gestao-multimarcas-para-agencias` com a identidade visual da série **Buzzconnect**, o que resultou numa reescrita completa do `index.html` (paleta, tipografia, componentes). Os 6 críticos abaixo **já vêm corrigidos nativamente** no HTML redesenhado (verificado por checagem de contraste WCAG feita durante a própria criação, documentada no `README.md`), mas essa passada específica (`frontend-design` review + `web-design-guidelines`) **não foi re-executada formalmente** sobre o novo HTML. Antes de publicar, considerar rodar `/lp-revisar` de novo para uma auditoria independente do design atual — o conteúdo abaixo fica só como histórico do que foi encontrado e corrigido na primeira versão.

## Aplicado automaticamente (6 críticos)

- [x] **Contraste AA no botão laranja** — `.btn--primary` tinha texto branco sobre fundo `#EB7C2E` (contraste ~2,8:1, abaixo do mínimo 4,5:1 da GUIDELINES §7; mesmo achado já documentado na LP irmã `buzztalk-gestao-multimarcas-para-agencias`). Trocado o texto para roxo escuro `var(--purple-deep)` (~6,5:1); hover inverte para roxo + texto branco.
- [x] **Gradiente de fundo na seção CTA final quebrava contraste** — `.cta-final` usava `linear-gradient(135deg, roxo, laranja)` com texto branco por cima; na ponta laranja o contraste caía para ~2,5-2,8:1 (falha AA). Também violava GUIDELINES §1 ("gradiente... não em fundo de seção"). Trocado para fundo sólido `var(--purple)` (mesmo perfil de contraste já validado na seção Urgência, 11-12,5:1).
- [x] **Laranja da marca como texto pequeno falhava AA** — `.wheel-item__index` (índice "01"-"06" da seção Visão 360) e `.timeline__time` (horários da Programação) usavam `var(--orange)` como cor de texto sobre fundo claro (contraste 2,56-2,82:1). Criada variante `--orange-text: #a44b3e` (laranja escurecido em direção ao roxo da marca, 4,75-5,75:1 conforme fundo) e aplicada nos dois seletores.
- [x] **3 kickers duplicando o H2 imediatamente abaixo (bug de conteúdo)** — nas seções Aprendizados, Palestrantes e Programação havia um `<span class="eyebrow">` repetindo literalmente o mesmo texto do `<h2>` logo abaixo (ex.: "O que você vai aprender" duas vezes seguidas). Removidos os 3 spans; ficou só o H2.
- [x] **Sticky header cobria o alvo do CTA principal** — os 4 CTAs "Quero participar" da página (navbar, hero, aprendizados, urgência) rolam até `#form`; sem compensação, o navbar `position:sticky` (~64-72px) cobria o topo dessa seção (headline + início do form) após o scroll, no destino do principal fluxo de conversão da LP. Adicionado `scroll-margin-top:88px` em `#form`.
- [x] **Ícones decorativos do footer sem `aria-hidden`** — os 2 SVGs de Instagram/LinkedIn no footer não tinham `aria-hidden="true"` (regra explícita da Web Interface Guidelines). Adicionado nos dois (o `aria-label` continua no `<a>` pai).

## Melhorias opcionais (6)

Para o usuário decidir. Aplicar via Edit manual ou pedir `/lp-revisar` novamente.

- [ ] **Contador regressivo sem `font-variant-numeric: tabular-nums`** — os 4 números do countdown (dias/horas/min/seg) trocam a cada segundo; sem largura tabular, os dígitos podem "tremer" 1px a cada troca. `.countdown__num { font-variant-numeric: tabular-nums }`.
- [ ] **`urgencia__cta-line` renderizado como `<p>`, mas copy.txt rotula como H3** — "Participe do evento e prepare sua estratégia..." está semanticamente marcado como H3 na copy estruturada; no HTML virou parágrafo estilizado (visualmente igual, mas não entra na árvore de headings pra navegação por leitor de tela). Trocar a tag para `<h3>` se quiser alinhar 100% com a estrutura da copy.
- [ ] **Email do form sem `spellcheck="false"`** — campo `#f-email` (Web Interface Guidelines: desabilitar spellcheck em e-mail/código/usuário).
- [ ] **`<meta name="theme-color">` ausente** — poderia casar com o fundo do header (`rgba(255,255,255,.9)` → branco) para polish da barra do navegador mobile.
- [ ] **Textos "Buzzmonitor" sem `translate="no"`** — proteção leve contra auto-tradução malformada em navegadores que traduzem a página.
- [ ] **`inputmode="tel"` ausente no campo WhatsApp** — `type="tel"` já sugere teclado numérico na maioria dos navegadores, mas `inputmode` reforça.

## Nice-to-haves (3)

Estilístico. Ignorar é aceitável.

- [ ] `&nbsp;` entre "14h" e "às 18h" e entre "Paulista" e "807" no ticket do hero, pra evitar quebra de linha no meio da frase no card estreito.
- [ ] `.contato__mail` poderia ganhar um estado `:hover` com leve variação de cor além do sublinhado já existente.
- [ ] Seção Palestrantes com card tracejado + avatar genérico funciona bem como placeholder; quando os palestrantes forem confirmados, migrar para o layout "prova social" padrão da GUIDELINES §8 (foto circular à esquerda, nome + cargo à direita).

## Auditorias determinísticas

- **GTM/região** (`check_gtm_region.py`): `status: ok` — container `GTM-WFJVK858` bate com região `brasil` (`<html lang="pt-BR">`). Selo `.tracking.lock` gravado.
- **Fidelidade de copy**: nenhum vazamento encontrado após os ajustes feitos durante a geração (kicker duplicado tratado acima como crítico de conteúdo). Zero em-dash (`—`/`&mdash;`) no HTML.
- **SEO** (§15): 1 description, 1 robots, 10 `og:*` (≥8), 4 `twitter:*` (≥4), 1 JSON-LD válido (`Organization`, `WebPage`, `Event`). `Organization.url` e `sameAs` batem com `brand-manifest.json`.
- **Multi-idioma** (§16): LP única, sem irmãs — hreflang omitido corretamente, canonical presente.
- **Logo regional** (§17): header e footer apontam para `https://buzzmonitor.com/` (não `"/"`), `target="_blank" rel="noopener"` presentes.
- **Logo web-safe** (§19): `logo-primary.svg` e `logo-reversed.svg` sem `<text>` vivo — OK.
- **OG image** (§18): ainda **pendente** — `assets/og-black-friday-alta-performance-outubro-2026.png` não existe (já rastreado no README, não é bloqueador desta revisão).

## Próximos passos

- Design aprovado? → `/lp-integrar-form buzzmonitor/black-friday-alta-performance-outubro-2026 "<snippet>"`
- Gerar OG image 1200×630 antes de publicar.
- Confirmar palestrantes reais (bloqueador documentado no README) antes de ir ao ar.
- Rever mais alguma melhoria acima? → editar manualmente ou rodar `/lp-revisar` novamente.
