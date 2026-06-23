---
name: seo-report
description: Gera dashboard visual de SEO do Buzzmonitor BR cruzando Google Search Console, Google Analytics 4 e Semrush. GSC/GA4 vêm de um script Python (OAuth da conta Google, credenciais locais); Semrush vem do MCP do Semrush — sem nenhuma chave de API no repositório. Produz um HTML interativo com KPIs, canais de tráfego e tabelas de top páginas e keywords.
argument-hint: "[data?] — caminho opcional p/ um seo_data.json já gerado; sem args, coleta na hora"
allowed-tools: Bash, Read, Write, mcp__ad5dce33-9482-461f-9925-8595fad14e6a__execute_report, mcp__ad5dce33-9482-461f-9925-8595fad14e6a__get_report_schema, mcp__ad5dce33-9482-461f-9925-8595fad14e6a__overview_research, mcp__ad5dce33-9482-461f-9925-8595fad14e6a__organic_research
version: 1.0.0
---

# /seo-report — Dashboard SEO Buzzmonitor BR

## O que esta skill faz

1. **Coleta Google** (se não houver JSON pronto): roda `seo_report_buzzmonitor.py`, que autentica via OAuth2 na conta Google do usuário e puxa **GSC + GA4**.
2. **Coleta Semrush via MCP** (sem chave de API): busca overview do domínio + top keywords orgânicas pelo MCP do Semrush, direto na skill.
3. **Lê** o `seo_data.json` (GSC + GA4) e funde com o Semrush do MCP.
4. **Gera** um dashboard HTML inline (sem dependências externas) e o abre no navegador.

> **Por que não tem chave de API no repo:** a parte Semrush, que antes usava uma chave hardcoded, agora vem pelo MCP do Semrush (autenticado fora do código). O Google usa OAuth com credenciais **locais por usuário** (`client_secret.json` / `token.json`), que ficam fora do repositório.

---

## Paths

```
SCRIPT      = .claude/skills/seo-report/seo_report_buzzmonitor.py   (no repo)
WORK_DIR    = ~/.seo-report-buzzmonitor/   (por usuário, fora do repo; ou defina SEO_REPORT_DIR)
  ├─ client_secret.json   (você baixa do Google Cloud Console — entrada)
  ├─ token.json           (gerado no 1º login — gitignored)
  └─ seo_data.json        (saída do script: gsc + ga4 — gitignored)
```

O `.gitignore` da pasta da skill já protege `client_secret.json`, `token.json` e `seo_data.json` caso apareçam no diretório do repo. **Nunca commite credenciais.**

---

## Fluxo de execução

### Passo 1 — Resolver origem dos dados Google (GSC + GA4)

Se o usuário passou `[data]` (caminho para um `.json` existente):
- Usar esse arquivo diretamente → ir para o Passo 3.

Se não há argumento:
- Verificar se `seo_data.json` existe no `WORK_DIR` e tem menos de 24 horas (campo `gerado_em`). Se sim, perguntar com chips:
  - **"Usar dados de hoje (gerado em {gerado_em})"** → Passo 3
  - **"Coletar dados novos agora"** → Passo 2
- Se não existir ou tiver mais de 24 horas → Passo 2.

### Passo 2 — Rodar o script Python (Google)

Verificar pré-condições (PowerShell no Windows):

```powershell
# 1. Python disponível?
python --version

# 2. Dependências instaladas?
python -c "import google.oauth2; from google.analytics.data_v1beta import BetaAnalyticsDataClient"
```

Se faltarem dependências, instalar:
```powershell
python -m pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client google-analytics-data
```

O script resolve o diretório de trabalho sozinho (`~/.seo-report-buzzmonitor/`, ou `SEO_REPORT_DIR`). Se `client_secret.json` não estiver lá, ele para com instrução clara. Para autenticar no Google, oriente o usuário:
> "Coloque o `client_secret.json` (credencial OAuth2 tipo Desktop, baixada do Google Cloud Console) em `~/.seo-report-buzzmonitor/`. No 1º uso abre o navegador para login; depois o `token.json` fica salvo e as execuções são silenciosas."

Rodar (não precisa de `cd` — os caminhos são absolutos, resolvidos pelo script):
```powershell
python .claude/skills/seo-report/seo_report_buzzmonitor.py
```

Se falhar com erro de autenticação, orientar: deletar `token.json` no `WORK_DIR` e rodar de novo.

### Passo 3 — Ler o JSON (GSC + GA4)

Ler `seo_data.json` (do `WORK_DIR` ou o caminho passado) com Read. Extrair `gerado_em`, `periodo`, `gsc`, `ga4`. Se `gsc` ou `ga4` vier como `{"erro": "..."}`, anotar para exibir card de aviso (não abortar).

### Passo 4 — Coletar Semrush via MCP (sem chave)

Buscar os dados do Semrush pelo MCP do Semrush (toolkit `overview_research` / `organic_research`). Padrões: `domain = "buzzmonitor.com"`, `database = "br"`.

**4.1 — Overview do domínio** (`execute_report`):
- `report = "domain_rank"`
- `params = {"domain": "buzzmonitor.com", "database": "br", "export_columns": "Dn,Or,Ot,Oc"}`
- A resposta é texto delimitado por `;` com 1 linha de cabeçalho + 1 de dados. Mapear:
  - `Organic Keywords` → `keywords_organicas`
  - `Organic Traffic` → `trafego_organico_estimado`
  - `Organic Cost` → `custo_organico_estimado`

**4.2 — Top keywords orgânicas** (`execute_report`):
- `report = "domain_organic"`
- `params = {"domain": "buzzmonitor.com", "database": "br", "export_columns": "Ph,Po,Nq,Tr", "display_limit": 15, "display_sort": "tr_desc"}`
- Para cada linha de dados, mapear: `Keyword` → `keyword`, `Position` → `posicao`, `Search Volume` → `volume`, `Traffic (%)` → `trafego_pct`.

Montar o objeto, **na mesma forma que o dashboard espera**:
```json
"semrush": {
  "overview": { "keywords_organicas": 745, "trafego_organico_estimado": 1198, "custo_organico_estimado": 345 },
  "top_keywords": [ { "keyword": "...", "posicao": 1, "volume": 720, "trafego_pct": 7.92 }, ... ]
}
```
Se o MCP falhar ou vier vazio (ex.: limite de unidades atingido), setar `"semrush": {"erro": "Semrush indisponível — {motivo}"}` para o dashboard mostrar o card de aviso. **Nunca abortar** — GSC + GA4 já bastam para gerar o dashboard.

> Se os parâmetros divergirem do esperado, chamar `get_report_schema(report=...)` antes do `execute_report`. As colunas acima foram validadas para `domain_rank` e `domain_organic`.

### Passo 5 — Calcular deltas e variações

Para cada métrica com `_anterior`, variação percentual:

```
delta_pct = round(((atual - anterior) / anterior) * 100, 1) se anterior > 0 senão None
sinal     = "▲" se delta_pct > 0 | "▼" se delta_pct < 0 | "—" se None
cor       = verde (#16a34a) se positivo | vermelho (#dc2626) se negativo (exceto bounce_rate: invertido) | cinza se None
```

Métricas: GSC `cliques`/`impressoes` (vs `_anterior`); GA4 `sessoes`/`usuarios` (vs `_anterior`).

### Passo 6 — Gerar o dashboard HTML

Usar a skill `frontend-design` como referência de qualidade. HTML completo, **totalmente inline** (sem CDN), dados embutidos como variáveis JS. Paleta: fundo branco/cinza claro, texto escuro, acento `#1e40af` (azul Buzzmonitor). Font-family: system-ui.

#### Estrutura do dashboard

```
┌─────────────────────────────────────────────────────────────┐
│  HEADER: "SEO Report — Buzzmonitor BR"                       │
│          Badge período  •  Badge gerado em  •  [avisos erro] │
├──────────────────────────────────────────────────────────────┤
│  SEÇÃO "Google Search Console"                               │
│  [ Cliques ] [ Impressões ] [ CTR ] [ Posição ]  (cards KPI) │
├──────────────────────────────────────────────────────────────┤
│  SEÇÃO "Google Analytics 4"                                  │
│  [ Sessões ] [ Usuários ] [ Bounce Rt ] [ Dur. Média ]       │
├───────────────────────────┬──────────────────────────────────┤
│  SEÇÃO "Semrush"          │  SEÇÃO "Canais de Tráfego (GA4)"  │
│  Keywords Orgânicas       │  barras horizontais proporcionais │
│  Tráfego Est. / Custo Est.│  por canal (sessões + %)          │
├───────────────────────────┴──────────────────────────────────┤
│  TABELA "Top Páginas do Blog — GSC (28 dias)"                │
│  URL · Cliques · Impressões · CTR · Posição média (top 10)    │
├─────────────────────────────────────────────────────────────┤
│  TABELA "Top Páginas do Blog — GA4 (28 dias)"                │
│  Página · Sessões · Usuários · Bounce Rate (top 10)           │
├─────────────────────────────────────────────────────────────┤
│  TABELA "Top Keywords — GSC (28 dias)"                       │
│  Keyword · Cliques · Impressões · Posição (top 15, badge)     │
├─────────────────────────────────────────────────────────────┤
│  TABELA "Top Keywords Orgânicas — Semrush"                   │
│  Keyword · Posição · Volume mensal · % Tráfego (top 15, badge)│
└─────────────────────────────────────────────────────────────┘
```

#### Regras de formatação de números
- ≥ 1.000.000 → `X.XM` · ≥ 1.000 → `X.XK` · CTR → `X.XX%` · Posição → `XX.X` · Duração (seg) → `Xm XXs` · Bounce → `XX.X%`

#### Canais de tráfego (GA4)
Barras horizontais proporcionais (maior = 100%). Ordenar por sessões desc. Máx. 8 canais (resto em "Outros"). Mostrar canal + sessões + % do total.

#### Badges de posição (tabelas de keywords)
```
posição 1–3   → fundo verde escuro (#166534), texto branco, "Top 3"
posição 4–10  → fundo azul (#1e3a8a), texto branco
posição 11–20 → fundo cinza (#374151), texto branco
posição > 20  → fundo cinza claro (#e5e7eb), texto escuro
```

#### Cards de KPI
Fundo branco, borda `1px solid #e5e7eb`, radius 8px, padding 20px. Label cinza no topo, valor grande bold, delta abaixo com ▲/▼ e cor.

#### Cards de aviso de erro
Se `gsc`, `ga4` ou `semrush` vier `{"erro": "..."}`, banner laranja no topo da seção:
> "⚠️ Dados do {fonte} indisponíveis — {mensagem}"

### Passo 7 — Salvar e abrir o dashboard

Salvar o HTML no `WORK_DIR` (fora do repo), com a data de hoje:
```
~/.seo-report-buzzmonitor/seo-report-buzzmonitor-{YYYY-MM-DD}.html
```
(Use o caminho absoluto resolvido — `$env:USERPROFILE\.seo-report-buzzmonitor\...` no Windows, ou `SEO_REPORT_DIR` se definido.)

Abrir no navegador padrão:
```powershell
Start-Process "$env:USERPROFILE\.seo-report-buzzmonitor\seo-report-buzzmonitor-{YYYY-MM-DD}.html"
```
(macOS: `open ...` · Linux: `xdg-open ...`.)

Informar ao usuário o caminho do arquivo gerado. Depois, resumir no chat em até 3 linhas:
- Métrica que mais cresceu e a que mais caiu (com delta)
- Keyword de melhor posição no GSC
- Página de blog com mais cliques

---

## Tratamento de erros comuns

| Erro | O que fazer |
|---|---|
| `client_secret.json` não encontrado | Explicar como baixar do Google Cloud Console e onde salvar (`WORK_DIR`); parar |
| `token.json` expirado / inválido | Deletar `token.json` no `WORK_DIR` e reautenticar |
| MCP Semrush sem unidades / erro | Card de aviso na seção Semrush; seguir com GSC + GA4 |
| Linha do Semrush vazia / malformada | Tratar silenciosamente, exibir `—` nas células |
| Script Python não encontrado | Confirmar o caminho `.claude/skills/seo-report/seo_report_buzzmonitor.py` |
| Python não instalado | Indicar instalação via python.org ou Microsoft Store |

---

## Exemplos de uso

```
/seo-report
# → coleta Google na hora (ou pergunta se usar os de hoje), busca Semrush via MCP e gera o dashboard

/seo-report "C:\Users\voce\.seo-report-buzzmonitor\seo_data.json"
# → usa o JSON já gerado (GSC+GA4), busca Semrush via MCP, vai direto ao dashboard
```

---

## Notas técnicas

- **Sem chave de API no repositório.** Semrush vem do MCP; Google usa OAuth com `client_secret.json`/`token.json` locais por usuário, fora do repo (gitignored).
- **GA4 property** `347467970` e **GSC** `sc-domain:buzzmonitor.com` ficam fixos no script (single-purpose Buzzmonitor BR). Período: últimos 28 dias vs 28 anteriores, calculado em runtime.
- **Semrush via MCP:** `database = "br"`, `domain = "buzzmonitor.com"`. Reports validados: `domain_rank` (overview) e `domain_organic` (keywords). Requer o MCP do Semrush conectado; os IDs das tools de MCP em `allowed-tools` podem variar por ambiente — se o autocomplete não achar, confirme o servidor Semrush ativo na sessão.
- **Não há diretório fixo de máquina.** O `WORK_DIR` é resolvido por `~/.seo-report-buzzmonitor/` ou pela variável `SEO_REPORT_DIR`.
