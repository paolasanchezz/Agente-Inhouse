# Revisao LP — cxpress/conheca-a-cxpress

**Data:** 2026-06-17
**Auditores:** frontend-design (review mode) + web-design-guidelines
**Contexto:** revisao apos reestruturacao de copy (arco Dor -> Solucao -> Resultado -> CTA; remocao da secao "Para quem")

## Aplicado automaticamente (criticos)

- [x] **GUIDELINES §8 — secao Dor estava em grid numerado** -> convertida para **lista vertical** (`<ul class="pain-list">`) com **icone X vermelho** (`--error` / `--error-bg`) em cada item. Texto encurtado para formato checklist. Era a gramatica de secao-tipo errada (problema nao pode ser grid).
- [x] **GUIDELINES §8 — secao Resultado usava check azul** -> trocado para **verde** (`--success` / `--success-bg`). Cria o contraste deliberado vermelho (dor) ↔ verde (resultado) que a §8 pede; antes dor-neutra + resultado-azul anulava a leitura cromatica.
- [x] **SEO §15 — pacote incompleto** (so 3 tags og, sem canonical/JSON-LD/twitter/og:image) -> adicionado pacote completo, espelhando a LP irma `atendimento-clinicas`: `canonical`, `robots`, `author`, `theme-color`, 10 tags `og:*`, 4 tags `twitter:*`, e JSON-LD (`Organization` + `WebPage` + `SoftwareApplication`). Counts validados: description 1, og 10, twitter 4, jsonld 1 (parseia OK).
- [x] **SEO §18 — OG image ausente** -> gerada `assets/og-image.png` (1200x630, ~50 KB, brand Cxpress). No deploy vira `/assets/cxpress/og-conheca-a-cxpress.png` (namespace guarda-chuva).
- [x] **Anti-IA — em-dash (tolerancia zero)** -> 2 ocorrencias em comentarios CSS removidas. `grep "—"` agora retorna 0.
- [x] **GTM (Passo 3.5)** — validado: `GTM-T4XDWHL3` no `<head>` + `<noscript>` bate com `tracking.json` regiao brasil. Sem acao.

### Melhorias de a11y aplicadas (a pedido do Victor)

- [x] `.cm-feedback` mudou de `role="status"`/`aria-live="polite"` para `role="alert"`/`aria-live="assertive"` (erros de submit anunciados na hora pelo leitor de tela).
- [x] Submit invalido agora move o **foco para o primeiro campo vazio** (antes ficava no botao).
- [x] Campo de e-mail ganhou `spellcheck="false"` + `autocapitalize="off"`.
- [x] Adicionado `<meta name="theme-color" content="#ffffff">`.

## Melhorias opcionais (decidir)

- [ ] **Mascote Samir ausente** — BRANDBOOK §7 recomenda o sagui como ponto de calor humano em LPs de atendimento (`samir-laptop.png` no hero, `samir-joinha.png` no CTA). Nao e quebra (Samir e opcional), mas a LP perde a assinatura humana da marca. Cuidar do `min-height: 0` (GUIDELINES §14) se entrar como `<img>` em grid.
- [ ] **Nenhuma secao escura** (GUIDELINES §1) — a LP alterna branco/cinza/lilas-claro mas nao tem o ponto de contraste dramatico. CTA final ou um bloco de urgencia poderiam ir para `--primary-dark`.
- [ ] **Form no hero diverge do §3** (que pede visual clean a direita) — e override consciente: §10 classifica webinar como ToFu e manda form cedo. Mantido de proposito.
- [ ] **`.cta-final` sem classe `reveal`** — deixado proposital: a secao de conversao fica sempre visivel, sem depender de animacao. (Demais secoes usam `reveal`.)

## Nice-to-haves

- [ ] Seta do botao CTA final e `↑` (vertical) mas o hover desliza na horizontal (`translateX`). Usar `→` ou ajustar o hover.
- [ ] `text-wrap: balance` nos headings (`.section-h2`, `.hero h1`) para evitar viuvas.
- [ ] Dedupe dos 4 SVGs de check identicos do `.outcome` via `<symbol>` + `<use>`.
- [ ] Placeholder real no e-mail (hoje `placeholder=" "` e hack para `:placeholder-shown`).
- [ ] CSS orfao `.speaker-bio + .speaker-bio` (so 1 bio no HTML).

## Proximos passos

- Publicar -> `/lp-publicar cxpress conheca-a-cxpress content.cxpress.io`
- Commit do source -> direto na main (autorizado pelo Victor, admin)
