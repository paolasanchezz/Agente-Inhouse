# Revisao LP — buzzmonitor/caso-smartfit

**Data:** 2026-08-06 (v1) · atualizado 2026-08-06 (v2, apos reescrita completa do copy pelo usuario)
**Auditores:** frontend-design (review mode) + web-design-guidelines (Vercel) + auditoria GTM/copy/SEO (lp-revisar)

## Segunda passada (v2 — copy reescrito)

Reauditei apos o usuario substituir SUB, H2/H3/BODY/LABEL de "Lo que vas a ver", RESULTADOS, bio da Milagro, os 4 itens de "Para quien es" e H2/BODY/labels do CTA FINAL. **Nenhum critico novo** — estrutura, CSS e os 2 criticos da v1 (hreflang removido, lazy-loading corrigido) seguem intactos, pois so o texto mudou.

- **Fidelidade de copy:** as 15 frases novas/alteradas batem literal com `copy.txt` v2, uma por uma. Em-dash: 0. Ellipsis: 1 ocorrencia, corretamente `&hellip;`.
- **GTM:** `GTM-MKQBX2MG` continua correto (2/2 blocos).
- **Nice-to-have (nao aplicado):** "Además" abre a segunda frase tanto no BODY 02 quanto no BODY 03 de "Lo que vas a ver" — repeticao de conector, ja anotada no `copy.txt` como sugestao pro usuario decidir (nao e "abrir paragrafo" no sentido estrito da regra, entao nao e critico).

## Aplicado automaticamente (2 criticos)

- [x] **Hreflang desnecessario (GUIDELINES §16)** — esta LP nao tem irma em outro idioma, mas o `<head>` trazia `hreflang="es-419"` (auto-referente) e `hreflang="x-default"`. A regra e explicita: "se for LP unica, omitir hreflang". Removidas as 2 linhas, mantido so o `canonical`.
- [x] **`loading="lazy"` em imagem acima da dobra (Web Interface Guidelines)** — o logo do Smart Fit no card do hero (`hero-card-logo`) estava com `loading="lazy"`, mas fica visivel sem scroll (dentro do hero). Lazy-loading acima da dobra atrasa a renderizacao em vez de ajudar. Atributo removido (carrega eager, como o resto do hero).

## Auditorias que passaram sem achados

- **Fidelidade de copy:** todo texto visivel bate literal com `copy.txt` (ja atualizado com a troca de CTA pra "¡Reserva tu lugar!" nas 2 ocorrencias, a pedido do usuario, com nota de rastreabilidade incluindo o aviso de que semanticamente "reservar lugar" combina mais com evento do que com chamada 1:1 — decisao consciente do usuario). Em-dash: 0.
- **GTM:** `GTM-MKQBX2MG` (regiao latam) presente no `<head>` e no `<noscript>`.
- **SEO:** 1 description, 10 `og:`, 4 `twitter:`, JSON-LD parseia (Organization + WebPage + Article), 1 canonical.
- **Logo:** header/footer apontam pra `regions.latam.home`, `aria-label` em ES, SVGs sem `<text>` vivo.
- **Acessibilidade:** skip-link, focus-visible, alt em todas as imagens (incluindo o logo do cliente Smart Fit, que carrega texto alternativo "Smart Fit" e NAO esta marcado `aria-hidden` — e informacao real, nao decorativa), decorativos com `aria-hidden`, `prefers-reduced-motion` coberto globalmente, `min-height:0` no `<img>` do speaker.
- **Estrutura "prova/speaker":** layout horizontal (foto esquerda, texto direita) ✓.
- **Secao nova "Resultados":** gramatica visual propria e consistente (cards brancos, borda superior em laranja, texto em display bold) — nao contradiz nenhuma gramatica existente do GUIDELINES §8, e o proprio §8 nao cobre "secao de estatisticas" como tipo fixo.
- **Uso do logo do cliente (Smart Fit):** autorizado explicitamente pelo usuario antes de integrar (nao foi decisao unilateral da skill).

## Nenhuma melhoria opcional nem nice-to-have desta vez

Revisao limpa — os 2 achados foram tratados como criticos e ja aplicados.

## Proximos passos

- CTA ainda e mock (`href="#"`) — quando tiver o link real de agendamento, rodar `/lp-integrar-form buzzmonitor/caso-smartfit "snippet"`.
- Publicar: `webinar.buzzmonitor.com` esta no fluxo CI — adicionar ao manifest + PR.
