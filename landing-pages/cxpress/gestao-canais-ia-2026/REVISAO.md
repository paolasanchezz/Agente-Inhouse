# Revisão — LP Cxpress / gestao-canais-ia-2026

**Data:** 2026-06-12
**Auditoria:** validação técnica (lp-gerar Passo 4) + Web Interface Guidelines (Vercel) + verificação no preview (desktop 1280 / mobile 390).

## Validação técnica (tudo OK)

- em-dash (—) e &mdash;: **0 ocorrências**
- SEO: 1 description · 10 og: · 4 twitter: · 1 canonical · JSON-LD parseia (Organization + WebPage + Event)
- Favicon: 1 link único (PNG do brand)
- GTM `GTM-T4XDWHL3`: head + noscript (2 ocorrências) — região brasil
- `<html lang="pt-BR">`, form mock (`action="#"`), nenhum `href="/"`
- Fidelidade da copy: todos os textos visíveis batem com `copy.txt`. Sem pull-quote/kicker/slogan inventado. Whitelist usada: nav meta ("Evento presencial"), labels de form, rótulos do countdown (Dias/Horas/Minutos/Segundos), badge "Vaga gratuita" (palavra "gratuita" já está na copy).

## Verificação no preview

- Countdown ao vivo até 16/07/2026 09:00 funcionando (33 dias na verificação), `tabular-nums`, `aria-live="polite"`.
- Foto do Enrico e faixa de clientes carregam (`./assets/`). Logos de marca (`../../brand/`) só resolvem pós-deploy (convenção do repo) — no preview mostram alt.
- 5 cards de benefício, 5 itens de timeline, 2 cards de palestrante, 5 inputs / 5 labels.
- **Mobile (§3):** headline ANTES do ticket card (h1 top 232 < ticket top 759). OK.
- Sem erros JS no console. Warnings do Meta Pixel (via GTM) em localhost são esperados (permissão de tráfego), some em produção.

## Achados Web Interface Guidelines

### Crítico
- Nenhum.

### Importante (aplicado)
- Input de e-mail sem `spellcheck`/`autocapitalize` → **adicionado** `spellcheck="false" autocapitalize="none"`.
- WhatsApp sem `inputmode` → **adicionado** `inputmode="tel"`.

### Nice-to-have
- `<meta name="theme-color">` ausente → **adicionado** (#232960).
- `.btn` sem `touch-action: manipulation` → **adicionado** (+ `-webkit-tap-highlight-color`).
- Logos SVG (header/footer) sem `width`/`height` explícitos (CLS mínimo). **Não aplicado** de propósito: tamanho é controlado por CSS (`height:30px; width:auto`) e forçar atributos com ratio errado arriscaria distorção. Baixo impacto.
- Placeholders dos inputs não terminam em "…" (regra genérica das guidelines). **Não aplicado**: são valores de exemplo ("Seu nome", "voce@empresa.com"), onde reticências não fazem sentido.

## Pendências para o usuário antes de publicar

1. **Foto + nome do convidado** do painel (card 2 hoje é placeholder com a copy "Convidado especial / Cliente Cxpress / Em breve").
2. **Formulário real** — hoje é mock. Definir provedor (Jotform / RD Station / HubSpot) e rodar `/lp-integrar-form cxpress/gestao-canais-ia-2026 "<snippet>"`.
3. **OG image** (1200×630) a gerar antes de publicar.
4. **CSP do mapa** — ao publicar, garantir `frame-src https://www.google.com` no `vercel.json` (o `lp-publicar` detecta drift de CSP; se faltar, patch cirúrgico).

## Próximo passo

Pausa do pipeline (GUIDELINES §11): design pronto e aprovável. Quando o Victor aprovar:
`/lp-publicar cxpress gestao-canais-ia-2026 content.cxpress.io`
