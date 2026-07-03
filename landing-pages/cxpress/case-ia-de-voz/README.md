# LP · Webinar perpétuo · Estudo de caso: IA de Voz (case-ia-de-voz)

LP de webinar perpétuo da Cxpress no modelo `conheca-a-cxpress` (form custom ClickMeeting + data dinâmica via `/api/next-webinar`). Copy escrita a partir da transcrição do vídeo "vozxpress cxpress.mp4" (entrevista com Beatriz, gerente de projetos na Elife, sobre o case GPT Realtime + VozXpress no Google My Business).

- **Criada em:** 2026-07-03
- **Destino:** `content.cxpress.io/case-ia-de-voz` (guarda-chuva Cxpress, projeto Vercel `cxpress-lp-playbook-whatsapp2026`)
- **GTM:** GTM-T4XDWHL3 (brasil)
- **Série ClickMeeting (chave no front):** `series=ia-voz` (fetch e payload do form já enviam)

## Fatos do case usados na copy (fonte: transcrição)

| Fato | Valor |
|---|---|
| Cliques no botão ligar do GMB | 200 mil/mês (~700 por loja) |
| Lojas no Google My Business | mais de 1.000 |
| Implementação (prompt + plataforma) | 1 semana (+1 semana de piloto) |
| Direcionamento correto | 90% (meta batida, 5 rotas de encaminhamento) |
| Gatilho do projeto | "insucesso de contato" nos top detratores do GMB |
| Stack | GPT Realtime (OpenAI) + VozXpress (módulo de voz da Cxpress) |

## Pendências antes de publicar

1. ~~**Criar a série recorrente no ClickMeeting**~~ ✅ FEITO (2026-07-03) — webinar "Cxpress Vozxpress" (conf id `10070428`, `automated`/`type:2`, `registration_enabled:1`), **`recurring_config_id` = `17671`**, room_pin 754-174-641, tz America/Sao_Paulo.
2. ~~**Adicionar a chave `ia-voz` ao mapa `SERIES`** do `api/next-webinar.js`~~ ✅ FEITO e NO AR (2026-07-03). Functions do Cxpress portadas com `?series=` e `SERIES={'ia-voz':'17671'}`, versionadas em `landing-pages/cxpress/_clickmeeting-api/` (a api do domínio era single-série/env-only; roteamento `?series=` portado do padrão Buzzmonitor). Deploy manual controlado feito (deploy `dpl_9ZQWQZ56ETwAyYPrX6tTYGuCg5ry`). Smoke test: `/api/next-webinar?series=ia-voz` → room 10070428 (rcid 17671, "Cxpress Vozxpress"); no-series → 17529 intacto; 6 vizinhas 200.
3. **Foto da Beatriz** em `assets/beatriz.jpg` (quadrada; enquanto não existir, a LP mostra placeholder). Confirmar também o sobrenome dela pra seção "Quem conta o case".
4. **Página de confirmação** (opcional): hoje o submit redireciona direto pro link da sala (`redirect_url`). Se quiser página `-confirmado` como a do conheca-a-cxpress, criar depois.
5. **Publicar via `/lp-publicar cxpress case-ia-de-voz content.cxpress.io`** (nunca deploy manual). OG image já gerada em `assets/og-image.png` (1200×630) — no deploy vira `/assets/cxpress/og-case-ia-de-voz.png`.

## Validações feitas na criação

- Em-dash: 0 · antítese-por-negação: 1 · exclamação na copy visível: 0
- SEO: description 1 · og ≥8 · twitter 4 · JSON-LD parseia
- Mascote `samir-joinha.png` copiado do modelo (LP-local)
