"""Normaliza CSVs exportados do Meta Business Suite (Instagram Insights).

Lida com encoding UTF-16 LE dos agregados, multi-line cells dos posts, e gera
um JSON único consolidado pronto pra skill consumir.

Uso:
    python parse_csvs.py <pasta-raw> [pasta-saida]

Default de saida: pasta pai da raw (ex: raw em `analytics/raw/` gera `analytics/parsed.json`).
"""
from __future__ import annotations

import csv
import io
import json
import sys
from pathlib import Path


def read_text(path: Path) -> str:
    raw = path.read_bytes()
    if raw[:2] == b"\xff\xfe":
        return raw.decode("utf-16-le").lstrip("﻿")
    if raw[:2] == b"\xfe\xff":
        return raw.decode("utf-16-be").lstrip("﻿")
    if raw[:3] == b"\xef\xbb\xbf":
        return raw[3:].decode("utf-8")
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError:
        return raw.decode("utf-16-le", errors="replace")


def parse_aggregate(path: Path) -> dict | None:
    text = read_text(path)
    lines = [l for l in text.splitlines() if l.strip()]
    if not lines:
        return None
    i = 0
    if lines[i].strip().lower().startswith("sep="):
        i += 1
    metric = lines[i].strip().strip('"') if i < len(lines) else path.stem
    i += 1
    if i < len(lines) and "Data" in lines[i]:
        i += 1
    data = []
    for line in lines[i:]:
        parts = [p.strip().strip('"') for p in line.split(",")]
        if len(parts) < 2:
            continue
        date = parts[0].split("T")[0]
        try:
            value = float(parts[1])
        except ValueError:
            continue
        data.append({"date": date, "value": value})
    return {"metric": metric, "data": data}


def parse_publico(path: Path) -> dict:
    text = read_text(path)
    lines = [l for l in text.splitlines() if l.strip() and not l.strip().lower().startswith("sep=")]
    rows = [
        [p.strip() for p in next(csv.reader(io.StringIO(line)), [])]
        for line in lines
    ]
    sections: dict[str, list] = {}
    i = 0
    while i < len(rows):
        row = rows[i]
        if len(row) == 1:
            section = row[0]
            sections[section] = []
            i += 1
            if i >= len(rows):
                break
            header = rows[i]
            if all(_is_float(c) or c == "" for c in header):
                # No header — single keys/values row?
                i += 1
                continue
            i += 1
            # Read rows until next single-col section header
            while i < len(rows) and len(rows[i]) > 1:
                data_row = rows[i]
                if all(_is_float(c) or c == "" for c in data_row):
                    # Paired with header (cities / countries pattern)
                    for k, v in zip(header, data_row):
                        if v == "" or k == "":
                            continue
                        try:
                            sections[section].append({"key": k, "value": float(v)})
                        except ValueError:
                            pass
                else:
                    # Matrix pattern (age/gender): first col = row label, rest paired with header cols
                    label = data_row[0]
                    for col_name, val in zip(header[1:], data_row[1:]):
                        if val == "":
                            continue
                        try:
                            sections[section].append({
                                "key": label,
                                "subkey": col_name,
                                "value": float(val),
                            })
                        except ValueError:
                            pass
                i += 1
        else:
            i += 1
    return sections


def _is_float(s: str) -> bool:
    try:
        float(s)
        return True
    except ValueError:
        return False


def _to_int(row: dict, key: str) -> int:
    try:
        return int(row.get(key) or 0)
    except ValueError:
        return 0


def _to_float(row: dict, key: str) -> float:
    try:
        return float(row.get(key) or 0)
    except ValueError:
        return 0.0


def parse_posts(path: Path) -> list[dict]:
    """Posts CSV uses standard csv module (multi-line quoted cells)."""
    text = read_text(path)
    reader = csv.DictReader(io.StringIO(text))
    posts = []
    for row in reader:
        views = _to_int(row, "Visualizações")
        reach = _to_int(row, "Alcance")
        likes = _to_int(row, "Curtidas")
        shares = _to_int(row, "Compartilhamentos")
        comments = _to_int(row, "Comentários")
        saves = _to_int(row, "Salvamentos")
        follows = _to_int(row, "Seguimentos")
        duration = _to_float(row, "Duração (s)")
        posts.append({
            "post_id": row.get("Identificação do post"),
            "account_id": row.get("Identificação da conta"),
            "username": row.get("Nome de usuário da conta"),
            "account_name": row.get("Nome da conta"),
            "description": row.get("Descrição"),
            "duration_s": duration,
            "published_at": row.get("Horário de publicação"),
            "permalink": row.get("Link permanente"),
            "type": row.get("Tipo de post"),
            "views": views,
            "reach": reach,
            "likes": likes,
            "shares": shares,
            "follows_from_post": follows,
            "comments": comments,
            "saves": saves,
            "engagement": likes + shares + comments + saves,
        })
    return posts


AGGREGATE_NAMES = {
    "alcance": "alcance",
    "seguidores": "seguidores_novos",
    "visitas": "visitas_perfil",
    "cliques": "cliques_link",
    "interacoes": "interacoes",
    "visualizacoes": "visualizacoes",
}


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    raw_dir = Path(sys.argv[1])
    out_dir = Path(sys.argv[2]) if len(sys.argv) > 2 else raw_dir.parent
    out_dir.mkdir(parents=True, exist_ok=True)

    result: dict = {
        "source_dir": str(raw_dir),
        "posts": [],
        "aggregates": {},
        "audience": {},
        "files_found": [],
        "files_skipped": [],
    }

    for csv_path in sorted(raw_dir.glob("*.csv")):
        name = csv_path.stem.lower()
        result["files_found"].append(csv_path.name)
        try:
            if "post" in name or name.startswith("may-") or name.startswith("jun-") \
                    or name.startswith("apr-") or name.startswith("jul-"):
                result["posts"].extend(parse_posts(csv_path))
            elif "publico" in name or "público" in name:
                result["audience"] = parse_publico(csv_path)
            elif name in AGGREGATE_NAMES:
                parsed = parse_aggregate(csv_path)
                if parsed:
                    result["aggregates"][AGGREGATE_NAMES[name]] = parsed
            else:
                parsed = parse_aggregate(csv_path)
                if parsed and parsed["data"]:
                    result["aggregates"][name] = parsed
                else:
                    result["files_skipped"].append(csv_path.name)
        except Exception as exc:
            result["files_skipped"].append(f"{csv_path.name} (erro: {exc})")

    out_path = out_dir / "parsed.json"
    out_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"OK -> {out_path}")
    print(f"Posts: {len(result['posts'])}")
    print(f"Aggregates: {list(result['aggregates'].keys())}")
    print(f"Audience sections: {list(result['audience'].keys())}")
    if result["files_skipped"]:
        print(f"Skipped: {result['files_skipped']}")


if __name__ == "__main__":
    main()
