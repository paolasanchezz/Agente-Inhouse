# LP Buzzmonitor · workshop-reportes-ia-cdmx-diciembre-2026

> Duplicada de `workshop-reportes-ia-cdmx-octubre-2026` em 2026-11-13 (original intacta). Unicas mudancas: data **Jueves 3 de diciembre, 9:30 h** (mesmo local: Hotel Fontan Reforma), 3a speaker **Adriana Uriostegui** (Business Development Representative; foto `assets/adriana-uriostegui.png`, recorte 800x800, grid de speakers 3 colunas / 2 em tablet / 1 em mobile) e JSON-LD com 3 performers. Form: mesmo Jotform LATAM `261188302248052` ja usado na original. OG regerada com a nova data (linha de data repintada sobre a OG da original).

---

# LP Buzzmonitor · workshop-reportes-ia-cdmx-octubre-2026

> Duplicada de `workshop-reportes-ia-octubre-2026-latam` (Bogotá) em 2026-10-07, trocando tudo de Bogotá por Ciudad de México.

**Evento:** Workshop "Cómo automatizar reportes de crisis, competencia y tendencias con IA" (7 analistas, 1 solo chat) · presencial y gratuito · [DÍA] [DD] de octubre de 2026, 16:00 h (Ciudad de México, UTC-6)
**Local:** [VENUE] · [DIRECCIÓN], Ciudad de México, MX
**Speaker:** [SPEAKER], [CARGO] (foto pendente em `assets/speaker-cdmx.png`)
**Regiao:** LATAM (es-419, variante MX: "computadora") · GTM `GTM-MKQBX2MG`
**Dominio alvo:** `evento.buzzmonitor.com/workshop-reportes-ia-cdmx-octubre-2026` (guarda-chuva de eventos presenciais)
**Copy-fonte:** mesma da LP de Bogotá → `copy.txt`

## Placeholders a preencher antes de publicar

Buscar `[` em `index.html` e `copy.txt`: `[VENUE]`, `[DIRECCIÓN]`, `[DÍA]`, `[DD]`, `[FECHA CORTA]` (navbar), `[SPEAKER]`, `[CARGO]`, `[BIO DEL SPEAKER]`. No JSON-LD: `startDate` `2026-10-[DD]T16:00:00-06:00`.

## Cortes feitos na copy (pedido: "corte o que nao e essencial, otimizado pra conversao")

- Secao "Buzzmonitor + Claude" (Trends / Mis Proyectos / Mi CRM): detalhe de produto, nao de evento.
- Lista "Que aprenderas" (10 itens): repetia os 7 analistas + a dinamica.
- Bloco de dados do evento repetido no fecho e o form de 7 campos (usa o Jotform LATAM compartilhado).
- Descricoes dos 7 analistas encurtadas para 1 frase.
- v2: copy toda reenfocada em "automatizar reportes de Social Media con IA" (pedido do Victor, 23/09).
- "computadora" (uso do México; a de Bogotá usa "computador").

## v10 (2026-10-14) — sem computadora + Cuándo/Dónde em destaque

Removida toda mencao a levar computadora (hero, registro, "Para quién"; lede do registro vira "Es presencial, gratis y práctico."). No hero, a linha de fatos vira uma tarjeta "Cuándo / Dónde" antes do CTA (data, hora, hotel e endereco). Hero continua cabendo em 1366×768 (media query de altura).

## v9 (2026-10-13) — speakers confirmadas

Lorena Rodríguez e María José Ramírez Rincón (Business Development Representative). Secao vira "Quiénes te acompañan" com 2 cards centrados. Fotos: fundo removido com Vision (macOS, recorte de sujeito), enquadramento de busto 800×800, reescala Lanczos + unsharp leve (sem retoque de pele). JSON-LD Event com 2 performers.

## v8 (2026-10-13) — data e local confirmados

Quarta 28 de outubro, 9:30 h, Hotel Fontan Reforma (Av. Paseo de la Reforma 24, Colonia Centro, Cuauhtémoc, CDMX). Aplicado no header, hero, registro, cierre ("El 28 de octubre, deja de armar reportes."), meta descriptions, JSON-LD Event (startDate + location) e na OG (linha de data e local). Speaker segue "Por definir".

## v7 (2026-10-07) — direcao premium

Pedido: menos "candy cane". Roxo dominante + laranja so como acento; sem blocos rosa nem pilulas coloridas (H1: "reportes" em laranja, "Claude y Buzzmonitor" com sublinhado fino); formas do brandbook em linha fina (1.5px) e glow suave no lugar de formas solidas; kicker = linha + ponto; ticker sem contorno; bolhas/chips/botoes em roxo; borda fina estatica no form; cierre roxo profundo (#2A0140) com glow e arcos finos, tag "Cupos limitados" em contorno. Pesos tipograficos de 900 para 800/700. Bloco CSS "PREMIUM (v7)" no fim do <style>. Versao anterior salva no scratchpad (index-candy.html).

## v6 (2026-10-07) — hero do Ulises + secao Problema removida

- Hero com copy literal do Ulises: nome "7 analistas, 1 solo chat" (1 linha, gradiente vermelho→laranja), H1 "Automatiza tus reportes con Claude y Buzzmonitor", sub "crisis, competencia y tendencias", body com **workshop presencial** em negrito (tambem no badge).
- Secao PROBLEMA ("Así se te va la tarde") removida; alternancia de fundos branco/off-white reajustada. Hero sem min-height (menos ar vertical).

## v5 (2026-10-07) — copy nova + hero em 1 tela + redes LATAM

- Copy reescrita (`copy.txt` v4): H1 "Deja de armar reportes. Empieza a pedirlos." (dor primeiro, fundamentos §0), nome oficial do workshop como overline, callback do H1 no cierre. Substitui H1/H2/sub escritos pelo Victor na v3 (pedido do Ulises).
- "armar" riscado com linha rosa animada; "pedirlos." na pilula roxa.
- Hero cabe em 1440×900 (quase todo em 1366×768); formas do brandbook distribuidas com parallax; QA automatico de sobreposicao forma×texto em 7 larguras = 0.
- Footer com redes LATAM (Instagram, X, Facebook, LinkedIn, YouTube), mesmas da LP oferta-webinar-reports-monitoreo-agencias.

## v4 (2026-10-07) — hierarquia + formas do brandbook + mock estilo Claude

- H1 em 4 niveis (texto literal): "Cómo automatizar" pequeno · "reportes" gigante + mosaico de formas girando · "crisis," em bloco rosa · "competencia" contorno · "tendencias" laranja · "con IA" em pilula roxa com semicirculo em gradiente.
- Formas geometricas do BRANDBOOK §Elementos Visuais (circulos, semicirculos, triangulos, arcos) no hero, kickers (trio circulo/semicirculo/triangulo), separadores do ticker, icones dos analistas, fundos de registro/problema/skills e no cierre (substituem os blobs).
- Mock do hero: interface estilo Claude (sidebar, compositor digitando, tool call "Buzzmonitor" com o icone da marca, card do artifact) abrindo um dashboard Buzzmonitor (KPI com count-up + sparkline, donut de sentimento, grafico de area com pico de crise, recomendacoes). Numeros do mock (12,480 / 38%) sao ilustrativos — decorativo, `aria-hidden`.
- `assets/logo-icon.png` copiado do brand (icone usado no mock).

## v3 (2026-10-07) — redesign dinamico

Pedido: versao mais dinamica, nada generica, identidade Buzzmonitor (laranja/vermelho/roxo), base branca, minimalista mas nao plana, muitas animacoes (moderna/tecnologica). Copy e placeholders intactos (diff literal com `copy.txt`; 0 em-dash).

**Desvio consciente do GUIDELINES §4** ("motion em 2-3 momentos"): a pedido explicito, a LP tem motion em quase toda secao. Tudo desliga com `prefers-reduced-motion` e nenhum texto depende de animacao (gate `html.js` + `<noscript>` + timeout de 4s).

Animacoes: entrada do hero palavra a palavra + sublinhado desenhado em "con IA" (gradiente com shimmer) · mock em loop (digita a pergunta → "escribiendo" → reporte com barras crescendo) com tilt 3D seguindo o mouse e orbitas girando · grade de pontos com spotlight no cursor · ticker com os 7 analistas · borda conica girando no form · X vermelhos desenhados no problema · ponto viajando entre os 3 passos · cards de analistas com spotlight e stagger · timeline que preenche com o scroll + bolhas de chat em sequencia · chips flutuando · cierre com blobs rosa/laranja, grao e tag balancando · botoes magneticos com brilho · barra de progresso de leitura. Fonte nova: JetBrains Mono (labels tecnicos). Versao anterior: historico do chat / scratchpad.

## Estrutura

| # | Secao | Fundo |
|---|---|---|
| 1 | Hero: badge presencial/gratuito, H1 "Cómo automatizar reportes de crisis, competencia y tendencias con IA", H2 + sub do Victor, CTA, linha de fatos (data, local, gratis) + mock chat→reporte | branco |
| 2 | Registro + Jotform (ToFu → form na 2.a secao, GUIDELINES §10) | off-white |
| 3 | Problema (4 X vermelhos) | branco |
| 4 | Skills: 3 passos | off-white |
| 5 | 7 analistas (grid 4+3) + CTA | branco |
| 6 | Dinamica: 3 rondas com bolhas de chat | off-white |
| 7 | Speaker | branco |
| 8 | Para quien (chips) | off-white |
| 9 | Fecho/urgencia (roxo + tag laranja rotacionada) | roxo |

Paleta: roxo `#390155` (tinta/CTA) + laranja `#EB7C2E` (acento); gradiente unico rosa→laranja (barras do mock, placa atrás do mock e "con IA" do H1). v2 (23/09): hero refeito a pedido do Victor (tema reportes; saiu o ingresso inclinado).

## Formulario

Jotform LATAM compartilhado `261188302248052` ("Webinars Buzzmonitor LATAM"), o mesmo form do Buzzmonitor Connect de julho e de outras LPs LATAM. **Nao editar o form** (muda todas as LPs que o usam). Campos: nome completo, correo profesional, empresa, cargo, pais, opt-out newsletter. Nao pede WhatsApp nem sobrenome separado (a copy original pedia).

## Pendencias

- [ ] Publicar via `/lp-publicar buzzmonitor workshop-reportes-ia-cdmx-octubre-2026 evento.buzzmonitor.com` (manifesto + PR → CI).
- [ ] Preencher placeholders (venue, endereço, data, speaker + bio).
- [ ] Foto do speaker em `assets/speaker-cdmx.png` (512×512).
- [ ] **Regerar OG** `assets/og-workshop-reportes-ia-cdmx-octubre-2026.png` — a atual é cópia da de Bogotá (data 07, Tinkko, Bogotá).
