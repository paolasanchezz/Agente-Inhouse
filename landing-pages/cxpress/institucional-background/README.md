# LP Cxpress — institucional-background

**Criada em:** 2026-10-07
**Destino:** `content.cxpress.io/institucional-background` (guarda-chuva, deploy via CI)

## O que é esta página

É a **versão anterior da `/institucional`**, preservada a pedido da Marielle em 07/10.

Conteúdo congelado no commit `3b683f2`, estado imediatamente anterior ao rebuild da
`/institucional` (PR #750, 06/10). Era uma portada do site WordPress `home.cxpress.io`,
capturada em 26/08.

A `/institucional` atual **não foi tocada** por esta entrega.

## O que mudou em relação ao original

Nada de conteúdo, layout ou copy. Só o que é específico de slug, para as duas páginas
coexistirem:

| Campo | Antes | Agora |
|---|---|---|
| `canonical` | `{{DOMAIN}}/institucional` | `{{DOMAIN}}/institucional-background` |
| `og:url` | `{{DOMAIN}}/institucional` | `{{DOMAIN}}/institucional-background` |
| OG image | `assets/og-institucional.png` | `assets/og-institucional-background.png` (renomeado; o build resolve por `og-{slug}.png`) |
| `robots` | `index, follow` | **`noindex, nofollow`** |

### Sobre o `noindex`

Não foi pedido, foi decisão de quem executou. Duas páginas quase idênticas sobre o mesmo
assunto, no mesmo domínio, competem na busca e diluem a `/institucional`, que é a que
recebe mídia. Como esta é arquivo de referência, fica fora do índice.

Se precisar ranquear, é trocar a linha 16 de volta para `content="index, follow"`.

## Defeitos herdados (de propósito, é um arquivo)

Esta página carrega os problemas que motivaram o rebuild. Ficam aqui porque o pedido foi
preservar a versão anterior como ela era:

- **Sem `font-family` no `body`:** 46 elementos caem em Times New Roman. Era a causa
  principal do rebuild.
- **42 imagens do WordPress** (2,51 MB).
- **Formulário na 8ª de 8 seções**, a 75% do arquivo.
- **Jotform `261034073026647`** (form de Google Ads). A `/institucional` atual usa o
  `261045149477663` (Meta), trocado pelo Guilherme no PR #751.

Não corrigir nada disso sem pedido explícito: o valor desta página é ser o retrato fiel da
versão anterior.

⚠️ A OG image é a da `/institucional`, apenas renomeada. Compartilhada em rede social, o
preview mostra o card da página principal.

---

# Documentação herdada da versão original

O que segue é o README da `/institucional` como estava antes do rebuild, preservado porque
descreve a portada do WordPress que é exatamente o que esta página contém.

LP do guarda-chuva **content.cxpress.io** (projeto Vercel `cxpress-lp-playbook-whatsapp2026`).
URL final: `https://content.cxpress.io/institucional`.

Portada do site institucional proprio da marca (`https://home.cxpress.io/`, WordPress) para
uma LP estatica de conversao unica. Origem capturada em 2026-08-26.

- **lang:** `pt-BR`
- **GTM:** `GTM-T4XDWHL3` (brasil, via `brand/cxpress/tracking.json`)
- **Formulario:** Jotform `261034073026647`, definido pelo Victor em 2026-08-26. Nao e o
  `261027639617663` da unificacao do PR #374: esta LP usa form proprio. A pagina de
  agradecimento pos-submit e config do Jotform, nao do embed, entao ela acompanha este form.
  Trocar = 1 linha no embed (`/lp-integrar-form`).

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
| Imagem flutuante `Group-1707478248.png` (`.z9p2x-float`) na secao de comparativo | pedido do Victor (2026-08-26). Era o badge com o mascote, achatado ~30% na vertical porque declarava `120x300` num arquivo `130x467`. Removida junto com a regra CSS e o asset |

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

`assets/` tem 42 imagens LP-local (portadas de `home.cxpress.io/wp-content/uploads`,
referenciadas como `./assets/X`). OG image gerada por `assets/render_og.py` a partir de
`assets/og-template.html` (mesmo padrao das demais LPs Cxpress).

`icon-facebook.png` e o unico asset que **nao** vem do WordPress: foi montado a partir do
icone canonico do Buzzmonitor (`landing-pages/buzzmonitor/*/assets/icon-facebook.webp`,
circulo 40x40 com ratio 1.000), recolado num tile 50x50 arredondado para bater com a
ocupacao dos vizinhos da fileira (~80%). O circulo entra em resolucao nativa, sem reescala.

## Proporcao das imagens (defeito herdado do WordPress)

Os atributos `width`/`height` de `<img>` sao *presentational hints*: fixam as duas dimensoes
e **distorcem** a imagem quando divergem do arquivo real. A origem trazia 12 imagens com
desvio acima de 5% (o pior caso, 44%, achatava o mascote da Cxpress em ~30% na vertical).
Todos os atributos foram alinhados aos pixels reais do arquivo.

**Pegadinha ao corrigir isso** (aconteceu aqui em 2026-08-26): alinhar os atributos ao
arquivo, sozinho, PIORA a imagem cujo CSS fixa apenas `width`. A largura passa a vir do CSS
e a altura do atributo, e as duas brigam. Foi o caso da faixa de canais do rodape
(`.k2x-icons`): saiu de 6% de desvio para 87%, renderizando 340x333 em vez de 340x44.
A correcao e emparelhada: atributos reais **e** `height: auto` em toda regra que fixa so a
largura. As 5 regras nesta LP (`.h9s2a-card img`, `.k2m8s-head img`, `.z9p2x-head img`,
`.z9p2x-list img`, `.k2x-icons`) ja levam `height: auto`.

Ao adicionar imagem nesta LP, declarar `width`/`height` com a dimensao real do arquivo, ou
omitir os dois; e se o CSS fixar so a largura, garantir `height: auto`. Auditoria rapida
(vale rodar no navegador, que e onde o conflito CSS-vs-atributo aparece):

```bash
py -c "
import re,os
from PIL import Image
h=open('index.html',encoding='utf-8').read()
for m in re.finditer(r'<img[^>]*>',h):
    t=m.group(0)
    s=re.search(r'src=\"\./assets/([^\"]+)\"',t); w=re.search(r'width=\"(\d+)\"',t); v=re.search(r'height=\"(\d+)\"',t)
    if not(s and w and v) or not os.path.exists('assets/'+s.group(1)): continue
    iw,ih=Image.open('assets/'+s.group(1)).size
    d=abs(int(w.group(1))/int(v.group(1))-iw/ih)/(iw/ih)*100
    if d>5: print('%-44s %sx%s vs %dx%d (%.0f%%)'%(s.group(1),w.group(1),v.group(1),iw,ih,d))
"
```

A fileira de canais (`.h9s2a-float img`) tambem usa `object-fit: contain` numa caixa fixa de
45x45, para os arquivos de origem (50x50, 51x50, 150x150) coexistirem sem distorcer.

## Validacao

- `build_umbrella.py`: OK, sem avisos para este slug
- `check_gtm_region.py`: 1 OK, 0 bloqueios
- `check_mobile_type.py`: h1=28 corpo=16 min=14, sem overflow real
  (`document.scrollWidth == clientWidth` a 375px; os 4 achados do medidor sao os slides
  fora de tela do carrossel, recortados por `overflow:hidden` no wrapper)
