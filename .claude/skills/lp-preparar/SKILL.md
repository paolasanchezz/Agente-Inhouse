---
name: lp-preparar
description: Estrutura copy crua em blocos rotulados (OVERLINE, H1, H2, BODY, CTA, etc.) e passa revisao anti-IA conservadora, sem alterar o tom. Publica no Notion e salva arquivo local para o lp-gerar consumir.
argument-hint: "[marca] [slug] [fonte] — ex: buzzmonitor monitoramento-maio https://notion.so/... ou buzzmonitor monitoramento-maio ./copy-bruta.txt"
allowed-tools: Read, Write, Glob, Grep, WebFetch, mcp__d23bd62b-b780-49e6-9a00-d29a01f11d75__notion-fetch, mcp__d23bd62b-b780-49e6-9a00-d29a01f11d75__notion-create-pages, mcp__d23bd62b-b780-49e6-9a00-d29a01f11d75__notion-update-page
version: 1.2.1
---

# Skill: Preparar Copy de Landing Page

Voce estrutura copy crua de LP em blocos rotulados para o gerador de HTML consumir. **Nao reescreve o tom, nao inventa secoes, nao decora com emojis.** Passa uma revisao anti-IA conservadora: marca sugestoes inline, nao aplica silenciosamente.

## Passo 0: Parsing e Contexto

Leia `.claude/skills/lp-preparar/CONTEXT.md` — marcas, estrutura de pastas, convencoes de slug, pasta Entregas do Notion.

Faca parsing de `$ARGUMENTS`:

| Argumento | Valores | Obrigatorio |
|---|---|---|
| `marca` | `buzzmonitor` \| `buzzcreators` \| `cxpress` \| `elife` | Sim |
| `slug` | kebab-case curto (ex: `monitoramento-maio`) | Sim |
| `fonte` | URL Notion, caminho de arquivo local, ou texto colado | Sim |

Se faltar algo, PARE e mostre uso:
```
Uso: /lp-preparar [marca] [slug] [fonte]
Exemplo: /lp-preparar buzzmonitor webinar-maio https://www.notion.so/Copy-LP...
```

## Passo 1: Carregar Base de Conhecimento

Leia, na ordem:

1. `landing-pages/GUIDELINES.md` — §5 (copy), §8 (secoes-tipo), §9 (copy dita estrutura), §10 (posicionamento do form), §11 (integracao tardia). Regras de design.
2. `landing-pages/CONTEXT.md` — runbook operacional comum a todas as skills lp-* (fluxos, assets, troubleshooting). Use principalmente §2.2 (matriz de alteracao) se a copy ja foi publicada antes.
3. `conhecimento/editorial/regras-anti-ia.md` — frases bloqueadas, filler words, anti-patterns estruturais.
4. `brand/{marca}/brand-manifest.json` — tom de voz e messaging (para reconhecer termos proprios da marca antes de revisar).
5. `brand/{marca}/BRANDBOOK.md` — grafias corretas (ex: "Buzzmonitor" nao "BuzzMonitor") e nomes oficiais de features.

## Passo 2: Obter Copy Bruta

Detectar tipo da fonte nesta ordem:

1. Comeca com `http://`, `https://`, ou contem `notion.so/` → **URL Notion.** Use `notion-fetch`. Extrair apenas texto, ignorar metadados.
2. Termina com `.txt`, `.md`, `.markdown`, ou contem `/` ou `\` (path): → **Arquivo local.** Use `Read`.
3. Tudo o mais → **Texto colado inline.** Usar como esta.

Se houver ambiguidade (ex: string sem extensao nem URL mas com espacos — parece texto): tratar como texto colado.

Normalize: remover emojis decorativos, remover markdown visual (===, ---, **negritos faceis**), preservar quebras logicas.

## Passo 3: Estruturar em Blocos Rotulados

Siga **a ordem narrativa da copy** (GUIDELINES §9). Nao reorganizar. Nao adicionar blocos que nao existem. Nao cortar.

### Rotulos canonicos

```
OVERLINE: texto supra-titulo, tag, ou contexto curto
H1: titulo principal (hero)
H2: titulo de secao
H3: subtitulo dentro de secao
SUB: subtitulo do hero ou de H2 (linha de apoio curta)
BODY: paragrafo de corpo
LIST ITEM: item de lista (cada item em linha separada com rotulo)
QUOTE: depoimento, citacao
LABEL: rotulo de campo, badge, chip, tag de urgencia
CTA: botao de acao (texto exato do botao)
FOOTER: rodape (copyright, links legais)
```

### Formato de saida

Texto flat, um rotulo por linha, separador `\n\n` entre secoes logicas:

```
=== HERO ===
OVERLINE: Webinar Online e Ao Vivo · 26 de Maio, 19h
H1: Monitorar concorrentes nao e espionagem. E estrategia.
SUB: Aprenda o metodo que empresas como X usam para antecipar movimentos de mercado.
CTA: Garanta sua vaga gratuita

=== PROBLEMA ===
H2: Voce olha para a concorrencia, mas nao enxerga.
LIST ITEM: Descobre lancamentos depois que ja viralizaram.
LIST ITEM: Depende de screenshots manuais para acompanhar campanhas.
LIST ITEM: Nao sabe quais temas sua concorrencia esta ganhando tracao.

=== BENEFICIOS ===
H2: O que voce vai levar deste webinar
LIST ITEM: Framework de monitoramento em 3 etapas
LIST ITEM: Como detectar mudancas de posicionamento em tempo real
LIST ITEM: Template pronto para reportar insights ao C-level

=== URGENCIA ===
LABEL: VAGAS LIMITADAS
H2: Apenas 200 vagas. Transmissao nao fica gravada para nao-inscritos.
BODY: Se voce chegou ate aqui, faz sentido garantir agora.
CTA: Quero minha vaga

=== FOOTER ===
FOOTER: (c) 2026 Buzzmonitor. Todos os direitos reservados.
```

### Regras

- **Copy literal.** Preservar aspas curvas, ellipsis, en-dash (`–`) e pontuacao original. Nao parafrasear.
- **Em-dash (`—`) NUNCA e preservado.** Mesmo que apareca na copy bruta, substituir por virgula/ponto/parenteses conforme tabela do Passo 4 antes de salvar. Tolerancia zero por `conhecimento/editorial/regras-anti-ia.md` e GUIDELINES §5.
- **Nao criar rotulos novos.** Se algo nao cabe em nenhum rotulo, usar `BODY`.
- **Agrupar por secao** com marcadores `=== NOME-DA-SECAO ===` (maiusculas, kebab com hifen ou espaco). Nome curto e descritivo.

## Passo 4: Revisao Anti-IA Conservadora

Passe a copy estruturada contra `regras-anti-ia.md`. **Nao reescreva.** Apenas marque. **Excecao:** em-dash, que tem fix automatico (ver 4.1).

### 4.1: Em-dash (`—`) — fix automatico antes de marcar qualquer outra coisa

Tolerancia zero por `regras-anti-ia.md`. **Substituir direto, nao marcar.** Antes de qualquer marcacao do 4.2 em diante:

1. Contar: `grep -c "—" copy.txt` (esperado: 0). Se > 0, prosseguir.
2. Para cada `—`, ler contexto (palavra antes + palavra depois) e substituir conforme tabela:

| Funcao do em-dash | Substituto |
|---|---|
| Pausa curta dentro da frase | virgula |
| Pausa forte / quebra de pensamento | ponto (duas frases, capitalizando a seguinte) |
| Aparte / informacao adicional | parenteses (envolvendo o trecho) |
| Atribuicao de citacao (`— Autor`) | nova linha + virgula, ou so virgula |

3. Re-contar: `grep -c "—" copy.txt` deve dar **0**. Se ainda > 0, refazer o sweep.

Tambem cuidar de `&mdash;` (entidade HTML) se a copy bruta veio de fonte HTML — mesma logica.

### 4.2: O que marcar (sem reescrever)

- Frases tipicas de IA ("No cenario atual", "E inegavel que", "Vale ressaltar", etc.)
- Filler words (realmente, simplesmente, basicamente, incrivelmente, efetivamente, etc.)
- Transicoes mecanicas ("Alem disso", "Nesse sentido", "Por outro lado")
- Metaforas aquaticas ("navegar", "mergulhar", "oceano de")
- Exclamacao excessiva (mais de 2 na LP inteira)
- Pergunta retorica repetida (mais de 1 por secao)

### Como marcar

Inline, logo apos a linha afetada:

```
BODY: No cenario atual, monitorar concorrentes e essencial.
# [SUGESTAO anti-IA] "No cenario atual" e frase de IA. Alternativa: "Monitorar concorrentes deixou de ser opcional." (deixar a escolha com o usuario)
```

Se nao encontrar nada (depois do 4.1 e 4.2): escreva ao final `# Revisao anti-IA: sem achados (em-dash: 0).`

## Passo 5: Salvar Arquivo Local

Caminho: `landing-pages/{marca}/{slug}/copy.txt`

Se a pasta nao existe, criar. Se `copy.txt` **ja existe**, antes de sobrescrever fazer backup:

```bash
cp "landing-pages/{marca}/{slug}/copy.txt" "landing-pages/{marca}/{slug}/copy.txt.$(date +%Y-%m-%d_%H%M).bak"
```

Depois sobrescrever (`copy.txt` e a versao autoritativa para `lp-gerar`). O .bak preserva edicoes manuais anteriores — se o usuario tiver alterado o arquivo fora do pipeline, nao se perde.

## Passo 6: Publicar no Notion

Publique na pasta Entregas — ID lido de `conhecimento/config/notion-ids.md` (chave `entregas`).

- **Titulo:** `Copy LP · {Marca} · {Slug} · YYYY-MM-DD`
- **Icon:** 📝
- **Conteudo:** bloco de code com linguagem `plain text` contendo o arquivo estruturado na integra. Se houver sugestoes anti-IA, lista-las em um toggle "Sugestoes anti-IA (opcionais)" **abaixo** do code block.

O code block e fonte-verdade editavel. O usuario vai colar de volta no `copy.txt` antes do `lp-gerar` se fizer alteracoes.

## Passo 7: Relatorio Final

Apresente ao usuario:

```
Copy preparada — {marca}/{slug}

Arquivo local: landing-pages/{marca}/{slug}/copy.txt
Notion: {URL}

Estrutura identificada:
- {N} secoes (HERO, PROBLEMA, BENEFICIOS, ...)
- {N} blocos totais
- {N} CTAs

Revisao anti-IA: {N} sugestoes marcadas / sem achados

Proximos passos:
- Revisar copy no Notion, aplicar edicoes desejadas
- Quando aprovada: /lp-gerar {marca} {slug}
```
