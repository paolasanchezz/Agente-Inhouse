"""HTTP health check em paralelo das URLs descobertas por discover.py.

Entrada: JSON via stdin no formato:
  {"urls": [{"project": "...", "domain": "...", "slug": "...", "mode": "...", "url": "..."}, ...]}

Saida: imprime JSON em stdout com:
  {
    "results": [
      {"url": "...",
       "project": "...",
       "status_code": 200,
       "elapsed_ms": 234,
       "verdict": "ok" | "warning" | "fail",
       "diagnostic": "..."  # explicacao curta quando nao-ok
      }
    ],
    "summary": {"total": N, "ok": N, "warning": N, "fail": N}
  }

Classificacao:
  ok      : 200-299
  warning : 3xx final apos follow, 4xx que NAO seja 404 (raro mas pode acontecer)
  fail    : 404 final, 5xx persistente (apos 1 retry), timeout, erro de DNS/cert

Implementa retry 1x em 5xx com backoff 2s antes de marcar como fail.
HEAD method com fallback pra GET (alguns CDNs retornam 405 em HEAD).
"""

import json
import sys
import time
import urllib.request
import urllib.error
import ssl
import socket
from concurrent.futures import ThreadPoolExecutor, as_completed


TIMEOUT_SEC = 10
MAX_WORKERS = 5


def http_check(url):
    """Retorna (status_code|None, elapsed_ms, diagnostic).

    diagnostic e string vazia em sucesso, ou descricao curta do erro.
    status_code = None significa erro de conexao (DNS, cert, timeout).
    """
    start = time.monotonic()
    try:
        # tentar HEAD primeiro
        req = urllib.request.Request(url, method="HEAD", headers={
            "User-Agent": "lp-health-check/1.0 (curl-equivalent)"
        })
        try:
            with urllib.request.urlopen(req, timeout=TIMEOUT_SEC) as r:
                elapsed = int((time.monotonic() - start) * 1000)
                return r.status, elapsed, ""
        except urllib.error.HTTPError as e:
            # 405 Method Not Allowed → tentar GET
            if e.code == 405:
                req = urllib.request.Request(url, method="GET", headers={
                    "User-Agent": "lp-health-check/1.0"
                })
                with urllib.request.urlopen(req, timeout=TIMEOUT_SEC) as r:
                    elapsed = int((time.monotonic() - start) * 1000)
                    return r.status, elapsed, ""
            elapsed = int((time.monotonic() - start) * 1000)
            return e.code, elapsed, ""
    except urllib.error.URLError as e:
        elapsed = int((time.monotonic() - start) * 1000)
        reason = str(e.reason)
        if isinstance(e.reason, socket.timeout):
            return None, elapsed, "timeout"
        if isinstance(e.reason, socket.gaierror):
            return None, elapsed, f"DNS falhou: {reason}"
        if isinstance(e.reason, ssl.SSLError):
            return None, elapsed, f"cert/SSL: {reason}"
        return None, elapsed, f"erro de conexao: {reason}"
    except Exception as e:
        elapsed = int((time.monotonic() - start) * 1000)
        return None, elapsed, f"erro inesperado: {e}"


def check_with_retry(item):
    """Faz check e retry 1x em 5xx. Retorna dict completo."""
    url = item["url"]
    status, elapsed, diag = http_check(url)

    # Retry 1x em 5xx ou erro de conexao temporario
    if (status is not None and 500 <= status < 600) or (
        status is None and diag.startswith("timeout")
    ):
        time.sleep(2)
        status_retry, elapsed_retry, diag_retry = http_check(url)
        status, elapsed, diag = status_retry, elapsed_retry, diag_retry

    # Classificar verdict
    if status is None:
        verdict = "fail"
        if not diag:
            diag = "sem resposta"
    elif 200 <= status < 300:
        verdict = "ok"
    elif 300 <= status < 400:
        # redirect final (apos urllib seguir todos os redirects, isso e raro)
        verdict = "warning"
        diag = f"redirect HTTP {status} nao seguido"
    elif status == 404:
        verdict = "fail"
        diag = "404 Not Found"
    elif 400 <= status < 500:
        verdict = "warning"
        diag = f"HTTP {status}"
    elif 500 <= status < 600:
        verdict = "fail"
        diag = f"HTTP {status} persistente (apos retry)"
    else:
        verdict = "warning"
        diag = f"HTTP {status} inesperado"

    return {
        "url": url,
        "project": item.get("project", ""),
        "domain": item.get("domain", ""),
        "slug": item.get("slug", ""),
        "mode": item.get("mode", ""),
        "status_code": status,
        "elapsed_ms": elapsed,
        "verdict": verdict,
        "diagnostic": diag,
    }


def main():
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError as e:
        print(json.dumps({"results": [], "summary": {}, "error": f"stdin nao e JSON valido: {e}"}))
        sys.exit(1)

    urls = payload.get("urls", [])
    if not urls:
        print(json.dumps({"results": [], "summary": {"total": 0, "ok": 0, "warning": 0, "fail": 0}}))
        return

    results = []
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as exe:
        futures = {exe.submit(check_with_retry, item): item for item in urls}
        for fut in as_completed(futures):
            results.append(fut.result())

    # ordenar por url pra output deterministico
    results.sort(key=lambda r: r["url"])

    summary = {
        "total": len(results),
        "ok": sum(1 for r in results if r["verdict"] == "ok"),
        "warning": sum(1 for r in results if r["verdict"] == "warning"),
        "fail": sum(1 for r in results if r["verdict"] == "fail"),
    }

    print(json.dumps({"results": results, "summary": summary}, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
