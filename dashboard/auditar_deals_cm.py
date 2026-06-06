"""auditar_deals_cm.py — Auditoria de deals de Content Marketing nao mapeados por falha de UTM.

PROBLEMA
--------
A dashboard CM (Buzzmonitor Brasil) decide se um deal e CM lendo `utm_source` + `url_conversao`
NA PROPRIA LINHA do deal (dashboard/queries.py::filtro_cm). Muitos deals chegam ao Supabase com
esses campos VAZIOS por falha da automacao AC->Supabase — mas a origem CM existe noutro lugar
(num deal-irmao da mesma conta/contato, no titulo, ou — fase 2 — numa nota / no contato do AC).
Esses deals viram CM "invisivel": somem da dashboard.

O QUE ESTE HARNESS FAZ (Tier 1 — so Supabase, read-only)
--------------------------------------------------------
1. Monta o conjunto CANDIDATO: deals com utm_source E url_conversao vazios, no periodo, com email,
   tirando ruido (dominios de teste/internos) e a EMAIL_BLACKLIST.
2. RECUPERA a UTM localmente (nunca grava no banco):
   - 2a. Propagacao intra-conta/email (ALTA): copia utm_source/medium/url de um deal-DOADOR CM
         (mesma account_id ou mesmo email) que passe no filtro_cm. Proxy de "o contato tem UTM".
   - 2b. Prefixo de titulo (MEDIA, revisao): [BLOG], webinar, web.*, checklist, meta, ig...
   - 2c. Formulario inbound / HOLD A (MEDIA, revisao): funil Inbound + tipo/origem de LP.
3. RE-RODA o filtro CM REAPROVEITANDO filtro_cm()/whitelist/blacklist de queries.py (zero drift),
   sobre as colunas EFETIVAS (COALESCE(original, recuperada)).
4. NET-NEW = emails que viram CM DEPOIS e nao estavam no conjunto CM ANTES (dedupe por email,
   igual a dashboard). Esses sao os "deals de CM nao mapeados por falha na automacao".
5. Escreve relatorio MD + CSVs em dashboard/auditoria/ (gitignored — contem PII).

SOMENTE LEITURA. Reusa o filtro_cm da dashboard; nao reimplementa a regra de CM.

Uso:
    uv run --python 3.12 --with "psycopg[binary]" python dashboard/auditar_deals_cm.py
    uv run --python 3.12 --with "psycopg[binary]" python dashboard/auditar_deals_cm.py --desde 2026-01-01 --ate 2026-06-02

Le SUPABASE_PG_URL de dashboard/.env. Rodar a partir da raiz do projeto.
"""
from __future__ import annotations

import argparse
import csv
import re
import sys
from datetime import date
from pathlib import Path

import psycopg

# imports locais — REUSO do filtro canonico da dashboard (anti-drift).
sys.path.insert(0, str(Path(__file__).parent))
from queries import (  # noqa: E402
    filtro_cm,
    EMAIL_WHITELIST,
    EMAIL_BLACKLIST,
    _sql_email_list,
    q_lista_leads,
)

OUT_DIR = Path(__file__).parent / "auditoria"

# ----------------------------------------------------------------------------- ruido
# Dominios que nunca sao lead CM real (teste, webhook, internos do grupo).
NOISE_DOMAINS = {
    "yopmail.com", "webhook.com", "teste.com", "test.com", "example.com",
    "mailinator.com", "sharklasers.com", "guerrillamail.com", "dealpolitico.com",
}
# Sufixos de email internos do grupo (nao sao geracao CM).
NOISE_EMAIL_SUFFIXES = (
    "@buzzmonitor.com.br", "@buzzmonitor.com", "@elife.com.br", "@elife.com",
)

# ----------------------------------------------------------------------------- titulo->canal (2b)
# So sinais CLAROS de CM. Casados em lower(title). Ordem importa (primeiro match vence).
# Ruidoso de proposito conservador: usado SO pra lista de REVISAO, nunca pro net-new automatico.
CM_TITLE_PATTERNS: list[tuple[str, str]] = [
    (r"\[?\s*blog", "blog"),
    (r"web\.|webinar|web ", "webinar"),
    (r"masterclass|trends", "webinar"),
    (r"checklist", "checklist"),
    (r"material|e-?book|whitepaper|relat[oó]rio", "material"),
    (r"\bmeta\b|\bfb\b|facebook", "meta"),
    (r"\b(ig|instagram|inst\.)\b", "instagram"),
    (r"linkedin|\bli\b", "linkedin"),
    (r"tiktok", "tiktok"),
    (r"whatsapp|\bwpp\b", "whatsapp"),
    (r"evento", "evento"),
    (r"gemini", "gemini"),
    (r"chatgpt|openai", "chatgpt.com"),
    (r"notion", "notion"),
]
# Prefixos/termos que claramente NAO sao CM — saem ate da lista de revisao.
NOT_CM_TITLE = re.compile(
    r"meetime|indica[cç][aã]o|vtex|\bic\.?\b|\bcomp\.|\brmkt\b|monit|\banaly\.|\bsdr\b|outbound|prospec",
    re.IGNORECASE,
)


def titulo_canal_cm(title: str | None) -> str | None:
    """Retorna o canal CM sugerido pelo titulo, ou None. Conservador (so sinais claros)."""
    if not title:
        return None
    t = title.lower()
    if NOT_CM_TITLE.search(t):
        return None
    for pat, canal in CM_TITLE_PATTERNS:
        if re.search(pat, t):
            return canal
    return None


def inbound_cm(funil: str | None, tipo: str | None, origem: str | None) -> bool:
    """Sinal 2c (HOLD A): lead Inbound vindo de LP / Solicitacao de Proposta."""
    if not funil or "inbound" not in funil.lower():
        return False
    blob = " ".join(x for x in (tipo, origem) if x).lower()
    return bool(re.search(r"proposta|solicita|\blp\b|landing", blob))


# ----------------------------------------------------------------------------- I/O
def load_url() -> str:
    """Espelha gerar_relatorio.load_url — le SUPABASE_PG_URL de dashboard/.env."""
    env_path = Path(__file__).parent / ".env"
    if not env_path.exists():
        raise SystemExit(f"ERRO: {env_path} nao existe. Copie dashboard/.env.example e preencha.")
    for raw in env_path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if line.startswith("SUPABASE_PG_URL="):
            return line.split("=", 1)[1].strip().strip('"').strip("'")
    raise SystemExit("ERRO: SUPABASE_PG_URL nao encontrado em dashboard/.env")


def fetch_dict(cur, sql: str) -> list[dict]:
    cur.execute(sql)
    cols = [d.name for d in cur.description]
    return [dict(zip(cols, row)) for row in cur.fetchall()]


# ----------------------------------------------------------------------------- SQL
def _noise_sql(col: str) -> str:
    """Clausula que EXCLUI ruido (dominios de teste + internos). `col` = expr de email lower/trim."""
    dominios = ", ".join(f"'{d}'" for d in sorted(NOISE_DOMAINS))
    sufixos = " OR ".join(f"{col} LIKE '%{suf}'" for suf in NOISE_EMAIL_SUFFIXES)
    return f"(split_part({col}, '@', 2) NOT IN ({dominios}) AND NOT ({sufixos}))"


def sql_auditoria(desde: date, ate: date | None) -> str:
    """Query unica: candidatos + melhor doador CM (conta/email) + is_cm_depois via filtro_cm reusado.

    A coluna is_cm_depois aplica o MESMO filtro_cm()/whitelist/blacklist da dashboard sobre as
    colunas EFETIVAS (recuperadas do doador). Candidato sem doador fica com utm/url NULL e nao passa.
    """
    F = filtro_cm()
    WL = _sql_email_list(EMAIL_WHITELIST)
    BL = _sql_email_list(EMAIL_BLACKLIST)
    email_norm = "lower(trim(email_contato_principal_bd_sdr))"
    ate_cand = f"AND cdate::date <= '{ate.isoformat()}'" if ate else ""
    noise = _noise_sql(email_norm)
    return f"""
WITH wl AS ({WL}),
     bl AS ({BL}),
cm_donors AS (
  SELECT account_id, {email_norm} AS email, utm_source, utm_medium, utm_content,
         url_conversao, cdate, id AS donor_id, 'comercial' AS donor_tab
  FROM deals_comercial_prod
  WHERE {F}
  UNION ALL
  SELECT account_id, {email_norm} AS email, utm_source, utm_medium, utm_content,
         url_conversao, cdate, id AS donor_id, 'contratos' AS donor_tab
  FROM deals_contratos_prod
  WHERE {F}
),
cand AS (
  SELECT id, account_id,
         {email_norm} AS email,
         email_contato_principal_bd_sdr AS email_raw,
         title, cdate,
         funil_inicial_lead_auto, tipo_inbound_auto, origem_negocio_inbound_auto
  FROM deals_comercial_prod
  WHERE cdate::date >= '{desde.isoformat()}' {ate_cand}
    AND (utm_source IS NULL OR btrim(utm_source) = '')
    AND (url_conversao IS NULL OR btrim(url_conversao) = '')
    AND email_contato_principal_bd_sdr IS NOT NULL
    AND {email_norm} NOT IN (SELECT email FROM bl)
    AND {noise}
),
da AS (  -- melhor doador por account_id (proximidade temporal)
  SELECT DISTINCT ON (c.id) c.id AS cid, cd.donor_id, cd.donor_tab,
         cd.utm_source, cd.utm_medium, cd.url_conversao, cd.cdate AS donor_cdate
  FROM cand c
  JOIN cm_donors cd ON cd.account_id = c.account_id AND c.account_id IS NOT NULL
  ORDER BY c.id, abs(EXTRACT(EPOCH FROM (cd.cdate - c.cdate)))
),
de AS (  -- melhor doador por email (fallback)
  SELECT DISTINCT ON (c.id) c.id AS cid, cd.donor_id, cd.donor_tab,
         cd.utm_source, cd.utm_medium, cd.url_conversao, cd.cdate AS donor_cdate
  FROM cand c
  JOIN cm_donors cd ON cd.email = c.email
  ORDER BY c.id, abs(EXTRACT(EPOCH FROM (cd.cdate - c.cdate)))
),
enriched AS (
  -- Preferencia: doador por EMAIL (mesmo contato — o que o Victor descreveu) vence o
  -- doador por CONTA (mesma empresa, possivelmente outro contato — sinal mais fraco).
  SELECT c.id, c.account_id, c.email, c.email_raw, c.title, c.cdate,
         c.funil_inicial_lead_auto, c.tipo_inbound_auto, c.origem_negocio_inbound_auto,
         COALESCE(de.donor_id, da.donor_id)   AS donor_id,
         COALESCE(de.donor_tab, da.donor_tab) AS donor_tab,
         CASE WHEN de.donor_id IS NOT NULL THEN 'email'
              WHEN da.donor_id IS NOT NULL THEN 'conta'
              ELSE NULL END                   AS match_kind,
         COALESCE(de.utm_source, da.utm_source)   AS utm_source,
         COALESCE(de.utm_medium, da.utm_medium)   AS utm_medium,
         COALESCE(de.url_conversao, da.url_conversao) AS url_conversao
  FROM cand c
  LEFT JOIN da ON da.cid = c.id
  LEFT JOIN de ON de.cid = c.id
)
SELECT
  id, account_id, email, email_raw, title, cdate::date AS dia,
  funil_inicial_lead_auto, tipo_inbound_auto, origem_negocio_inbound_auto,
  donor_id, donor_tab, match_kind,
  utm_source AS utm_recuperada,
  url_conversao AS url_recuperada,
  (
    email NOT IN (SELECT email FROM bl)
    AND ( email IN (SELECT email FROM wl) OR {F} )
  ) AS is_cm_depois
FROM enriched
ORDER BY (match_kind = 'email') DESC NULLS LAST, dia DESC
"""


# ----------------------------------------------------------------------------- Fase 2 (AC) — seam
def enrich_from_ac(candidatos_sem_doador: list[dict]) -> list[dict]:
    """FASE 2 (nao implementada na v1 — decisao "so Supabase por ora").

    Quando houver AC_API_KEY + AC_API_URL num .env, esta funcao deve, SO para os candidatos
    ainda sem UTM recuperada (com cache + rate-limit):
      1. GET /deals/{id}/notes  -> regex de utm_source / url de conversao na nota.
      2. UTM autoritativa do CONTATO via custom fields do AC:
         845=utm_source, 846=utm_medium, 847=utm_campaign, 848=utm_content, 851=URL Conversao.
         (Supabase deals.id == AC deal id; deal.contact -> contact id; deal.organization == account_id.)
    Deve devolver os candidatos com utm_source/url_conversao preenchidos, pra reentrarem no
    re-filtro (passo 3). Ver .claude/skills/auditar-deals-cm/CONTEXT.md (mapa AC validado).
    """
    return candidatos_sem_doador  # no-op


# ----------------------------------------------------------------------------- relatorio
def _w(rows: list[dict], path: Path, fields: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        wr = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        wr.writeheader()
        wr.writerows(rows)


def main() -> None:
    ap = argparse.ArgumentParser(description="Auditoria de deals CM nao mapeados por falha de UTM.")
    ap.add_argument("--desde", default="2026-01-01", help="Data inicial (YYYY-MM-DD). Default 2026-01-01.")
    ap.add_argument("--ate", default=None, help="Data final (YYYY-MM-DD). Default: sem limite superior.")
    ap.add_argument("--out", default=None, help="Diretorio de saida. Default dashboard/auditoria/.")
    args = ap.parse_args()

    desde = date.fromisoformat(args.desde)
    ate = date.fromisoformat(args.ate) if args.ate else None
    out_dir = Path(args.out) if args.out else OUT_DIR
    out_dir.mkdir(parents=True, exist_ok=True)
    hoje = date.today()
    periodo = f"{desde.isoformat()} -> {ate.isoformat() if ate else 'hoje'}"

    url = load_url()
    with psycopg.connect(url, autocommit=True) as conn:
        with conn.cursor() as cur:
            cur.execute("SET statement_timeout = '300s'")

            # ANTES: emails CM no periodo, com dados crus (REUSO de q_lista_leads da dashboard).
            ate_leads = ate or hoje
            antes_rows = fetch_dict(cur, q_lista_leads(desde, ate_leads))
            antes_emails = {
                (r.get("email") or "").strip().lower() for r in antes_rows if r.get("email")
            }
            print(f"[antes] Leads CM no periodo (dashboard, dados crus): {len(antes_emails)} emails unicos")

            # Candidatos + doadores + is_cm_depois
            print(f"[query] auditando candidatos {periodo} ...")
            rows = fetch_dict(cur, sql_auditoria(desde, ate))
            print(f"[cand]  candidatos (utm+url vazios, com email, sem ruido): {len(rows)}")

    # -------- classificacao (Python) --------
    def origem_disp(r: dict) -> str:
        u = (r.get("utm_recuperada") or "").strip()
        if u:
            return u
        url = (r.get("url_recuperada") or "").strip()
        if url:
            return "url:" + url.replace("https://", "").replace("http://", "")[:42]
        return "?"

    cm = [r for r in rows if r.get("is_cm_depois")]
    email_cm = [r for r in cm if r.get("match_kind") == "email"]   # mesmo contato (ALTA)
    conta_cm = [r for r in cm if r.get("match_kind") == "conta"]   # mesma empresa (REVISAO)
    email_cm_emails = {r["email"] for r in email_cm}
    conta_cm_emails = {r["email"] for r in conta_cm}

    # NET-NEW (headline) = recuperado por EMAIL e ainda nao contado pela dashboard.
    net_new_emails = email_cm_emails - antes_emails
    # Adicional por empresa (mesma conta, outro contato) -> revisao, fora do headline.
    conta_rev_emails = conta_cm_emails - antes_emails - net_new_emails
    ja_contados = (email_cm_emails | conta_cm_emails) & antes_emails

    def dedupe(rws: list[dict], emails: set[str]) -> list[dict]:
        best: dict[str, dict] = {}
        for r in rws:
            if r["email"] in emails:
                b = best.get(r["email"])
                if b is None or (r.get("dia") or date.min) > (b.get("dia") or date.min):
                    best[r["email"]] = r
        return sorted(best.values(), key=lambda r: r.get("dia") or date.min, reverse=True)

    net_new = dedupe(email_cm, net_new_emails)
    conta_rev = dedupe(conta_cm, conta_rev_emails)

    # REVISAO (titulo/inbound): sem doador nenhum, mas sinal de CM, email ainda nao listado.
    ja_listados = antes_emails | net_new_emails | conta_rev_emails
    revisao_raw: list[dict] = []
    prefixos_amb: dict[str, int] = {}
    for r in rows:
        if r.get("donor_id") or r["email"] in ja_listados:
            continue
        canal = titulo_canal_cm(r.get("title"))
        inb = inbound_cm(r.get("funil_inicial_lead_auto"), r.get("tipo_inbound_auto"),
                         r.get("origem_negocio_inbound_auto"))
        if canal or inb:
            r2 = dict(r)
            r2["sinal"] = ",".join(s for s in [f"titulo:{canal}" if canal else "", "inbound" if inb else ""] if s)
            revisao_raw.append(r2)
        else:
            m = re.search(r"\[([^\]]+)\]", r.get("title") or "")
            if m:
                p = m.group(1).strip().lower()
                prefixos_amb[p] = prefixos_amb.get(p, 0) + 1
    rev_best: dict[str, dict] = {}
    for r in revisao_raw:
        b = rev_best.get(r["email"])
        if b is None or (r.get("dia") or date.min) > (b.get("dia") or date.min):
            rev_best[r["email"]] = r
    revisao = sorted(rev_best.values(), key=lambda r: r["email"])
    revisao_emails = set(rev_best)

    # contagem por canal (net-new, email)
    por_canal: dict[str, int] = {}
    for r in net_new:
        s = origem_disp(r)
        por_canal[s] = por_canal.get(s, 0) + 1

    # -------- escrever saidas --------
    stamp = hoje.isoformat()
    csv_fields = ["id", "email_raw", "dia", "match_kind", "utm_recuperada", "url_recuperada",
                  "donor_id", "donor_tab", "title",
                  "funil_inicial_lead_auto", "tipo_inbound_auto", "origem_negocio_inbound_auto"]
    _w(net_new, out_dir / f"net-new-contato-{stamp}.csv", csv_fields)
    _w(conta_rev, out_dir / f"revisao-mesma-empresa-{stamp}.csv", csv_fields)
    _w(revisao, out_dir / f"revisao-titulo-inbound-{stamp}.csv", csv_fields + ["sinal"])
    _w([{"prefixo": k, "n": v} for k, v in sorted(prefixos_amb.items(), key=lambda x: -x[1])],
       out_dir / f"prefixos-titulo-nao-mapeados-{stamp}.csv", ["prefixo", "n"])

    def _tab(f, rws, n, extra_sinal=False):
        if not rws:
            f.write("_Nenhum._\n\n")
            return
        if extra_sinal:
            f.write("| deal | data | sinal | titulo |\n|---|---|---|---|\n")
        else:
            f.write("| deal | data | origem recuperada | doador | titulo |\n|---|---|---|---|---|\n")
        for r in rws[:n]:
            tit = (r.get("title") or "").replace("|", "/")[:48]
            if extra_sinal:
                f.write(f"| {r['id']} | {r['dia']} | {r.get('sinal')} | {tit} |\n")
            else:
                f.write(f"| {r['id']} | {r['dia']} | {origem_disp(r)} | "
                        f"{r.get('donor_id')} ({r.get('donor_tab')}) | {tit} |\n")
        if len(rws) > n:
            f.write(f"\n_... +{len(rws) - n} no CSV._\n")
        f.write("\n")

    md = out_dir / f"AUDIT-CM-UTM-{stamp}.md"
    with md.open("w", encoding="utf-8") as f:
        f.write("# Auditoria — Deals CM nao mapeados por falha de UTM\n\n")
        f.write(f"- **Periodo:** {periodo}\n- **Gerado em:** {stamp}\n")
        f.write("- **Fonte:** Supabase (read-only). Filtro CM reaproveitado de `dashboard/queries.py`.\n")
        f.write("- **Tier:** 1 (so Supabase). Recuperacao por **email** (mesmo contato) = alta confianca; "
                "por **conta** (mesma empresa) + titulo/inbound = revisao. AC (notas + contato) = Fase 2.\n\n")
        f.write("## Resumo\n\n| Metrica | Valor |\n|---|---:|\n")
        f.write(f"| Leads CM no periodo ANTES (dashboard) | {len(antes_emails)} |\n")
        f.write(f"| Candidatos (utm+url vazios, com email, sem ruido) | {len(rows)} |\n")
        f.write(f"| **NET-NEW por contato (email) — alta confianca** | **{len(net_new_emails)}** |\n")
        f.write(f"| Adicional por empresa (mesma conta, revisar) | {len(conta_rev_emails)} |\n")
        f.write(f"| Em revisao por titulo/inbound (sem doador) | {len(revisao_emails)} |\n")
        f.write(f"| Recuperados mas ja contados (sibling CM no periodo) | {len(ja_contados)} |\n")
        f.write(f"| Prefixos de titulo ambiguos (nao mapeados) | {len(prefixos_amb)} |\n\n")
        ganho = (len(net_new_emails) / len(antes_emails) * 100) if antes_emails else 0
        f.write(f"> NET-NEW de alta confianca = **+{ganho:.1f}%** sobre os {len(antes_emails)} leads CM "
                f"hoje contados no periodo.\n\n")

        f.write("## NET-NEW por canal recuperado (alta confianca, email)\n\n")
        if por_canal:
            f.write("| origem recuperada | deals |\n|---|---:|\n")
            for k, v in sorted(por_canal.items(), key=lambda x: -x[1]):
                f.write(f"| {k} | {v} |\n")
        else:
            f.write("_Nenhum._\n")
        f.write("\n")

        f.write(f"## NET-NEW — alta confianca / mesmo contato ({len(net_new)} emails)\n\n")
        f.write("Recuperados por **propagacao de UTM de outro deal do mesmo email** (mesmo contato). "
                "CSV: `net-new-contato.csv`.\n\n")
        _tab(f, net_new, 60)

        f.write(f"## Revisao — mesma empresa, outro contato ({len(conta_rev)} emails)\n\n")
        f.write("Doador CM e da **mesma conta (empresa)** mas e outro email. Pode ser influencia de "
                "conteudo, mas precisa confirmacao (nao e o mesmo contato). CSV: `revisao-mesma-empresa.csv`.\n\n")
        _tab(f, conta_rev, 40)

        f.write(f"## Revisao — titulo/inbound ({len(revisao_emails)} emails)\n\n")
        f.write("Sem doador, mas titulo ou formulario inbound sugerem CM. CSV: `revisao-titulo-inbound.csv`.\n\n")
        _tab(f, revisao, 40, extra_sinal=True)

        if prefixos_amb:
            f.write("## Prefixos de titulo ambiguos (mapear com o Victor)\n\n")
            f.write("Candidatos sem doador cujo titulo tem `[prefixo]` nao classificado. "
                    "Decidir quais sao canais CM (igual a whitelist de slugs foi construida).\n\n")
            f.write("| prefixo | deals |\n|---|---:|\n")
            for k, v in sorted(prefixos_amb.items(), key=lambda x: -x[1])[:30]:
                f.write(f"| {k} | {v} |\n")
            f.write("\n")

        f.write("## Remediacao sugerida\n\n")
        if 0 < len(net_new_emails) <= 25:
            f.write("Volume pequeno + alta confianca. Da pra adicionar a `EMAIL_WHITELIST` de "
                    "`dashboard/queries.py` (Victor confirma cada um). Bloco sugerido:\n\n```python\n")
            for r in net_new:
                f.write(f"    '{(r['email_raw'] or '').strip().lower()}',"
                        f"  # {r['id']} — {origem_disp(r)} via doador {r.get('donor_id')}\n")
            f.write("```\n\n")
        elif len(net_new_emails) > 25:
            f.write(f"Volume ALTO ({len(net_new_emails)} emails de alta confianca) — inviavel manter inline "
                    "na `EMAIL_WHITELIST`. O certo e **corrigir a automacao AC->Supabase** que deveria "
                    "preencher utm_source/url_conversao no deal, ou criar a tabela `cm_email_whitelist` "
                    "(ja prevista em `queries.py:11`) populada por este audit. NAO editar inline.\n\n")
        else:
            f.write("Nenhum net-new de alta confianca neste periodo. Ver listas de revisao.\n\n")

    print(f"[antes] {len(antes_emails)}  [net-new email] {len(net_new_emails)}  "
          f"[empresa-revisar] {len(conta_rev_emails)}  [titulo/inbound] {len(revisao_emails)}")
    print(f"[ok] relatorio: {md}")


if __name__ == "__main__":
    main()
