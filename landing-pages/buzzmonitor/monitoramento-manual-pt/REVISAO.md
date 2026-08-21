# Revisão LP — buzzmonitor/monitoramento-manual-pt

**Data:** 2026-08-11
**Auditores:** frontend-design (review mode) + web-design-guidelines (Vercel Labs) + checagens determinísticas (GTM, SEO, copy)

## Aplicado automaticamente (5 críticos)

- [x] **I18N-HREFLANG-MISSING** — esta LP é a tradução PT-PT de `plataforma-completa-monitoramento` (BR), mas a heurística automática de "slug-base" não detecta a relação porque os nomes de pasta divergem (`monitoramento-manual-pt` vs `plataforma-completa-monitoramento`, não seguem o padrão `{base}`/`{base}-pt`). Adicionado no `<head>` (linhas 17-19): `hreflang="pt-BR"` → BR, `hreflang="pt-PT"` → esta página, `x-default` → BR (mercado principal). GUIDELINES §16.
- [x] **SEO-OG-LOCALE-ALTERNATE** — adicionado `<meta property="og:locale:alternate" content="pt_BR">` (linha 27), par do hreflang acima.
- [x] **MOTION-NO-FALLBACK** (`.bg-gradient`, linha ~221) — animação `shift` (12s infinite) na seção SOLUCAO não tinha guard de `prefers-reduced-motion`. Adicionado `@media (prefers-reduced-motion: reduce){ .bg-gradient{ animation:none; } }`. Web Interface Guidelines (Vercel): "Respect Motion Preferences".
- [x] **MOTION-NO-FALLBACK** (`.bg-aurora`, linha ~265) — mesma falha na seção PARA-QUEM (`aurora` 10s infinite). Adicionado guard equivalente.
- [x] **PERF-TRANSITION-ALL** (`.btn-glow`, linha 146) — `transition:all 0.3s ease` trocado por `transition:box-shadow 0.3s ease, transform 0.3s ease` (lista explícita de propriedades, conforme Web Interface Guidelines).

## Melhorias opcionais — requerem decisão do usuário, NÃO aplicadas (2)

Estes dois itens já existiam **idênticos no original BR** (`plataforma-completa-monitoramento`) por decisão explícita do usuário em rodadas anteriores. Corrigi-los aqui quebraria a paridade visual que você pediu ("formato idêntico ao original") sem sincronizar a mudança na LP BR também. Decisão sua:

- [ ] **CONTRASTE AA — `.btn-primary`** (linha ~138, usado em todos os CTAs com `.btn-glow`): texto branco sobre fundo laranja `#EB7C2E` mede ≈2.82:1 — abaixo do 4.5:1 exigido pela WCAG AA para texto normal (GUIDELINES §7). O README do original documenta que essa é uma reintrodução deliberada da falha em 2026-07-29, a pedido do usuário. Se quiser corrigir, a opção mais simples é texto escuro (`var(--ink)` ou `var(--purple)`) sobre o mesmo laranja — mas isso teria que ser replicado na LP BR também para manter a paridade.
- [ ] **COPY-VAZAMENTO — overline "Os nossos diferenciais"** (linha 507, seção SOLUCAO): este texto não existe em nenhuma versão do `copy.txt` (nem BR nem PT-PT) — foi adicionado pela `frontend-design` durante a geração do HTML original e nunca veio da copy aprovada. Mantido aqui só por paridade com o original (mesma falha lá). Se quiser, posso remover o overline (deixando só o H2) ou substituí-lo por texto literal da copy — mas, de novo, para não gerar assimetria entre BR e PT, o ideal é decidir e aplicar nas duas.

## Nice-to-haves (3)

Estilístico / cosmético. Aceitável manter.

- [ ] Ícones da seção PROBLEMA (linhas 493-497) misturam lupa/✕/?/!/⚠ em vez do padrão único "X vermelho" de GUIDELINES §8 — decisão de estilo já aprovada no original (2026-07-24/29). Mantido por paridade.
- [ ] CSS morto: `.form-card`/`.form-field` (linhas ~328-336, incl. `outline:none` num input que não existe mais no HTML — a página usa embed Jotform desde a origem, nunca teve o form mock). Não afeta nada visível; pode ser removido num cleanup futuro.
- [ ] `<h2 class="overline">Quem já saiu do manual</h2>` (linha 611, seção PROVA) usa `<h2>` para um texto estilizado como eyebrow, enquanto todas as outras seções usam `<span class="overline">` para o mesmo papel visual. Hierarquia de heading continua válida (h2→h3), mas é uma inconsistência semântica. Inherited do original.

## Checagens determinísticas (todas OK)

- **GTM** (`check_gtm_region.py`): status `ok` — container `GTM-NCFT22CW` (Portugal) correto no `<script>` e no `<noscript>`. Selo `.tracking.lock` gravado.
- **Fidelidade de copy:** 0 em-dash no HTML; estrutura bate 1:1 com `copy.txt` (11 seções, 6 benefícios, 5 itens de problema, 4 cases — mesma contagem do original BR).
- **SEO obrigatório:** `meta description` (1), `meta robots` (1), `og:` (10, ≥8), `twitter:` (4, ≥4), JSON-LD (1, parseia como JSON válido, `Organization.url` = home PT do manifest, `sameAs` inclui LinkedIn + Instagram PT), `canonical` (1).
- **Logo regional:** header/footer apontam para `https://getbuzzmonitor.com/pt/` (não `"/"`), `target="_blank" rel="noopener"` presentes, `aria-label` localizado. SVGs de logo (`logo-primary.svg`, `logo-reversed.svg`) sem `<text>` vivo — seguros pra usar.
- **Acessibilidade geral:** skip-link presente e funcional, `:focus-visible` global sem `outline:none` real (o único `outline:none` está em CSS morto, ver nice-to-have), todas as imagens com `alt`, ícones decorativos com `aria-hidden`, `.reveal` com fallback `<noscript>`.

## Fora do escopo desta revisão (follow-up sugerido)

- **BR (`plataforma-completa-monitoramento`) não tem o hreflang recíproco** apontando para esta página PT-PT. Google recomenda hreflang bidirecional entre variantes de idioma. Não editei a LP BR (arquivo de produção já publicado, fora do escopo desta tarefa) — sugiro um `/lp-revisar buzzmonitor/plataforma-completa-monitoramento` dedicado para adicionar o par `hreflang="pt-PT"` + `og:locale:alternate` lá também antes de publicar esta.
- **OG image e `logo-wall.png`** com texto em PT-BR embutido nos píxeis — já documentado no `README.md` desta LP, segue pendente.

## Próximos passos

- Decidir os 2 itens de "Melhorias opcionais" (contraste do CTA e overline sem copy-fonte) — aplicar aqui e no original se decidir corrigir.
- Considerar o follow-up de hreflang recíproco no BR.
- Publicar: PR aberto com o slug `"monitoramento-manual-pt"` já no manifest do guarda-chuva — aguardar merge (auto-merge do bot ou aprovação do Victor) para o CI buildar e deployar em `content.buzzmonitor.com/monitoramento-manual-pt`.
