# Log de Revisão — Newsletter Semanal 2026-W19
**Marca**: Cxpress | **Região**: brasil | **Idioma**: PT-BR
**Data da revisão**: 2026-05-04 (versão original)
**Revisão adicional**: 2026-05-04 (passe de enxugamento + remoção da pergunta-eixo visível, conforme feedback Victor)

## Edição revisada
- **Assunto**: Quando o atendimento trava, o problema é volume ou sistema?
- **Pergunta-eixo (INTERNA — NÃO visível na NL)**: Quando o atendimento da sua empresa trava, o problema é o volume ou o sistema?
- **Status**: APROVADA (com 1 pendência de verificação — URLs sociais)

## Mudanças do passe de enxugamento (versão final)
- **Bloco "## A pergunta da semana" REMOVIDO** — pergunta-eixo virou comentário HTML interno (`<!-- Pergunta-eixo (planejamento interno, NÃO publicar): "..." -->`); não aparece para o leitor
- **Limite de palavras reduzido**: 600 → 300 (corpo)
- **Mini-blocos da resposta encurtados**: ~95 palavras cada → ~40 palavras cada (1-2 frases por bloco)
- **Abertura encurtada**: 51 → 40 palavras
- **Posts secundários**: 2 bullets → 1 bullet (na seção "Mais pra explorar")
- **Total do corpo**: ~376 palavras → ~185 palavras (redução de ~50%)
- Alinhada com novas regras de `template-newsletter.md` v2.1.0 e `news-gerar` v2.1.0

---

## Passada 1: Fact-check, estrutura, links

### Fact-check
- **Pergunta-eixo**: bate com `dor-semana.md` ✓
- **Posts-âncora (3)**: todas as URLs validadas contra `dor-semana.md` ✓
  - https://blog.cxpress.io/o-problema-do-atendimento-ao-cliente-nao-e-o-volume-e-o-sistema/
  - https://blog.cxpress.io/centralizacao-de-canais-otimize-whatsapp-chat-e-email-centralizacao-de-canais/
  - https://blog.cxpress.io/reduzir-tma-melhore-atendimento-satisfacao/
- **Frases-chave alinhadas com ângulo de cada post-âncora** ✓
- **Cases nominais**: nenhum case real citado (BRANDBOOK §2 marca "Cases de Sucesso Verificados" como "a preencher pelo time"). NL usa apenas exemplo genérico ("uma clínica com cinco canais e três atendentes") sem inventar nome de empresa ✓
- **Nomes de features**: nenhuma feature da Cxpress citada pelo nome no corpo ✓
- **Conceitos nomeados**:
  - "produtividade marginal" — termo econômico padrão, definição usada (produtividade adicional cai com cada novo input) está correta ✓
  - "multicanal vs omnichannel" — definição usada (omnichannel = histórico integrado entre canais; multicanal = canais paralelos sem ponte) está correta ✓
  - "TMA", "NPS", "turnover", "handoff" — termos técnicos padrão de CX/RH, sem definição imprecisa ✓

### Estrutura de blocos
- Cabeçalho (assunto + pré-header + metadados) ✓
- Saudação `Oi, {{nome}}.` ✓
- Abertura jornalística (51 palavras, dentro do range 40-60) ✓
- Pergunta da semana em destaque (blockquote markdown + bold) ✓
- Resposta em capítulos (3 mini-blocos) ✓
- Mais pra explorar (2 bullets — opcional, incluído) ✓
- Na imprensa: NÃO incluído (sem clipping na semana — coerente com `clipping-pr.md`) ✓
- Bloco extra: NÃO incluído (sem gancho real da semana) ✓
- Rodapé (assinatura + 3 links sociais) ✓

### Orçamento de links
| Bloco | Min | Encontrado | Max | OK? |
|---|---|---|---|---|
| Resposta em capítulos | 3 | 3 | 3 | ✓ |
| Mais pra explorar | 0 | 2 | 2 | ✓ |
| Na imprensa | 0 | 0 | 1 | ✓ |
| Bloco extra | 0 | 0 | 1 | ✓ |
| **Total contextuais** | **3** | **5** | **6** | **✓** |
| Mínimo blog próprio | 3 | 5 | — | ✓ |
| Notícias gerais (não permitidas) | 0 | 0 | 0 | ✓ |

### Dedupe vs `_state.json`
- `_state.json` foi criado nesta semana (primeira execução v2.0) — sem histórico anterior para comparar
- Pergunta-dor "atendimento que não escala": nunca usada antes ✓
- 5 links contextuais: nenhum em janela de cooldown (4 semanas) ✓

---

## Passada 2: Linguagem jornalística e anti-IA

### Lead jornalístico
Abertura: "Durante muito tempo, escalar atendimento foi sinônimo de contratar mais gente."
- Estrutura de virada do BRANDBOOK Cxpress (§1 "Arquetipos de frase: Lead com virada") ✓
- NÃO começa com "imagine que...", "no mundo atual...", "vivemos uma era..." ✓
- Aceito sem reescrita

### Frases curtas
- Comprimento médio estimado: ~14 palavras/frase ✓
- Frase mais longa: 24 palavras ("O gargalo deixa de ser a quantidade de mãos disponíveis e passa a ser o quanto cada mão precisa caçar contexto antes de responder") — abaixo do limite máximo de 30 ✓

### Tom não-vendedor
- Menções a "Cxpress" no corpo (excluindo URLs e assinatura): **0** ✓
- Menções a "demo", "teste", "webinar", "agendar": **0** ✓
- Links contextuais para domínio próprio fora do blog (demo/landing): **0** ✓
- 100% dos 5 links contextuais apontam para blog.cxpress.io ✓

### Edutainment por mini-bloco
| Mini-bloco | Edutainment encontrado |
|---|---|
| 1. Mais atendentes em canais separados multiplicam o caos | Definição clara (produtividade marginal, gargalo arquitetural) + exemplo concreto (clínica com 5 canais, 3 atendentes, paciente repete 3x) |
| 2. Quando os canais conversam, o histórico segue o cliente | Analogia útil (canais como ilhas) + definição (multicanal vs omnichannel) |
| 3. TMA cai quando o agente para de caçar informação | Exemplo concreto (3 abas) + indicador mensurável (NPS, turnover) |

Todos os mini-blocos atendem ao critério (≥1 dos quatro: analogia, dado, exemplo, definição). ✓

### Anti-IA (varredura completa)
- **Em-dashes (—) como pontuação narrativa**: 0 ocorrências (Ctrl+F manual) ✓
- **Filler words** ("realmente", "no mundo atual", "de forma X", "vivemos uma era"): 0 ✓
- **Antíteses-por-negação**: **2** (limite: 2) — no limite máximo
  1. "perde histórico em vez de resolver tickets" (forma "X em vez de Y")
  2. "IA dentro da arquitetura, não como mais um silo" (forma "X, não Y")
- **"Em resumo" / "em conclusão"**: 0 ✓
- **Listas decorativas de 3 itens**: 0 (a estrutura "3 mini-blocos" é estrutural, não decorativa) ✓
- **Conectivos mecânicos** ("Além disso", "Por outro lado", "Nesse contexto"): 0 ✓

### Idioma (PT-BR)
- Acentuação verificada (três, histórico, fragmentação, única, tendências) ✓
- Tratamento "você" (2ª pessoa) consistente ✓
- "pra" no lugar de "para" em momento conversacional — aceito no registro editorial PT-BR
- Cxpress como substantivo feminino: zero violações no corpo (a marca não é citada nominalmente fora dos URLs e da assinatura "Equipe Cxpress") ✓

---

## Passada 3: Otimização

### Enxugamento
- Texto já enxuto na geração — nenhum corte adicional necessário
- Cada frase justifica sua existência: tese, evidência, exemplo, ou transição

### Fluxo lógico
Abertura → Pergunta-eixo → Bloco 1 (diagnóstico do problema) → Bloco 2 (mecanismo da solução) → Bloco 3 (efeito mensurável) → Mais pra explorar → Assinatura. Progressão natural ✓

### Cabeçalho
- **Assunto** (60 chars): "Quando o atendimento trava, o problema é volume ou sistema?" — jornalístico, sem clickbait ✓
- **Pré-header** (74 chars, limite 80): "Mais atendentes resolvendo num sistema fragmentado só multiplicam o caos." ✓

### Contagem
- **Corpo**: ~376 palavras (limite 600) ✓
- Antes da revisão: 376 → Depois: 376 (sem cortes)

---

## Pendências para o usuário

### `[VERIFICAR]` — URLs de redes sociais
- O BRANDBOOK §5 confirma que Cxpress tem perfis em Instagram, Facebook, YouTube e LinkedIn, mas não lista os URLs exatos
- NL usa estimativas:
  - LinkedIn: `https://www.linkedin.com/company/cxpress/`
  - Instagram: `https://www.instagram.com/cxpress.io/`
  - Site: `https://home.cxpress.io/` (este sim confirmado pelo BRANDBOOK)
- **Ação**: confirmar URLs dos 2 primeiros antes do disparo. Se diferentes, atualizar tanto o arquivo local quanto a página no Notion

### Sem outras pendências
Nenhum dado marcado `[VERIFICAR]` no corpo da newsletter — todas as informações são genéricas ou vêm de posts-âncora reais do blog.

---

## Resumo
**APROVADA** com 1 pendência menor (URLs sociais a verificar).

Newsletter pronta para disparo após confirmação dos URLs sociais. Tom não-vendedor, eixo jornalístico em pergunta-dor, 5 links contextuais (todos blog próprio), edutainment em cada mini-bloco, anti-IA aplicado (zero em-dashes, antíteses no limite, frases curtas).
