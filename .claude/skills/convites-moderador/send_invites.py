#!/usr/bin/env python3
"""
Envia convite de moderador (role=presenter) para a próxima sessão de cada
série recorrente configurada em config.json, via API ClickMeeting v1.

Uso:
    python send_invites.py                # envia tudo
    python send_invites.py --dry-run      # só imprime o que enviaria
    python send_invites.py --series 17529 # filtra 1 série específica

Saída: log compacto no stdout + exit code 0 (tudo ok) / 1 (alguma falha).
"""

import argparse
import json
import os
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except (AttributeError, OSError):
    pass

CLICKMEETING_API_BASE = "https://api.clickmeeting.com/v1"
SCRIPT_DIR = Path(__file__).resolve().parent
CONFIG_PATH = SCRIPT_DIR / "config.json"


def load_env_var(name: str) -> str:
    if os.environ.get(name):
        return os.environ[name]
    repo_root = SCRIPT_DIR.parents[2]
    env_file = repo_root / ".env.local"
    if env_file.exists():
        for line in env_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line.startswith(f"{name}="):
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    raise SystemExit(f"[FATAL] {name} ausente em env e em {env_file}")


def http_json(url: str, api_key: str, method: str = "GET", form_body: dict | None = None) -> tuple[int, dict | list | None, str]:
    headers = {"X-Api-Key": api_key, "Accept": "application/json"}
    data = None
    if form_body is not None:
        data = urllib.parse.urlencode(form_body, doseq=True).encode("utf-8")
        headers["Content-Type"] = "application/x-www-form-urlencoded"
    req = urllib.request.Request(url, headers=headers, data=data, method=method)
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
            try:
                return resp.status, json.loads(raw), raw
            except json.JSONDecodeError:
                return resp.status, None, raw
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", errors="replace") if e.fp else ""
        try:
            return e.code, json.loads(raw), raw
        except json.JSONDecodeError:
            return e.code, None, raw


def next_session_for_series(active: list, recurring_config_id: str) -> dict | None:
    now = datetime.now(timezone.utc)
    eligible = []
    for c in active:
        if not c or not c.get("starts_at"):
            continue
        if str(c.get("recurring_config_id") or "") != str(recurring_config_id):
            continue
        if c.get("registration_enabled") not in (1, True):
            continue
        try:
            starts = datetime.fromisoformat(c["starts_at"])
        except ValueError:
            continue
        if starts <= now:
            continue
        eligible.append((starts, c))
    eligible.sort(key=lambda t: t[0])
    return eligible[0][1] if eligible else None


def send_invite(api_key: str, room_id: int, lang: str, email: str, dry_run: bool) -> tuple[bool, str]:
    if dry_run:
        return True, "[DRY-RUN] não enviado"
    url = f"{CLICKMEETING_API_BASE}/conferences/{room_id}/invitation/email/{lang}"
    body = {
        "attendees[0][email]": email,
        "template": "advanced",
        "role": "presenter",
    }
    status, parsed, raw = http_json(url, api_key, method="POST", form_body=body)
    if 200 <= status < 300 and isinstance(parsed, dict) and parsed.get("status") == "OK":
        return True, "enviado"
    snippet = (raw or "")[:200].replace("\n", " ")
    return False, f"HTTP {status} · {snippet}"


def main() -> int:
    p = argparse.ArgumentParser(description="Envia convite de moderador para próxima sessão de cada série ClickMeeting.")
    p.add_argument("--dry-run", action="store_true", help="Não envia — só imprime o plano.")
    p.add_argument("--series", help="Filtra 1 série específica (ex: 17529).")
    args = p.parse_args()

    if not CONFIG_PATH.exists():
        raise SystemExit(f"[FATAL] config.json não encontrado em {CONFIG_PATH}")
    config = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    series_cfg: dict = config.get("series", {})
    if args.series:
        if args.series not in series_cfg:
            raise SystemExit(f"[FATAL] série {args.series} não está em config.json")
        series_cfg = {args.series: series_cfg[args.series]}

    api_key = load_env_var("CLICKMEETING_API_KEY")

    print(f"=== Convites de moderador · {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===")
    print(f"Séries: {', '.join(series_cfg.keys())}{' · DRY-RUN' if args.dry_run else ''}\n")

    status, active, _ = http_json(f"{CLICKMEETING_API_BASE}/conferences/active", api_key)
    if status != 200 or not isinstance(active, list):
        print(f"[FATAL] /conferences/active retornou HTTP {status}")
        return 1

    overall_ok = True
    for rid, cfg in series_cfg.items():
        label = cfg.get("label", rid)
        email = cfg.get("moderator_email")
        lang = cfg.get("lang", "br")
        if not email:
            print(f"  [SKIP] {label} ({rid}) — sem moderator_email em config")
            overall_ok = False
            continue

        session = next_session_for_series(active, rid)
        if not session:
            print(f"  [SKIP] {label} ({rid}) — nenhuma sessão futura ativa")
            continue

        room_id = session["id"]
        starts_at = session["starts_at"]
        ok, msg = send_invite(api_key, room_id, lang, email, args.dry_run)
        flag = "OK " if ok else "ERR"
        print(f"  [{flag}] {label} ({rid}) → {email} · sessão #{room_id} ({starts_at}) · {msg}")
        if not ok:
            overall_ok = False

    print(f"\n{'✅ Todos os convites processados' if overall_ok else '⚠️  Houve falhas — ver acima'}")
    return 0 if overall_ok else 1


if __name__ == "__main__":
    sys.exit(main())
