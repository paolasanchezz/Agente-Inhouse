# LP Buzzmonitor — reports-monitoreo-ia-agencias-latam

**Gerado em:** 2026-09-25
**Copy-fonte:** duplicado e traduzido a partir de `landing-pages/buzzmonitor/reports-monitoramento-ia-agencias/index.html` (PT-BR), a pedido da usuária.
**Webinar:** Reportes y Monitoreo con IA para Agencias — 29 de outubro de 2026, 10h México (multi-fuso LATAM)
**Domínio-alvo:** webinar.buzzmonitor.com (guarda-chuva migrado pro CI)

## Decisões tomadas na duplicação/tradução

1. **Data:** a fonte era 6 de outubro. A pedido da usuária, a nova data é **29 de outubro de 2026** (quinta-feira, mesma proporção de dia da semana), escolhida em vez de 22 de outubro pra dar mais tempo de produção/divulgação já que a LP ainda estava sendo construída.
2. **Horário multi-país:** a fonte só mostrava "11h (Brasília)". Como o público ES-LATAM é multi-país, foi adicionado o desdobramento padrão já usado nas demais LPs LATAM da marca: `10:00 MX · 11:00 COL/PER · 12:00 CL · 13:00 ARG · 18:00 ESP` (equivalente real às 11h de Brasília/10h do México, mesmo padrão de `gestion-de-crisis-ia-latam-septiembre-2026`).
3. **GTM:** trocado de `GTM-WFJVK858` (Brasil) pra `GTM-MKQBX2MG` (região LATAM, `brand/buzzmonitor/tracking.json`).
4. **Formulário:** a fonte usa o JotForm compartilhado de eventos BR (`252154974852667`, "BR | MKT | LPs - Eventos Geral"). Trocado pelo JotForm compartilhado de eventos LATAM já usado em `gestion-de-crisis-ia-latam-septiembre-2026`, `webinar-atencion-multicanal-latam` e `social-listening-mayo-2026-latam`: **`261188302248052`**.
5. **Links institucionais/JSON-LD:** `sameAs`/URL da Organization trocados de `buzzmonitor.com` (BR) + Instagram `@buzzmonitorbr` pra `buzzmonitor.com/es/` + Instagram `@buzzmonitor.es`, seguindo o padrão já confirmado nas outras LPs LATAM da marca.
6. **Rodapé:** o link de Política de Privacidade (`buzzmonitor.com/politica-de-privacidade/`, só existe em PT) foi **removido** em vez de adivinhar uma URL em espanhol não confirmada — mesma decisão já tomada em `gestion-de-crisis-ia-latam-septiembre-2026`, cujo rodapé também não tem esse link.
7. **Locale de formatação de número** (contagem animada da prova social): trocado de `toLocaleString('pt-BR')` pra `toLocaleString('es-419')`.

## Conteúdo mantido tal como no original (sem alterar o mérito), a pedido explícito da usuária

- **FAQ (5 perguntas)**: respostas a objeções reais de vendas, com a mesma ressalva do LP fonte — **vale revisar com o time comercial antes de publicar/anunciar**, já que são respostas específicas sobre franquia, licença multi-cliente, dado retroativo, setup e acesso do cliente final. A usuária confirmou "me parece bien", sem pedir mudanças.
- **"Cupos limitados"** (seção final, perks): mantido tal como no original ("Vagas limitadas"), apesar da seção de urgência ter sido reescrita no LP fonte pra tirar o tom de escassez — essa frase específica não foi alterada lá, então não foi alterada aqui.

## Ajustes pós-primeira-entrega (2026-09-25, 2ª rodada)

1. **Dado de mercado trocado**: o "92% das empresas brasileiras" (dado BR, não LATAM) foi substituído por um dado genuinamente regional, pesquisado via WebSearch/WebFetch e verificado por citação literal (não estimado/calculado): **"69% de las empresas en Latinoamérica ya usa IA para generar contenido de marketing"**, fonte "Evolución del Marketing en Latinoamérica 2026" (NTT DATA + IAB México + Tecnológico de Monterrey, 775 entrevistas a ejecutivos C-Level em 10 países). Outros dados do mesmo estudo (não usados aqui, mas disponíveis se quiser trocar): "45% aplica IA em marketing conversacional"; "empresas sem IA implementada caíram de 26% para 3%".
2. **Seção de Speakers adicionada** ("Con quién vas a aprender"), reaproveitando 1:1 o HTML/CSS/fotos de `agentes-automatizacion-junio-2026-latam`: **Nadia Lezcano** e **María José Ramírez**, ambas "Business Development" — fotos copiadas de `agentes-automatizacion-junio-2026-latam/assets/{nadia,maria}.jpg` pra `assets/` desta LP. Posicionada entre "Para quién" e "Prueba social" (mesma posição relativa do LP de referência, entre "Para quem" e "Urgência").
3. **Countdown trocado de embutido no ticket pra seção independiente**: removido o widget `.box-countdown` de dentro do card "Save the date"; adicionada a seção `.countdown-wrap` (fundo roxo cheio, D/H/M/S grande) logo abaixo do hero, reaproveitando 1:1 o HTML/CSS/JS de `agentes-automatizacion-junio-2026-latam` (mesmos ids `cd-d/cd-h/cd-m/cd-s`, mesma função de "flip" ao trocar o numero). Alvo mantido: 29/10/2026 10:00 Cidade do México (UTC-6).
4. **Seção "Prueba social" trocada de cards de numero animado pra mural de logos + KPIs sobrepostos**, reaproveitando 1:1 o HTML/CSS de `agentes-automatizacion-junio-2026-latam` (`.mural-stage`/`.mural-frame`/`.mural-track`/`.kpi-overlay`) e as imagens **compartilhadas da marca** `brand/buzzmonitor/assets/murais/mural-1.jpeg` e `mural-2.jpeg` (mesmo asset usado em dezenas de outras LPs Buzzmonitor — não é um asset novo/inventado). Os 4 KPIs (1.000+, 300+, 500+, 10k) são os mesmos numeros que já estavam nos cards antigos, só que agora sobrepostos ao mural em vez de contarem animados. Script JS orfão de contagem animada (`.stat-card .num[data-target]`, sem mais elemento na pagina) removido.

## Estado

- [x] HTML gerado (tradução completa, ES-LATAM)
- [x] Manifest atualizado (`dominios/webinar-buzzmonitor-com/manifest.json`)
- [x] OG image 1200×630 → `assets/og-reports-monitoreo-ia-agencias-latam.png` (gerada via `assets/render_og.py`, adaptando `og-source.html` de `gestion-de-crisis-ia-latam-septiembre-2026`, mesma paleta/logo/estrutura, copy propria: "Reportes y Monitoreo con IA", 29 de octubre, 10:00 MX)
- [ ] Revisão de design (`/lp-revisar`)
- [ ] Confirmação da Catharina sobre o dado "92%" e as respostas do FAQ (ver acima)
- [x] Publicado — autorizado pela usuária em 2026-09-25 ("hazlo así y publicala!")

## Notas linguísticas (ES-LATAM)

- Tratamento: **tú** (informal), consistente em toda a página (nunca "usted"/"vosotros").
- "relatório" → **reporte** (não "informe"), conforme padrão linguístico ES-LATAM.
- CTA reaproveitado das demais LPs LATAM da marca: "Quiero mi lugar gratis" (substituindo "Garantir minha vaga"/"Quero minha vaga").
- Zero em-dash, `&hellip;` mantido (não `...` literal), sem "vosotros", sem vocabulário de Espanha.
