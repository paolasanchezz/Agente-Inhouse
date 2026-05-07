# Cxpress · Webinar WhatsApp em SaaS e Tecnologia · maio 2026

LP recuperada do live em **2026-05-07** apos publicacao em outra maquina sem source no repo (incidente do mesmo dia — ver `landing-pages/CONTEXT.md` §7.2).

## Origem

- **Live:** https://content.cxpress.io/webinar-tecnologia-maio2026
- **Deploy origem:** `dpl_3rKKvvAfdinBXbQB1MeFFdJP51Au` (creator: victor.lopes@buzzmonitor.com.br via claude-code agent, 2026-05-07 ~11h)
- **Reconstrucao:** `index.html` baixado direto do deploy production via Vercel API V7 (Passo 0.5.d.iii do `/lp-publicar` v3.1.0). Paths absolutos (`/assets/...`) revertidos para o padrao source (`../../brand/cxpress/assets/...`) compativel com o pipeline.

## O que falta (debito tecnico)

- **`copy.txt`** — a copy estruturada (output do `/lp-preparar`) **nao existe**. So temos o HTML resultado.
  - Pra futuras alteracoes de copy, opcao A (rapida): editar `index.html` direto. Opcao B (canonica): rodar engenharia reversa `/lp-preparar` extraindo blocos do HTML pra reconstruir `copy.txt`, depois `/lp-gerar`.
- **`REVISAO.md`** — auditoria do `/lp-revisar` nunca foi rodada nesse source. Recomendado rodar `/lp-revisar cxpress/webinar-tecnologia-maio2026` antes da proxima alteracao significativa.
- **Confirmacao do form integrado** — checar se o form embedado no live e Jotform/RD/HubSpot e qual snippet veio. Se for embed real, esta correto. Se for mock, rodar `/lp-integrar-form`.

## Tema do evento

WhatsApp para SaaS e Tecnologia. Webinar gratuito, 29 de maio 2026, 11h.

## Como atualizar

```
/lp-publicar cxpress webinar-tecnologia-maio2026 content.cxpress.io
```

A partir da v3.1.0, o sync via Vercel API garante que vizinhas (livraria, playbook-whatsapp2026) nao sao apagadas no deploy.
