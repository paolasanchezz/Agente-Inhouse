"""Envia email de alerta quando ha falhas/warnings no health check.

Le do ambiente:
  RESEND_API_KEY    — API key da conta Resend (obrigatorio)
  HEALTH_EMAIL_FROM — remetente (default: 'Health Check <onboarding@resend.dev>')
  HEALTH_EMAIL_TO   — destinatario (default: 'victor.lopes@buzzmonitor.com.br')

Le do stdin um JSON unico no formato:
  {
    "summary": {"total": N, "ok": N, "warning": N, "fail": N},
    "results": [...],   # output do check.py
    "drift": [...],     # opcional — items de drift detectados pela skill
    "report_path": "landing-pages/health-checks/INCIDENT-YYYY-MM-DD-HHMM.md"
  }

Saida em stdout:
  "ok: email enviado para X (id: re_...)" em sucesso
  "erro: ..." em falha (exit code 1)

NAO envia email se nao houver falhas E nao houver warnings/drift relevantes —
a skill ja filtra isso antes de chamar este script, mas defensivamente
re-checamos aqui.
"""

import json
import os
import sys
import urllib.request
import urllib.error

# Fonte de verdade do que conta como drift acionavel vive em drift.py (mesmo dir).
try:
    from drift import ACTIONABLE_KINDS
except ImportError:
    ACTIONABLE_KINDS = ("fonte_sem_deploy", "deploy_orfao")


def build_subject(payload):
    s = payload.get("summary", {})
    fails = s.get("fail", 0)
    warns = s.get("warning", 0)
    drift_n = sum(1 for d in (payload.get("drift") or []) if d.get("kind") in ACTIONABLE_KINDS)
    parts = []
    if fails:
        parts.append(f"{fails} fora do ar")
    if warns:
        parts.append(f"{warns} aviso")
    if drift_n:
        parts.append(f"{drift_n} drift")
    detail = ", ".join(parts) if parts else "incidente"
    return f"[Health Check LPs] {detail}"


def build_text_body(payload):
    """Email em texto puro com tabela ASCII simples — mais robusto que HTML."""
    lines = []
    s = payload.get("summary", {})
    lines.append(f"Health check executado: {s.get('total', 0)} URLs verificadas")
    lines.append(
        f"  OK: {s.get('ok', 0)}  |  Warning: {s.get('warning', 0)}  |  Falha: {s.get('fail', 0)}"
    )
    lines.append("")

    fails = [r for r in payload.get("results", []) if r.get("verdict") == "fail"]
    if fails:
        lines.append("=== FALHAS ===")
        for r in fails:
            status = r.get("status_code")
            status_txt = str(status) if status is not None else "—"
            lines.append(f"  [{status_txt}] {r['url']}")
            if r.get("diagnostic"):
                lines.append(f"        {r['diagnostic']}")
        lines.append("")

    warnings = [r for r in payload.get("results", []) if r.get("verdict") == "warning"]
    if warnings:
        lines.append("=== AVISOS ===")
        for r in warnings:
            status = r.get("status_code")
            status_txt = str(status) if status is not None else "—"
            lines.append(f"  [{status_txt}] {r['url']}  ({r.get('diagnostic', '')})")
        lines.append("")

    drift = payload.get("drift") or []
    actionable = [d for d in drift if d.get("kind") in ACTIONABLE_KINDS]
    informative = [d for d in drift if d.get("kind") not in ACTIONABLE_KINDS]
    if actionable:
        lines.append("=== DRIFT (source vs deploy) ===")
        for d in actionable:
            lines.append(f"  {d.get('kind', '?')}: {d.get('item', '?')}  - {d.get('note', '')}")
        lines.append("")
    if informative:
        lines.append("=== INFORMATIVO (nao acionavel, sem alerta) ===")
        for d in informative:
            lines.append(f"  {d.get('kind', '?')}: {d.get('item', '?')}  - {d.get('note', '')}")
        lines.append("")

    report = payload.get("report_path")
    if report:
        lines.append(f"Relatorio completo: {report}")
        lines.append("Inspecione o arquivo no repo para diagnostico detalhado.")

    return "\n".join(lines)


def send_via_resend(api_key, from_addr, to_addr, subject, body_text):
    """POST https://api.resend.com/emails. Retorna (ok: bool, info: str)."""
    payload = {
        "from": from_addr,
        "to": [to_addr],
        "subject": subject,
        "text": body_text,
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        "https://api.resend.com/emails",
        data=data,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            # Resend fica atras de Cloudflare, que bloqueia UA "Python-urllib/3.x"
            # com erro 1010. Identificar como cliente legitimo.
            "User-Agent": "lp-health-check/1.0",
            "Accept": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            resp = json.loads(r.read())
            return True, resp.get("id", "sem-id")
    except urllib.error.HTTPError as e:
        try:
            err_body = e.read().decode("utf-8", errors="replace")
        except Exception:
            err_body = ""
        return False, f"HTTP {e.code}: {err_body[:300]}"
    except Exception as e:
        return False, f"erro: {e}"


def main():
    api_key = os.environ.get("RESEND_API_KEY")
    if not api_key:
        print("erro: RESEND_API_KEY nao definido no ambiente", file=sys.stderr)
        sys.exit(1)

    from_addr = os.environ.get("HEALTH_EMAIL_FROM") or "Health Check <onboarding@resend.dev>"
    to_addr = os.environ.get("HEALTH_EMAIL_TO") or "victor.lopes@buzzmonitor.com.br"

    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError as e:
        print(f"erro: stdin nao e JSON valido — {e}", file=sys.stderr)
        sys.exit(1)

    # Defensive: nao enviar se 0 falhas + 0 warnings + 0 drift ACIONAVEL.
    # vercel_app_only (informativo) nao dispara email sozinho.
    s = payload.get("summary", {})
    actionable_drift = [d for d in (payload.get("drift") or []) if d.get("kind") in ACTIONABLE_KINDS]
    if s.get("fail", 0) == 0 and s.get("warning", 0) == 0 and not actionable_drift:
        print("ok: nada para notificar (tudo verde)")
        return

    subject = build_subject(payload)
    body = build_text_body(payload)
    ok, info = send_via_resend(api_key, from_addr, to_addr, subject, body)

    if ok:
        print(f"ok: email enviado para {to_addr} (id: {info})")
    else:
        print(f"erro: falha ao enviar email — {info}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
