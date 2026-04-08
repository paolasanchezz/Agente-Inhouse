# Agente de Newsletter - Buzzmonitor

Este projeto automatiza a criacao de newsletters semanais para a Buzzmonitor, plataforma brasileira de social listening e inteligencia de redes sociais.

## Idioma
Todo conteudo gerado deve ser em **portugues brasileiro**.

## Estrutura do Projeto
- `conhecimento/` — Base de conhecimento verificada (produto, concorrentes, estilo)
- `conhecimento/pt-portugal/` — Padrao linguistico do Portugues Europeu
- `conhecimento/es-latam/` — Padrao linguistico do Espanhol Latino-Americano
- `pesquisa/` — Output da fase de pesquisa do mes corrente (arquivos anteriores em `pesquisa/arquivo/YYYY-MM/`)
- `newsletters/YYYY-MM/` — Newsletters finais organizadas por mes
- `traducoes/YYYY-MM/` — Traducoes de copy organizadas por mes

## Skills Disponiveis

### Newsletter
- `/pesquisar` — Pesquisa blog, noticias e concorrentes
- `/gerar-newsletter` — Gera 5 rascunhos a partir da pesquisa
- `/revisar` — Revisa qualidade, fatos e estilo
- `/pipeline` — Executa tudo em sequencia

### Traducao de Copy
- `/pesquisar-padrao pt-pt` — Pesquisa sites portugueses e atualiza o padrao linguistico PT-PT
- `/pesquisar-padrao es-latam` — Pesquisa sites LATAM e atualiza o padrao linguistico ES-LATAM
- `/traduzir [arquivo] [pt-pt|es-latam]` — Traduz copy BR para PT-PT ou ES-LATAM (requer arquivo e padrao linguistico)
- `/revisar-traducao [arquivo] [pt-pt|es-latam]` — Revisa como nativo e publica no Notion (pasta Entregas)
- `/pipeline-traducao [arquivo] [pt-pt|es-latam]` — Executa traducao + revisao em sequencia

## Regras de Qualidade (OBRIGATORIAS)

### Construcoes Proibidas
1. **Nunca** usar "Nao e X, e Y" ou variacoes ("Nao se trata de X, mas sim de Y")
2. **Nunca** usar aberturas genericas de IA: "No cenario atual...", "Em um mundo cada vez mais...", "Nos ultimos anos...", "E inegavel que..."
3. **Nunca** usar filler words: "realmente", "verdadeiramente", "simplesmente", "basicamente", "literalmente", "definitivamente"
4. **Nunca** iniciar mais de 1 paragrafo por newsletter com "Imagine que..."
5. **Nunca** usar listas de exatamente 3 itens como padrao (variar entre 2, 4, 5)
6. **Nunca** usar "Alem disso" como abertura de paragrafo mais de 1 vez por newsletter
7. **Nunca** usar CTAs agressivos ("Nao perca!", "Corra!", "Ultima chance!")

### Obrigacoes
- Cada newsletter deve abrir com gancho baseado em dado real, vies cognitivo ou cenario surpreendente
- Buzzmonitor deve ser posicionada como facilitadora, nunca como protagonista
- Preferir dados concretos e exemplos reais a afirmacoes genericas
- **Maximo 600 palavras por newsletter**
- Verificar nomes de features contra `conhecimento/buzzmonitor.md` antes de publicar
- **Todo texto deve ter acentuacao e pontuacao corretas em portugues brasileiro** (nao omitir acentos)
- **Se usar nome de vies cognitivo ou efeito psicologico, a descricao deve corresponder a definicao real do conceito**

## Arquivos de Referencia

### Newsletter
- `conhecimento/buzzmonitor.md` — Features, cases, nomes corretos do produto
- `conhecimento/concorrentes.md` — Mapa competitivo com diferenciais
- `conhecimento/estilo-newsletter.md` — Guia de estilo detalhado e anti-patterns

### Traducao
- `conhecimento/pt-portugal/padrao-linguistico.md` — Vocabulario, tom e anti-patterns PT-PT
- `conhecimento/es-latam/padrao-linguistico.md` — Vocabulario, tom e anti-patterns ES-LATAM
