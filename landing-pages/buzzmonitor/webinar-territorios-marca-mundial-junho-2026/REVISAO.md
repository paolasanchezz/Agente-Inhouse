# Revisao LP — buzzmonitor/webinar-territorios-marca-mundial-junho-2026

**Data:** 2026-07-17
**Auditores:** varredura GTM (local, 27 LPs do dominio) + frontend-design (review mode) + web-design-guidelines

## Aplicado automaticamente (5 fixes seguros)

- [x] **GTM com ID errado** — linhas 12 + noscript — `GTM-MKQBX2MG` (latam) -> `GTM-NCFT22CW` (portugal). Regiao pt-PT (cascata §5.1) x `tracking.json`.
- [x] **Motion a11y** — `.nav-meta .dot::after` (linha 319) agora entra no bloco `@media (prefers-reduced-motion: reduce)`. Era a unica animacao infinita sem fallback.
- [x] **Contraste** — `.punchline .line` (linha 401) `--c-n500` -> `--c-n700`. "A realidade e esta:" passa a cumprir AA sobre fundo n100.
- [x] **HTML invalido** — removido `</div>` orfao (ex-linha 984, residuo do bloco countdown apagado na edicao pos-evento). `<main>` continua balanceado.
- [x] **Anti-IA** — 2 em-dashes em comentario (CSS linha ~773 + JS ~1303) -> hifen. Gate objetivo `grep -c "—"` agora = 0.

## Criticos que EXIGEM decisao (nao aplicados — estrutural/marca/conteudo)

- [ ] **Funil pos-evento contraditorio** (CONTEUDO/NEGOCIO). O ticket do hero diz "Evento encerrado -> Ver proximos webinars" (linha 974-978), MAS o botao primario do hero diz "Quero inscrever-me" -> `#inscricao` (965), e a secao `#inscricao` (987-1005) ainda vende inscricao ao vivo de um evento que ja passou (25/jun, hoje 17/jul): "Inscricao gratuita", "25 de Junho · 15:00", "A inscricao garante o acesso a transmissao em direto", + **Jotform ativo** (`261127236463050`). Precisa de direcao: alinhar tudo ao proximo webinar (como o ticket ja faz) / oferecer gravacao / manter form pra proxima sessao? Ao reworkar, escurecer tambem a data laranja "25 de Junho" (`.final .when b`, ~2.6:1, reprova AA).
- [ ] **Contraste do botao primario** (MARCA). Branco sobre `--c-accent` `#EB7C2E` ≈ 2.8:1 — reprova AA em TODOS os CTAs. E a cor de botao da marca, entao vale pras 26 outras LPs tambem; e decisao de brand/GUIDELINES, nao fix de 1 pagina. O `:hover` ja vira roxo (passa); o problema e o estado padrao.

## Melhorias (opcional — nao aplicadas)

- [ ] Eyebrows accent-2 (`#DE2451`) em texto pequeno sobre n100 ~4.3:1 (borderline AA) — §7.
- [ ] 3 secoes n100 seguidas (`.problem`/`.different`/`.final`) sem alternancia branco↔n100 (§1/§2).
- [ ] CSS/JS morto da versao pre-evento: countdown, `.form` (679-709, form real e Jotform), `.play-orb`, acordeao `.gv-*`, `.ticket-date/-rows`, `.tz-chip .flag/.country`, classe `.section-h2`. Podar reduz peso.
- [ ] Card unico de "proximos webinars" estica p/ 880px — limitar largura ou centralizar.
- [ ] `scroll-behavior: smooth` incondicional (131) — envolver em `@media (no-preference)`.
- [ ] Fotos dos speakers (1164/1170/1176) e imgs do mural sem `width`/`height` — add dimensoes (CLS).
- [ ] `.mural-track` (marquee) sem controle de pausa (mitigado por reduced-motion).
- [ ] Jotform sem fallback `<noscript>` (entangled c/ pos-evento).
- [ ] `.check-emoji` com `drop-shadow` teal fora da paleta (507).

## Nice-to-have

- [ ] Fallback da display font e serif (Georgia) — usar sans na stack (111).
- [ ] Texto `background-clip:text` sem `color` solida de fallback (§4).
- [ ] Speakers em cards verticais vs layout horizontal (§8); logo repetido 3x sob speakers.
- [ ] `color-scheme` nao declarado; `preconnect` p/ GTM + Jotform ausente.
- [ ] E-mail footer `eventos@buzzmonitor.com.br` numa LP pt-PT — confirmar caixa certa p/ Portugal.
- [ ] Cargos em ingles sem `lang="en"`; `translate="no"` inconsistente.
- [ ] H1 lidera pela solucao, nao pela dor (§3/§5) — decisao de copy.

## Verificado OK (nao sao achados)

- Link do card de agenda -> `/territorios-marca-mundial-2026`: a LP-destino EXISTE no dominio (confirmado na varredura) — nao e link quebrado.
- Varredura GTM: 27 LPs do `webinar.buzzmonitor.com`, 0 outros containers trocados.
- Skip-link, hierarquia de headings, `aria-labelledby`, `rel=noopener`, `:focus-visible`, viewport sem `user-scalable`, `.reveal` com fallback no-JS + reduced-motion, fonts `display=swap`.

## Proximos passos

- Decisoes pendentes: **funil pos-evento** + **contraste do botao** (ver chat).
- Publicar (dominio migrado -> CI): `/lp-publicar buzzmonitor webinar-territorios-marca-mundial-junho-2026 webinar.buzzmonitor.com` (Passo 5.3 valida GTM no live).
