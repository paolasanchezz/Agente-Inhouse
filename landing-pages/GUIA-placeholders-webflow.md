# Playbook — Placeholders provisórios de imagem para LPs no Webflow

Guia reutilizável para montar uma landing page inteira **sem depender das imagens finais**, deixando cada imagem trivialmente substituível depois. Nasceu da reprodução da LP `ia-para-social-listening` (Buzzmonitor) via MCP do Webflow (superfície headless `data_*`).

---

## 1. Princípio

Nenhuma imagem "de verdade" é embutida na fase de construção. Todo lugar que vai receber imagem é um **placeholder nomeado**. Isso permite validar layout, cor, tipografia, animação e copy antes de existir qualquer arte, e torna a troca posterior um casamento direto por nome.

**Por que não usar `<img>` direto no build headless:** o `data_whtml_builder` converte `<img>` do HTML numa tag inválida (`imgraw`) que **não renderiza**. Além disso, imagem real amarra o build a ter o arquivo pronto. O placeholder nomeado evita os dois problemas.

---

## 2. Anatomia do placeholder

Um bloco (`div`) com:
1. **Borda tracejada + fundo neutro** — deixa claro que é temporário.
2. **Ícone genérico** (ex.: ícone de "foto").
3. **Rótulo em texto = o nome exato do asset** (ex.: `img-social-listening`), em fonte monoespaçada.

Variações por formato (mesma ideia, tamanhos diferentes): tile de logo (retângulo), ícone social (quadrado), mockup de seção (retângulo grande), logo pequeno (header/rodapé/depoimento).

> Regra de CSS no headless: **apenas seletores de classe única** (sem descendente, sem elemento puro, sem `!important`). Cada placeholder tem sua própria classe completa.

---

## 3. Convenção de nomes (o pulo do gato)

**Regra de ouro:** o rótulo do placeholder = o `displayName` do asset no Webflow (ignorando a extensão). Assim a substituição é um casamento direto por nome.

Padrão em `kebab-case`, minúsculas, sem acento/espaço; o prefixo indica a natureza e o nome descreve **o papel na página** (não o conteúdo específico — troca o cliente e o nome continua válido):

| Tipo | Padrão | Exemplos |
|---|---|---|
| Logo da marca | `logo-{marca}` (+ `-branco` p/ fundo escuro) | `logo-buzzmonitor`, `logo-buzzmonitor-branco` |
| Logos de clientes (lista) | `img-cliente-NN` (2 dígitos) | `img-cliente-01` … `img-cliente-11` |
| Ícones sociais (por rede) | nome puro da rede | `facebook`, `instagram`, `youtube`, `threads`, `bluesky`, `tiktok`, `linkedin`, `whatsapp`, `g-business`, `g-play`, `email`, `wordpress`, `reclame-aqui`, `pinterest`, `reddit` |
| Mockups de seção (por função) | `img-{funcao}` | `img-social-listening`, `img-ai-insights`, `img-monitoramento-audiovisual`, `img-gestao-crises` |
| Imagem de bloco | `img-{bloco}` | `img-experimente-14-dias` |
| Logos de depoimento | `logo-depoimento-NN` | `logo-depoimento-01/02/03` |

---

## 4. Fluxo de substituição (quando os arquivos existirem)

O cliente sobe os arquivos nos **Assets** do Webflow com o `displayName` = nome do placeholder. Para cada placeholder:

1. **Listar assets** (`data_assets_tool > list_assets`) e casar `displayName` → `assetId`.
2. **Localizar o tile** e os IDs dos filhos (`data_element_tool > query_elements`, filtrando por classe; use `children_depth` e leia o texto do rótulo para mapear com certeza — a ordem do `query` nem sempre é a do DOM).
3. **Criar um elemento `Image` de verdade** dentro do tile ligado ao asset (`data_element_builder`, `type: Image`, `set_image_asset: { image_asset_id }`, `set_style` com a classe de imagem contida).
4. **Remover os filhos do placeholder** (ícone + rótulo) e **trocar a classe** do container (tirar a borda tracejada) via `set_style`.
5. **Publicar** (`data_sites_tool > publish_site`, `publishToWebflowSubdomain`).

> Não existe "trocar a imagem original": o placeholder nunca foi imagem. É **criar Image novo + limpar o placeholder**.

**Marquees/loops:** se um item aparece 2× (duplicata para loop sem emenda), troque **as duas ocorrências**. Mapeie cada tile pelo texto do rótulo, não pela posição.

---

## 5. Prévia antes do Webflow

A prévia inline (no chat) usa as **mesmas caixas nomeadas** — o sandbox bloqueia imagens de domínios externos, então valida-se layout/ordem/copy sem arte real. A fidelidade visual das imagens fica para o site publicado (onde os assets do Webflow carregam).

---

## 6. Checklist de entrega ao cliente

- Gerar uma **lista das imagens por seção** com o nome exato de cada placeholder, para o cliente subir nos Assets com o mesmo nome (ver exemplo em `landing-pages/buzzmonitor/webflow-teste-claude-imagens-checklist.md`).
- Seções sem imagem (form embedado, vídeo, blocos só de texto) não entram na lista.

---

## 7. Armadilhas técnicas do MCP do Webflow (headless `data_*`)

Aprendidas reproduzindo LPs via a superfície headless (`data_whtml_builder`, `data_element_tool`, `data_style_tool`, `data_assets_tool`, `data_sites_tool`). Os `data_*` operam por `siteId`+`pageId` — **não precisam do Designer aberto** (evita o congelamento das tools Designer live).

- **CSS só com seletor de classe única.** Proibido: descendente (`.card img`, `.bzp h1`), elemento puro e `!important`. Cada elemento precisa da sua própria classe completa. Combo na mesma tag via `class="a b"` é ok (as regras CSS são `.a` e `.b` separadas).
- **`<img>` no whtml vira `<imgraw>`** — tag inválida que **não renderiza**. É a razão central da estratégia de placeholder deste guia. Para imagem real: subir asset e criar elemento `Image` (`data_element_builder` type `Image` + `set_image_asset`).
- **`style` inline no whtml vira classe auto `inline-span-N`**, e os nomes **colidem entre chamadas** (cada chamada reinicia em `-0`) → estilos vazam entre elementos. Nunca use `style` inline; crie classe dedicada (`data_style_tool`) e aplique com `set_style`.
- **`@keyframes` e `<style>` proibidos no whtml.** Animação precisa vir de fora. `<link>` só sobrevive como **elemento raiz** do html (aninhado dentro de `<div>` é descartado).
- **Custom code / scripts de site/página = 404 no plano gratuito** ("Custom code block not found"). Workaround: injetar Google Fonts via `<link>` raiz no body (whtml prepend) em vez de custom code; construir na página existente (criar página nova também é gateado: "User is not able to create pages").
- **Timeout ≠ falha.** Chamadas de build frequentemente retornam timeout mas **aplicam no servidor**. Sempre re-consultar o estado (`query_elements`) antes de retentar, pra não duplicar. `504` sustentado pode atingir só o endpoint de insert enquanto leitura/`publish_site` seguem ok — transitório, esperar e retentar.
- **Upload de asset por URL:** `pages.greatpages.com.br` é **bloqueado** no fetch server-side do Webflow (PNG/webp dão "Failed"); usar o domínio `files.greatpages.com.br/arquivos/paginas_editor/...` (funciona). SVG/JPG às vezes passam mesmo no `pages`.
- **Publicar:** `data_sites_tool > publish_site` com `publishToWebflowSubdomain` → `{slug}.webflow.io`.

> Estas armadilhas foram validadas nos plano/contas atuais (superfície `data_*` reconectada em 2026-06). Se o comportamento do MCP mudar, atualize esta seção — ela é a fonte-verdade no repo, não uma memória de máquina.
