# Brand Template do Canva — Buzzmonitor

> **Pré-requisito da skill `/social-canva`**.
> **Abordagem**: 1 template multi-página onde cada página é um layout (capa, narrativa, CTA, e variantes). A skill chama `create-design-from-brand-template` com `page_numbers: [N]` pra pegar a página certa.
> Esse padrão cobre 95% dos carrosséis editoriais do Instagram e deixa fácil expandir conforme novos layouts forem necessários.

## Abordagem em 2 frases

1. **Você tem 1 template** com 3+ páginas. Cada página = 1 layout que a skill vai usar pra um tipo de slide.
2. **Em cada página**, os textos preenchíveis precisam estar **marcados como campos de dataset** com nomes específicos (`TITULO`, `PARAGRAFO`, etc.) — é o que permite a skill preencher via API.

## Como configurar o template no Canva (passo a passo)

### Você já tem 1 template existente: `EAHMXaCZdd4`

Vamos expandir ele em vez de criar do zero.

### Passo 1 — Adicionar páginas ao template

Abrir o template `EAHMXaCZdd4` no editor:

1. No painel lateral esquerdo (ou inferior, dependendo da view) clica em **"+ Add page"** / **"+ Adicionar página"**
2. Cria **3 páginas no mínimo**: Capa, Narrativa, CTA (cada uma com layout diferente — ver especificação abaixo)
3. Mantém **dimensões 1080×1350** em todas as páginas
4. Aplica o brand kit "Buzzmonitor" pra cada (cores, fontes, logos vêm dele)

### Passo 2 — Configurar dataset fields em cada página

**Esse é o pulo do gato.** Em cada caixa de texto preenchível, você precisa **conectar a um campo de dataset com nome específico**.

No Canva Teams, o caminho mais comum é:

- **Painel "Apps"** (menu lateral) → busca **"Bulk Create"** → conecta cada caixa de texto a um campo

OU

- Clica no template → **"..."** canto superior direito → **"Make this a brand template"** ou **"Edit template settings"** → configura os fields

OU

- Clica numa caixa de texto → painel direito de propriedades → rolar até **"Dataset"** / **"Field"** → conectar

**Cada campo deve ter o nome EXATO especificado mais abaixo** (TITULO, SELO, PARAGRAFO, etc.). Sem isso, a skill não consegue identificar qual texto editar.

### Passo 3 — Me passar o mapeamento de páginas

Quando terminar, me diz qual número de página corresponde a cada layout:

```
- Capa = página N
- Narrativa = página M
- CTA = página K
```

Eu atualizo `canva-template-ids.json` com esse mapeamento e a skill fica pronta.

---

## Página "Capa" — Cover do carrossel

**Função**: primeiro slide de qualquer carrossel — abre a narrativa, prende o olhar.

**Dimensões**: 1080×1350 px (4:5 — formato vencedor de feed Instagram)

**Layout sugerido**:
- Fundo: cor primária da marca OU imagem de fundo discreta
- Selo pequeno no topo (ex: "BUZZ PILLS", "PERGUNTA DA SEMANA", "RECAP")
- Título grande, centralizado, ocupando 60-70% da área (3-4 linhas)
- Subtítulo opcional abaixo, menor (1-2 linhas)
- Logo Buzzmonitor sutil em um canto (rodapé ou canto superior direito)

**Campos do dataset** (marcar no Canva):

| Nome do campo | Tipo | Exemplo | Obrigatório |
|---|---|---|---|
| `SELO` | text | "BUZZ PILLS" / "PERGUNTA DA SEMANA" / "RECAP" | sim |
| `TITULO` | text | "A flor virou clichê. O jantar virou status." | sim |
| `SUBTITULO` | text | "E a marca campeã do Dia dos Namorados 2026 nem fala de amor." | opcional |

**Variações sugeridas** (criar depois, conforme necessidade):
- Cover claro vs escuro (2 versões)
- Cover com foto vs sem foto

---

## Página "Narrativa" — Slide intermediário

**Função**: slides 2 até penúltimo — corpo do storytelling. Reutilizado várias vezes no mesmo carrossel.

**Dimensões**: 1080×1350 px

**Layout sugerido**:
- Fundo: cor secundária da marca (ou branco) — contrastando com a capa
- Indicador de progresso no topo (ex: "2 / 7" ou barrinha discreta)
- Bloco de texto principal — pode ter 1-3 frases curtas, fonte grande/legível
- Destaque visual leve (cor de marca em palavra-chave, ou ícone pequeno)
- Logo discreta no rodapé

**Campos do dataset**:

| Nome do campo | Tipo | Exemplo | Obrigatório |
|---|---|---|---|
| `NUMERO_SLIDE` | text | "2 / 7" | sim |
| `PARAGRAFO` | text | "A gente passou 8 dias ouvindo o que o Brasil dizia sobre Dia dos Namorados nas redes. 3.118 conversas depois, um padrão pulou primeiro." | sim |
| `DESTAQUE_OPCIONAL` | text | "3.118 conversas" — pode aparecer em letra grande/cor de marca, opcional | opcional |

**Variações sugeridas** (criar depois):
- Slide com número/dado grande (variante "dado")
- Slide com print/screenshot embedado (variante "UGC" / "case")

---

## Página "CTA" — Slide final

**Função**: último slide do carrossel — fecha o arco, chama pra ação.

**Dimensões**: 1080×1350 px

**Layout sugerido**:
- Fundo: cor primária ou de destaque da marca (chamar atenção)
- Headline curto, frase de fechamento
- Convite (CTA) destacado
- Destino visual claro (ex: "link na bio" / "comenta abaixo" / "marca um amigo")
- Logo Buzzmonitor visível
- Handle do Instagram (@buzzmonitorbr) opcional

**Campos do dataset**:

| Nome do campo | Tipo | Exemplo | Obrigatório |
|---|---|---|---|
| `HEADLINE_CTA` | text | "Esse tipo de leitura, a gente entrega pra marcas todo mês." | sim |
| `CONVITE` | text | "Sua próxima data: Festas Juninas. Quer ouvir antes da concorrência?" | sim |
| `DESTINO` | text | "Link na bio" / "Comenta abaixo" / "DM aberto" | sim |

---

## Como a skill `/social-canva` vai usar

Depois que você criar os 3 templates e me passar os IDs, a skill vai:

1. Receber 1 post da `copies-junho.md` (caption + slides)
2. Pra cada slide, decidir qual template usar:
   - Slide 1 → Template 1 (Cover)
   - Slides 2 a N-1 → Template 2 (Narrativa) reaplicado pra cada
   - Slide N → Template 3 (CTA)
3. Mapear o texto da copy → campos do dataset
4. Criar N designs no Canva (1 por slide) via MCP
5. Te devolver os links/IDs dos designs gerados, prontos pra revisar e baixar

**Sobre o slide de capa específico** (caption do feed): a caption fica **na descrição** do post no Instagram, não no design. A skill só cuida das artes (slides). A caption você copia da `copies-junho.md` na hora de publicar.

---

## Roadmap de páginas (futuro)

Conforme usar mais a skill, adicionar páginas especializadas ao mesmo template:

- **Página "Dado"** — variante de Narrativa com número GIGANTE
- **Página "UGC"** — variante de Narrativa com caixa pra screenshot/print
- **Página "Capa Case"** — variante de Capa com bloco "Cliente: X"
- **Página "Capa Webinar"** — variante de Capa com data/hora destacada

Avisar quando criar — eu mapeio na config e adiciono ao roteamento da skill.

---

## Checklist pra você

- [x] Conta Canva é **Teams** (confirmado)
- [x] Brand Kit "Buzzmonitor" criado (kAHMXCYNo9Y)
- [x] Template `EAHMXaCZdd4` criado
- [ ] **Página Capa** desenhada (com 3 campos de dataset: `SELO`, `TITULO`, `SUBTITULO`)
- [ ] **Página Narrativa** desenhada (com 3 campos: `NUMERO_SLIDE`, `PARAGRAFO`, `DESTAQUE_OPCIONAL`)
- [ ] **Página CTA** desenhada (com 3 campos: `HEADLINE_CTA`, `CONVITE`, `DESTINO`)
- [ ] Campos de dataset configurados com nome EXATO em cada página
- [ ] Me passar o mapeamento: `Capa = página N · Narrativa = página M · CTA = página K`
