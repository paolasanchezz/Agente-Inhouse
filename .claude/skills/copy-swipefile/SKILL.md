---
name: copy-swipefile
description: Mantém um swipe file (banco de referencias) de boas copys organizado e pesquisavel.
argument-hint: "add [url-ou-texto] | buscar [tema]"
allowed-tools: WebFetch, WebSearch, Read, Write, Bash, Glob, Grep
version: 1.0.0
---

# Skill: Swipe File de Copy

Voce gerencia um banco de referencias de boas copys — o swipe file do Agente Inhouse. O swipe file e armazenado em `conhecimento/copywriting/swipe-file/`.

## Passo 0: Parsing de Argumentos

Faca o parsing de `$ARGUMENTS`:
- **Acao**: `add` ou `buscar`
- **Conteudo**: URL, texto da copy, ou tema de busca

Se a acao nao for clara, pergunte ao usuario.

---

## Acao: ADD — Adicionar nova referencia

### Passo 1: Obter a copy

Se o usuario passou uma **URL**:
1. Use WebFetch para acessar a pagina
2. Extraia o texto da copy (anuncio, email, post, roteiro)

Se o usuario passou **texto direto**:
1. Use o texto fornecido

Se o usuario nao passou nada:
1. Pergunte: "Qual copy voce quer adicionar? Cole o texto ou passe a URL."

### Passo 2: Analisar a copy

Leia `conhecimento/copywriting/fundamentos-copy.md` para usar como referencia de analise.

Analise a copy nos seguintes aspectos:

| Campo | Descricao |
|---|---|
| **Tipo** | video-curto / estatico / email / pagina-de-venda / outro |
| **Pago ou organico** | ads / organico |
| **Estagio do funil** | TOFU / MOFU / BOFU |
| **Tecnica principal** | premissa / storytelling / ironia / prova-social / hook-forte / sentimentos-opostos / super-sinceridade / comando / outro |
| **Elementos literarios** | hiperbole / antitese / callback / linguagem-fantasiosa / cronica / nenhum |
| **Nicho** | saas / ecommerce / infoproduto / servicos / outro |
| **Marca/Fonte** | Nome da marca ou fonte original |
| **Por que funciona** | Analise de 2-3 frases usando vocabulario de fundamentos-copy.md |
| **Nota (1-5)** | Avaliacao de qualidade da copy |

### Passo 3: Salvar no swipe file

Determine o proximo numero sequencial com sort numerico (NAO lexicografico — `10` deve vir depois de `001`):

```bash
ls conhecimento/copywriting/swipe-file/ | grep -E '^[0-9]+-' | sort -V | tail -1
```

`sort -V` (version sort) ordena `001`, `002`, ..., `009`, `010`, `011`... corretamente. `sort -n` tambem funciona mas so se os nomes comecarem com digito puro; `sort -V` tolera separadores. Extraia o numero do primeiro trecho (antes do `-`), incremente e preencha com zeros a 3 digitos.

Crie o arquivo `conhecimento/copywriting/swipe-file/NNN-{slug}.md` (NNN com padding: `001`, `010`, `123`):

```markdown
---
tipo: {tipo}
pago-organico: {ads|organico}
funil: {TOFU|MOFU|BOFU}
tecnica: {tecnica-principal}
elementos-literarios: [{lista}]
nicho: {nicho}
marca: {marca-fonte}
nota: {1-5}
data: YYYY-MM-DD
---

# {Titulo descritivo}

## Copy

{Texto completo da copy}

## Analise

**Por que funciona:**
{Analise detalhada}

**Tecnicas identificadas:**
- {tecnica 1}: {como foi usada}
- {tecnica 2}: {como foi usada}

**Como adaptar para as marcas Elife:**
{Sugestao concreta de adaptacao}
```

### Passo 4: Atualizar indice

Leia (ou crie se nao existir) `conhecimento/copywriting/swipe-file/INDICE.md`.

Adicione uma linha ao indice:
```markdown
| NNN | {titulo} | {tipo} | {funil} | {tecnica} | {nota} | {data} |
```

Informe ao usuario: "Adicionado ao swipe file: NNN-{slug}.md"

---

## Acao: BUSCAR — Encontrar referencias

### Passo 1: Entender a busca

O usuario pode buscar por:
- **Tema livre:** "hooks para SaaS", "storytelling", "email de venda"
- **Filtro especifico:** "tipo:video-curto funil:TOFU"
- **Tecnica:** "premissa", "ironia", "prova-social"

### Passo 2: Pesquisar no swipe file

1. Use Grep para buscar nos arquivos de `conhecimento/copywriting/swipe-file/`:
   - Busque no frontmatter (tipo, funil, tecnica, nicho)
   - Busque no corpo (texto da copy, analise)
2. Ordene por nota (maior primeiro)

### Passo 3: Apresentar resultados

Mostre ate 5 resultados relevantes:

```
## Resultados para "{tema}"

### 1. {titulo} (nota: {X}/5)
- **Arquivo:** NNN-{slug}.md
- **Tipo:** {tipo} | **Funil:** {funil} | **Tecnica:** {tecnica}
- **Trecho:** {primeiras 2-3 linhas da copy}
- **Por que e relevante:** {1 frase}

### 2. ...
```

Se nao encontrar resultados, sugira:
- Termos alternativos de busca
- Executar `/copy-pesquisar` para coletar novas referencias

---

## Regras

- **Nao duplique:** Antes de adicionar, verifique se a copy ja existe no swipe file (busque trechos-chave)
- **Analise com fundamentos:** Sempre use o vocabulario e frameworks de `fundamentos-copy.md`
- **Slug limpo:** O slug do arquivo deve ser kebab-case, max 40 chars, sem acentos
- **Frontmatter padrao:** Sempre inclua todos os campos do frontmatter, mesmo que seja "nenhum" ou "outro"
