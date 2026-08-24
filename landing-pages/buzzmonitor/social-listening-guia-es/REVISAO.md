# Revisão LP — buzzmonitor/social-listening-guia-es

**Data:** 2026-08-24
**Auditores:** frontend-design (review mode) + web-design-guidelines (Vercel Web Interface Guidelines) + auditorias determinísticas (GTM, SEO, fidelidade de copy)

## Aplicado automaticamente (1 crítico)

- [x] **Link morto no footer** — `<a href="#">Política de Privacidad</a>` não levava a lugar nenhum. Corrigido para `https://getbuzzmonitor.com/es/privacidad/` com `target="_blank" rel="noopener"`, seguindo o precedente exato já usado em `ia-para-social-listening-es/index.html:558`.

## Auditorias determinísticas — todas OK

- **GTM (`check_gtm_region.py`):** `status: ok` — região `latam` (detectada pelo sufixo `-es` do slug), container `GTM-MKQBX2MG` presente no `<head>` e no `<noscript>`. Selo `.tracking.lock` gravado.
- **SEO §15:** description=1, robots=1, og:=10 (≥8), twitter:=4 (≥4), JSON-LD=1 (parseia válido), canonical=1.
- **Logo regional §17:** navbar e footer apontam para `https://getbuzzmonitor.com/es/` (home LATAM do manifest, não hardcoded para `/`), `target="_blank" rel="noopener"` nos dois.
- **Logo web-safe §19:** `logo-primary.svg` e `logo-reversed.svg` são raster/base64, sem `<text>` vivo — seguros.
- **Em-dash (tolerância zero):** 0 ocorrências no HTML.
- **Fidelidade de copy:** todos os H1/H2 conferidos linha a linha contra `copy.txt` — match literal, nenhum pull-quote/kicker/disclaimer inventado fora da whitelist (labels de form, disclaimer de consentimento genérico, footer, skip-link, aria-labels).
- **Multi-idioma:** LP sem irmãs (nenhuma `social-listening-guia`/`social-listening-guia-pt` no repo) — hreflang autorreferenciado (es-419 + x-default) é opcional aqui, mas inofensivo; não removido.

## Melhorias opcionais (5)

Para o usuário decidir. Aplicar via Edit manual ou pedir `/lp-revisar` novamente.

- [ ] **Contraste do botão CTA (texto branco sobre laranja `#EB7C2E`)** mede ≈2,8:1 — abaixo do AA (4,5:1) para texto normal. **Não corrigi isso automaticamente** porque é a combinação oficial de `generation-rules.json` ("ctaButton: secondary com neutral.0 como texto") e está presente também no `skip-link` de `mcp-es` — é uma decisão de marca consistente em toda a família de LPs, não um erro desta peça. Se quiser, existe precedente de variante AA já criada em `mcp-es` (`--secondary-aa: #B5571F`, "contraste >= AA sobre branco para texto pequeno") que poderia inspirar uma correção brand-wide — mas isso é decisão do Victor/marca, não desta revisão pontual.
- [ ] `.form-field input:focus{outline:none}` usa `:focus` em vez de `:focus-visible` — troca simples para não acionar o destaque em clique de mouse, só em navegação por teclado (o `border-color` já funciona como indicador visual, então não é crítico).
- [ ] `<img>` dos logos (marca + 10 logos de clientes) sem atributos `width`/`height` explícitos — Web Interface Guidelines recomienda para evitar CLS. Risco baixo aqui porque a altura já é fixada via CSS, mas o `logo-wall` (flex-wrap) pode reflowar levemente enquanto cada logo carrega.
- [ ] Os 10 `<img>` de `.logo-wall` (abaixo da dobra) sem `loading="lazy"`.
- [ ] `.stat strong` (os números 1.000+, 300+, 500+, 10 mil) sem `font-variant-numeric: tabular-nums` — cosmético, ajuda no alinhamento visual entre os 4 números.

## Nice-to-haves (1)

- [ ] `<nav aria-label="Enlaces legales">` no footer envolve só 1 link — funcionalmente correto, mas overkill para um único item.

## Próximos passos

- Design aprovado? → `/lp-integrar-form buzzmonitor/social-listening-guia-es "snippet"` (aguardando decisão do form/automação — ActiveCampaign confirmado com Paola, mas snippet ainda não foi passado)
- Pendências de conteúdo que seguem abertas (ver README.md): confirmar mural de logos da seção CLIENTES + gerar OG image 1200×630
- Rever mais algum ponto? → editar e rodar `/lp-revisar` novamente
