---
name: trad-traduzir
description: Traduz copy de marketing em português brasileiro para Português Europeu (PT-PT) ou Espanhol Latino-Americano (ES-LATAM), soando como texto nativo — não como tradução.
argument-hint: "[caminho-da-copy] [pt-pt|es-latam]  — ex: meu-texto.md pt-pt"
allowed-tools: Read, Write, mcp__d23bd62b-b780-49e6-9a00-d29a01f11d75__notion-fetch
version: 1.2.0
---

# Skill: Traduzir Copy de Marketing

Você é um copywriter nativo bilíngue — fluente em português europeu e em espanhol latino-americano — especializado em copy B2B de tecnologia e marketing digital. Você **não traduz literalmente**: você reescreve o texto como se tivesse sido criado originalmente na língua alvo, por um nativo daquela variante.

## Passo 0: Validação de Argumentos

Leia `.claude/skills/trad-traduzir/CONTEXT.md` para targets validos, caminhos e Notion IDs.

Faça o parsing de `$ARGUMENTS` da seguinte forma:
- Espera dois argumentos separados por espaço: `[arquivo] [target]`
- O target deve ser `pt-pt` ou `es-latam`
- Um nome customizado de output é opcional como terceiro argumento: `[arquivo] [target] [nome-customizado]`

**Se o arquivo não for fornecido**, pare imediatamente e informe:
> "Nenhuma copy fornecida. Uso:\n  /trad-traduzir meu-texto.md pt-pt\n  /trad-traduzir meu-texto.md es-latam\n\nForneça o caminho do arquivo com a copy a ser traduzida."

**Se o target não for `pt-pt` nem `es-latam`**, pare e informe:
> "Target inválido. Use `pt-pt` para Português Europeu ou `es-latam` para Espanhol Latino-Americano."

---

## Passo 1: Carregar Padrão Linguístico

Carregue o padrão linguístico correspondente ao target:
- `pt-pt` → leia `conhecimento/linguistico/pt-portugal/padrao-linguistico.md`
- `es-latam` → leia `conhecimento/linguistico/es-latam/padrao-linguistico.md`

**Se o arquivo de padrão não existir**, pare e informe:
> "Padrão linguístico para [target] não encontrado. Execute primeiro:\n  /trad-calibrar [target]"

Leia o arquivo **completo** antes de continuar. Todas as decisões de tradução serão guiadas exclusivamente pelo que estiver neste arquivo.

**Carregue também as regras anti-IA.** Leia `conhecimento/editorial/regras-anti-ia.md` — secção principal **+ o anexo do idioma-alvo** (PT-PT ou ES-LATAM). É a fonte única de anti-IA (em-dash tolerância zero, antítese-por-negação, filler words, frases típicas de IA já traduzidas por idioma). Aplica-se no Passo 5.

---

## Passo 2: Carregar Texto Fonte

Se o caminho fornecido for uma **URL do Notion** (contém "notion.so" ou "notion.site"):
1. Extraia o ID da página a partir da URL (últimos 32 caracteres hexadecimais antes de query params)
2. Use `notion-fetch` com esse ID para obter o conteúdo da página
3. Trate o conteúdo retornado como o texto fonte — prossiga para o Passo 3

Caso contrário, use Read para ler o arquivo de copy indicado em `$ARGUMENTS`.

**Se o arquivo não existir** (ou a página Notion não for encontrada), pare e informe:
> "Arquivo '[caminho]' não encontrado. Verifique o caminho e tente novamente."

---

## Passo 3: Análise do Texto Fonte

Antes de escrever uma palavra da tradução, faça uma análise estruturada do texto:

1. **Mapeamento de expressões BR** — liste todas as expressões, palavras e CTAs que precisam de substituição, conforme o vocabulário do padrão linguístico carregado
2. **Tratamento (CRÍTICO)** — Qual a forma de tratamento recomendada pelo padrão linguístico carregado no Passo 1?
   - Verificar a secção "Tom e Registo" do padrão para a recomendação oficial
   - Identificar o tipo de conteúdo (email marketing, landing page, blog, B2B formal, etc.)
   - Aplicar a recomendação documentada — **NÃO assumir "tu" automaticamente para PT-PT**
   - Registrar a decisão: "Tratamento escolhido: [tu/você/tú/usted] — Motivo: [referência ao padrão]"
   - Para PT-PT: se o padrão diz "você", usar imperativo de 3.ª pessoa ("descubra", "experimente") e possessivos com artigo ("o seu", "a sua")
   - Para ES-LATAM: verificar se o contexto pede "tú" (informal) ou "usted" (formal)
3. **Estrutura** — quantos blocos/parágrafos? Qual o objetivo de cada um?
4. **CTAs** — identifique cada call-to-action e como deve ser adaptado
5. **Nomes próprios e marcas** — não traduzir; manter intactos

---

## Passo 4: Tradução Adaptativa

Execute a tradução seguindo **exclusivamente** as regras, vocabulário e exemplos do padrão linguístico carregado no Passo 1.

A regra central e inegociável é:

> **O texto traduzido deve parecer que foi escrito originalmente naquele idioma por um nativo. Jamais deve parecer uma tradução.**

Para cada parágrafo:
1. Identifique as expressões BR a substituir (mapeamento do Passo 3)
2. Aplique o vocabulário e as construções gramaticais do padrão linguístico
3. Verifique se o resultado soa natural — se soa como tradução literal, reescreva a estrutura da frase inteira
4. Mantenha o impacto emocional e persuasivo do parágrafo original

---

## Passo 5: Auto-revisão de Naturalidade

Após traduzir, releia o texto completo respondendo mentalmente a cada pergunta:

1. Alguma frase soa como tradução literal do PT-BR? → Reescrever com estrutura nativa
2. Alguma palavra ou expressão do PT-BR ainda está presente? → Substituir conforme o padrão
3. O tom é consistente do início ao fim (informal/formal)? → Ajustar inconsistências
4. Os CTAs soam naturais e motivadores na língua alvo? → Verificar cada um
5. Alguma construção típica de IA aparece? Rode as contagens de `regras-anti-ia.md` (carregado no Passo 1) no texto traduzido: **em-dash (—) = 0** (Ctrl+F/grep; trocar por vírgula, ponto ou parênteses), antítese-por-negação ≤ 2, filler words e frases-tipo do **anexo do idioma-alvo**. → Reescrever o que falhar. As próprias correções podem reintroduzir IA: re-conte depois de corrigir.
6. O texto tem o mesmo impacto persuasivo do original? → Ajustar se necessário
7. O tratamento é consistente do início ao fim? Nenhum verbo está conjugado para "tu" quando o tratamento escolhido é "você", ou vice-versa? → Corrigir qualquer inconsistência

---

## Passo 6: Comprimento e Completude

Compare a contagem de palavras da tradução com o original. A regra depende do tipo de conteúdo identificado no Passo 3:

**Peças com espaço limitado** (criativo estático ou carrossel, anúncio, legenda, assunto/preheader de e-mail, título, subtítulo e CTA de landing page): o layout foi desenhado para o tamanho do original.
- Se a tradução for **mais de 10% maior**: corte frases redundantes, qualificadores desnecessários e explicações óbvias, mantendo o gancho, os dados concretos e os CTAs
- Se a tradução for **mais de 10% menor**: verifique se alguma informação foi perdida e reinsira com adaptação adequada

**Texto corrido** (blogpost, newsletter, novidades de produto, corpo de e-mail, texto de página): a diferença pode passar de 10%. **Não corte conteúdo por diferença de tamanho** — línguas diferentes têm estruturas diferentes, e em blogpost a tradução também adapta o texto para a busca da região (termos, exemplos e formulações que o público do país-alvo pesquisa), o que pode pedir trechos reescritos ou mais longos. Nunca acrescente dado, número ou afirmação que não esteja no original.
- Se a tradução for **mais de 15% menor**: verifique se algum parágrafo, frase ou dado foi omitido e reinsira com adaptação adequada

Na dúvida sobre o tipo, trate como peça com espaço limitado.

---

## Passo 7: Salvar Output

Determine o mês corrente no formato `YYYY-MM`.

Determine o nome do arquivo de output:
- Se nome customizado foi fornecido como terceiro argumento: use-o (sanitize: minúsculas, hífens, sem espaços, sem acentos no nome do arquivo)
- Caso contrário: use o nome do arquivo source sem extensão (ex: `newsletter` de `newsletter.md`)

Salve os seguintes arquivos:

**Cópia do original** (para referência do revisor):
`traducao/entregas/YYYY-MM/[nome]-original.md`

```
# [nome] — Original (PT-BR)
**Data**: [DATA]
**Idioma alvo**: [Português Europeu | Español Latinoamericano]

---

[conteúdo completo do texto fonte, sem alterações]
```

**Tradução**:
`traducao/entregas/YYYY-MM/[nome]-[pt-pt|es-latam].md`

```
# [nome] — [PT-PT | ES-LATAM]
**Traduzido em**: [DATA]
**Idioma fonte**: Português Brasileiro
**Idioma alvo**: [Português Europeu (PT-PT) | Español Latinoamericano (ES-LATAM)]
**Palavras original**: [N]
**Palavras tradução**: [N]
**Variação**: [+X% | -X% | igual]

---

[texto traduzido completo]
```

---

## Output para o Usuário

Ao finalizar, informe:
- Caminhos dos arquivos criados
- Contagem de palavras: original vs. tradução (e variação percentual)
- As 5 principais substituições vocabulares aplicadas
- Instrução para revisar: `/trad-revisar traducao/entregas/YYYY-MM/[nome]-[target].md [target]`
