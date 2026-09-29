# Webinar Cxpress OUT — troca de criativos + LP nova (variante B)

- **Data:** 2026-09-22
- **Conta:** Cxpress Brasil (BRL) · `1266529690796936`
- **Campanha:** `[meta][meio][conversão][webinar][outubro]` · `120251126001680183` (existente, nao alterada)
- **Origem do pedido:** Notion "Otimização dos anúncios | Webinar Cxpress OUT" (`3e23934026fd80adb8b9f2ee62b4af19`)
- **Status final:** TUDO PAUSADO (adset + 4 ads). Ativacao pendente de aprovacao do Victor.

## Decisao de estrutura

Victor pediu os 4 anuncios **num unico adset existente**. Escolhido o `Ad_05` — unico
ativo e melhor CpL da campanha (R$ 47,25 vs R$ 73,84 e R$ 84,26). Reaproveitar o adset
preserva publico/pixel/posicionamento, que o MCP da Meta **nao le** (limitacao conhecida)
e portanto nao permitiria clonar com garantia.

Os outros 3 adsets da campanha (`Ad_01` `120251126001670183`, `Ad_02` `120251126171350183`,
`Ad_04` `120251126200590183`) ja estavam PAUSADOS e nao foram tocados.

## Adset

| Campo | Antes | Depois |
|---|---|---|
| ID | `120251166345190183` | (mesmo) |
| Nome | `00\|Lal_Clientes\|Ad_05` | `00\|Lal_Clientes\|BlackFriday_LP-B` |
| Verba/dia | R$ 32,00 | **R$ 350,00** (35000 centavos) |
| Status | ACTIVE | PAUSED (forcado pela edicao) |
| optimization_goal | OFFSITE_CONVERSIONS (Conversao Webinar, `1099190376613999`) | inalterado |

Verba = total da Fase 1 da planilha do Notion (5 ads x R$ 70 = R$ 350/dia), redistribuido
entre 4 anuncios num adset so. **7x o teto do guardrail** (R$ 50/adset/dia) — passou pelo hook.

## Criativos e anuncios criados

Pagina: Cxpress `111141128464819`. Headline `👉 Garanta sua vaga` · CTA `APPLY_NOW`.
LP: `https://content.cxpress.io/black-friday-atendimento-b` (+ UTM padrao da casa, ancora `#inscricao` no fim).
Copy: legendas aprovadas do Notion, verbatim.

| Ad | ad_id | creative_id | image_hash (Feed 1080x1350) |
|---|---|---|---|
| WEB_BlackB_atendimento_01 (Gestao de atendimento) | `120251216808530183` | `1058251420312473` | `08f2dbd95e7ca8ccacac8aea268fbebb` |
| WEB_BlackB_atendimento_02 (Speakers) | `120251216810110183` | `1409348687294819` | `52bc214cff7ac7b7350a415f92f8a572` |
| WEB_BlackB_atendimento_03 (Alto volume sem caos) | `120251216811260183` | `1814278130018814` | `35519defa84a670a418ed01a22b79a7c` |
| WEB_BlackB_atendimento_04 (Gerente de atendimento) | `120251216812870183` | `2808422746224746` | `ecaa9eb7a8899e0425f6453856e5bf6e` |

Ad antigo `WEB_Black_atendimento_05` (`120251166345200183`) → PAUSADO.
**Criativo 05 nao foi subido** (pedido explicito do Victor).

## Pendencias / limitacoes

1. **Story nao anexado.** O MCP nao expoe customizacao de imagem por posicionamento — cada
   criativo leva 1 imagem (a de Feed). Os 4 Story (1080x1920) estao no acervo da conta:
   `9a70747752662cca59f3cf494494f1c8` (01) · `3f0e75ac770ab011f2d55ac39ce17c17` (02) ·
   `27a34fbc43497bc72f2ad70152ac43b3` (03) · `0b2243d27c284fad5c8e1b30fdf7321c` (04).
   Anexar a mao no Ads Manager se quiser asset por posicionamento.
2. **Instagram:** `ads_get_ig_accounts` volta vazio nessa conta (permissao `instagram_basic`
   nao concedida ao app do MCP), entao `instagram_user_id` nao foi setado. O preview
   INSTAGRAM_STANDARD renderiza normalmente pela identidade da pagina — entrega em IG OK.
3. **Sobreposicao de leilao:** os 4 adsets da campanha usam o mesmo publico (Lal_Clientes).
   Como agora so 1 adset roda, o problema fica neutralizado enquanto os outros 3 seguirem pausados.
