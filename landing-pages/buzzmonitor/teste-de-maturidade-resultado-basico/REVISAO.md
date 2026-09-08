# Revisao LP — buzzmonitor/teste-de-maturidade-resultado-basico

**Data:** 2026-09-08
**Auditores:** frontend-design (review mode) + web-design-guidelines + auditorias deterministicas (GTM, copy-fidelidade, SEO/hreflang/logo/OG)

> Esta LP compartilha 100% da estrutura HTML/CSS/JS com as outras 4 irmas da familia "teste-de-maturidade-resultado" — a auditoria estrutural/design foi feita uma vez sobre essa base compartilhada e vale para as 5. Achados especificos de conteudo (copy, SEO, GTM) foram checados individualmente nesta LP.

## Aplicado automaticamente (1 critico)

- [x] **Foco de teclado "fantasma" atras da capa** — enquanto a capa (`.hero`, overlay fixo) cobre a tela, os links dentro de `#resultado-gate` e do `<footer>` (CTA final, redes sociais, politica de privacidade) continuavam alcancaveis por Tab mesmo escondidos visualmente atras da capa opaca (WCAG 2.4.3, ordem de foco). `aria-hidden` sozinho nao impede foco real de teclado. Corrigido adicionando `inert` nesses containers enquanto fechados, removido no clique junto com o `aria-hidden` (script no fim do `index.html`). Aplicado tambem retroativamente em `teste-de-maturidade-resultado-inicial` (mesma estrutura) pra manter a familia consistente.

## Melhorias opcionais (2)

Para o usuario decidir — nao aplicadas.

- [ ] **Contraste do texto branco sobre laranja `--orange` (#EB7C2E) fica em ~2,82:1** — abaixo do minimo WCAG AA mesmo pra texto grande (precisa 3:1) e bem abaixo do minimo pra texto normal (4.5:1). Afeta `.btn-orange` (botao "Agende..." do menu, "Ver resultado" da capa, CTA final) e a extremidade mais clara do gradiente do badge `.resultado__badge`. Com `--orange-dark` (#CF6314) o contraste sobe pra ~3,85:1 (passa pra texto grande, ainda nao pra texto normal do menu que e 14px). **Nao apliquei a correcao** porque essa cor/estilo de botao vem herdada literal da LP-mae `teste-de-maturidade` (ja aprovada e no ar) e se repete em outras LPs Buzzmonitor — mudar aqui deixaria essas 5 LPs inconsistentes com a familia maior. Se o Victor quiser, da pra: (a) trocar o texto do botao pra `var(--purple)` em vez de branco, (b) escurecer o gradiente pra `--orange-dark` como base, ou (c) aceitar como esta (padrao ja estabelecido na marca).
- [ ] **3 "receitas" de gradiente na mesma LP** (fundo animado da capa em tons de roxo, texto "pronto" laranja->rosa claro, badge laranja->laranja-escuro) — GUIDELINES §1 recomenda no maximo 1 tipo de gradiente por LP. Sao todos da mesma familia de cor da marca (roxo/laranja), entao nao brigam visualmente, mas e um desvio tecnico da regra. Se quiser, dá pra unificar (ex: badge solido em vez de gradiente).

## Nice-to-haves (0)

Nenhum achado estilistico adicional alem do que ja esta documentado no README (CTA mockado, OG image pendente).

## Auditorias deterministicas — todas OK

- **GTM/regiao:** `status: ok` — container `GTM-WFJVK858` bate com a regiao `brasil` (cascata via `<html lang="pt-BR">`). Selo `.tracking.lock` gravado.
- **Copy-fidelidade:** em-dash = 0 no HTML; badge/H2/paragrafos batem literal com `copy.txt`; nenhum pull-quote, kicker ou punchline inventado fora da whitelist.
- **SEO:** 1 meta description, 10 tags `og:`, 4 tags `twitter:`, 1 JSON-LD (parseia, `Organization.url`/`sameAs` batem com o brand-manifest), 1 canonical. Sem LPs irmas em outro idioma pra este slug, entao hreflang omitido corretamente.
- **Logo:** header/footer apontam pra `https://buzzmonitor.com/` (nao `"/"`), `target="_blank" rel="noopener"`, SVGs sem `<text>` vivo (nao serifam).
- **OG image:** ainda nao gerada (`{{OG_IMAGE_PATH}}` placeholder) — pendencia ja conhecida, nao e um achado novo desta revisao.

## Proximos passos

- Decidir sobre o contraste do botao laranja (melhoria acima) — afeta a familia toda, nao so esta LP.
- Gerar OG image 1200×630 antes de publicar.
- Design aprovado? → `/lp-publicar buzzmonitor teste-de-maturidade-resultado-basico [dominio]`.

## Re-revisao (2026-09-08) — acentuacao corrigida + form real integrado

Desde a revisao acima, 3 mudancas entraram na LP (pedidas pelo Victor no chat, fora do fluxo `/lp-revisar`): acentuacao PT-BR corrigida em toda a copy (estava saindo sem nenhum acento), form mock trocado pelo embed real do Jotform (`jsform/252995108251662`, UTM `resultado-basico`), CTA extra no fim do texto de diagnostico, e fundo do CTA final trocado de pontilhado pra degrade animado. Re-rodei as auditorias deterministicas pra confirmar que nada quebrou:

- **Copy-fidelidade (re-checada):** comparei programaticamente badge/H2/paragrafos do `index.html` contra `copy.txt` (ambos ja com acento) — **match literal, 100%**, incluindo contagem de paragrafos (4/4).
- **Acentuacao:** title, meta description (og/twitter), JSON-LD e todo o corpo confirmados com acento correto (`Nível Básico`, `você está`, `operação`, etc). Nenhum residuo do bug de substituicao parcial que apareceu durante a correcao (esse bug so afetou temporariamente o `index.html` de outras LPs da familia, ja corrigido em todas).
- **Em-dash, SEO, JSON-LD, GTM:** todos re-confirmados OK (0 em-dash, 10 `og:`, 4 `twitter:`, 1 description, JSON-LD parseia, GTM `status: ok`).
- **Fix de foco (`inert`) da revisao anterior:** confirmado intacto (2 toggles set/remove no script).

Nenhum achado novo. Pendencias seguem as mesmas: contraste do botao laranja (melhoria, decisao do Victor) e OG image.
