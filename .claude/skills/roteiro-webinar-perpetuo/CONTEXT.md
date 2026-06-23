# Contexto Compartilhado — Webinar

> Este arquivo e lido pela skill `roteiro-webinar-perpetuo` antes de qualquer acao.

---

## Protocolo de Copy (os 3 pilares — OBRIGATORIO)

Webinar e copy publica (audio + slides). Carregar antes de escrever:

1. **Linguistico** — se `idioma` != `pt-br`: `conhecimento/linguistico/{pt-portugal|es-latam}/padrao-linguistico.md` (pasta pelo idioma resolvido). Se nao carregar, PARAR (rodar `/trad-calibrar [pt-pt|es-latam]`).
2. **Boas praticas** — `conhecimento/copywriting/fundamentos-copy.md` + `funil-copy.md` + `video-curto-talking-head.md` + `video-curto-organico.md` (retencao/lo-fi) + `email-copy.md` (CTA + gancho de titulo). O speaker fala a camera; as tecnicas sao aplicadas **por nome de secao** nos Passos 2-3 (lidas do doc em runtime, nunca decoradas — melhorou o doc, melhorou o roteiro).
3. **Anti-IA** — `conhecimento/editorial/regras-anti-ia.md` + anexo do idioma (PT-PT / ES-LATAM).

Referencia global em `CLAUDE.md` (secao "Protocolo de Copy").

---

## Marcas Validas + Inferencia

A `marca` e **opcional** nos argumentos. Se omitida, infira a partir do `tema` pelos sinais abaixo (1 marca dominante → use e declare no plano; empate ou nenhum sinal → PARE e pergunte, nao chute). Sempre **carregue o `BRANDBOOK.md` INTEIRO** da marca resolvida — nao so as secoes extraidas.

| Marca | BRANDBOOK | Sinais no tema (para inferencia) |
|---|---|---|
| `buzzmonitor` | `brand/buzzmonitor/BRANDBOOK.md` | social listening, monitoramento, escuta de redes, mencoes, sentimento, reputacao, crise, trending, analytics de redes |
| `cxpress` | `brand/cxpress/BRANDBOOK.md` | atendimento, SAC, WhatsApp, omnicanal, chatbot, ticket, suporte, customer experience, central de atendimento |
| `buzzcreators` | `brand/buzzcreators/BRANDBOOK.md` | influenciador, creator, criador de conteudo, marketing de influencia, ROI de influencia, campanha com creators |
| `elife` | `brand/elife/BRANDBOOK.md` | consultoria, social intelligence, consumidores sinteticos, pesquisa de consumo, social CRM, inteligencia de consumo |

## Regiao ⟺ Idioma (eixo unico, 1:1)

`regiao` e `idioma` sao o mesmo eixo. O usuario pode passar **um, o outro, os dois ou nenhum**:

| Regiao | Idioma (codigos aceitos) | Pasta linguistico | Pasta produto lang |
|---|---|---|---|
| `brasil` | `pt-br` / `br` (PT-BR) | nenhuma | nenhuma |
| `portugal` | `pt-pt` / `pt` (PT-PT) | `pt-portugal` | `pt-pt` |
| `latam` | `es-latam` / `es` (ES-LATAM) | `es-latam` | `es` |

- Deu so um → derive o outro pela tabela. Deu nenhum → `brasil` / `pt-br`.
- Deu os dois e inconsistentes → **`idioma` manda** na copy e no pilar linguistico; avise no plano.
- Se `idioma` != `pt-br`: carregar `conhecimento/produto/{marca}/{pasta-lang}/{marca}.md` + `conhecimento/linguistico/{pasta-linguistico}/padrao-linguistico.md` (**gate**: se faltar, PARAR e rodar `/trad-calibrar [pt-pt|es-latam]`).
- O `idioma` resolvido vai no campo `idioma:` do frontmatter de TODAS as entregas e rege a subsecao "Adaptacao por Regiao" do BRANDBOOK (artigo gramatical incluso).

## Identidade de Marca

Sempre carregar `brand/{marca}/brand-manifest.json` para tom de voz (campos `voice.toneAttributes`, `voice.samplePhrases.do/dont`, `voice.messagingPillars`).

## Estrutura do Webinar Perpetuo (padrao)

Webinar perpetuo = video pre-gravado que roda como se fosse "ao vivo" para leads novos. Diferente de webinar ao vivo:
- **Sem interacao real** — speaker nao responde Q&A no momento. Engajamento e fingido com referencias genericas ("vejo perguntas chegando", "muitos comentando isso") so se a marca permitir; caso contrario, evitar.
- **Tem que prender desde o segundo 1** — leads novos largam rapido. Hook forte no inicio + reforco de promessa antes da demo.
- **Demo da plataforma e o ponto alto** — leva pelo menos 40-50% do tempo total. E o que justifica o webinar versus um post de blog.
- **CTA inevitavel ao final** — agendamento de demo / teste gratis / fala com vendas, conforme estagio.

## Distribuicao de tempo por duracao total

| Duracao | Abertura (Hook + Contexto + Dor) | Solucao + Demo | Fechamento + CTA |
|---|---|---|---|
| 5 min | 1 min | 3 min | 1 min |
| 10 min | 2 min | 6 min | 2 min |
| 15 min | 3 min | 9 min | 3 min |
| 20 min | 4 min | 12 min | 4 min |
| 30 min | 5 min | 20 min | 5 min |

Default: **10 min**.

## Slides de Abertura (deck PPT/Keynote)

5-7 slides enxutos que aparecem ANTES da demo (durante a abertura). Funcao: dar contexto visual enquanto o speaker fala.

Regras:
- **1 ideia por slide** — nunca empilhar bullets.
- **Texto minimo** — frase de 4-8 palavras + visual ou dado grande.
- **Sem clipart generico.** Se a marca tem mockups/screenshots no BRANDBOOK, sugerir uso especifico.

Composicao tipica (10 min):
1. **Capa** — titulo do webinar + nome do speaker + marca
2. **Quem fala** — speaker em 1 frase de credibilidade
3. **Promessa** — o que voce vai aprender em N minutos
4. **Contexto/dado** — o numero ou fato que abre a dor
5. **A dor** — frase unica que cristaliza o problema
6. **Ponte para demo** — "vou te mostrar como isso se resolve na pratica"
7. **(opcional)** Agenda dos 3 momentos da demo

## Demo da plataforma

Sugerir telas/features especificas do BRANDBOOK da marca (grafias exatas). Cada momento da demo carrega:
- **Tela:** o que o speaker abre na plataforma (feature exata)
- **O que mostrar:** acoes especificas (cliques, filtros, fluxo)
- **Fala sugerida:** 1-3 frases que o speaker fala enquanto navega
- **Por que importa:** conexao com a dor levantada na abertura

Se a marca nao tem mockup de uma feature mencionada, sugerir captura generica + nota "verificar com produto".

## Convencoes de Output

- Pasta local: `conhecimento/copywriting/criacao/{marca}/YYYY-MM-DD/webinar-{slug}/`
- Arquivos:
  - `roteiro.md` — script completo com timestamps
  - `slides-abertura.md` — copy de cada slide do deck
  - `INDICE.md` — resumo + proximos passos
  - `REVISAO-LOG.md` — log da varredura anti-IA

## Notion

ID lido de `conhecimento/config/notion-ids.md` (chave `entregas`). Publicar em subpasta `Webinars — {NomeDaMarca}` (criar se nao existir).
