# LP Buzzmonitor — buzztalk-gestao-multimarcas-para-agencias

**Gerado em:** 2026-08-27
**Copy-fonte:** `copy.txt` (output de /lp-preparar, a partir da página Notion "Copy LP ✅" — evento Buzz Talks Agências 01/10)

## Origem

Recriação da LP legada `conteudo.buzzmonitor.com.br/buzztalk-gestao-multimarcas-para-agencias` (GreatPages, fora da Vercel) para o guarda-chuva `content.buzzmonitor.com`, com a identidade visual da série Buzz Talks — que corresponde à paleta oficial Buzzmonitor (roxo `#390155`, laranja `#EB7C2E`, teal `#0E9D9B`) e tipografia League Spartan + Hanken Grotesk + Lato.

Evento atualizado para a próxima edição (01/10/2026), conforme página de planejamento no Notion "Buzz Talks - Agências (01/10)".

## Estrutura

- HERO — headline, contexto, form de inscrição mock (nome, e-mail, empresa, cargo, WhatsApp)
- COMO CHEGAR — endereço confirmado (Av. Paulista, 807, Espaço Paulista) + mapa embed do Google Maps + contador regressivo (JS, alvo 01/10/2026 09h BRT, com fallback noscript)
- APRENDIZADOS — 4 bullets do que será ensinado, grid com check
- PALESTRANTES — Tereza Rici (Senior Account Executive, Buzzmonitor) + Barbara Gomes (Speaker convidada, Ana Couto), foto e logo da empresa de cada uma
- CRONOGRAMA — timeline de 5 etapas (seção escura, roxo)
- PROVA SOCIAL — quote do Bruno Braga + CTA
- NUMEROS — "+ de 1000 clientes" + CTA
- CONTATO — email e WhatsApp
- FOOTER — redes sociais + copyright + política de privacidade

## Estado

- [x] HTML gerado
- [x] OG image 1200×630 → `assets/og-buzztalk-gestao-multimarcas-para-agencias.png` (gerada via Chrome headless a partir de `assets/og-template-buzztalk-gestao-multimarcas-para-agencias.html`)
- [x] Revisão (frontend-design review + web-design-guidelines) — ver `REVISAO.md` (6 críticos corrigidos: contraste do botão laranja, 4 textos inventados removidos, fallback do contador)
- [ ] Formulário integrado — rodar `/lp-integrar-form buzzmonitor/buzztalk-gestao-multimarcas-para-agencias [snippet]`
- [ ] **BLOQUEADOR antes de publicar ao vivo** (não é só nice-to-have — a página não pode ir ao ar assim):
  - [x] Endereço do evento — confirmado 2026-08-27 (Av. Paulista, 807, Espaço Paulista Promoções Eventos) + mapa embed
  - [x] Palestrantes confirmados 2026-08-28 — Tereza Rici (Senior Account Executive, Buzzmonitor) e Barbara Gomes (Speaker convidada, Ana Couto), fotos + logos das empresas
  - [ ] Formulário real conectado a um provedor (Jotform/RD Station/HubSpot) via `lp-integrar-form`
- [ ] **Nota de infra:** o embed do Google Maps exige `https://www.google.com` em `frame-src` — já patcheado em `landing-pages/dominios/content-buzzmonitor-com/vercel.json` (mudança em arquivo mecânico do guarda-chuva, PR provavelmente cai em `precisa-revisao-victor` em vez de auto-merge, ver CONTEXT.md §2.6)
- [ ] Publicado — rodar `/lp-publicar buzzmonitor buzztalk-gestao-multimarcas-para-agencias content.buzzmonitor.com`

## Assets referenciados

- `../../brand/buzzmonitor/assets/logos/logo-primary.svg` (header)
- `../../brand/buzzmonitor/assets/logos/logo-reversed.svg` (footer)
- `../../brand/buzzmonitor/assets/logos/logo-icon.png` (favicon)
- `./assets/evento-plateia-buzzmonitor.jpg` (foto de plateia de edição anterior do evento, fundo com parallax da seção de prova social, fornecida pelo usuário em 2026-08-27)
- `./assets/BuzzTalksLogo.png` (logo oficial da série Buzz Talks, único logo do header, fornecida pelo usuário em 2026-08-27)
- `./assets/palestrante-tereza-rici.jpg` (foto da palestrante Tereza Rici, fornecida pelo usuário em 2026-08-28; renomeada de `Tereza Rici.jpeg`)
- `./assets/convidada-barbara-gomes.jpg` (foto da speaker convidada Barbara Gomes, fornecida pelo usuário em 2026-08-27; renomeada de `mediador-barbara-gomes.jpg` quando o papel dela mudou de "Mediador" para "Speaker convidada")
- `./assets/anacouto-logo.png` (logo da agência Ana Couto, empresa da Barbara Gomes, fornecida pelo usuário em 2026-08-28; renomeada de `Anacoutologo.png`)

## Decisão: fotos da LP original não reaproveitadas

O usuário autorizou baixar os assets do GreatPages para replicar a identidade visual. Ao inspecionar, os arquivos eram: 3 fotos de palestrantes de uma edição anterior do evento (pessoas reais, não confirmadas para esta nova edição — "Speaker: à definir" / "Convidado(a): à definir" na página de planejamento), 1 logo de agência parceira terceira sem relação com este evento, e 2 imagens que são apenas o gradiente oficial roxo↔teal da marca (recriado via CSS, sem necessidade do binário). Reutilizar fotos de pessoas específicas para um evento que elas não estão confirmadas para participar seria uma representação factualmente incorreta, então a LP usa apenas formas geométricas e gradiente via CSS (linguagem visual da marca, BRANDBOOK §4) no lugar de fotografia.
