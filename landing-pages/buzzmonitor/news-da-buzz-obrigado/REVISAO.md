# Revisao LP — buzzmonitor/news-da-buzz-obrigado

**Data:** 2026-08-27
**Auditores:** frontend-design (review mode) + web-design-guidelines + auditorias determinísticas (GTM, em-dash, pacote SEO)

## Aplicado automaticamente (1 crítico)

- [x] Contraste AA: `.eyebrow` ("Inscrição confirmada") usava `var(--teal)` (#0E9D9B) sobre texto branco = ~3.3:1, abaixo do AA (4.5:1). Trocado para `var(--primary)` (#390155) — mesmo fix já aplicado na LP-mãe `news-da-buzz` pro mesmo padrão (`.eyebrow-sm` "Prévia real").

## Crítico sinalizado, NÃO corrigido automaticamente (decisão de marca, herdado da LP-mãe)

- [x] **~~Contraste do botão CTA laranja~~** — não se aplica mais: o botão "Seguir a Buzzmonitor no LinkedIn" foi removido em 2026-08-27 (pedido da Catharina). CSS `.btn`/`.btn svg`/`.btn:hover` removido junto por ficar órfão.

## Melhorias opcionais (1)

- [ ] `alt="Buzzmonitor"` nos logos do header/footer duplica a `aria-label` do link pai (leitor de tela anuncia o nome 2x). GUIDELINES §17 recomenda `alt=""` quando o `aria-label` já está no `<a>`. Não fixei porque a LP-mãe e o precedente (`estudo-diversidade-2026-obrigado`) usam o mesmo padrão — mudar só aqui criaria inconsistência dentro da própria família de páginas.

## Nice-to-haves (0)

Nenhum.

## Auditorias determinísticas

- **GTM (Passo 3.5):** `status: ok`, container `GTM-WFJVK858` bate com a região (`brasil` via `<html lang="pt-BR">`). Stamp gravado.
- **Em-dash:** 0 ocorrências (`—` e `&mdash;`).
- **SEO (Passo 3.7.a):** `meta description` = 1, `meta robots` = 1 (`noindex, follow`, exceção deliberada de thanks page — ver README). `og:`, `twitter:` e JSON-LD ausentes de propósito (mesma exceção do precedente `estudo-diversidade-2026-obrigado`/`cxpress/video-atendimento-obrigado`): ninguém compartilha essa URL.
- **Fidelidade de copy (Passo 3.6):** não aplicável — página não tem `copy.txt` de origem (copy escrita direto pra esta thanks page, como o precedente).
- **Multi-idioma (Passo 3.7.c):** não aplicável — sem LPs irmãs (`news-da-buzz` não tem variantes `-es`/`-pt`).
- **Logo regional (Passo 3.7.d):** header/footer apontam pra `https://buzzmonitor.com/` (home da marca), não `/`. OK. Logos são raster (Buzzmonitor já é base64 nos SVGs, sem `<text>` vivo).

## Próximos passos

- Publicar: `/lp-publicar buzzmonitor news-da-buzz material.buzzmonitor.com` (guarda-chuva, publica as duas LPs — mãe + thanks page — em batch).
