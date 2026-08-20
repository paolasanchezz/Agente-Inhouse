# Estudo — substituir o form GreatPages por integração direta com a API do ActiveCampaign

**Data:** 2026-08-11 · **Autor:** agente inhouse (a pedido do Victor) · **Status:** estudo, nada implementado
**Escopo disparador:** `content.buzzmonitor.com/la-mejor-plataforma-social-listening-es`
**Escopo real:** todas as LPs estáticas que hoje postam no endpoint do GreatPages (2 hoje, tendência de crescer)

> ⚠️ Este documento é **só análise**. Vale o guardrail de integrações comerciais: nada em AC / n8n /
> Supabase é alterado sem pedido explícito do Victor.

---

## 1. Como funciona hoje (verificado no código)

```
LP estática (Vercel, content.buzzmonitor.com)
   │  fetch POST JSON  (cross-origin, keepalive)
   ▼
contenido.getbuzzmonitor.com/conversion        ← GreatPages (page id 2705735)
   │  integração nativa GreatPages → AC
   ▼
ActiveCampaign: contato criado/atualizado
   │  (provável) automação interna do AC
   ▼
Deal criado no pipeline
   │  n8n sync
   ▼
Supabase → dashboards CM
```

Detalhe do que a LP manda ([index.html:708-756](../../landing-pages/buzzmonitor/la-mejor-plataforma-social-listening-es/index.html)):

- payload no formato proprietário do GreatPages: `{campos: {0: {id, titulo, valor}, …}, elemento, eid, enav, eclid, euser}`
- IDs de campo hardcoded do form original (`input_2705735_1_178031366413316005-nome` etc.)
- 12 campos: nome, e-mail, telefone, país, empresa, 5 UTMs, gclid, adset + referral / dispositivo / URL
- redireciona pra `contenido.getbuzzmonitor.com/muchas-gracias`

**As duas LPs que usam esse padrão hoje:**

| LP | page id GreatPages |
|---|---|
| `buzzmonitor/la-mejor-plataforma-social-listening-es` | 2705735 |
| `buzzmonitor/ia-para-social-listening-es` | 1657740 |

### 1.1 O que está frágil nisso (não é opinião — está no código)

1. **Não existe confirmação de entrega.** O `/conversion` é cross-origin e não expõe
   `Access-Control-Allow-Origin` na resposta do POST, então o browser envia mas não consegue **ler**
   o resultado. O código conclui igual no `.then` e no `.catch`, mais um `setTimeout(go, 6000)`.
   Tradução: **se o GreatPages devolver 500, a LP mostra sucesso e redireciona pro obrigado do
   mesmo jeito.** Lead perdido em silêncio, sem alarme, sem log nosso.
2. **Acoplamento a uma página de terceiro que ninguém do time gerencia mais.** Se alguém editar,
   arquivar ou recriar o form nas páginas 2705735 / 1657740 no GreatPages, os IDs mudam e as nossas
   LPs param de gerar lead — sem erro visível.
3. **Dependência de domínio alheio ao nosso deploy** (`contenido.getbuzzmonitor.com`) tanto pro POST
   quanto pro `/muchas-gracias`.
4. **Zero controle sobre o que chega no deal.** O que o GreatPages preenche no contato e o que a
   automação do AC copia pro negócio é caixa-preta pra nós.

---

## 2. O que a API do ActiveCampaign permite (verificado na doc oficial)

Base: `https://<conta>.api-us1.com/api/3` · auth por header `Api-Token`.

| Ação | Endpoint | Observação |
|---|---|---|
| Criar/atualizar contato | `POST /contact/sync` | **Upsert por e-mail.** Aceita `fieldValues: [{field, value}]` inline |
| Criar negócio | `POST /deals` | `title`, `contact`, `value`, `currency`, `group`(pipeline), `stage`, `owner` — **`owner` é obrigatório**. Aceita `fields: [{customFieldId, fieldValue}]` inline |
| Campo custom do deal (avulso) | `POST /dealCustomFieldData` | Padrão já usado nos nossos workflows n8n |
| Tag / lista | `POST /contactTags` · `POST /contactLists` | Pra disparar automações existentes |
| Negócios de um contato | `GET /contacts/{id}/deals` | Necessário pra evitar deal duplicado |

**Pegadinhas confirmadas:**

- `value` do deal é **em centavos** (`$456,78` → `45678`).
- **Rate limit: 5 req/s por conta** — não por token. Ou seja, é o mesmo balde que os ~20 workflows
  n8n de sync AC↔Supabase já consomem. Estouro devolve `429` + `Retry-After`.
- O token do AC é **full-access na conta inteira** (não há escopo por recurso). **Nunca pode ir pro
  browser.** Isso é o que define a arquitetura do item 3.

### 2.1 Já temos precedente interno

- `[AC] [BUZZMONITOR LATAM] - Tami Chat LATAM → ActiveCampaign (Contato + Deal)` (n8n `6h52Tovo8kBYCN4W`,
  **desligado**) — é exatamente o desenho contato+deal via API, mas ficou como template: token, owner
  e IDs estão com placeholder (`COLE_SEU_API_TOKEN_AQUI`). Serve de esqueleto pronto.
- `Webhook → Atualizar Negócio com Campos do Contato` (n8n `6fGqjmIlrg3zSNRG`, **ativo**) — já faz
  `GET fieldValues` → acha o deal mais recente → `POST /dealCustomFieldData`. É o padrão que
  usaríamos pra levar UTM pro negócio.

> 🔴 **Achado de segurança (fora do escopo, mas registro):** o workflow ativo `6fGqjmIlrg3zSNRG` tem o
> **token da API do AC da conta `elife` em texto puro** dentro do parâmetro do nó HTTP (visível pra
> qualquer um com acesso ao n8n e a quem exportar o JSON do workflow). Mesmo caso da
> `CLICKMEETING_API_KEY`. Recomendo rotacionar e passar a usar a credencial `activeCampaignApi` do
> n8n (o nó já declara `nodeCredentialType`, o header manual é redundante).

---

## 3. Consequência: a LP não fala com o AC sozinha

Como o token é full-access, **é obrigatório um intermediário server-side**. Três desenhos possíveis:

### Opção A — webhook no n8n (recomendada pra v1)

`LP → POST https://n8n…/webhook/lead-lp → contact/sync → deals → dealCustomFieldData`

| ✅ | ❌ |
|---|---|
| Infra e credencial AC já existem e são gerenciadas lá | Webhook público → precisa de honeypot + segredo compartilhado |
| É onde vive **todo** o resto da integração AC — um lugar só | n8n fora do ar = lead perdido (mitigável, ver §5) |
| Log de execução, retry e workflow de erro nativos | Latência maior que same-origin |
| Editável por quem não é dev | Mais um workflow crítico no parque (~50 hoje) |
| Zero mudança no pipeline de deploy das LPs | |

### Opção B — Vercel Function no guarda-chuva

`LP → POST /api/lead (same-origin) → AC`

| ✅ | ❌ |
|---|---|
| Same-origin: sem CORS, resposta legível, **erro de verdade pro usuário** | Hoje o guarda-chuva é 100% estático (`build_umbrella.py` monta `dist/` e o CI roda `vercel deploy --prod`); passa a ter runtime Node |
| Versionado no repo, revisado por PR, deploy pelo CI que já existe | Token do AC vira env var **por projeto Vercel** (são 5 guarda-chuvas) |
| Latência mínima, sem terceiros | Novo modo de falha no CI de LP (hoje blindado e com rollback automático) |
| | Ninguém fora do time de dev mexe |

Tecnicamente viável sem reescrever o CI: bastaria o `build_umbrella.py` copiar uma pasta `api/` pro
`dist/` — o Vercel detecta função por zero-config. Mas é uma mudança estrutural num pipeline que
custou caro pra estabilizar.

### Opção C — form nativo do AC (`proc.php`)

Postar direto no endpoint público de formulário do AC, sem token.
**Descartada:** não cria negócio (só contato), amarra o layout ao que o AC expõe, e não resolve o
problema de confirmação de entrega. Se um dia quisermos zero-backend, é o plano B.

---

## 4. O ganho que justifica o esforço (mais do que "tirar o GreatPages")

Trocar o transporte é o benefício pequeno. O grande é **escrever a atribuição direto no negócio, na
hora da conversão**:

- Hoje a UTM chega no **contato** e depende de automação/ETL pra virar campo do **negócio**. Os
  buracos disso estão documentados: no LATAM a tabela `deals_latam_inbound_staging` está com
  **UTM 100% vazia** (gap de ETL, `dashboard/MAPEAMENTO-CAMPOS-latam.md` §6); no Brasil, 40-54% dos
  deals não têm rastreio e existe uma skill inteira (`/auditar-deals-cm`) só pra recuperar UTM perdida.
- Criando o deal via API, mandamos `fields: [{customFieldId: <utm_source>, …}]` **no mesmo request**.
  A atribuição nasce correta no negócio, sem depender de automação intermediária.

Ou seja: isso não é um projeto de formulário, é um projeto de **qualidade de atribuição**.

### 4.1 Achado adjacente (independe desta decisão)

O filtro CM LATAM (`FILTRO_CM_LATAM`) só reconhece URL de conteúdo que contenha **`getbuzzmonitor.com`**.
Essas LPs migraram pra **`content.buzzmonitor.com`** — que **não casa** com essa regra (assim como o
`material.buzzmonitor.com` do MCP-ES, que precisou de regra própria). E o `input_uri` que a LP manda
é o `window.location.href`, ou seja, `content.buzzmonitor.com/...`.

**Efeito:** lead dessas LPs que chegue **sem `utm_source` da whitelist** (direto, orgânico, referral)
fica **fora da dashboard CM LATAM**. Não vira lead CM. Fix de 1 linha em `URL_FORTE_CM`, mas é decisão
do Victor — só estou registrando.

---

## 5. Riscos e o que precisa ser resolvido antes

| # | Risco | Como tratar |
|---|---|---|
| 1 | **`owner` é obrigatório no `POST /deals`.** Se hoje existe automação de round-robin no AC distribuindo o dono, criar o deal por API **atropela** essa distribuição | Verificar no AC. Se houver round-robin, ou mantemos a criação do deal pela automação (só trocamos o transporte do contato) ou replicamos a distribuição |
| 2 | **Deal duplicado.** `contact/sync` é upsert, mas `POST /deals` **sempre cria**. Reenvio do form = 2 negócios | Antes de criar: `GET /contacts/{id}/deals`, e se houver deal aberto no mesmo pipeline, atualizar em vez de criar |
| 3 | **Rate limit 5 req/s por conta**, compartilhado com os syncs Supabase | Retry com backoff no 429 + respeitar `Retry-After`. Pico de campanha coincidindo com sync pesado é cenário real |
| 4 | **Spam.** Endpoint próprio não tem a proteção nativa do GreatPages | Honeypot + campo de timestamp (descarta submit < 2s) + rate limit por IP. Sem CAPTCHA por ora |
| 5 | **Quebrar o filtro CM.** As dashboards leem `utm_source` / `url_conversao` com nomes e formatos específicos | Espelhar exatamente os mesmos campos/valores que existem hoje. Validar contra a dashboard antes de desligar o GreatPages |
| 6 | **Consentimento / opt-in.** O GreatPages pode estar inscrevendo em lista com regra de opt-in própria | Confirmar qual lista e qual status de inscrição, e replicar |
| 7 | **n8n vira caminho crítico de lead** (na opção A) | Durante a migração, dual-write: se o novo endpoint falhar, a LP cai no GreatPages como fallback |

---

## 6. Plano sugerido (faseado, cada fase reversível)

**Fase 0 — descoberta no AC** *(precisa de acesso; ~1h)*
Responder, olhando a conta:
- Qual conta recebe esses leads? (`elifeeurope` pra LATAM segundo nosso mapa, mas o template do n8n
  aponta `buzzmonitor.api-us1.com` — **precisa ser confirmado, não inferido**)
- Que automação cria o negócio hoje? Tem round-robin de owner?
- IDs de: lista, pipeline (`group`), stage inicial, e os `customFieldId` de UTM no **negócio**
- Que tags o GreatPages aplica

**Fase 1 — shadow (não escreve nada)**
LP passa a postar **nos dois** endpoints. O novo (n8n) só **loga** o payload, sem tocar no AC.
Comparar 1 semana: volume bate? campos batem? Custo ~zero, risco zero.

**Fase 2 — cutover do contato**
O novo endpoint passa a fazer `contact/sync` + tag/lista. O **negócio continua nascendo da automação
do AC**, exatamente como hoje. GreatPages sai do caminho. Aqui já se resolve o problema nº 1 do §1.1
(passa a existir confirmação de entrega real e erro visível pro usuário).

**Fase 3 — deal via API** *(opcional, é onde está o ganho de atribuição)*
Criar o negócio no mesmo request, com UTM já preenchida nos campos do negócio. Só depois de resolver
o round-robin (risco nº 1) e o dedupe (nº 2).

Esforço estimado: Fase 1 ~2h · Fase 2 ~4h + validação · Fase 3 ~6h + validação na dashboard.

---

## 7. Recomendação

1. **Sim, vale a pena** — mas o argumento forte não é "tirar o GreatPages", é **parar de perder lead
   em silêncio** (§1.1.1) e **nascer com atribuição correta no negócio** (§4).
2. **Opção A (n8n)** pra v1: aproveita credencial, log e retry que já existem, não mexe no CI de LP
   que custou caro pra estabilizar, e o esqueleto do workflow já está lá (`6h52Tovo8kBYCN4W`).
3. **Faseado**, com shadow antes de cutover, e mantendo a criação do deal pela automação do AC até
   entender o round-robin.
4. **Não começa sem a Fase 0.** Metade das decisões acima depende de olhar a conta do AC.

## 8. O que preciso de você pra seguir

- [ ] Confirmar **qual conta do AC** recebe os leads dessas LPs LATAM
- [ ] Acesso (ou as respostas) da Fase 0: automação que cria o deal, pipeline/stage/owner, IDs dos campos custom
- [ ] Decidir **A (n8n)** ou **B (Vercel function)**
- [ ] Autorização explícita pra mexer em n8n/AC (guardrail)
- [ ] Decidir se corrige o filtro CM LATAM pro domínio `content.buzzmonitor.com` (§4.1) — independente disso
- [ ] Decidir sobre a rotação do token do AC exposto no workflow n8n (§2.1)

---

## Fontes

- [ActiveCampaign — Rate limits](https://developers.activecampaign.com/reference/rate-limits)
- [ActiveCampaign — Create a deal](https://developers.activecampaign.com/reference/create-a-deal-new)
- [ActiveCampaign — Sync a contact's data](https://developers.activecampaign.com/reference/sync-a-contacts-data)
- Código: `landing-pages/buzzmonitor/la-mejor-plataforma-social-listening-es/index.html:708-756`
- n8n: workflows `6h52Tovo8kBYCN4W` (template contato+deal) e `6fGqjmIlrg3zSNRG` (campos do contato → negócio)
- `dashboard/MAPEAMENTO-CAMPOS-latam.md` (filtro CM LATAM e gap de UTM no inbound)
