# ClickMeeting → Google Sheets (inscritos de webinars)

Workflow do n8n que copia os inscritos dos webinars do ClickMeeting para uma
planilha do Google Sheets, e mantém atualizado sozinho (roda a cada 6h).

- **Arquivo:** `clickmeeting-inscritos-google-sheets.json`
- **Planilha destino:** https://docs.google.com/spreadsheets/d/1CTmui4aWRDoj3rgBEXVa1B0SKDcsznZdLmR2uA_2s8E/edit
  (dona: victor.lopes@buzzmonitor.com.br · já vem com a linha de cabeçalho)

## O que ele faz

1. Lê todas as conferências da conta (`/conferences/active` + `/conferences/inactive`).
2. Filtra só as séries que interessam (mapa `SERIES` no nó **Montar lista de sessões**).
3. Para cada sessão, busca os inscritos (`/conferences/{id}/registrations`).
4. Monta 1 linha por pessoa e grava na planilha em modo **Append or Update**
   (chave = Email + Série), então rodar de novo não duplica — só atualiza/insere.

### Colunas
`Data inscrição · Nome · Email · Empresa · País · Cidade · Marca/Sala · Série · Sessão · Origem · Link de acesso`

> O ClickMeeting **não** guarda marca nem região por inscrito — só a sala em que
> ele caiu. Por isso a coluna **Marca/Sala** é derivada da série, e **País/Cidade**
> vêm do geo (IP) que o ClickMeeting captura. Recorte fino por marca×região exigiria
> criar salas dedicadas por LP ou capturar a origem na inscrição (projeto à parte).

### Mapa de séries (estado em 2026-06-25)
| Série (recurring_config_id) | Marca/Sala |
|---|---|
| 17529 | CX BR \| Conheça Cxpress — sala default da Cxpress |
| 17497 | CX (legado) |
| 17544 | BUZZ LATAM \| Atención |
| 17560 | CREATORS case |
| 17601 | BUZZ BR \| MCP |

> **Atenção à chave de deduplicação:** o nó Google Sheets deve casar por
> **Email + Série** (não só Email). Um mesmo e-mail pode estar inscrito em mais
> de uma sala (ex: webinar de Cxpress + de Atención) — casar só por Email
> colapsa os dois numa linha e mostra a marca errada (a última que escreveu).
> Email + Série mantém uma linha por (pessoa, sala). Incidente 2026-06-25.

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

- **Nova série/sala no ClickMeeting?** Edite o objeto `SERIES` no nó
  *Montar lista de sessões* (chave = recurring_config_id, valor = rótulo).
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
