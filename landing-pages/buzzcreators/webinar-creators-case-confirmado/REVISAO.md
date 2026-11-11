# Revisao LP — buzzcreators/webinar-creators-case-confirmado

**Data:** 2026-11-11
**Auditores:** passada de design (criterios frontend-design + GUIDELINES) e passada de a11y/HTML (Web Interface Guidelines), as duas feitas pelo agente. Checks deterministicos: `check_gtm_region.py`, `bump_mobile_type.py --dry-run`, grep de em-dash e ancora.

## Decisoes preservadas (nao sao achados)

- Autoplay no mudo a partir de 3:00 (`VIDEO_START = 180`), com o botao laranja de som cobrindo o player. O clique ativa o som e volta para 3:00.
- CTAs com `utm_source=webinar&utm_content=agradecimento-perpetuo-creators-case`, na mesma aba e sem repassar as UTMs da URL.
- `noindex, follow`.

## Aplicado automaticamente (3 criticos)

- [x] **Label in Name (WCAG 2.5.3).** O botao de som tinha `aria-label="Ativar o som e assistir do início"`, diferente do texto visivel "O vídeo já começou. Clique para ouvir". Quem usa comando de voz fala o que ve e nao acha o botao. Tirei o `aria-label`, e o nome acessivel agora vem do texto visivel (o SVG ja e `aria-hidden`).
- [x] **Piso tipografico mobile (§20).** `.confirm p` passou de `clamp(17px…)` para `clamp(18px…)` (piso de lead).
- [x] **Ellipsis (§5).** "Carregando o vídeo..." virou "Carregando o vídeo…".

## Checks que passaram / nao se aplicam

- GTM: `status: ok`, `expected: null`, nada injetado. O `dataLayer` ja empurra `lead_webinar_perpetuo_01` e `webinar_perpetuo_01_som_ativado` para quando o GTM entrar.
- Em-dash: 0.
- Fidelidade da copy: **pulada**, porque esta pagina nao tem `copy.txt`. Os textos vieram do roteiro do video, e a marca do case nao aparece.
- Pacote SEO (§15): **nao se aplica**, por ser pagina de agradecimento `noindex`. Nao precisa de canonical, JSON-LD nem OG completa, e o preview social nao deve ser compartilhado.
- Logo: `logo-color.png` (PNG, §19 ok), com link pra home em nova aba.
- Ancora: "Ver o resumo" usa `href="#resumo-title"`, sem JS que grave hash (§22, o build cobre).
- Movimento: o pulso do botao so roda em `prefers-reduced-motion: no-preference`.

## Melhorias opcionais (5)

- [ ] **Piso §20 nao aplicado de proposito em 2 textos dentro do player.** `.video-sound-pill` (15px, o piso de botao seria 17px) e `.video-end-title` (18px, o script sugere 22px) ficam dentro de um player 16:9 que tem ~190px de altura em 375px. Subir a fonte quebra a pilula em 2 linhas e aperta a tela final. Conferir num celular real antes de mexer.
- [ ] **Pausar antes do som (WCAG 2.2.2).** A camada do botao cobre o player inteiro, entao quem usa mouse so alcanca os controles do YouTube (pausar) depois de clicar para ouvir. Pelo teclado da pra chegar no iframe, que vem antes do botao no DOM. Se quiser fechar o ponto, a camada pode cobrir so a faixa de baixo.
- [ ] **Lead disparado em todo carregamento.** `lead_webinar_perpetuo_01` sai tambem em reload e em visita direta. Ja esta no GUIA §5. Se o GTM for usar esse evento como conversao, deduplicar com `sessionStorage`.
- [ ] **`bump_mobile_type.py` sugere +1px** em `.eyebrow`, `.chips li`, `.stat-label` e `.footer`. Todos ja estao no piso de 14px.
- [ ] **Safari/iOS e economia de bateria nao testados** (autoplay no mudo pode nao disparar, e nesse caso o botao de som continua visivel por cima do play).

## Nice-to-haves (1)

- [ ] `.items h3` usa `clamp(22px, 2vw, 22px)`, que na pratica e 22px fixo.

## Proximos passos

- Publicar junto com a captura -> `/lp-publicar buzzcreators webinar-creators-case webinar.buzzmonitor.com` (os 2 slugs no manifesto)
