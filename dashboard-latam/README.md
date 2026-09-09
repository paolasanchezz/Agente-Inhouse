# Dashboard CM Buzzmonitor LATAM — dinâmica (LOCAL)

Versão **interativa** da dashboard de Content Marketing LATAM, com **seletor de data**
(presets 7d/15d/30d/90d/MtD/YtD + intervalo livre) e consulta ao Supabase **ao vivo**.

> **Por que local?** O Vercel não consegue conectar no Supabase com o user `looker_readonly`
> (pooler IPv4 — mesmo motivo da `dashboard-pessoal`). Então esta versão roda **na sua máquina**.
> A versão **publicada** (snapshot semanal estático, sem seletor) continua em
> https://dashboards-elife.vercel.app/latam/ — as duas coexistem e usam o mesmo visual/critério.

## Como rodar

```bash
uv run --python 3.12 --with "psycopg[binary]" python dashboard-latam/server.py
# abre http://127.0.0.1:8010
```

(ou pelo `/run` / preview do Claude Code — config `dashboard-latam` no `.claude/launch.json`)

## Como funciona

- `server.py` serve a **shell** (barra com presets + date-picker) em `/` e um endpoint
  `/render?preset=…` ou `/render?ini=YYYY-MM-DD&fim=YYYY-MM-DD`.
- O `/render` **reaproveita o `render_html` do dashboard estático** (`dashboard/gerar_relatorio_latam.py`)
  para o período escolhido — mesmos blocos, funil de 5 fases, espanhol, USD. O seletor troca o
  conteúdo via `fetch` (iframe `srcdoc`), sem recarregar a página.
- **Cache em memória** por intervalo (botão ↻ ignora o cache e re-consulta o banco).
- Lê `SUPABASE_PG_URL` de `dashboard/.env` (read-only).

## Limitações herdadas (ver `dashboard/DEPLOY-latam.md` §pendências)

- **Cierres**: as datas de cierre não estão populadas no `contratos` (caem no fallback `mdate`) →
  contratos antigos aparecem como se fossem do período. Validação pendente.
- **Leads/Perdidos subestimados**: pipeline `Nutrición` não é sincronizado; UTM vazio no inbound.

Nada aqui depende de deploy — é uso interno local.
