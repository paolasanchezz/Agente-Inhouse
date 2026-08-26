# institucional

LP do guarda-chuva **content.cxpress.io** (projeto Vercel `cxpress-lp-playbook-whatsapp2026`).
URL final: `https://content.cxpress.io/institucional`.

Portada do site institucional proprio da marca (`https://home.cxpress.io/`, WordPress) para
uma LP estatica de conversao unica. Origem capturada em 2026-08-26.

- **lang:** `pt-BR`
- **GTM:** `GTM-T4XDWHL3` (brasil, via `brand/cxpress/tracking.json`)
- **Formulario:** Jotform `261027639617663` ("LPs - Proposta"). Escolhido por ser o form de
  proposta usado hoje pela maioria das LPs Cxpress e por **nao** ser a variante de remarketing.
  A alternativa e o `261045149477663` ("CXPRESS BR | MKT | LPs - Proposta | REMARKETING"),
  que faz mais sentido se esta LP for receber trafego de remarketing. Trocar = 1 linha no
  embed (`/lp-integrar-form`). A pagina de agradecimento e config do Jotform, nao do embed.

## O que foi removido da origem

| Removido | Motivo |
|---|---|
| `<header class="k92hf-header">` + menu mobile | pedido: LP sem menu |
| Coluna de navegacao do rodape (Navegacao / Funcionalidades / Recursos) | pedido: sem paginas alternativas |
| Blocos "Termos e Politicas" do rodape | eram `href="#"` (links mortos) |
| Icones sociais do rodape | eram `href="#"` (links mortos) |
| Secao Newsletter (Mailchimp, `y7h2k-sec`) | segundo formulario competindo com o de proposta numa LP de conversao unica |
| Credito "Criado por Wibix" | credito do build WordPress, nao se aplica a esta LP |
| Scripts/estilos de plugin WordPress (emoji, handl-utm-grabber, oEmbed, feeds) | sem funcao fora do WP |

Todos os CTAs (`Agendar demonstracao`, `Falar com um especialista`) agora apontam para a
ancora `#proposta`. Nao sobrou nenhum link para `home.cxpress.io` ou `blog.cxpress.io`.

## Diferencas tecnicas em relacao a origem

- **jQuery eliminado.** Os 4 snippets do WordPress (carrossel do hero, contadores, abas de
  solucoes, reveal on scroll) foram portados para JS puro. Zero dependencia externa de script.
- **Fontes via Google Fonts.** A origem servia 12 TTFs (~3 MB) do `wp-content/uploads`, dos
  quais so Open Sans e Inter eram usados. Trocado por Google Fonts.
- **`box-sizing: border-box` explicito.** A origem herdava isso das folhas globais do
  WordPress, que nao foram portadas. Sem essa regra as secoes (`width:100%` + padding)
  estouravam 40px no mobile.
- **Reveal on scroll redundante.** `IntersectionObserver` mais checador por scroll/load, os
  dois idempotentes. O iframe do Jotform desloca o layout depois do load; com o mecanismo
  unico da origem, um elemento acima da dobra podia ficar presa em `opacity:0` ate o
  primeiro scroll.

## Assets

`assets/` tem 43 arquivos LP-local (imagens portadas de `home.cxpress.io/wp-content/uploads`,
referenciadas como `./assets/X`). OG image gerada por `assets/render_og.py` a partir de
`assets/og-template.html` (mesmo padrao das demais LPs Cxpress).

## Validacao

- `build_umbrella.py`: OK, sem avisos para este slug
- `check_gtm_region.py`: 1 OK, 0 bloqueios
- `check_mobile_type.py`: h1=28 corpo=16 min=14, sem overflow real
  (`document.scrollWidth == clientWidth` a 375px; os 4 achados do medidor sao os slides
  fora de tela do carrossel, recortados por `overflow:hidden` no wrapper)
