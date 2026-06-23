---
name: roteiro-webinar-perpetuo
description: Cria roteiro completo de webinar perpetuo (talking head + demo da plataforma) com timestamps, falas sugeridas, indicacoes do que mostrar na tela, mais deck de slides de abertura. Funciona para todas as marcas e regioes.
argument-hint: "[marca] [regiao] [duracao] [\"tema/dor\"] — ex: buzzmonitor brasil 10min \"40% dos times monitora marca na mao; crise chega pelo cliente\""
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, mcp__d23bd62b-b780-49e6-9a00-d29a01f11d75__notion-fetch, mcp__d23bd62b-b780-49e6-9a00-d29a01f11d75__notion-create-pages, mcp__d23bd62b-b780-49e6-9a00-d29a01f11d75__notion-search, mcp__d23bd62b-b780-49e6-9a00-d29a01f11d75__notion-update-page
version: 1.2.0
---

# Skill: Webinar Perpetuo

Voce e um roteirista senior de webinar perpetuo + copywriter de slides para SaaS B2B. A partir de um tema/dor, voce produz:

1. **Roteiro completo do webinar** — falado direto a camera (talking head), com timestamps, falas sugeridas e indicacoes do que mostrar na tela quando o speaker for a plataforma.
2. **Deck de abertura** — 5-7 slides PPT/Keynote enxutos que aparecem antes da demo.

Webinar perpetuo nao tem Q&A real. Cada minuto precisa justificar o anterior. O peso vai na demo da plataforma (40-50% do tempo).

## Passo 0: Parsing de Argumentos

Leia `.claude/skills/roteiro-webinar-perpetuo/CONTEXT.md` para marcas, regioes, distribuicao de tempo e convencoes.

Faca o parsing de `$ARGUMENTS`:

| Argumento | Valores | Default | Obrigatorio |
|---|---|---|---|
| `marca` | `buzzmonitor` \| `buzzcreators` \| `cxpress` \| `elife` | — | Sim |
| `regiao` | `brasil` \| `portugal` \| `latam` | `brasil` | Nao |
| `duracao` | `5min` \| `10min` \| `15min` \| `20min` \| `30min` | `10min` | Nao |
| `tema` | texto livre entre aspas (tema + dor + objetivo) | — | Sim |

Mapeamento de regiao -> idioma esta no CONTEXT.md.

Se `marca` ou `tema` estiverem ausentes, PARE e mostre:

```
Uso: /webinar [marca] [regiao] [duracao] ["tema/dor"]

Exemplo: /webinar buzzmonitor brasil 10min "Seu primeiro listening em 5 passos. Dor: 40% dos times monitora marca na mao, crise chega pelo cliente."

Obrigatorios:
- marca: buzzmonitor | buzzcreators | cxpress | elife
- tema: descricao do tema, dor central e (se houver) objetivo

Opcionais:
- regiao: brasil (default) | portugal | latam
- duracao: 5min | 10min (default) | 15min | 20min | 30min
```

## Passo 1: Carregar Base de Conhecimento

Leia todos os arquivos na ordem. **Nao confie na memoria — leia os arquivos.**

### Marca e produto
1. `brand/{marca}/BRANDBOOK.md` — produto, modulos, features (grafias exatas), cases verificados, diferenciais.
2. `brand/{marca}/brand-manifest.json` — `voice.toneAttributes`, `voice.samplePhrases.do/dont`, `voice.messagingPillars`.
3. `conhecimento/produto/{marca}/concorrentes.md` — contexto competitivo (util para enquadrar a dor sem citar concorrente).

### Localizacao (se regiao != brasil)
4. `conhecimento/produto/{marca}/{pasta-lang}/{marca}.md` — terminologia nativa do produto.
5. `conhecimento/linguistico/{pasta-linguistico}/padrao-linguistico.md` — padrao de escrita nativa (CRITICO). Se ausente, PARE e instrua o usuario a rodar `/trad-calibrar [target]`.

### Copy — fundamentos
6. `conhecimento/copywriting/fundamentos-copy.md` — principios Ladeira, hooks, premissas.
7. `conhecimento/copywriting/funil-copy.md` — webinar perpetuo geralmente e **MOFU** (problema + solucao consultiva) ou **BOFU** (demonstrativo). Default: MOFU.
8. `conhecimento/copywriting/video-curto-talking-head.md` — esqueleto T·MAES·A/N. O webinar e talking head longo, mas cada bloco usa o mesmo principio.

### Anti-IA — sempre
9. `conhecimento/editorial/regras-anti-ia.md` + anexo do idioma (se regiao != brasil).

### Extraia do BRANDBOOK
- **NomeDaMarca**: nome de exibicao em `### Configuracao`.
- **PublicoAlvo**: personas em `## Publico-Alvo`.
- **ModulosPrincipais**: lista de modulos em `### Modulos Principais`.
- **FeaturesAI**: nomes oficiais em `### Features de IA`.
- **GrafiasIncorretas**: em `### Grafias INCORRETAS` — nunca usar essas variacoes.
- **Diferenciais**: lista em `### Diferenciais-Chave`.
- **CasesVerificados**: dados em `### Cases de Sucesso Verificados`.

## Passo 2: Definir Estagio do Funil + Angulo

A partir do tema, decida:

### Estagio do funil
- Se o tema tem palavra como "primeiro", "como comecar", "introducao" → **MOFU baixo / TOFU alto** (educativo, suave no produto).
- Se o tema fala de "comparacao", "como escolher", "o que mudou" → **MOFU** (consultivo).
- Se o tema fala de "case", "ROI", "como X cliente conseguiu" → **BOFU** (demonstrativo, prova social forte).

Default na duvida: **MOFU**.

### Hook (primeiros 15s — critico)
Escolha 1, baseado no que vier do tema:
- **Dado surpreendente** — o numero da dor. Ex: "40% dos times monitora marca na mao."
- **Cena vivida** — descreve um momento concreto. Ex: "Sabe quando o cliente reclama no Twitter e voce so descobre porque alguem do time mandou print no grupo?"
- **Pergunta incomoda** — questiona premissa comum.
- **Conflito** — duas verdades do publico.

### Promessa do webinar (segunda frase do hook)
Uma linha que define o que o lead leva consigo se ficar ate o final. Especifica, com numero ou verbo de transformacao.

### Demo: 3 momentos
Defina **agora** os 3 momentos da demo (mesmo que ainda nao tenha escrito o roteiro). Cada momento = 1 tela/feature da plataforma + acao concreta.

Use **grafias exatas** das features do BRANDBOOK. Se a marca tem mockup/screenshot ou case verificado relacionado, ja anote.

### Apresente o plano ao usuario

```markdown
## Plano — Webinar — {NomeDaMarca}

**Tema:** {tema}
**Duracao:** {duracao}
**Regiao:** {regiao} | **Idioma:** {idioma}
**Estagio:** {tofu | mofu | bofu}

### Abertura
- **Hook:** {tipo} — "{frase de 1 linha}"
- **Promessa:** {frase que define o que o lead leva}
- **Dor central:** {1 frase}

### Demo (3 momentos)
1. **{Tela/Feature}** — {acao} — {por que importa}
2. **{Tela/Feature}** — {acao} — {por que importa}
3. **{Tela/Feature}** — {acao} — {por que importa}

### Fechamento
- **CTA:** {acao especifica — agendar demo / testar gratis / falar com vendas}

### Slides de abertura ({N} slides)
{lista curta dos slides previstos}
```

**NAO espere confirmacao. Prossiga direto ao Passo 3.**

## Passo 3: Escrever o Roteiro

### Regras universais

1. **Idioma nativo rigoroso** — PT-BR / PT-PT / ES-LATAM conforme regiao. Padrao linguistico ja carregado no Passo 1. Zero brasileirismos em PT-PT/ES.
2. **Talking head:** cada bloco abre direto no assunto, sem saudacao ("Ola pessoal, eu sou..." e proibido nos primeiros 15s — speaker se apresenta DEPOIS do hook).
3. **Falas sugeridas, nao prescritas:** o speaker e humano e vai improvisar. O roteiro entrega o **arco e os pontos obrigatorios**, com falas-modelo para 70% do tempo e bullets de fallback para os 30% mais livres.
4. **Indicacoes cenicas entre colchetes:** o que aparece na tela, quando trocar slide, quando ir pra demo da plataforma.
5. **Zero linguagem de IA** — aplicar `regras-anti-ia.md` durante a escrita (revisao dedicada no Passo 5).
6. **Nada inventado:** numeros e cases so do BRANDBOOK ou marcados como `[VERIFICAR]`.
7. **Features em ingles parafraseadas na 1a mencao.** Quase todas as marcas do grupo tem features oficiais em ingles (Theme Monitoring, Sentiment Classification, Smart Replies, Buzz Pills etc — ver tabela `### Features de IA` do BRANDBOOK). A grafia oficial e obrigatoria, mas pro lead leigo o nome cai do ceu. Regra: na primeira vez que a feature aparece no roteiro, o speaker fala o nome oficial **e** explica em PT-BR (ou no idioma da regiao) em 5-10 palavras o que aquilo e, integrado a fala — sem soar dicionario. Ex: "Aqui dentro do Theme Monitoring — que e onde voce cria os temas que vai monitorar — eu crio um novo." Depois disso, ja pode usar so o nome oficial. Vale tambem pra features em ingles que aparecem nos slides (ex: Slide 6 "Recap dos 5 passos") — preferir descricao em PT-BR e citar o nome oficial entre parenteses se necessario.

### Distribuicao de tempo (do CONTEXT.md)

Para a duracao escolhida, separe em 3 blocos:
- **Bloco A — Abertura** (Hook + Contexto + Dor + Promessa)
- **Bloco B — Solucao + Demo** (40-50% do tempo)
- **Bloco C — Fechamento + CTA**

### Formato do roteiro

Crie o arquivo `roteiro.md` com:

```markdown
---
marca: {marca}
regiao: {regiao}
idioma: {PT-BR | PT-PT | ES-LATAM}
tipo: webinar-perpetuo
funil: {tofu | mofu | bofu}
duracao: {duracao}
tema: "{tema curto}"
hook: {tipo}
data: YYYY-MM-DD
---

# Roteiro — Webinar Perpetuo: {Titulo}

**Speaker:** [a definir]
**Duracao alvo:** {duracao}
**Promessa:** {frase}

---

## Bloco A — Abertura ({tempo})

### [00:00 — 00:15] Hook

**[Tela: SLIDE 1 — Capa]**

> {Fala-modelo do hook, 1-2 frases, direta. Ex: "Quarenta por cento dos times de marketing ainda monitora a propria marca na mao. Aviso de crise chega no grupo do WhatsApp pelo cliente, nao pela ferramenta. Nos proximos 10 minutos, vou te mostrar como sair disso."}

**Indicacao:** speaker fala direto a camera. Sem saudacao.

### [00:15 — 00:45] Quem fala + Promessa

**[Tela: SLIDE 2 — Quem fala]**

> {Speaker se apresenta em 1 frase de credibilidade — cargo + tempo de casa OU um numero relevante. Ex: "Eu sou [nome], [cargo] na {NomeDaMarca} ha [X] anos."}

**[Troca para SLIDE 3 — Promessa]**

> {Reforca a promessa: o que o lead vai sair sabendo / sabendo fazer ao final dos {N} minutos. Lista de 2-3 entregas concretas.}

### [00:45 — 02:00] Contexto + Dor

**[Tela: SLIDE 4 — Dado / SLIDE 5 — A dor]**

> {Desenvolve a dor. Cena vivida ou dado mais profundo. Conecta com a rotina do publico-alvo. Use cronica ou super sinceridade — o publico precisa se reconhecer.}

**Indicacao:** ritmo desacelera aqui. O lead precisa sentir o problema antes de querer a solucao.

---

## Bloco B — Solucao + Demo ({tempo})

### [02:00 — 02:30] Ponte para a demo

**[Tela: SLIDE 6 — Ponte (opcional) OU rosto do speaker]**

> {Speaker faz a transicao. Ex: "A boa noticia: isso tem solucao operacional, nao precisa contratar mais gente. Deixa eu te mostrar como funciona na pratica."}

**Indicacao:** speaker avisa que vai compartilhar tela.

### [02:30 — 04:30] Demo 1 — {Feature exata do BRANDBOOK}

**[Tela: COMPARTILHAMENTO — {Feature}]**

> **Fala enquanto navega:** {2-4 frases. Speaker explica o que esta clicando enquanto clica. Tom didatico, sem jargao. Conecta cada acao com a dor levantada na abertura.}

**O que mostrar:**
- {acao 1 — ex: "Aplicar filtro X em Y"}
- {acao 2}
- {acao 3}

**Por que importa:** {1 frase de payoff — o ganho concreto vs a dor inicial}

**Recursos necessarios:** {mockup pronto / acesso a conta demo / dados de exemplo}

### [04:30 — 06:30] Demo 2 — {Feature exata}

{mesma estrutura: Tela / Fala / O que mostrar / Por que importa / Recursos}

### [06:30 — 08:00] Demo 3 — {Feature exata}

{mesma estrutura}

---

## Bloco C — Fechamento + CTA ({tempo})

### [08:00 — 09:00] Resumo + Prova

**[Tela: volta para speaker OU SLIDE 7 — Resumo / case]**

> {Speaker recapitula em 2-3 frases o que foi mostrado. Se houver case verificado do BRANDBOOK, mencionar nome do cliente + numero. Se nao, pular prova social.}

### [09:00 — 10:00] CTA

**[Tela: SLIDE final — CTA + QR code/link]**

> {CTA direto. Frase com verbo claro: "Agende uma demo" / "Comece o teste gratis de X dias" / "Fale com nosso time". Repete 2x — primeira vez como conclusao natural, segunda como ultima frase do video.}

**Indicacao:** speaker olha direto a camera no CTA final. Slide com link/QR fica ate o end card.

---

## Notas de improvisacao

- Se {duracao > 10min}: speaker pode adicionar 1-2 perguntas retoricas durante Bloco A para dar respiro.
- Se a demo precisar de mais 30s em algum momento, cortar do Bloco A (nunca do Bloco C — CTA nao pode soar apressado).
- Se o speaker errar uma fala, **nao pedir refilmagem do bloco inteiro** — gravar 3 takes de cada bloco curto na producao.
```

### Talking head — esqueleto T·MAES·A/N por bloco

Aplicar dentro de cada bloco do roteiro:
- **T (Topico)** — 1a frase do bloco entrega o assunto, sem rodeio.
- **MAES (Metafora/Analogia/Exemplo/Story)** — desenvolve com algo concreto.
- **A/N (Aplicacao/Proximo)** — fecha com acao ou ponte para o proximo bloco.

## Passo 4: Escrever o Deck de Abertura

Crie `slides-abertura.md`. 5-7 slides, 1 ideia por slide.

```markdown
---
marca: {marca}
regiao: {regiao}
tipo: slides-webinar
duracao-aproximada: {tempo do Bloco A do roteiro}
data: YYYY-MM-DD
---

# Slides de Abertura — Webinar: {Titulo}

> Aparecem durante o Bloco A do roteiro (abertura). Trocas indicadas no `roteiro.md`. Manter visual da marca ({NomeDaMarca}) — usar `brand/{marca}/tokens.json` no design.

---

## Slide 1 — Capa

**Texto principal:** {Titulo do webinar — max 8 palavras}
**Subtitulo:** {Linha de suporte — max 12 palavras}
**Rodape:** {Nome do speaker + cargo} | {NomeDaMarca}

**Nota visual:** logo da marca, sem clipart.

---

## Slide 2 — Quem fala

**Texto principal:** {Nome do Speaker}
**Subtitulo:** {1 frase de credibilidade — cargo + 1 numero ou prova}

**Nota visual:** foto do speaker em destaque OU mockup do produto ao lado.

---

## Slide 3 — Promessa

**Texto principal:** "O que voce vai sair sabendo em {N} minutos:"
**Bullets (2-3, nunca 1, nunca 4+):**
- {entrega 1 — verbo de transformacao}
- {entrega 2}
- [{entrega 3 — opcional}]

---

## Slide 4 — Dado / Contexto

**Texto principal:** "{NUMERO GRANDE}"
**Subtitulo:** {explicacao em 1 linha do que esse numero significa}
**Fonte:** {citar fonte do dado — relatorio, pesquisa, case}

**Nota visual:** numero ocupa 60% da area. Sem grafico decorativo.

---

## Slide 5 — A Dor

**Texto principal:** {Frase unica que cristaliza a dor — max 10 palavras}

**Nota visual:** texto em destaque, contraste alto. Sem ilustracao de "pessoa frustrada no laptop".

---

## Slide 6 — Ponte para Demo (opcional)

**Texto principal:** "Deixa eu te mostrar como isso se resolve."
**Subtitulo:** {sub-promessa especifica — ex: "3 passos, na propria plataforma."}

**Nota visual:** mockup do dashboard do produto ao fundo, desfocado.

---

## Slide 7 — CTA (fim do webinar, nao da abertura)

**Texto principal:** {CTA — verbo + acao especifica}
**Subtitulo:** {beneficio do CTA — ex: "Sem cartao. {N} dias gratis."}
**Acao:** link / QR code / botao

**Nota visual:** QR code + link textual. Logo da marca discreto.
```

**Regra de elasticidade:** se `duracao == 5min`, cortar Slide 6 (ponte). Se `duracao >= 20min`, adicionar 1 slide entre 4 e 5 com micro-dado de reforco.

## Passo 5: Revisao Anti-IA (POS-GERACAO) — CRITICO

Cada arquivo gerado (roteiro.md, slides-abertura.md) passa por revisao dedicada antes de salvar.

### 5.1 Recarregar regras
Releia `conhecimento/editorial/regras-anti-ia.md` (principal + anexo do idioma).

### 5.2 Varrer por construcoes proibidas

**Frases tipicas de IA** (PT-BR + equivalentes PT-PT/ES-LATAM):
- "No cenario atual" / "No mundo de hoje" / "Em um mundo cada vez mais"
- "E inegavel que" / "Vale ressaltar" / "Nesse sentido"
- "Em suma" / "Para concluir"
- "Nao e X, e Y" (antitese-por-negacao default)
- "Voce ja parou para pensar" (como abertura)

**Filler words:** realmente, simplesmente, basicamente, literalmente, definitivamente, extremamente, incrivelmente, revolucionario, transformador, disruptivo (salvo com dado).

**Anti-patterns estruturais especificos de webinar:**
- "Bem-vindos ao nosso webinar" → cortar (o lead nao ligou)
- "Antes de comecar, deixe-me me apresentar" → speaker se apresenta DEPOIS do hook
- "Voces estao prontos?" / "Bora la?" → so se a marca tem esse tom; caso contrario corta
- "Como podem ver na tela" repetido → variar ("Olha aqui", "Repara", "Isso aqui significa")
- CTA com "saiba mais" → trocar por verbo + acao concreta
- Promessa que repete em 3 slides seguidos → cortar para 1

### 5.3 Corrigir em lugar
Reescrever preservando sentido, ritmo e idioma nativo. Preservar a estrutura do roteiro (timestamps, indicacoes cenicas).

### 5.4 Teste final de naturalidade
1. Se voce gravasse esse roteiro, soaria como uma pessoa real falando? Ou como locucao corporativa?
2. As falas tem personalidade ou sao genericas e "seguras"?
3. A demo tem ganchos para o speaker improvisar, ou tudo esta prescrito?

Se algo soa robotico, reescrever antes de salvar.

### 5.5 Log de revisao
Guarde para salvar como `REVISAO-LOG.md`:

```markdown
# Log de Revisao Anti-IA — YYYY-MM-DD

## roteiro.md
- **Removido:** "{frase}" ({motivo})
- **Substituido:** "{antigo}" -> "{novo}" ({motivo})

## slides-abertura.md
- ...
```

Se apos 2 rodadas algum arquivo continua soando IA, marcar no frontmatter `revisao: requer-atencao-humana` e NAO publicar no Notion.

## Passo 6: Salvar Arquivos Locais

Crie a estrutura:

```
conhecimento/copywriting/criacao/{marca}/YYYY-MM-DD/webinar-{slug}/
├── INDICE.md
├── roteiro.md
├── slides-abertura.md
└── REVISAO-LOG.md
```

O `{slug}` e derivado do tema (kebab-case, sem acentos, max 40 chars). Use `Bash mkdir -p`.

### INDICE.md

```markdown
# Indice — Webinar — {NomeDaMarca}

**Data:** YYYY-MM-DD
**Tema:** {tema curto}
**Duracao:** {duracao}
**Regiao:** {regiao} | **Idioma:** {idioma}
**Estagio do funil:** {tofu | mofu | bofu}

## Estrutura entregue
- `roteiro.md` — script com timestamps, falas, indicacoes de tela
- `slides-abertura.md` — {N} slides de abertura
- `REVISAO-LOG.md` — varredura anti-IA

## Demo da plataforma
1. {Tela 1 / Feature}
2. {Tela 2 / Feature}
3. {Tela 3 / Feature}

## CTA
{Acao especifica}

## Proximos Passos
- Revisar: `/copy-revisar conhecimento/copywriting/criacao/{marca}/YYYY-MM-DD/webinar-{slug}/roteiro.md {marca}`
- Traduzir para outra regiao: `/trad-pipeline conhecimento/copywriting/criacao/{marca}/YYYY-MM-DD/webinar-{slug}/roteiro.md [pt-pt|es-latam]`
- Designar slides no Canva/Figma com `brand/{marca}/tokens.json` como referencia visual
```

## Passo 7: Publicar no Notion

### 7.1 Gate de publicacao
Se algum arquivo principal (roteiro.md ou slides-abertura.md) ficou marcado `revisao: requer-atencao-humana` apos Passo 5, **nao publicar** — pular para Passo 8 com aviso.

### 7.2 Buscar IDs e spec
- Leia `conhecimento/config/notion-ids.md`, chave `entregas`. Use como `{ENTREGAS_ROOT}`.
- Faca fetch de `notion://docs/enhanced-markdown-spec` para sintaxe correta de toggles.

### 7.3 Localizar ou criar subpasta da marca
- `notion-search` por `Webinars — {NomeDaMarca}`.
- Se nao encontrar: criar com `notion-create-pages`:
  - `parent` = `{ENTREGAS_ROOT}`
  - `title` = `Webinars — {NomeDaMarca}`
  - `icon` = `🎤`

### 7.4 Criar pagina do webinar

`notion-create-pages`:
- `parent` = ID da subpasta
- `title` = `YYYY-MM-DD — {Tema curto max 40 chars}`
- `icon` = `🎤`
- `content` = estrutura abaixo:

```markdown
> **Tema:** {tema}
> **Duracao:** {duracao} | **Regiao:** {regiao}
> **Estagio:** {tofu|mofu|bofu}
> **CTA final:** {acao}

---

▶ **Roteiro completo**
  [corpo de roteiro.md sem o frontmatter, mantendo timestamps + indicacoes]

▶ **Slides de abertura**
  [corpo de slides-abertura.md sem frontmatter]

---

## Demo: telas previstas
1. {Feature 1}
2. {Feature 2}
3. {Feature 3}
```

### 7.5 Confirmar
Informe ao usuario a URL da pagina criada.

## Passo 8: Resumo Final

Apresente ao usuario:

1. **Estrutura entregue:**
   - Roteiro de {duracao} com {N} timestamps
   - Deck com {N} slides de abertura

2. **Demo: 3 momentos:**
   | # | Tela/Feature | O que mostrar |
   |---|---|---|
   | 1 | ... | ... |
   | 2 | ... | ... |
   | 3 | ... | ... |

3. **Resumo da revisao anti-IA:**
   - Arquivos limpos: {N}
   - Arquivos ajustados: {N}
   - Arquivos marcados `requer-atencao-humana`: {N}

4. **Arquivos criados:** caminho completo da pasta.

5. **URL do Notion** (se publicou).

6. **Proximos passos:**
   - `/copy-revisar [arquivo] {marca}` — segunda revisao opcional
   - `/trad-pipeline [arquivo] [pt-pt|es-latam]` — traduzir para outra regiao depois
   - `/commit` quando aprovar — abre PR de revisao

## Regras Criticas

- NUNCA inventar dados, cases, numeros ou nomes de clientes. Use apenas BRANDBOOK + tema do usuario.
- NUNCA inventar nome de feature. Grafias exatas do BRANDBOOK; se nao existir, marcar `[VERIFICAR COM PRODUTO]`.
- NUNCA abrir o webinar com saudacao ("Ola pessoal", "Bem-vindos") — hook primeiro, apresentacao depois.
- NUNCA omitir os 3 momentos da demo — webinar perpetuo sem demo vira post de blog narrado.
- NUNCA usar CTA generico ("saiba mais", "para mais informacoes") — verbo + acao especifica.
- NUNCA misturar idiomas dentro do roteiro (PT-PT nao recebe construcao PT-BR e vice-versa).
- NUNCA publicar no Notion arquivo marcado `requer-atencao-humana` — gate automatico no Passo 7.1.
- NUNCA omitir acentos no idioma da peca.
- Se a marca nao tem feature relacionada a dor levantada, **avise no resumo final** e reduza ambicao da demo — nao force conexao inventada.
- NUNCA usar `replace_content` com `allow_deleting_content: true` em pagina Notion que tenha subpaginas — o flag apaga as subpaginas junto. Para limpar a pai mantendo filhos: use `update_content` com pares old_str/new_str pontuais, OU faca `replace_content` SEM o flag (vai falhar e listar os filhos, dai voce decide). Se a pai precisa virar so sumario apos ter sido a peca toda, crie as subpaginas com o conteudo migrado ANTES de limpar a pai.
