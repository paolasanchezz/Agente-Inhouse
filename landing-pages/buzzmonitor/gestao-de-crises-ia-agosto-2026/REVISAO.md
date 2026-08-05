# Revisao LP — buzzmonitor/gestao-de-crises-ia-agosto-2026

**Data:** 2026-07-23
**Auditores:** frontend-design (review mode) + web-design-guidelines + auditoria GTM/SEO/copy do lp-revisar

## Aplicado automaticamente (11 criticos)

- [x] 12 em-dashes (`—`) no HTML (meta description, og:description e 10 comentarios) — linhas 16, 18, 241, 358, 378, 531, 610, 668, 670, 764, 771, 778 (numeracao pre-fix) — substituidos por virgula/dois-pontos conforme a funcao (tolerancia zero, `regras-anti-ia.md`)
- [x] SEO incompleto: faltavam `meta robots`, `canonical`, 7 tags `og:` (site_name, locale, url, image, image:width/height/alt), 4 tags `twitter:` e o bloco `JSON-LD` inteiro — pacote completo adicionado no `<head>` (Organization + WebPage + Event, seguindo o padrao de `webinar-diversidade-2026`)
- [x] OG image ausente — gerada `assets/og-gestao-de-crises-ia-agosto-2026.png` (1200x630, via `assets/og-source.html` + Playwright headless) no padrao visual das demais LPs de webinar Buzzmonitor
- [x] Logo do header linkava para `https://getbuzzmonitor.com.br/`, divergente de `brand/buzzmonitor/brand-manifest.json#regions.brasil.home` (`https://buzzmonitor.com/`) — corrigido pra apontar pro manifest
- [x] Logo do footer sem link (`<img>` solto) — envolvido em `<a href="https://buzzmonitor.com/" target="_blank" rel="noopener">` conforme GUIDELINES §17
- [x] Contador regressivo (`.box-countdown`) usava `role="timer" aria-label="..."` sem `aria-hidden` — exatamente o anti-padrao documentado em GUIDELINES §7 (contador que atualiza a cada segundo expondo pra leitor de tela). Trocado por `aria-hidden="true"` — a data ja vive no hero e no JSON-LD
- [x] Contraste AA: `.urgency .tag` (texto branco sobre `--grad-hot`) reprovava no extremo laranja do gradiente (~2.8:1, abaixo do minimo 3:1 pra texto grande) — trocado pra `var(--c-n900)` (texto escuro), que passa nas duas pontas do gradiente (~4:1 e ~6.6:1)

## Melhorias opcionais (3)

Para o usuario decidir. Aplicar via Edit manual ou pedir `/lp-revisar` novamente.

- [ ] **H1 do hero abre pela solucao, nao pela dor** (`Gestão de Crises com IA.`) — GUIDELINES §3/§5 preferem H1 nomeando a dor e H2/sub carregando a promessa. A dor aparece no `hero-sub` ("A proxima crise... ja esta sendo escrita nas redes"). Postura conservadora do anti-IA: sinalizar, nao reescrever o tom sem aprovacao de quem assina a copy.
- [ ] **Ordem narrativa**: secao "Diferencial" (`O conceito`) aparece antes de "O que voce vai levar" (Programa); GUIDELINES §6 sugere Oferta/Programa antes de Diferencial. Pode ser decisao intencional de copy (estabelecer o conceito antes do programa) — nao e uma inversao grosseira, so diverge do default.
- [ ] **Contraste do punchline gradiente** (`.punchline .big`, texto com `background-clip: text` no `--grad-hot`) fica abaixo de AA (~2.6-2.7:1) na ponta laranja do gradiente contra o fundo off-white. Esse e um padrao de assinatura visual repetido em varias LPs do repositorio (nao exclusivo desta) — recomendo tratar como decisao de design system (avaliar trocar o gradiente ou adicionar `text-shadow`/contorno), nao um fix isolado nesta LP.

## Nice-to-haves (2)

Estilistico. Ignorar e aceitavel.

- [ ] Titulo da secao "Diferencial" usa `<h3 id="diff-title">` enquanto as demais secoes usam `<h2>` pro titulo principal — pequena inconsistencia semantica de hierarquia (nao quebra leitura, so estilo).
- [ ] Classe `.hero-h2 .ital` definida no CSS mas nao utilizada em nenhum lugar do HTML — codigo morto cosmetico.

## Notas

- **Copy fidelity (Passo 3.6):** sem `copy.txt` na pasta — auditoria de fidelidade literal contra fonte pulada (fonte original ja nao existe mais, LP herdada do `ia-no-sac-agosto-2026` com pivot de tema). Em-dash e SEO auditados normalmente (independem de copy.txt).
- **GTM:** ja estava correto (`GTM-WFJVK858`, batendo com `brand/buzzmonitor/tracking.json#regions.brasil`). Nenhuma acao necessaria.
- **Hreflang:** LP sem variantes em outro idioma (nenhuma `-es`/`-pt` irma) — omissao de hreflang esta correta.
- **Form:** ja integrado (Jotform `252154974852667`, mesmo provider usado em `webinar-diversidade-2026`), wrapper CSS canonico, sem JS placeholder residual. Nenhuma acao necessaria.

## Proximos passos

- Design aprovado? -> Rodar `/lp-publicar buzzmonitor gestao-de-crises-ia-agosto-2026 webinar.buzzmonitor.com`
- Rever mais algum critico? -> editar e rodar `/lp-revisar` novamente
