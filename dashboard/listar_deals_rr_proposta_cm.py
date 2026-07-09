"""
Lista os deals CM (Buzzmonitor Brasil) que tocaram RR ou Proposta nos ultimos 12 meses.

Aplica o MESMO filtro CM da dashboard semanal:
  - whitelist de utm_source + slugs CM em conteudo.buzzmonitor.com.br + blog/material/evento (filtro_cm)
  - exclusao google/cpc e DEALS_EXCLUIDOS_URL_DATA (Webinar Analise Preditiva)
  - EMAIL_WHITELIST override (deals confirmados como CM pelo Victor)
  - EMAIL_BLACKLIST exclusao (testes/internos/outbound reclassificados)
  - Regra 90d pos-conversao (account_id com conversao CM <= 90d antes do evento)
  - filtro_inbound() exclui funil 'Outbound' (mantem Inbound + nao-classificados + whitelist;
    reativado 2026-07-01 — antes era no-op TRUE de 2026-05-19)

Saida: dashboard/deals-rr-proposta-cm-12m.html (auto-contido).

Uso:
    uv run --python 3.12 --with "psycopg[binary]" python dashboard/listar_deals_rr_proposta_cm.py
"""
from __future__ import annotations

import html
import sys
from collections import Counter, defaultdict
from datetime import date, timedelta
from pathlib import Path

import psycopg

sys.path.insert(0, str(Path(__file__).parent))
from queries import (
    filtro_cm,
    filtro_inbound,
    _sql_email_list,
    EMAIL_WHITELIST,
    EMAIL_BLACKLIST,
)


AC_BASE = "https://buzzmonitor.activehosted.com/app/deals"

# Mapeamento de stage (bigint) -> nome da etapa do pipeline.
# Inferido pelo pico de data_inicio_X correspondente em cada stage (12m).
STAGE_NAMES = {
    220: "Lead Distribuido",
    221: "Prospeccao",
    222: "Conexao",
    223: "Qualificacao",
    224: "Reuniao Agendada",
    225: "Reuniao Realizada",
    226: "Proposta",
    227: "Aceite Formal",
    228: "Nutricao",
    258: "Stage 258",
}


# ============ CTE: conversoes CM casadas POR EMAIL (em vez de account_id) ============
# Mudanca em relacao a cte_conversoes_cm() canonica da dashboard semanal:
# casa o lead CM e o evento RR/Proposta pelo MESMO email do contato principal,
# nao pelo mesmo account_id. Motivo: o agrupamento por account_id captura
# "influencia indireta" (alguem da empresa converteu em CM e outro contato
# entrou em RR depois) como atribuicao direta — e em contas-saco (account
# 125244 "E S P I C H E I" tem 3007 contatos de empresas distintas) gera
# falso positivo em escala. Casar por email/contato e o granular correto.
def cte_conversoes_cm_email(janela_inicio: date) -> str:
    janela = (janela_inicio - timedelta(days=90)).isoformat()
    f = filtro_cm()
    return f"""WITH conversoes_cm AS (
  SELECT
    LOWER(TRIM(email_contato_principal_bd_sdr)) AS email,
    cdate AS data_conv
  FROM deals_comercial_prod
  WHERE email_contato_principal_bd_sdr IS NOT NULL
    AND cdate >= '{janela}'
    AND {f}
  UNION ALL
  SELECT
    LOWER(TRIM(email_contato_principal_bd_sdr)),
    cdate
  FROM deals_contratos_prod
  WHERE email_contato_principal_bd_sdr IS NOT NULL
    AND cdate >= '{janela}'
    AND {f}
)"""


def load_url() -> str:
    env_path = Path(__file__).parent / ".env"
    for raw in env_path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if line.startswith("SUPABASE_PG_URL="):
            return line.split("=", 1)[1].strip().strip('"').strip("'")
    raise SystemExit("ERRO: SUPABASE_PG_URL nao encontrado em dashboard/.env")


def fetch_dict(cur, sql: str) -> list[dict]:
    cur.execute(sql)
    cols = [d.name for d in cur.description]
    return [dict(zip(cols, row)) for row in cur.fetchall()]


def q_deals_rr_proposta(ini: date, fim: date) -> str:
    """
    Deals CM Buzzmonitor BR que tocaram RR ou Proposta no periodo [ini, fim].

    Um deal qualifica se:
      - data_inicio_reuniao_realizada::date BETWEEN ini E fim, COM CM 90d (POR EMAIL), OU
      - data_envio_proposta_auto::date BETWEEN ini E fim, COM CM 90d (POR EMAIL), OU
      - email NA whitelist
      - email NAO na blacklist

    A regra dos 90d aqui casa pelo MESMO EMAIL do contato principal (nao
    account_id como na dashboard semanal). Decisao: account_id agrupa demais
    (contas-saco como "E S P I C H E I" com 3007 contatos) e contamina a
    atribuicao com influencia indireta. Email/contato e o granular certo.

    Retorna 1 linha por deal (dedup por id).
    """
    cte = cte_conversoes_cm_email(ini)
    bl = _sql_email_list(EMAIL_BLACKLIST)
    wl = _sql_email_list(EMAIL_WHITELIST)
    d1, d2 = ini.isoformat(), fim.isoformat()

    return f"""
{cte},
wl AS ({wl}),
bl AS ({bl})
SELECT
  d.id,
  d.title AS deal,
  d.cdate::date AS data_inscricao,
  d.status AS status_raw,
  d.stage AS stage_id,
  d.funil_bd_sdr,
  d.data_inicio_reuniao_realizada::date AS data_rr,
  d.data_fim_reuniao_realizada::date AS data_fim_rr,
  d.data_envio_proposta_auto::date AS data_proposta,
  d.data_fechamento_auto::date AS data_fechamento,
  d.data_negocio_perdido_auto AS data_perdido,
  d.motivo_perda_bd_sdr AS motivo_perda,
  d.utm_source,
  d.utm_content,
  d.url_conversao,
  d.email_contato_principal_bd_sdr AS email,
  d.value AS valor,
  d.currency,
  COALESCE(d.bd_auto, d.sdr_sdr) AS bd,
  TRIM(COALESCE(du.first_name,'') || ' ' || COALESCE(du.last_name,'')) AS proprietario,
  d.sdr_sdr,
  d.plataformas_concorrentes_sdr AS plataforma_atual_sdr,
  d.decisores_projeto_nome_bd AS decisores_nome,
  d.objetivo_buzzmonitor_bd AS objetivo,
  d.dores_atuais_bd AS dores,
  d.bant_timing_bd AS timing_bd,
  -- flags: o EVENTO (RR/Proposta) caiu na janela 12m E passa 90d CM POR EMAIL no instante do evento?
  (
    d.data_inicio_reuniao_realizada::date BETWEEN '{d1}' AND '{d2}'
    AND d.email_contato_principal_bd_sdr IS NOT NULL
    AND EXISTS (
      SELECT 1 FROM conversoes_cm cm
      WHERE cm.email = LOWER(TRIM(d.email_contato_principal_bd_sdr))
        AND cm.data_conv <= d.data_inicio_reuniao_realizada
        AND d.data_inicio_reuniao_realizada - cm.data_conv <= INTERVAL '90 days'
    )
  ) AS rr_cm_em_janela,
  (
    d.data_envio_proposta_auto::date BETWEEN '{d1}' AND '{d2}'
    AND d.email_contato_principal_bd_sdr IS NOT NULL
    AND EXISTS (
      SELECT 1 FROM conversoes_cm cm
      WHERE cm.email = LOWER(TRIM(d.email_contato_principal_bd_sdr))
        AND cm.data_conv <= d.data_envio_proposta_auto
        AND d.data_envio_proposta_auto - cm.data_conv <= INTERVAL '90 days'
    )
  ) AS prop_cm_em_janela
FROM deals_comercial_prod d
LEFT JOIN dim_users du ON du.id = d.owner
WHERE {filtro_inbound("d")}
  AND d.data_fechamento_auto IS NULL  -- exclui deals Ganho
  AND lower(trim(COALESCE(d.status, ''))) <> 'ganho'
  AND COALESCE(d.funil_bd_sdr, '') <> 'Outbound'  -- exclui deals reclassificados como Outbound pelo BD/SDR
  AND lower(trim(COALESCE(d.email_contato_principal_bd_sdr, ''))) NOT IN (SELECT email FROM bl)
  AND (
    (
      d.data_inicio_reuniao_realizada::date BETWEEN '{d1}' AND '{d2}'
      AND d.email_contato_principal_bd_sdr IS NOT NULL
      AND EXISTS (
        SELECT 1 FROM conversoes_cm cm
        WHERE cm.email = LOWER(TRIM(d.email_contato_principal_bd_sdr))
          AND cm.data_conv <= d.data_inicio_reuniao_realizada
          AND d.data_inicio_reuniao_realizada - cm.data_conv <= INTERVAL '90 days'
      )
    )
    OR
    (
      d.data_envio_proposta_auto::date BETWEEN '{d1}' AND '{d2}'
      AND d.email_contato_principal_bd_sdr IS NOT NULL
      AND EXISTS (
        SELECT 1 FROM conversoes_cm cm
        WHERE cm.email = LOWER(TRIM(d.email_contato_principal_bd_sdr))
          AND cm.data_conv <= d.data_envio_proposta_auto
          AND d.data_envio_proposta_auto - cm.data_conv <= INTERVAL '90 days'
      )
    )
    OR
    (
      lower(trim(COALESCE(d.email_contato_principal_bd_sdr, ''))) IN (SELECT email FROM wl)
      AND (
        d.data_inicio_reuniao_realizada::date BETWEEN '{d1}' AND '{d2}'
        OR d.data_envio_proposta_auto::date BETWEEN '{d1}' AND '{d2}'
      )
    )
  )
ORDER BY COALESCE(d.data_envio_proposta_auto, d.data_inicio_reuniao_realizada) DESC,
         d.id DESC
"""


def derivar_estagio(r: dict) -> str:
    """Estagio mais avancado atingido."""
    if r.get("data_proposta"):
        return "Proposta"
    if r.get("data_rr"):
        return "Reuniao Realizada"
    return "—"


def derivar_status(r: dict) -> tuple[str, str]:
    """(label, css_class)."""
    if r.get("data_fechamento"):
        return ("Ganho", "ganho")
    if r.get("data_perdido"):
        return ("Perdido", "perdido")
    raw = (r.get("status_raw") or "").strip()
    if raw.lower() == "ganho":
        return ("Ganho", "ganho")
    if raw.lower() == "perdido":
        return ("Perdido", "perdido")
    return ("Aberto", "aberto")


def fmt_data(d) -> str:
    if not d:
        return "—"
    if isinstance(d, str):
        return d
    return d.strftime("%d/%m/%Y")


def fmt_valor(r: dict) -> str:
    v = r.get("valor")
    if v is None:
        return "—"
    try:
        v = float(v)
    except Exception:
        return "—"
    cur = (r.get("currency") or "BRL").upper()
    sym = {"BRL": "R$", "USD": "US$", "EUR": "EUR "}.get(cur, cur + " ")
    return f"{sym} {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def truncar_url(u: str, n: int = 70) -> str:
    if not u:
        return "—"
    return u if len(u) <= n else u[: n - 1] + "…"


def render_html(deals: list[dict], hoje: date, ini: date) -> str:
    # Conta de RR/Proposta usa as flags vindas do SQL (rr_cm_em_janela,
    # prop_cm_em_janela), que aplicam evento-em-janela + regra 90d CM no instante
    # do evento — mesma semantica de q_count_evento() da dashboard semanal.
    # `in_win` continua util para a marcacao visual "(fora 12m)" no celula da data.
    def in_win(d) -> bool:
        return bool(d) and ini <= d <= hoje

    src_counter: dict[str, dict] = defaultdict(
        lambda: {"total": 0, "rr": 0, "prop": 0, "perdido": 0, "aberto": 0}
    )
    cont_counter: dict[str, dict] = defaultdict(
        lambda: {"total": 0, "rr": 0, "prop": 0, "perdido": 0, "aberto": 0}
    )

    for r in deals:
        src = (r.get("utm_source") or "(vazio)").strip() or "(vazio)"
        cont = (r.get("utm_content") or "(vazio)").strip() or "(vazio)"
        for ctr, key in [(src_counter, src), (cont_counter, cont)]:
            c = ctr[key]
            c["total"] += 1
            if r.get("rr_cm_em_janela"):
                c["rr"] += 1
            if r.get("prop_cm_em_janela"):
                c["prop"] += 1
            if r.get("data_perdido"):
                c["perdido"] += 1
            else:
                c["aberto"] += 1

    def ranking_rows(counter: dict[str, dict]) -> list[dict]:
        rows = []
        for k, v in counter.items():
            tx_prop = (v["prop"] / v["total"] * 100) if v["total"] else 0
            tx_aberto = (v["aberto"] / v["total"] * 100) if v["total"] else 0
            rows.append({
                "dim": k,
                "total": v["total"],
                "rr": v["rr"],
                "prop": v["prop"],
                "perdido": v["perdido"],
                "aberto": v["aberto"],
                "tx_prop": tx_prop,
                "tx_aberto": tx_aberto,
            })
        # ranking: Proposta desc, depois Aberto desc, depois Total desc
        rows.sort(key=lambda x: (-x["prop"], -x["aberto"], -x["total"]))
        return rows

    src_rows = ranking_rows(src_counter)
    cont_rows = ranking_rows(cont_counter)

    # Resumo (Ganho ja excluido na query). RR/Proposta contam via flags
    # rr_cm_em_janela / prop_cm_em_janela — espelham q_count_evento() exatamente.
    total = len(deals)
    n_rr = sum(1 for r in deals if r.get("rr_cm_em_janela"))
    n_prop = sum(1 for r in deals if r.get("prop_cm_em_janela"))
    n_perd = sum(1 for r in deals if r.get("data_perdido"))
    n_aberto = total - n_perd

    # Construir linhas da tabela principal
    tr_rows = []
    for r in deals:
        estagio = derivar_estagio(r)
        status_lbl, status_cls = derivar_status(r)
        ac_url = f"{AC_BASE}/{r['id']}"
        url = r.get("url_conversao") or ""
        url_short = truncar_url(url)
        url_attr = html.escape(url, quote=True)

        utm_src = r.get("utm_source") or ""
        utm_cont = r.get("utm_content") or ""

        def cell_data_evento(d):
            if not d:
                return "—"
            base = fmt_data(d)
            if not (ini <= d <= hoje):
                return f'{base} <span class="off-win" title="fora da janela 12m">(fora 12m)</span>'
            return base

        tr_rows.append(f"""
        <tr>
          <td class="deal-id">{r['id']}</td>
          <td class="deal-title">{html.escape(r.get('deal') or '')}</td>
          <td>{fmt_data(r.get('data_inscricao'))}</td>
          <td><span class="badge badge-stage">{estagio}</span></td>
          <td><span class="badge badge-{status_cls}">{status_lbl}</span></td>
          <td>{cell_data_evento(r.get('data_rr'))}</td>
          <td>{cell_data_evento(r.get('data_proposta'))}</td>
          <td class="mono">{html.escape(utm_src) or '<span class="muted">—</span>'}</td>
          <td class="mono">{html.escape(utm_cont) or '<span class="muted">—</span>'}</td>
          <td class="url-cell">{'<a href="' + url_attr + '" target="_blank" rel="noopener" title="' + url_attr + '">' + html.escape(url_short) + '</a>' if url else '<span class="muted">—</span>'}</td>
          <td>{fmt_valor(r)}</td>
          <td><a class="btn-ac" href="{ac_url}" target="_blank" rel="noopener" title="Abrir deal {r['id']} no ActiveCampaign">Abrir no AC ↗</a></td>
        </tr>""")

    def rank_table_rows(rows: list[dict]) -> str:
        out = []
        for i, r in enumerate(rows, 1):
            out.append(f"""
        <tr>
          <td class="rank">#{i}</td>
          <td class="mono">{html.escape(r['dim'])}</td>
          <td>{r['total']}</td>
          <td>{r['rr']}</td>
          <td><b>{r['prop']}</b></td>
          <td>{r['aberto']}</td>
          <td>{r['perdido']}</td>
          <td><b>{r['tx_prop']:.1f}%</b></td>
        </tr>""")
        return "\n".join(out)

    src_html = rank_table_rows(src_rows)
    cont_html = rank_table_rows(cont_rows)

    return f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<title>Deals CM — Reuniao Realizada / Proposta — Buzzmonitor Brasil — 12m</title>
<style>
  :root {{
    --bg:#0f1115; --panel:#161a22; --border:#232935;
    --text:#e7ecf3; --muted:#8a93a4; --accent:#5b8def;
    --ok:#1faa6b; --warn:#d97706; --bad:#dc2626; --soft:#374151;
  }}
  *,*::before,*::after {{ box-sizing:border-box; }}
  html,body {{ margin:0; padding:0; }}
  body {{ font:14px/1.45 -apple-system, BlinkMacSystemFont, "Segoe UI", Inter, Roboto, sans-serif;
         background:var(--bg); color:var(--text); }}
  .wrap {{ max-width:1480px; margin:0 auto; padding:32px 24px 80px; }}
  header h1 {{ font-size:22px; margin:0 0 4px; }}
  header .sub {{ color:var(--muted); font-size:13px; }}
  section {{ margin-top:32px; }}
  h2 {{ font-size:16px; letter-spacing:.02em; text-transform:uppercase; color:var(--muted);
        margin:0 0 12px; padding-bottom:8px; border-bottom:1px solid var(--border); }}

  .kpis {{ display:grid; grid-template-columns:repeat(6,1fr); gap:12px; margin-top:16px; }}
  .kpi {{ background:var(--panel); border:1px solid var(--border); border-radius:10px;
         padding:14px 16px; }}
  .kpi .lbl {{ font-size:11px; color:var(--muted); text-transform:uppercase; letter-spacing:.04em; }}
  .kpi .val {{ font-size:26px; font-weight:600; margin-top:4px; }}

  .panel {{ background:var(--panel); border:1px solid var(--border); border-radius:10px;
           overflow:hidden; }}
  .table-scroll {{ overflow-x:auto; }}
  table {{ width:100%; border-collapse:collapse; font-size:13px; }}
  thead th {{ background:#1c2230; color:var(--muted); font-weight:600; text-align:left;
             padding:10px 12px; border-bottom:1px solid var(--border);
             position:sticky; top:0; }}
  tbody td {{ padding:9px 12px; border-bottom:1px solid var(--border); vertical-align:top; }}
  tbody tr:hover {{ background:#1a202b; }}
  .deal-id {{ color:var(--muted); font-family:ui-monospace,monospace; }}
  .deal-title {{ max-width:280px; }}
  .mono {{ font-family:ui-monospace, SFMono-Regular, Menlo, monospace; font-size:12px; }}
  .muted {{ color:var(--muted); }}
  .url-cell a {{ color:var(--accent); text-decoration:none; }}
  .url-cell a:hover {{ text-decoration:underline; }}
  .btn-ac {{
    display:inline-block; white-space:nowrap; text-decoration:none;
    background:var(--accent); color:#fff; font-weight:600; font-size:12px;
    padding:6px 10px; border-radius:6px; border:1px solid transparent;
    box-shadow:0 1px 0 rgba(0,0,0,.15);
    transition:background .12s ease, transform .04s ease;
  }}
  .btn-ac:hover  {{ background:#4274d6; }}
  .btn-ac:active {{ transform:translateY(1px); }}

  .badge {{ display:inline-block; padding:2px 8px; border-radius:999px; font-size:11px;
           font-weight:600; letter-spacing:.02em; }}
  .badge-stage    {{ background:#1e293b; color:#cbd5e1; }}
  .badge-aberto   {{ background:rgba(91,141,239,.18); color:#9cb8ff; }}
  .badge-ganho    {{ background:rgba(31,170,107,.18); color:#5ee3a5; }}
  .badge-perdido  {{ background:rgba(220,38,38,.18); color:#ffa6a6; }}
  .off-win {{ color:var(--muted); font-size:10.5px; font-style:italic; margin-left:4px; }}

  .rank {{ color:var(--muted); width:48px; }}
  .grid-2 {{ display:grid; grid-template-columns:1fr; gap:24px; }}
  @media (min-width:1100px) {{ .grid-2 {{ grid-template-columns:1fr 1fr; }} }}

  .filterbar {{ display:flex; gap:8px; align-items:center; margin-bottom:12px; flex-wrap:wrap; }}
  .filterbar input, .filterbar select {{
    background:#0f1115; color:var(--text); border:1px solid var(--border);
    border-radius:8px; padding:8px 10px; font-size:13px;
  }}
  .filterbar input {{ min-width:280px; }}
  .filterbar .count {{ color:var(--muted); margin-left:auto; }}
</style>
</head>
<body>
  <div class="wrap">
    <header>
      <h1>Deals CM — Reuniao Realizada / Proposta (sem Ganho)</h1>
      <div class="sub">Buzzmonitor Brasil · ultimos 12 meses ({fmt_data(ini)} a {fmt_data(hoje)}) · gerado {hoje.isoformat()} · filtro CM com regra 90d por <b>email</b> · exclui Ganho · exclui <b>Funil [BD e SDR] = Outbound</b></div>
      <div class="kpis">
        <div class="kpi"><div class="lbl">Total deals</div><div class="val">{total}</div></div>
        <div class="kpi"><div class="lbl">Atingiram RR</div><div class="val">{n_rr}</div></div>
        <div class="kpi"><div class="lbl">Receberam Proposta</div><div class="val">{n_prop}</div></div>
        <div class="kpi"><div class="lbl">Aberto</div><div class="val" style="color:#9cb8ff">{n_aberto}</div></div>
        <div class="kpi"><div class="lbl">Perdido</div><div class="val" style="color:#ffa6a6">{n_perd}</div></div>
      </div>
    </header>

    <section>
      <h2>Tabela completa</h2>
      <div class="filterbar">
        <input type="text" id="q" placeholder="Buscar por deal, email, utm, URL...">
        <select id="fStage">
          <option value="">Todos os estagios</option>
          <option>Reuniao Realizada</option>
          <option>Proposta</option>
        </select>
        <select id="fStatus">
          <option value="">Todos os status</option>
          <option>Aberto</option>
          <option>Perdido</option>
        </select>
        <span class="count" id="countLabel">{total} deals</span>
      </div>
      <div class="panel">
        <div class="table-scroll">
          <table id="tbl">
            <thead>
              <tr>
                <th>ID</th>
                <th>Deal</th>
                <th>Inscricao</th>
                <th>Estagio</th>
                <th>Status</th>
                <th>Data RR</th>
                <th>Data Proposta</th>
                <th>UTM Source</th>
                <th>UTM Content</th>
                <th>URL Conversao</th>
                <th>Valor</th>
                <th>AC</th>
              </tr>
            </thead>
            <tbody>
              {''.join(tr_rows)}
            </tbody>
          </table>
        </div>
      </div>
    </section>

    <section class="grid-2">
      <div>
        <h2>Ranking — UTM Source</h2>
        <div class="panel"><div class="table-scroll">
          <table>
            <thead><tr>
              <th>#</th><th>UTM Source</th>
              <th>Total</th><th>RR</th><th>Prop.</th>
              <th>Aberto</th><th>Perd.</th>
              <th>% Prop.</th>
            </tr></thead>
            <tbody>{src_html}</tbody>
          </table>
        </div></div>
      </div>
      <div>
        <h2>Ranking — UTM Content</h2>
        <div class="panel"><div class="table-scroll">
          <table>
            <thead><tr>
              <th>#</th><th>UTM Content</th>
              <th>Total</th><th>RR</th><th>Prop.</th>
              <th>Aberto</th><th>Perd.</th>
              <th>% Prop.</th>
            </tr></thead>
            <tbody>{cont_html}</tbody>
          </table>
        </div></div>
      </div>
    </section>
  </div>

<script>
(function(){{
  const q = document.getElementById('q');
  const fStage = document.getElementById('fStage');
  const fStatus = document.getElementById('fStatus');
  const tbody = document.querySelector('#tbl tbody');
  const rows = Array.from(tbody.querySelectorAll('tr'));
  const countLabel = document.getElementById('countLabel');
  function apply(){{
    const term = (q.value || '').toLowerCase().trim();
    const stg = fStage.value;
    const sta = fStatus.value;
    let n = 0;
    rows.forEach(tr => {{
      const txt = tr.textContent.toLowerCase();
      const stageTd = tr.children[3].textContent.trim();
      const statusTd = tr.children[4].textContent.trim();
      const matchTerm = !term || txt.includes(term);
      const matchStg = !stg || stageTd === stg;
      const matchSta = !sta || statusTd === sta;
      const show = matchTerm && matchStg && matchSta;
      tr.style.display = show ? '' : 'none';
      if(show) n++;
    }});
    countLabel.textContent = n + ' deals';
  }}
  q.addEventListener('input', apply);
  fStage.addEventListener('change', apply);
  fStatus.addEventListener('change', apply);
}})();
</script>
</body>
</html>
"""


def render_csv(deals: list[dict]) -> str:
    """Gera CSV UTF-8 com todas as colunas para upload no Drive (vira Google Sheets)."""
    import csv
    import io

    header = [
        "ID", "Deal", "Data Inscricao",
        "Etapa", "Status", "Funil [BD e SDR]",
        "Estagio atingido", "Data RR", "Data Fim Reuniao Realizada", "Data Proposta",
        "Valor do negocio", "Currency",
        "Proprietario do negocio",
        "SDR [SDR]", "Plataforma Atual [SDR]",
        "UTM Source", "UTM Content", "URL Conversao",
        "Email",
        "Decisores do projeto - NOME [BD]",
        "Objetivo com a Buzzmonitor [BD]",
        "Dores atuais [BD]",
        "Timing [BD]",
        "Link AC",
    ]
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\n")
    w.writerow(header)
    for r in deals:
        etapa = STAGE_NAMES.get(r.get("stage_id"), f"Stage {r.get('stage_id') or ''}")
        if r.get("data_proposta"):
            estagio_atingido = "Proposta"
        elif r.get("data_rr"):
            estagio_atingido = "Reuniao Realizada"
        else:
            estagio_atingido = ""
        status_lbl, _ = derivar_status(r)

        valor = r.get("valor")
        try:
            valor_str = f"{float(valor):.2f}" if valor is not None else ""
        except Exception:
            valor_str = ""

        def d2s(d):
            if not d:
                return ""
            return d.isoformat() if hasattr(d, "isoformat") else str(d)

        w.writerow([
            r.get("id") or "",
            r.get("deal") or "",
            d2s(r.get("data_inscricao")),
            etapa,
            status_lbl,
            r.get("funil_bd_sdr") or "",
            estagio_atingido,
            d2s(r.get("data_rr")),
            d2s(r.get("data_fim_rr")),
            d2s(r.get("data_proposta")),
            valor_str,
            r.get("currency") or "",
            r.get("proprietario") or "",
            r.get("sdr_sdr") or "",
            r.get("plataforma_atual_sdr") or "",
            r.get("utm_source") or "",
            r.get("utm_content") or "",
            r.get("url_conversao") or "",
            r.get("email") or "",
            r.get("decisores_nome") or "",
            r.get("objetivo") or "",
            r.get("dores") or "",
            r.get("timing_bd") or "",
            f"{AC_BASE}/{r['id']}",
        ])
    return buf.getvalue()


def main():
    hoje = date.today()
    ini = hoje - timedelta(days=365)
    print(f"Janela: {ini} -> {hoje}")

    url = load_url()
    print("Conectando ao Supabase...")
    with psycopg.connect(url, autocommit=True) as conn, conn.cursor() as cur:
        cur.execute("SET LOCAL statement_timeout = '180s'")
        print("Rodando query principal...")
        deals = fetch_dict(cur, q_deals_rr_proposta(ini, hoje))
        print(f"  -> {len(deals)} deals retornados.")

    print("Renderizando HTML...")
    html_out = render_html(deals, hoje, ini)
    out_path = Path(__file__).parent / "deals-rr-proposta-cm-12m.html"
    out_path.write_text(html_out, encoding="utf-8")
    print(f"OK HTML -> {out_path}")

    csv_out = render_csv(deals)
    csv_path = Path(__file__).parent / "deals-rr-proposta-cm-12m.csv"
    # BOM UTF-8 pra Excel/Sheets abrirem com acentos corretos
    csv_path.write_text("﻿" + csv_out, encoding="utf-8")
    print(f"OK CSV  -> {csv_path}")


if __name__ == "__main__":
    main()
