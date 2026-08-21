# Revisao LP — buzzmonitor/gestion-crisis

**Data:** 2026-08-07
**Auditores:** auditoria manual (fidelidade de copy + GTM + SEO + GUIDELINES) seguindo o mesmo checklist aplicado em `caso-smartfit`, `primer-listening-5-pasos` e `webinar-atencion-multicanal-latam`

## Auditorias que passaram sem achados

- **Fidelidade de copy:** todo texto visivel (H1, SUB, overlines, 5x H3/BODY/LABEL de "Lo que vas a ver", H2/2x LABEL de Resultados, bio + tags de Lorena, 4x LIST ITEM de "Para quien es", H2/BODY/LABEL/CTA final) bate literal com `copy.txt`, conferido frase a frase. `get_page_text` do preview confirma o texto renderizado identico ao copy-fonte.
- **Anti-IA:** em-dash 0 (`grep -c '—'` = 0). Ellipsis: 1 ocorrencia ("si&hellip;"), corretamente como `&hellip;`, nao literal "...".
- **GTM:** `GTM-MKQBX2MG` presente 2/2 (head + noscript), validado tambem por `landing-pages/build/check_gtm_region.py` (regiao latam OK).
- **SEO:** 1 meta description, 14 tags `og:`/`twitter:` combinadas, JSON-LD com 3 nos (Organization + WebPage + Article) todos coerentes com o slug `gestion-crisis`, 1 `canonical`.
- **build_umbrella.py:** rodou contra o manifest atualizado (32 LPs, 0 avisos) — sem quebra de outras entradas do guarda-chuva.
- **GUIDELINES §9 (copy dita estrutura):** grid de "Lo que vas a ver" tem 5 cards (nao os 3 do template de referencia `caso-smartfit`), porque a copy trouxe 5 componentes numerados 01-05. Grid de Resultados tem 2 cards (nao 4), porque a copy so trouxe 2 LABELs de stats. Nenhum card vazio ou duplicado pra preencher espaco.
- **GUIDELINES §16 (hreflang):** nao ha LP-irma em outro idioma pra `gestion-crisis` — corretamente omitido hreflang, so `canonical` presente (mesmo padrao ja corrigido em `caso-smartfit`).
- **GUIDELINES §14 (`min-height:0`):** presente no `<img>` da foto do speaker (herdado do CSS compartilhado, `.speaker-photo-frame img { min-height: 0; }`).
- **Acessibilidade:** skip-link, `:focus-visible`, alt em imagens informativas (foto da Lorena com alt descritivo), decorativos (`decor-*`, `speaker-photo-decor`, `results-logos` container, icones de check) marcados `aria-hidden`, `prefers-reduced-motion` coberto globalmente.
- **Uso do logo do cliente (CRM Bonus):** autorizado explicitamente pelo usuario apos esclarecimento sobre a relacao E-CLIK/CRM Bonus (ver `README.md` e nota no `copy.txt`) — nao foi decisao unilateral da skill.
- **Adaptacoes de design vs. template de referencia:** removido o `hero-card-logo` do formulario do hero (presente em `caso-smartfit` porque e caso de cliente com logo proprio; esta LP e webinar, sem logo de cliente no hero) — decisao de design consistente com as demais LPs de webinar desta leva (`primer-listening-5-pasos`, `webinar-atencion-multicanal-latam`).

## Nenhum critico encontrado

Como o HTML foi gerado diretamente a partir do template ja revisado e publicado de `caso-smartfit` (que ja passou por 2 rodadas de correcao de criticos: hreflang removido, lazy-loading corrigido), o CSS compartilhado ja vem limpo. As unicas mudancas estruturais (5 cards de programa, 2 cards de resultado, ausencia de logo de cliente no hero) sao adaptacoes de conteudo previstas no proprio grid responsivo, sem necessidade de ajuste de CSS.

## Verificacao de assets (preview local)

- `./assets/crm-bonus-logo.jpg` carrega corretamente (447x447, confirmado via `naturalWidth` no preview).
- `./assets/lorena-rodriguez.jpg` e os logos `../../brand/buzzmonitor/assets/logos/*.svg` nao carregaram no preview `file://` local (limitacao conhecida da ferramenta de preview pra arquivos fora de um servidor real — mesmos caminhos relativos ja confirmados funcionais em producao em `caso-smartfit`). Confirmacao definitiva sera feita via HTTP real apos o deploy CI.

## Proximos passos

- CTA ainda e mock (`href="#form"`, formulario local sem backend) — quando tiver o link real de inscricao, rodar `/lp-integrar-form buzzmonitor/gestion-crisis "snippet"`.
- Publicar: `webinar.buzzmonitor.com` esta no fluxo CI — adicionar ao manifest (ja feito) + abrir PR.

## Segunda passada (2026-08-07, pos-publicacao)

Usuario reportou apos ver a LP no ar: (1) pedido de troca de overline/H2 de "Lo que vas a ver" e (2) logos da secao Resultados ilegiveis por serem pequenos demais.

- **Texto:** overline trocado para "Lo que aprenderás", H2 para "Cinco pasos para detectar y gestionar una crisis, con el caso real de E-CLIK." — aplicado identico no `copy.txt` e no `index.html`, conferido literal.
- **Logos:** `.results-logos img` aumentado de `height: 26px` para `44px` (69% maior), gap de 18px para 24px, separador "×" de 14px para 18px. Mudanca de CSS e local a este arquivo (nao afeta `caso-smartfit`, que tem seu proprio bloco `<style>` inline).
- Revalidado: em-dash 0, ellipsis so `&hellip;` (1 ocorrencia), GTM 2/2, `check_gtm_region.py` OK.
- Nenhuma outra secao ou LP tocada.

## Terceira passada (2026-08-07, polimento visual dos logos)

Usuario pediu pra melhorar ainda mais a apresentacao dos logos ("mas grandes o mas bonitos"). Diagnostico: `crm-bonus-logo.jpg` e um quadrado JPEG com fundo preto solido (sem transparencia) — a 44px, flutuando sobre o fundo cinza claro da secao, lia como um recorte solto, nao como um elemento desenhado.

- **Tamanho:** `.results-logos img` de 44px para 52px; gap de 24px para 26px; separador "×" de 18px para 20px.
- **Tratamento visual (novo):** classe `.client-logo` adicionada so ao `<img>` do CRM Bonus (nao ao logo Buzzmonitor, que e SVG transparente e ja se integra bem) — `border-radius: var(--radius-md)` (cantos arredondados, mesmo token usado em cards) + `box-shadow: var(--shadow-md)` (mesma sombra usada em `.hero-form`), pra que o quadrado preto pareça um badge de marca intencional em vez de um screenshot colado.
- Revalidado: em-dash 0, GTM 2/2.

## Quarta passada (2026-08-20 — resumo do texto + resultados ampliados)

Victor pediu (via Paola), pro texto de um case real de E-CLIK que ele mandou: (1) resumir o BODY das 5 tarjetas de "Lo que aprenderás" e (2) trazer mais dados pra secao de Resultados.

- **Resumo das 5 tarjetas:** BODY reescrito mais curto em cada uma, mantendo toda funcionalidade/dado ja presente (Theme Monitoring, classificacao por sentimento, identificacao de perfis/alcance, evolucao hora a hora, comparacao antes/depois, alertas + Buzz Pills). Nada foi cortado que mudasse o significado, so reduzida a redundancia de frases. LABELs ("Qué vas a ver") mantidos, ja eram curtos.
- **Resultados:** o texto longo do caso (fornecido por Victor) so trouxe os 2 dados numericos que ja estavam na LP (crisis <1h, 28 melhorias) — nao havia mais cifras verificaveis. Em vez de inventar numero (proibido pelo Brandbook), foram adicionados 2 insights qualitativos extraidos literalmente do texto do caso: centralizacao de canais (redes sociais + valoracoes de apps num so painel) e cruzamento de dados pra analise de VOC. Nenhum dos dois repete o card de "alertas automaticas" ja coberto em "Lo que aprenderás" (05).
- **Titulo da secao:** trocado de "Los números del caso" pra "Los resultados del caso" — acomoda o conteudo misto (2 numericos + 2 qualitativos) e reusa o mesmo titulo ja usado em `caso-smartfit`.
- **Grid:** `.results-grid` ja usa `grid-template-columns: repeat(2, 1fr)` — 4 cards caem naturalmente em 2x2, sem precisar mudar CSS.
- **Nao tocado:** a integracao real com ClickMeeting (formulario, `/api/next-webinar`, `/api/clickmeeting-register`, redirect pra `/gestion-crisis-confirmado`) que ja estava no arquivo — essa parte foi integrada em outra sessao/PR, fora do escopo deste ajuste, e permaneceu intacta.
- Revalidado: em-dash 0 (as 2 ocorrencias de "..." literais encontradas sao strings de JS pre-existentes do form — "Enviando...", "Redirigiendo..." — nao sao copy visivel nem foram tocadas nesta passada), GTM 2/2, `check_gtm_region.py` OK.
