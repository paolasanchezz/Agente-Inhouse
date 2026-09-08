# Revisao LP — buzzmonitor/teste-de-maturidade-resultado-avancado

**Data:** 2026-09-08
**Auditores:** frontend-design (review mode) + web-design-guidelines + auditorias deterministicas (GTM, copy-fidelidade, SEO/hreflang/logo/OG)

> Auditoria estrutural/design completa (design review + web-interface-guidelines) foi feita sobre a LP irma `teste-de-maturidade-resultado-basico` — as 5 LPs da familia compartilham 100% do HTML/CSS/JS, entao os achados estruturais valem igualmente aqui. Ver `landing-pages/buzzmonitor/teste-de-maturidade-resultado-basico/REVISAO.md` para o detalhe completo (1 critico aplicado + 2 melhorias registradas). Esta revisao confirma que os mesmos achados/fixes se aplicam e roda as checagens especificas de conteudo desta LP.

## Aplicado automaticamente (1 critico, replicado da LP irma)

- [x] **Foco de teclado "fantasma" atras da capa** — mesmo fix aplicado nas 5 LPs da familia: `inert` adicionado/removido em `#resultado-gate` e `<footer>` junto com o `aria-hidden`, sincronizado com o clique em "Ver resultado".

## Melhorias opcionais (2, mesmas da familia — nao aplicadas)

- [ ] Contraste ~2,82:1 do texto branco sobre `--orange` nos botoes (`.btn-orange`) — herdado da LP-mae `teste-de-maturidade`, afeta a familia toda. Ver detalhe e opcoes de correcao no REVISAO.md da LP `-basico`.
- [ ] 3 receitas de gradiente na mesma LP (GUIDELINES §1 recomenda 1) — mesma familia de cor, nao briga visualmente.

## Nice-to-haves (0)

## Auditorias deterministicas — todas OK

- **GTM/regiao:** `status: ok` — `GTM-WFJVK858` bate com `brasil`. Selo gravado.
- **Copy-fidelidade:** em-dash = 0; badge "Nivel Avancado", H2 e os 5 paragrafos batem literal com `copy.txt`.
- **SEO:** 1 description, 10 `og:`, 4 `twitter:`, 1 JSON-LD valido, 1 canonical. Sem hreflang (sem LPs irmas de outro idioma pra este slug).
- **Logo:** href correto (`https://buzzmonitor.com/`), `target="_blank" rel="noopener"`, SVGs sem `<text>` vivo.
- **OG image:** pendente (placeholder), pendencia ja conhecida.

## Proximos passos

- Mesmos da LP `-basico`: decisao sobre contraste do botao (familia toda), OG image.
- Design aprovado? → `/lp-publicar buzzmonitor teste-de-maturidade-resultado-avancado [dominio]`.

## Re-revisao (2026-09-08) — acentuacao corrigida + form real integrado

Mesmas 3 mudancas da familia (acentuacao PT-BR, form real do Jotform com UTM `resultado-avancado`, CTA extra + degrade animado no CTA final).

**1 bug encontrado e corrigido nesta LP especificamente:** o script de correcao de acento rodou a substituicao do token "nivel avancado" (dentro do 1º paragrafo do diagnostico) antes de tentar substituir o paragrafo inteiro, o que fez o paragrafo inteiro nao bater mais com o texto esperado e ficar so parcialmente acentuado ("nível avançado" acentuado, mas "visao", "utilizacao", "decisoes", "comunicacao", "comecam", "inteligencia", "negocio" continuaram sem acento no meio da mesma frase). Corrigido manualmente no `index.html` e no `copy.txt` com o texto integral e corretamente acentuado.

Re-checagem programatica confirmou (pos-fix): badge/H2/5 paragrafos batendo literal com `copy.txt`, acentuacao correta em title/meta/JSON-LD/corpo (incluindo o paragrafo que tinha o bug), e em-dash/SEO/JSON-LD/GTM todos OK. Fix de `inert` da revisao anterior intacto.
