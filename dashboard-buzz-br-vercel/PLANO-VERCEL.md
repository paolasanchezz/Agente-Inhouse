# Plano — Dashboard CM Buzzmonitor BR dinâmica no Vercel (estática com intervalo livre)

> Status: **proposta aguardando aprovação do Victor**. Nada de código ainda.
> Data: 2026-06-30. Autor: agente inhouse.

---

## 1. Objetivo

Servir a experiência da **dashboard local dinâmica** (`dashboard-pessoal`, hoje só em `127.0.0.1:8000`) — com **date-picker de intervalo livre** e **todos os dados de 2026** — no link protegido do Vercel (`dashboard-buzzmonitor-brasil.vercel.app`), **sem o Vercel precisar conectar no Supabase**.

### Por que não é só "subir a dash local"
A dash local consulta o Supabase a cada clique. O próprio código dela documenta que **já tentaram** rodar isso como função no Vercel e **não funcionou** — o pooler IPv4 do Supabase não aceita o usuário `looker_readonly`. Por isso ela ficou presa no local.

### A saída (decidida com o Victor)
Versão **estática**: gera os dados aqui (onde o Supabase conecta) → embute num arquivo → o navegador calcula os períodos em cima dos dados embutidos. Zero banco no Vercel = mais seguro e sem o bloqueio de conexão.

---

## 2. O que já está pronto (reaproveitado)

A blindagem feita em 2026-06-30 fica **inteira** — a dash nova mora no mesmo projeto Vercel:
- Senha forte (Basic Auth via `middleware.js`, credencial no `.env.local`, fora do git).
- `X-Robots-Tag: noindex` + `robots.txt` (fora dos buscadores).
- Vercel SSO Standard como camada extra nas URLs internas.
- Pasta sibling protegida + trava de deploy.

**Só troca o conteúdo servido** (o `index.html` + um JSON de dados) — a casca de segurança não muda.

---

## 3. A garantia central: por que os números vão bater com a local

A regra de "o que é Content Marketing" é complexa (atribuição 90 dias, coorte de perdidos, whitelist/blacklist, reconversões). **Reescrever isso em JavaScript = convite pra divergência.** A estratégia evita isso:

> **A lógica CM roda no Python (fonte única). O navegador só filtra por data e soma/agrupa.**

Fundamento técnico verificado no código:
- **A "CM-ness" de cada registro é fixa** — não depende do intervalo que o usuário escolhe. A regra 90d compara a data do evento com conversões passadas na mesma conta; isso independe do range consultado (a janela da query só limita escopo por performance). Logo, dá pra pré-computar a CM-ness de **todos** os eventos de 2026 de uma vez.
- **Rankings, KPIs e listas derivam dos mesmos eventos** — o ranking por source/content é `GROUP BY` dos eventos que já contamos; não é um dado separado. Se o navegador tem os eventos, ele deriva tudo.
- **Séries de 12 meses e proporção de reuniões são fixas** (não dependem do range) → pré-computadas prontas no export.

O navegador só faz aritmética de datas (derivar os 4 períodos) + contagem/agrupamento. Baixo risco.

---

## 4. Nuances de paridade que o plano precisa respeitar (senão diverge)

Estas são as armadilhas identificadas na leitura do código — cada uma tem tratamento definido:

| Nuance | Regra no Python | Tratamento no navegador |
|---|---|---|
| **Dedup de Leads** | `COUNT(DISTINCT email)` / `DISTINCT ON (email)` **dentro do período** | Exportar **todos** os deals-lead (sem dedup); o navegador dedupa por e-mail **dentro do range** (pega o `cdate` mais recente). Exportar já-dedupado-no-ano divergiria em sub-ranges. |
| **Dedup de Perdidos** | Igual, por e-mail, dentro do período | Mesmo tratamento (dedup no range, mais recente por `data_perda`). |
| **CE não tem lista** | Só count; sem lista visível | Exportar os eventos CE (data + dims) mesmo sem exibir, pra contar e rankear. |
| **Regra 90d** | `_atrib_cm_90d` decide se o evento é CM | Pré-computada no Python; cada evento exportado **já vem carimbado como CM ou não** (só os CM entram no export). |
| **Perdidos = coorte** | Leads criados no período **e** perdidos (por `cdate`, não pela data da perda) | Filtrar por `cdate` no range; a métrica já fica ≤ 100%. |
| **Datas à meia-noite (`::date`)** | Comparações normalizadas por `::date` | Exportar as datas já em `YYYY-MM-DD` (sem hora); o navegador compara string ISO. |
| **Âncora "hoje"** | `date.today()` no servidor | Congelar o `hoje` no momento do export e o navegador usa **esse** hoje (não o relógio do PC) pros presets e para o denominador do YtD. |
| **Valores** | Fechamento = numérico; Proposta = texto livre parseado | Exportar como estão; o front já tem `parseValorText`/`fmtMoedaBr`. |
| **Escopo temporal** | Range livre | Export cobre **2026 inteiro** (+ cauda de 2025 só para alimentar as séries de 12 m). Ranges 100% dentro de 2025 ficam fora do escopo v1 (a dash é "dados de 2026"). |

---

## 5. Arquitetura da solução

```
[Aqui, máquina do Victor]                    [Vercel — sibling protegida]
 exportar_dados.py                            index.html  (motor de cálculo em JS)
   └─ reusa lib/queries.py (filtro CM,   →    dados-2026.json  (eventos CM carimbados)
      regra 90d, séries)                      middleware.js + vercel.json + robots.txt
   └─ gera dados-2026.json                        (segurança já pronta)
```

- **`exportar_dados.py`** (novo): conecta no Supabase, reusa os predicados de `lib/queries.py` (`filtro_cm`, `_atrib_cm_90d`, `cte_conversoes_cm`) em queries "raw" (todas as linhas do ano, **sem** a dedup de período), e grava `dados-2026.json` com: `leads[]`, `ce[]`, `ra[]`, `rr[]`, `prop[]`, `fech[]`, `perdidos[]`, `serie_12m`, `proporcao_sources`, `gerado_em`.
- **`index.html`** (adaptado do `public/index.html` da local): troca `fetch('/api/dashboard')` por um **motor de agregação em JS** que lê o JSON e produz o mesmo objeto `data` que o `render()` já espera. O `render()`, os gráficos e o CSS **não mudam**.
- **`dados-2026.json`**: servido como arquivo estático no mesmo domínio (sem fetch a banco, sem CORS).

Estimativa de volume: centenas a poucos milhares de linhas (dash de CM) → JSON de ~0,5–2 MB. O passo 1 confirma o número real antes de seguir.

---

## 6. Etapas (com entregável e checkpoint)

**Passo 1 — Exportador + amostra de volume**
- Escrever `exportar_dados.py`, gerar o `dados-2026.json` e reportar tamanho + contagem por lista.
- Checkpoint: confirmar que o arquivo não fica pesado demais. Se passar de ~3 MB, reavaliar (comprimir ou reduzir campos).

**Passo 2 — Motor de agregação em JS**
- Portar `calcular_periodos` (4 períodos) e escrever as funções de contagem/dedup/ranking em JS, entregando o formato exato do `render()`.
- Manter `render()`, gráficos e CSS intactos.

**Passo 3 — ✅ Checkpoint de paridade (inegociável)**
- Harness que, para uma bateria de intervalos (presets + custom + casos-limite: 1 dia, virada de mês, início/fim de ano), compara **número a número** o resultado da **dash local** (fonte de verdade, via `coletar()`) com o **motor JS** rodando sobre o export.
- Só avança se bater em **todos**. Qualquer divergência vira correção antes de subir.
- Entregável: um relatório de paridade que você pode conferir.

**Passo 4 — Empacotar + deploy**
- Copiar `index.html` + `dados-2026.json` para a sibling protegida; deploy via a trava (mesmo fluxo seguro de hoje).
- Verificar no ar: intervalo livre funcionando, senha barrando, noindex ativo.

**Passo 5 — Atualização on-demand (fluxo recorrente)**
- Transformar "rodar exportador → copiar → deploy → validar" num comando único (adaptar a skill `dashboard-atualizar` ou criar uma nova).
- Decisão em aberto (ver §8).

---

## 7. Riscos e mitigações

| Risco | Mitigação |
|---|---|
| Números divergirem da local | Passo 3 (paridade número a número) é gate obrigatório. Lógica CM não é reescrita — fica no Python. |
| Arquivo pesado no navegador | Medir no Passo 1; JSON separado (não embutido no HTML); só os campos necessários. |
| Regra CM muda no futuro | O exportador reusa `lib/queries.py`. Mudou a regra lá → re-exportar reflete automático. O JS (só agrega) não precisa mexer. |
| Fuso/`::date` sutil | Exportar datas já como `YYYY-MM-DD`; comparação por string ISO no navegador. |
| Presets "envelhecerem" | Âncora `hoje` congelada no export; front usa a data do export, não o relógio. Atualizar = re-exportar. |

---

## 8. Decisões em aberto (preciso do teu OK)

1. **Substituir ou coexistir?** A dinâmica-estática vai pro mesmo link e **substitui** o snapshot semanal atual (minha recomendação — é o que você quer ver lá). O `dashboard/` (snapshot) e a skill `dashboard-atualizar` atual seriam aposentados/substituídos pelo novo fluxo. Confirmar.
2. **Onde mora o código novo:** proponho uma pasta nova `dashboard-buzz-br-vercel/` (fonte do `index.html` + exportador), separada da `dashboard-pessoal` (que continua sendo o local dinâmico ao vivo). Confirmar.
3. **Escopo 2026** (ranges dentro de 2025 ficam fora do v1). Confirmar que está ok.

---

## 9. O que NÃO muda
- A dash local (`dashboard-pessoal`, ao vivo) continua existindo e funcionando como está.
- Toda a camada de segurança do Vercel (senha, noindex, sibling, trava de deploy).
- O visual, os gráficos e o `render()` da dash.
