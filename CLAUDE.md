# Agente Inhouse — Buzzmonitor

Este agente automatiza a criacao de newsletters e traducoes de copy para a Buzzmonitor, plataforma brasileira de social listening e inteligencia de redes sociais.

## Idioma
Todo conteudo gerado deve ser em **portugues brasileiro**.

---

## Como Usar Este Agente

| Comando | O que faz |
|---|---|
| `/news-pipeline` | Faz tudo: pesquisa, gera 5 newsletters e revisa. Use para o fluxo completo. |
| `/news-pesquisar` | So a pesquisa (blog Buzzmonitor, noticias, concorrentes) |
| `/news-gerar` | So gera os rascunhos (requer pesquisa feita antes) |
| `/news-revisar` | So revisa os rascunhos gerados |
| `/trad-pipeline [arquivo] pt-pt` | Traduz e revisa para Portugues Europeu |
| `/trad-pipeline [arquivo] es-latam` | Traduz e revisa para Espanhol Latino-Americano |
| `/trad-traduzir [arquivo] [pt-pt\|es-latam]` | So traduz (sem revisar) |
| `/trad-revisar [arquivo] [pt-pt\|es-latam]` | So revisa uma traducao ja feita |
| `/trad-calibrar pt-pt` | Atualiza o padrao linguistico PT-PT com novos exemplos nativos |
| `/trad-calibrar es-latam` | Atualiza o padrao linguistico ES-LATAM com novos exemplos nativos |

**Exemplo de traducao**: `/trad-pipeline meu-texto.md pt-pt`

---

## Onde Encontrar os Resultados

| O que procura | Onde esta |
|---|---|
| Newsletters do mes atual | `newsletter/entregas/YYYY-MM/` |
| Pesquisa que originou as newsletters | `newsletter/pesquisa/` |
| Newsletters de meses anteriores | `newsletter/entregas/arquivo/` |
| Traducoes do mes atual | `traducao/entregas/YYYY-MM/` |
| Informacoes sobre o produto | `conhecimento/produto/` |
| Guia de estilo de escrita | `conhecimento/editorial/` |
| Padroes linguisticos (PT-PT / ES-LATAM) | `conhecimento/linguistico/` |

---

## Estrutura do Projeto

```
CLAUDE.md                        <- voce esta aqui
conhecimento/
  produto/                       <- buzzmonitor.md, concorrentes.md
  editorial/                     <- estilo-newsletter.md
  linguistico/                   <- pt-portugal/, es-latam/
newsletter/
  pesquisa/                      <- material do ciclo atual
  entregas/YYYY-MM/              <- newsletters finais por mes
traducao/
  entregas/YYYY-MM/              <- traducoes finais por mes
.claude/                         <- configuracao do agente (nao editar)
```

---

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
- Verificar nomes de features contra `conhecimento/produto/buzzmonitor.md` antes de publicar
- **Todo texto deve ter acentuacao e pontuacao corretas em portugues brasileiro** (nao omitir acentos)
- **Se usar nome de vies cognitivo ou efeito psicologico, a descricao deve corresponder a definicao real do conceito**

---

## Arquivos de Referencia

### Newsletter
- `conhecimento/produto/buzzmonitor.md` — Features, cases, nomes corretos do produto
- `conhecimento/produto/concorrentes.md` — Mapa competitivo com diferenciais
- `conhecimento/editorial/estilo-newsletter.md` — Guia de estilo detalhado e anti-patterns

### Traducao
- `conhecimento/linguistico/pt-portugal/padrao-linguistico.md` — Vocabulario, tom e anti-patterns PT-PT
- `conhecimento/linguistico/es-latam/padrao-linguistico.md` — Vocabulario, tom e anti-patterns ES-LATAM
