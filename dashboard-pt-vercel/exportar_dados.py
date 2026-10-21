"""exportar_dados.py — Portugal: gera dados-pt-{marca}.json para as dashboards no Vercel.

As 3 marcas PT compartilham schema, etapas e logica, entao compartilham tambem este
exportador: `--marca bm|cxpress|elife|todas`. A logica (coorte por cdate, etapa por
titulo, classificacao CM) e fonte unica em `dashboard/queries_portugal.py` — aqui so
projetamos uma linha por deal e deixamos o motor.js agregar no navegador.

Uso:
    uv run --python 3.12 --with "psycopg[binary]" python dashboard-pt-vercel/exportar_dados.py --marca todas
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DASH = ROOT.parent / "dashboard"
sys.path.insert(0, str(DASH))

import psycopg  # noqa: E402

import queries_portugal as Q  # noqa: E402

HOJE = date.today()
# Versao do formato deste JSON. Bumpar JUNTO com dashboards-umbrella/contratos/pt.json
# quando um campo lido pelo painel for removido, renomeado, mudar de tipo ou de literal.
# Adicionar campo NAO bumpa. validar_contrato.py falha se os dois divergirem.
SCHEMA_VERSION = 1


def load_url() -> str:
    """Le SUPABASE_PG_URL do ambiente (CI) ou de dashboard/.env (local)."""
    if os.environ.get("SUPABASE_PG_URL"):
        return os.environ["SUPABASE_PG_URL"].strip()
    env = DASH / ".env"
    if env.exists():
        for line in env.read_text(encoding="utf-8").splitlines():
            if line.startswith("SUPABASE_PG_URL="):
                return line.split("=", 1)[1].strip()
    raise SystemExit("ERRO: SUPABASE_PG_URL nao encontrado em dashboard/.env")


def exportar(cur, marca: str) -> dict:
    cfg = Q.MARCAS[marca]
    deals = []
    for sql, origem in Q.q_todas(marca):
        cur.execute(sql)
        cols = [d.name for d in cur.description]
        for row in cur.fetchall():
            r = dict(zip(cols, row))
            fonte = Q.normalizar_utm(r["utm_source"])
            url = r["url_conversao"]
            etapa = Q.MAPA_ETAPAS.get((r["etapa_titulo"] or "").strip(), "outro")
            reuniao = Q.chegou_reuniao(etapa, r["ordem_etapa"], r["ordem_reuniao"])
            deals.append({
                "id": r["id"],
                "t": r["deal"],
                "d": r["d_criacao"].isoformat() if r["d_criacao"] else None,
                "m": r["d_modificacao"].isoformat() if r["d_modificacao"] else None,
                "o": origem,
                "e": etapa,
                "s": r["status"],
                "v": float(r["valor"] or 0),
                "cur": r["moeda"] or "EUR",
                "f": fonte,
                "md": Q.normalizar_utm(r["utm_medium"]),
                "cp": (r["utm_campaign"] or "").strip() or None,
                "dom": Q.dominio_de(url),
                "pa": Q.caminho_de(url),
                "c": Q.classificar(fonte, url),
                "r": 1 if reuniao else 0,
            })

    deals.sort(key=lambda x: (x["d"] or "", x["id"]))
    return {
        "schema_version": SCHEMA_VERSION,
        "gerado_em": HOJE.isoformat(),
        "marca": marca,
        "nome": cfg["nome"],
        "moeda": "EUR",
        "escopo": (
            "Coorte por data de criacao do deal. Etapa e o ESTADO ATUAL (nao ha "
            "historico de etapa em PT), por isso o painel mostra distribuicao, nunca "
            "conversao entre etapas. Reuniao e fechamento tambem saem da etapa "
            "atual, sem data. CM e classificacao, nao filtro."
        ),
        "etapas": [list(e) for e in Q.ETAPAS_CANONICAS],
        "terminais": sorted(Q.ETAPAS_TERMINAIS),
        "ganhas": sorted(Q.ETAPAS_GANHAS),
        "deals": deals,
    }


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser()
    ap.add_argument("--marca", default="todas", choices=list(Q.MARCAS) + ["todas"])
    args = ap.parse_args()
    marcas = list(Q.MARCAS) if args.marca == "todas" else [args.marca]

    with psycopg.connect(load_url(), autocommit=True) as conn, conn.cursor() as cur:
        for marca in marcas:
            dados = exportar(cur, marca)
            out = ROOT / f"dados-pt-{marca}.json"
            out.write_text(json.dumps(dados, ensure_ascii=False, default=str),
                           encoding="utf-8")
            n = len(dados["deals"])
            n26 = sum(1 for d in dados["deals"] if (d["d"] or "") >= "2026-01-01")
            cm = sum(1 for d in dados["deals"]
                     if d["c"] == "cm" and (d["d"] or "") >= "2026-01-01")
            sem = sum(1 for d in dados["deals"]
                      if d["c"] == "sem_rastreio" and (d["d"] or "") >= "2026-01-01")
            reu = sum(1 for d in dados["deals"]
                      if d["r"] and (d["d"] or "") >= "2026-01-01")
            fec = sum(1 for d in dados["deals"]
                      if d["e"] in Q.ETAPAS_GANHAS and (d["d"] or "") >= "2026-01-01")
            print(f"{marca:9s} -> {out.name}  {n} deals ({n26} em 2026: "
                  f"{cm} CM, {sem} sem rastreio, {reu} reunioes, {fec} fechamentos)  "
                  f"{out.stat().st_size // 1024} KB")


if __name__ == "__main__":
    main()
