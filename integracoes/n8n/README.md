# ClickMeeting → Google Sheets (inscritos de webinars)

Workflow do n8n que copia os inscritos dos webinars do ClickMeeting para uma
planilha do Google Sheets, e mantém atualizado sozinho (roda a cada 6h).

- **Arquivo:** `clickmeeting-inscritos-google-sheets.json`
- **Planilha destino:** https://docs.google.com/spreadsheets/d/1CTmui4aWRDoj3rgBEXVa1B0SKDcsznZdLmR2uA_2s8E/edit
  (dona: victor.lopes@buzzmonitor.com.br · já vem com a linha de cabeçalho)

## O que ele faz

1. Lê todas as conferências da conta (`/conferences/active` + `/conferences/inactive`).
2. Descobre sozinho as séries de webinar perpétuo — **qualquer** conferência
   recorrente do tipo webinar (nó **Montar lista de sessões**), sem lista fixa.
   Séries de teste são ignoradas (nome começa com "test"/"teste" ou id em `BLOQUEIO_RID`).
3. Para cada sessão, busca os inscritos (`/conferences/{id}/registrations`).
4. Monta 1 linha por pessoa e grava na planilha em modo **Append or Update**
   (chave = **Email**), então rodar de novo atualiza a pessoa em vez de duplicar.

### Colunas
`Data inscrição · Nome · Email · Empresa · País · Cidade · Marca/Sala · Série · Sessão · Origem · Link de acesso`

> O ClickMeeting **não** guarda marca nem região por inscrito — só a sala em que
> ele caiu. Por isso a coluna **Marca/Sala** é derivada da série, e **País/Cidade**
> vêm do geo (IP) que o ClickMeeting captura. Recorte fino por marca×região exigiria
> criar salas dedicadas por LP ou capturar a origem na inscrição (projeto à parte).

### Auto-descoberta de séries (desde 2026-07-07)
Não há mais lista fixa de `recurring_config_id`. O nó **Montar lista de sessões**
processa **toda** conferência recorrente de webinar que a API retornar, e a coluna
**Marca/Sala** recebe o próprio nome do webinar no ClickMeeting. Quando o marketing
troca ou cria webinars, a planilha acompanha sozinha — foi justamente o mapa fixo
que causou a desatualização anterior (apontava para o Conheça Cxpress antigo `17529`
e não conhecia os webinars novos: Vozxpress, Que es MCP e o Conheça atual).

Séries de webinar ativas hoje (só referência — **não** é config):

| Série (recurring_config_id) | Nome no ClickMeeting |
|---|---|
| 17689 | Conheça Cxpress |
| 17671 | Cxpress Vozxpress |
| 17601 | Buzzmonitor MCP |
| 17646 | Buzzmonitor Que es MCP |
| 17544 | Buzzmonitor Atención al Cliente |
| 17560 | buzzcreators-case |

> Excluídas automaticamente: séries de teste (ex.: `17643` "teste1"). Para tirar
> outra série da planilha, adicione o id em `BLOQUEIO_RID` ou faça o nome bater em
> `BLOQUEIO_NOME`, no nó *Montar lista de sessões*.

> **Chave de deduplicação: apenas `Email`** (decisão do Victor, 2026-07-07). Rodar
> de novo atualiza a pessoa em vez de duplicar. Tradeoff assumido: se a mesma pessoa
> se inscrever em duas séries diferentes, as linhas colapsam numa só (fica a última
> série gravada). Se um dia quiser uma linha por (pessoa, série), troque a matching
> column do nó Google Sheets pra `Email + Série` (contexto: incidente 2026-06-25).

## Setup no n8n (uma vez)

1. **Importar:** n8n → *Workflows* → *Import from File* → escolha o `.json`.
2. **Credencial ClickMeeting** (tipo *Header Auth*):
   - Name: `X-Api-Key`
   - Value: a `CLICKMEETING_API_KEY` (mesma do `.env.local` do repo / do Vercel).
   - Vincule essa credencial nos 3 nós **CM: ...**.
3. **Credencial Google Sheets** (OAuth2) — conecte com a conta
   **victor.lopes@buzzmonitor.com.br** (dona da planilha). Vincule no nó
   **Google Sheets: gravar inscritos**.
4. Abra a planilha e renomeie a 1ª aba para **`Inscritos`** (o nó procura por esse nome).
5. **Testar:** clique em *Execute Workflow* (nó *Disparo manual*). Deve trazer os
   ~15 inscritos atuais. Confira a aba `Inscritos`.
6. **Ativar:** ligue o toggle *Active* — o *Schedule Trigger* passa a rodar a cada 6h.

## Manutenção

- **Nova série/sala no ClickMeeting?** Nada a fazer — entra sozinha na próxima
  execução, com a **Marca/Sala** = nome do webinar. Só mexa se quiser **excluir**
  uma série (ex.: teste): `BLOQUEIO_RID`/`BLOQUEIO_NOME` no nó *Montar lista de sessões*.
- **Mudar cadência:** ajuste o nó *A cada 6 horas*.
- **Volume:** baixo (dezenas). A varredura de todas as sessões por execução é
  proposital — backfilla o histórico e se autocorrige. Se um dia o volume de
  sessões explodir, dá pra limitar `inactive` às últimas N por data.

## Notas técnicas

- Os dois nós de Code são tolerantes a o HTTP Request dividir o array em itens
  **ou** entregar o array bruto — não quebra em nenhum dos casos.
- O nó de inscritos usa *On Error: Continue* pra uma sessão problemática não
  derrubar a execução inteira.
- Nada de segredo é versionado: a API key vive só na credencial do n8n.
