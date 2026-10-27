# Revisao LP — cxpress/oferta-whatsapp-equipe

**Data:** 2026-10-23
**Auditoria:** design + acessibilidade/HTML feitas na sessao, mais as checagens deterministicas da skill (GTM, SEO, ancoras, OG, fidelidade de copy)

## Checagens deterministicas

| Checagem | Resultado |
|---|---|
| GTM (`check_gtm_region.py`) | `ok`, `GTM-T4XDWHL3` (brasil), selo `.tracking.lock` gravado |
| meta description / robots / canonical | 1 / 1 / 1 |
| og: / twitter: | 10 / 4 |
| JSON-LD | 1 bloco, parseia |
| hreflang | pt-BR + x-default (LP unica, sem irmas `-es`/`-pt`) |
| Logo header/footer | aponta para `https://home.cxpress.io`, `target="_blank"`, SVGs sem `<text>` |
| Ancoras (§22) | nenhuma escrita de hash, nenhum link absoluto com `#`. Dominio migrado: o build injeta a trava |
| Em-dash | 0 |
| Fidelidade de copy | texto visivel literal da `copy.txt`; mudancas posteriores foram so negrito, cor e quebra de linha pedidas pela usuaria |
| Ilustracao do Impacto | `aria-hidden`, sem texto, animacao desligada com `prefers-reduced-motion` |
| Overflow a 375px | nenhum |

## Aplicado automaticamente (2 criticos)

- [x] **OG image ausente.** Template `assets/og-template.html` atualizado (H1 desta LP, paleta preto + azul da pagina) e renderizado com Chrome headless em `assets/og-oferta-whatsapp-equipe.png`, 1200×630. Sem `og-image.png`.
- [x] **CTA final levava ao topo da pagina, nao ao formulario.** `href="#top"` caia no H1; no celular o formulario fica abaixo do texto do hero e a pessoa precisava rolar de novo. Agora `href="#oferta"`, com `id="oferta"` no painel da oferta e `scroll-margin-top`.

## Melhorias opcionais (4, aplicadas a pedido da usuaria em 2026-10-23)

- [x] **JSON-LD sem `sameAs`.** Incluidos direto nesta LP `https://www.linkedin.com/company/cxpress/` e `https://www.instagram.com/cxpress.io/` (as URLs mais usadas nas outras LPs Cxpress). O `brand/cxpress/brand-manifest.json` segue no formato antigo (`websites`, sem `regions`); migrar o manifest e uma mudanca a parte, que afeta todas as LPs Cxpress.
- [x] **Rodape com texto duplicado.** Removida a linha solta "Condições gerais de uso da Cxpress · Políticas de privacidade"; os links ficam no bloco "Termos e Políticas".
- [x] **Densidade de negrito na secao Impacto.** De 7 para 2 trechos: "app não oficial" e "justo na semana que mais importa".
- [x] **Disclaimer do form** (`.form-note`) subiu de 12,5px para 14px no desktop e de 13px para 14px no celular.

## Segunda revisao (2026-10-23)

Auditoria de design + acessibilidade feita por um agente revisor separado (leitura independente), mais as checagens deterministicas repetidas: GTM `ok` com selo em dia, SEO completo (description, robots, canonical, og 10, twitter 4, JSON-LD), OG image presente, em-dash 0, "ao vivo" 0, ancoras sem `#`. Copy literal da `copy.txt`. Contrastes AA conferidos (kicker 7,96:1; azul com branco 5,56:1; `--ink-mute` 4,86:1).

### Aplicado (1 critico)

- [x] **Rolagem suave sem fallback de movimento.** `html { scroll-behavior: smooth }` nao tinha desligamento para `prefers-reduced-motion`. Adicionado `scroll-behavior: auto` dentro da media query.

### Melhorias opcionais (6, aplicadas a pedido da usuaria em 2026-10-23)

- [x] **Kicker do hero quebrava em 2-3 linhas no celular.** Abaixo de 980px a pilula vira overline sem fundo (texto azul com o ponto), sem borda quebrada.
- [x] **Sem CTA visivel sem rolar.** Botao-ancora "Garantir oferta" (`.hero-cta`, texto literal da copy) no hero, levando a `#oferta`. Aparece so no layout de 1 coluna (ate 980px); no desktop o form ja esta ao lado do texto.
- [x] **Rotulo da faixa de clientes** de 13px para 14px.
- [x] **`text-wrap`:** `balance` em `.depois-closer`, `.form-heading`, `.clientes__label`; `pretty` em `.hero-body`, `.section-lede`, `.benefit-card p`, `.form-bullets li`.
- [x] **Inputs do form mock:** borda em `--ink-mute` (4,86:1) e foco com contorno azul solido de 2px.
- [x] **Faixa de logos:** pausa tambem no foco do teclado (`tabindex="0"` + `:focus`, com contorno visivel) e no toque (`:active`).

## Nice-to-haves (2 + 6 da segunda revisao)

- [ ] Padding do painel do form de 32px para 24px abaixo de 640px.
- [ ] `.form-heading` como `<p>`: virar titulo ou ligar o `<form>` a ele com `aria-labelledby`.
- [ ] Alvo do skip-link (`<main id="top">`) sem `tabindex="-1"`.
- [ ] Logo do header/footer com `aria-label` no link e `alt="Cxpress"` na imagem: nome redundante; a §17 pede `alt=""`.
- [ ] `style="background:var(--paper)"` inline repetido nos 4 cards de beneficio: mover para a classe.
- [ ] Peso 600 da Source Sans 3 carregado sem uso aparente.

- [ ] OG image renderiza o titulo em Arial (Open Sans nao esta instalada na maquina). Mesmo comportamento da LP irma; para ficar identica a pagina, instalar Open Sans antes de renderizar.
- [ ] Ilustracao poderia trocar os icones genericos de pessoa por fotos ou avatares da marca, se houver.

## Proximos passos

- Design aprovado? -> `/lp-integrar-form cxpress/oferta-whatsapp-equipe "{snippet}"`
- Publicar -> `/lp-publicar cxpress oferta-whatsapp-equipe content.cxpress.io`
