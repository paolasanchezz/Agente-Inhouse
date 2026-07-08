"""Gera relatorio.md a partir de parsed.json — esqueleto mecânico do relatório.

Uso: python _gen_report.py <pasta-mes> [--marca Nome] [--handle conta] [--secundarias a,b]
Ex:  python _gen_report.py social-media/buzzmonitor/2026-05/analytics --marca Buzzmonitor --handle buzzmonitorbr --secundarias buzzcreatorsbr

Defaults (compatibilidade com uso antigo, pré multi-marca): marca Buzzmonitor,
handle buzzmonitorbr, secundárias buzzcreatorsbr. Handles/marca vêm de
brand/{marca}/social-media.json — a skill resolve e passa via CLI.
"""
from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path
from statistics import mean


def fmt_int(n):
    return f"{int(n):,}".replace(",", ".")


def safe_div(a, b):
    return a / b if b else 0


def rel_display(p: Path) -> Path:
    """Path relativo ao cwd pra exibição; cai pro absoluto se estiver fora dele."""
    try:
        return p.relative_to(Path.cwd())
    except ValueError:
        return p


def short(desc, n=70):
    if not desc:
        return "—"
    one = desc.replace("\n", " ").replace("\r", " ").strip()
    return one[:n] + ("…" if len(one) > n else "")


def main():
    ap = argparse.ArgumentParser(description="Gera relatorio.md a partir de parsed.json")
    ap.add_argument("pasta", help="pasta do mes (ex: social-media/buzzmonitor/2026-05/analytics)")
    ap.add_argument("--marca", default="Buzzmonitor", help="displayName da marca (pro titulo do relatorio)")
    ap.add_argument("--handle", default="buzzmonitorbr", help="username da conta propria no Instagram")
    ap.add_argument("--secundarias", default="buzzcreatorsbr",
                    help="CSV de handles de contas secundarias (cross-check); vazio pra nenhuma")
    args = ap.parse_args()

    base = Path(args.pasta)
    marca = args.marca
    handle = args.handle
    secundarias = [h.strip() for h in args.secundarias.split(",") if h.strip()]

    parsed = json.loads((base / "parsed.json").read_text(encoding="utf-8"))
    posts = parsed["posts"]
    aggregates = parsed.get("aggregates", {})
    audience = parsed.get("audience", {})

    buzz = [p for p in posts if p["username"] == handle]
    creators = [p for p in posts if p["username"] in secundarias]
    ugc = [p for p in posts if p["username"] != handle and p["username"] not in secundarias]

    if not buzz:
        print(f"Nenhum post de @{handle} encontrado.")
        return

    from datetime import datetime as _dt

    def parse_dt(s):
        # Meta exporta como "MM/DD/YYYY HH:MM" (US format)
        return _dt.strptime(s.strip(), "%m/%d/%Y %H:%M")

    def iso_date(s):
        return parse_dt(s).strftime("%Y-%m-%d")

    dates = sorted(iso_date(p["published_at"]) for p in buzz)
    first_date, last_date = dates[0], dates[-1]
    n_posts = len(buzz)

    weeks = {parse_dt(p["published_at"]).isocalendar()[1] for p in buzz}
    posts_per_week = n_posts / max(len(weeks), 1)
    cadence_status = "✅ saudável" if posts_per_week >= 3 else "⚠️ abaixo do mínimo (recomendado: 3/semana)"

    # por formato
    by_fmt = defaultdict(list)
    for p in buzz:
        by_fmt[p["type"]].append(p)
    fmt_stats = []
    for fmt, ps in by_fmt.items():
        fmt_stats.append({
            "fmt": fmt,
            "n": len(ps),
            "avg_views": mean(p["views"] for p in ps),
            "avg_reach": mean(p["reach"] for p in ps),
            "avg_eng": mean(p["engagement"] for p in ps),
            "avg_saves": mean(p["saves"] for p in ps),
        })
    fmt_stats.sort(key=lambda x: -x["avg_views"])

    # ranks
    def post_row(p):
        er = safe_div(p["engagement"], p["reach"]) * 100
        return {
            "date": iso_date(p["published_at"]),
            "type": p["type"].replace(" do Instagram", ""),
            "tema": short(p["description"], 60),
            "views": p["views"],
            "reach": p["reach"],
            "eng": p["engagement"],
            "er": er,
            "saves": p["saves"],
            "shares": p["shares"],
            "permalink": p["permalink"],
        }

    top_views = [post_row(p) for p in sorted(buzz, key=lambda x: -x["views"])[:3]]
    top_er = [post_row(p) for p in sorted(
        buzz, key=lambda x: -safe_div(x["engagement"], x["reach"])
    )[:3]]
    top_saves = [post_row(p) for p in sorted(buzz, key=lambda x: -x["saves"])[:3]]
    bottom_views = [post_row(p) for p in sorted(buzz, key=lambda x: x["views"])[:3]]

    # tendências agregadas (se houver)
    aggr_section = ""
    if aggregates:
        lines = ["## Tendências agregadas", ""]
        if "seguidores_novos" in aggregates:
            d = aggregates["seguidores_novos"]["data"]
            total = sum(x["value"] for x in d)
            avg = total / len(d) if d else 0
            lines.append(f"- **Novos seguidores no período**: {int(total)} ({avg:.1f}/dia em média)")
        if "alcance" in aggregates:
            d = aggregates["alcance"]["data"]
            vals = [x["value"] for x in d]
            if vals:
                pico_idx = vals.index(max(vals))
                lines.append(
                    f"- **Alcance**: pico de {fmt_int(max(vals))} em "
                    f"{d[pico_idx]['date']}; média diária {fmt_int(int(mean(vals)))}"
                )
        if "cliques_link" in aggregates:
            d = aggregates["cliques_link"]["data"]
            vals = [x["value"] for x in d]
            if len(vals) >= 14:
                ult7 = mean(vals[-7:])
                ant7 = mean(vals[-14:-7])
                trend = "subindo" if ult7 > ant7 * 1.05 else "caindo" if ult7 < ant7 * 0.95 else "estável"
                lines.append(
                    f"- **Cliques no link**: tendência {trend} "
                    f"(últimos 7d {ult7:.0f}/dia vs 7d anteriores {ant7:.0f}/dia)"
                )
        if "interacoes" in aggregates:
            d = aggregates["interacoes"]["data"]
            vals = [x["value"] for x in d]
            if vals:
                pico_idx = vals.index(max(vals))
                lines.append(
                    f"- **Interações**: dia de pico {d[pico_idx]['date']} "
                    f"({fmt_int(max(vals))}) — cruzar com posts publicados nessa data"
                )
        aggr_section = "\n".join(lines) + "\n\n"

    # audiência
    audience_section = ""
    if audience:
        lines = ["## Audiência (snapshot)", ""]
        cities = audience.get("Principais cidades", [])[:5]
        if cities:
            lines.append("**Top 5 cidades:**")
            for c in cities:
                lines.append(f"- {c['key']} — {c['value']}%")
            lines.append("")
        countries = next(
            (audience[k] for k in audience if "país" in k.lower() or "pa" in k.lower() and "ses" in k.lower()),
            [],
        )[:3]
        if countries:
            lines.append("**Top 3 países:**")
            for c in countries:
                lines.append(f"- {c['key']} — {c['value']}%")
            lines.append("")
        age_key = next((k for k in audience if "faixa" in k.lower() or "et" in k.lower()), None)
        if age_key:
            ages = audience[age_key]
            by_age = defaultdict(dict)
            for row in ages:
                by_age[row["key"]][row["subkey"]] = row["value"]
            lines.append("**Faixa etária:**")
            for age, vals in by_age.items():
                total = sum(vals.values())
                fem = vals.get("Mulheres", 0)
                lines.append(f"- {age}: {total:.1f}% (Mulheres {fem}% / Homens {vals.get('Homens', 0)}%)")
            lines.append("")
        audience_section = "\n".join(lines) + "\n"

    # contas secundárias (cross-check)
    creators_section = ""
    if creators:
        nomes_sec = ", ".join(f"@{h}" for h in secundarias)
        lines = [f"## Contas secundárias — {nomes_sec} (cross-check)", ""]
        lines.append(f"- {len(creators)} posts no período")
        lines.append(f"- Média de views: {mean(p['views'] for p in creators):.0f}")
        lines.append(f"- Média de reach: {mean(p['reach'] for p in creators):.0f}")
        lines.append(f"- Média de engajamento: {mean(p['engagement'] for p in creators):.1f}")
        creators_section = "\n".join(lines) + "\n\n"

    # UGC
    ugc_section = ""
    if ugc:
        lines = ["## UGC / parceiros marcando", ""]
        for p in sorted(ugc, key=lambda x: -x["views"])[:5]:
            lines.append(
                f"- **@{p['username']}** — {p['type'].replace(' do Instagram','')} "
                f"em {iso_date(p['published_at'])}: {fmt_int(p['views'])} views, "
                f"{p['likes']} likes, {p['comments']} comentários. {short(p['description'], 50)}"
            )
        lines.append("")
        ugc_section = "\n".join(lines) + "\n"

    # Tabela formato
    fmt_table_lines = [
        "| Formato | N | Avg views | Avg reach | Avg engagement | Avg saves |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for s in fmt_stats:
        fmt_table_lines.append(
            f"| {s['fmt'].replace(' do Instagram','')} | {s['n']} | "
            f"{int(s['avg_views'])} | {int(s['avg_reach'])} | "
            f"{int(s['avg_eng'])} | {s['avg_saves']:.1f} |"
        )

    def rank_table(rows, score_label, score_fn):
        lines = [
            f"| # | Data | Tipo | Tema | Views | Reach | {score_label} |",
            "|---|---|---|---|---:|---:|---:|",
        ]
        for i, r in enumerate(rows, 1):
            lines.append(
                f"| {i} | {r['date']} | {r['type']} | {r['tema']} | "
                f"{r['views']} | {r['reach']} | {score_fn(r)} |"
            )
        return "\n".join(lines)

    md = f"""# Relatório de Performance — Instagram {marca}

> **Período coberto**: {first_date} a {last_date} ({n_posts} posts da @{handle})
> **Gerado por**: `/social-analytics`
> **Fonte**: `{rel_display(base)}/raw/`

## TL;DR

- **Cadência**: {n_posts} posts em {len(weeks)} semana(s) — **{posts_per_week:.1f}/semana** ({cadence_status})
- **Formato vencedor**: {fmt_stats[0]['fmt'].replace(' do Instagram','')} (avg {int(fmt_stats[0]['avg_views'])} views) vs {fmt_stats[-1]['fmt'].replace(' do Instagram','')} ({int(fmt_stats[-1]['avg_views'])} views)
- **Top post**: {top_views[0]['date']} — {top_views[0]['tema']} ({fmt_int(top_views[0]['views'])} views, {top_views[0]['shares']} compartilhamentos)
- **Bottom post**: {bottom_views[0]['date']} — {bottom_views[0]['tema']} ({fmt_int(bottom_views[0]['views'])} views)
{('- **UGC**: ' + str(len(ugc)) + ' post(s) de terceiros marcando — sinal de alavanca não explorada') if ugc else ''}

## Cadência

- **Total**: {n_posts} posts
- **Semanas cobertas**: {len(weeks)}
- **Média**: {posts_per_week:.1f} posts/semana — {cadence_status}

## Top performers — por views (alcance)

{rank_table(top_views, "Engagement", lambda r: f"{r['eng']}")}

## Top performers — por engagement rate (qualidade)

{rank_table(top_er, "ER %", lambda r: f"{r['er']:.1f}%")}

## Top performers — por saves (referência futura)

{rank_table(top_saves, "Saves", lambda r: f"{r['saves']}")}

## Bottom performers

{rank_table(bottom_views, "Engagement", lambda r: f"{r['eng']}")}

## Performance por formato

{chr(10).join(fmt_table_lines)}

{aggr_section}{audience_section}{creators_section}{ugc_section}## Limitações

- Amostra pequena ({n_posts} posts) — achados são **hipóteses**, não conclusões. Acumular ≥3 meses pra padrões confiáveis.
- {"Agregados do período rolam 28d em vez de mês fechado — pico/tendência podem cruzar meses." if aggregates else "Sem dados agregados nesta análise — exportar Resultados (Insights > Resultados) pra completar."}
- Análise temática é qualitativa — dependendo das descriptions dos posts.
"""

    out = base / "relatorio.md"
    out.write_text(md, encoding="utf-8")
    print(f"OK -> {out}")


if __name__ == "__main__":
    main()
