# Buzz Compass — fórmula de scoring

Todos os 4 sub-scores e o Compass Score final são **calculados em código** (`api/radar.js`), a
partir de dados reais devolvidos pela API do Buzzmonitor Trends para o segmento informado pelo
lead (janela de 30 dias). A IA nunca escolhe nem ajusta esses números — ela só escreve a
narrativa em cima deles. Isso é intencional: um score que "a IA decidiu" não é auditável; uma
fórmula documentada é.

**Histórico:** os nomes e a fórmula do sub-score #4 mudaram em 2026-09-02. Era "Inteligência
competitiva" (canais ativos + contagem de influenciadores) — descartado porque não media
concorrência nenhuma de verdade, e a busca de influenciadores por trás dele podia trazer nomes
irrelevantes (ex.: perfis de celebridades sem relação com o segmento). Os sub-scores #1 e #3
também foram renomeados pra bater com o que a fórmula realmente mede (ver nomes atuais abaixo).

## 1. Volume do mercado

Volume total de menções do segmento em 30 dias (`historical_volume.json`, soma de
positivo+neutro+negativo), mapeado em faixas (escala log, porque volume de menções varia em
ordens de grandeza entre segmentos):

| Volume total (30d) | Score |
|---|---|
| ≤ 50 | 15 |
| ≤ 200 | 30 |
| ≤ 1.000 | 50 |
| ≤ 5.000 | 70 |
| ≤ 20.000 | 85 |
| > 20.000 | 97 |

## 2. Sentimento

```
score = positivos / (positivos + negativos) × 100
```

Menções neutras ficam fora do denominador (não carregam informação de polaridade). Sem
positivo/negativo suficiente, o score cai no neutro (50) por definição segura.

## 3. Ritmo de crescimento

Compara os últimos 7 dias contra os 7 dias anteriores, na série diária de volume
(`historical_volume.json`, `grouping=period_daily`):

```
crescimento_pct = (últimos_7d - anteriores_7d) / anteriores_7d
score = 50 + clamp(crescimento_pct × 100, -50, +50)
```

50 = estável. Acima de 50 = segmento ganhando tração. Abaixo = perdendo. O teto/piso de ±50
evita que um pico isolado (ex.: um trend viral de 1 dia) distorça o score pra fora da escala
0-100.

## 4. Diversidade de temas

Mede se a conversa do segmento está concentrada em poucos assuntos ou espalhada por muitos,
usando a mesma chamada de termos mais citados (`historical_volume.json`, `grouping=term`) que já
alimenta a nuvem de palavras. A API sempre devolve um teto fixo de 20 termos por segmento
(testado em vários segmentos reais), então **contar quantos termos existem não diferencia nada**
— o sinal real está em quanto os 3 termos principais concentram do volume total:

```
top3_share = soma(valor dos 3 termos mais citados) / soma(valor de todos os termos)
score = 100 - clamp(((top3_share - 0.25) / 0.20) × 100, 0, 100)
```

Quanto MENOR a concentração nos 3 termos principais, mais diversificada a conversa (mais ângulos
de conteúdo pra explorar). A faixa `[0.25, 0.45]` foi calibrada observando a concentração real de
6 segmentos testados (variou de ~13% a ~42% dependendo do termo isolado, ~29% a ~42% olhando os
top 3) — é uma calibração empírica, documentada como tal, não uma constante universal.

**Por que essa fórmula substituiu a anterior:** a versão antiga ("Inteligência competitiva")
combinava canais ativos + contagem de influenciadores, mas não media concorrência nenhuma de
verdade, e a busca de influenciadores por trás dela podia trazer nomes completamente
irrelevantes ao segmento (ex.: celebridades sem relação com o tema). Diversidade de temas usa só
o dado de termos, que já demonstrou ser confiável e sem esse tipo de ruído.

## 5. Compass Score (final)

Média ponderada dos 4 sub-scores:

```
radar_score = volume_do_mercado×0.25 + sentimento×0.25 + ritmo_de_crescimento×0.30 + diversidade_de_temas×0.20
```

Pesos maiores em ritmo de crescimento (é o sinal mais "acionável agora") e sentimento/presença (os dois
sinais mais diretamente verificáveis pelo próprio lead). Pesos são ajustáveis — estão nomeados em
código (`radarScoreFinal()`), não hardcoded como número mágico solto.

## Sinal extra: menções da própria empresa

A function também roda uma chamada extra (`historical_volume.json`, grouping `sentiment`) usando
o nome da empresa do lead, não o segmento. Esse número **não entra em nenhum score** — ele vira
insight na narrativa: se vier perto de zero (comum pra marcas pequenas, já que a versão gratuita
do Trends só enxerga o que já foi indexado por projetos de clientes), isso é tratado como dado
válido ("sua marca ainda não aparece nas conversas do seu mercado"), não como erro.

## Totem: Compass Score da MARCA, leitura do SEGMENTO

O totem (`api/totem.js`) mostra **um score da marca** (`api/_lib/score.js`, testado em `tests/score.test.js`) e uma leitura
do **segmento** (a conversa inteira do mercado, com a marca e os concorrentes dentro). Cada parte da tela leva a etiqueta
**Marca** ou **Segmento**. O score de mercado da LP original não existe no totem.

| Sub-score (0 a 100) | Peso | Como é calculado |
|---|---|---|
| **Presença** | 25% | metade pela participação na conversa frente a uma divisão igual entre as marcas comparadas (2x a fatia justa = 100), metade pela escala de volume (mesmas faixas da LP original). Sem concorrentes, só o volume |
| **Reputação** | 30% | % de posts positivos entre os que têm polaridade; com 200 menções ou mais, 30% do sub-score vem do peso das queixas (10% das menções com linguagem de reclamação zera essa parte) |
| **Ritmo de crescimento** | 20% | última semana contra a anterior, mesma fórmula da LP original (50 = estável, teto e piso de 50 pontos) |
| **Vantagem competitiva** | 25% | 50 + 0,6 x (reputação da marca - média dos concorrentes) + 0,4 x (ritmo da marca - média dos concorrentes), de 0 a 100. Sem concorrentes, 50 |

`Compass Score = 0,25 x Presença + 0,30 x Reputação + 0,20 x Ritmo + 0,25 x Vantagem`.

**Marca com pouca conversa nunca vira "sem dados".** A Trends só devolve 30 dias (testado: 60, 90 e 180 dias voltam o
mesmo total e a série diária tem 31 pontos), então não dá para ampliar o período. Em vez disso, Reputação e Ritmo são
**completados pelo segmento na proporção da falta de dados** (ponderação por confiança): o peso da marca é
`n / (n + K)`, com `n` = posts com polaridade e `K` = 40 para Reputação, e `n` = menções nas duas últimas semanas e `K` = 30
para Ritmo. Com muita conversa, o número é só da marca; sem nenhuma, é o do segmento. Abaixo de 60% de peso da marca, o
sub-score recebe o rótulo "estimado" e a tela mostra uma nota. A Presença não entra nessa regra: ser pouco falada é o
próprio resultado, e a leitura trata isso como espaço a ocupar. A Vantagem usa as mesmas regras para cada concorrente.

**@ do Instagram da marca (campo opcional).** O visitante pode informar o perfil. Ele entra de duas formas: (1) como
alternativa `OR @perfil` na busca da marca, que ajuda a ancorar nomes de palavra comum (vivo, natura); (2) uma conferência na
busca de perfis da Trends (`bmPerfilInstagram`, junto com o plano de buscas, sem somar tempo). A Trends só conhece perfis
com 1.000+ seguidores que estejam na base dela, e a busca é aproximada (o nome devolvido é comparado com o @ e com a marca).
Achou: a tela mostra "perfil confirmado" com nome e seguidores. Não achou (ex.: `@naturabrasil` não está na base):
nada é recusado, o @ segue valendo na busca e a tela diz que ele é usado como referência. Limitação: `@perfil` na busca de
posts só pega **menções** ao perfil, não os posts que o perfil publica; por isso é âncora, não medição do perfil.

Os pesos, `K` e os limiares são constantes no topo de `score.js`; são calibração por julgamento, não por dados históricos.

O restante desta seção descreve a leitura do segmento e da comparação:

- **Busca por grupo e busca do mercado.** Uma query por grupo (marca, cada concorrente, categoria) na onda 1, para medir
  volume e escolher concorrentes; depois a união `(categoria) OR (marca) OR (c1) ...` é lida com as mesmas chamadas da LP
  original (sentimento, canais, volume diário, termos, termos emergentes por quinzena, gênero, posts). Idioma pt, todas as
  redes no volume (posts usam facebook, instagram, misc, twitter). Sintaxe aceita e testada: `OR`, aspas, parênteses,
  `-termo`; `AND`/`NOT` não funcionam (ver README).
- **Amostra.** Temas de oportunidade e risco vêm de uma amostra aleatória de 30 posts (a skill de buscas usa `random`);
  os top posts exibidos e o formato que performa, dos mais engajados.
- **Nuvem.** Os termos que vêm da própria busca (categoria, marca e concorrentes) e as palavras de ruído de rede social
  ("link", "bio", "whatsapp") saem da lista antes de desenhar a nuvem: senão o termo buscado sempre domina.
- **Comparação (não entra no Compass Score).** Participação na conversa = volume da marca / soma dos volumes da marca e dos
  concorrentes. % positivo = positivos / (positivos + negativos). Crescimento = últimos 7 dias contra os 7 anteriores.
  Marca com menos de 50 menções não é ranqueada por % positivo nem por crescimento. A série diária de cada linha é
  desenhada na própria escala (compara ritmo, não volume).
- **Escolha dos concorrentes.** Os informados sempre entram, mesmo sem conversa (zero é resultado). O que faltar vem da
  sugestão da IA, preferindo o volume mais próximo ao da marca; candidato sem nenhuma conversa é descartado.
- **Busca do segmento.** Vem da IA (termos do que a pessoa fala sobre o segmento, sem nomes de marcas). Sem IA, cai para as
  palavras do segmento ligadas por OR (ex.: "Calçados e Chinelos" vira `Calçados OR Chinelos`).
- **Gênero.** Mesma regra da LP: só Feminino e Masculino entram na pizza (perfis sem gênero identificado são a maioria).
- **Cache.** A análise é GET e fica 24h na borda: mesma marca, segmento e concorrentes = mesmo resultado nesse período.
