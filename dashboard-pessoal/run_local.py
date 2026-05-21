"""run_local.py — servidor local que simula a Vercel.

Serve `public/` como static + invoca api/dashboard.py em /api/dashboard.
Sem precisar de Vercel CLI.

Uso:
    uv run --python 3.12 --with "psycopg[binary]" python dashboard-pessoal/run_local.py
    # abre http://localhost:8000
"""
from __future__ import annotations

import io
import json
import os
import sys
import time
import traceback
from datetime import date
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

# Forca UTF-8 no stdout pra logs com acentos/setas no Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))


def _load_env():
    env_path = ROOT / ".env"
    if not env_path.exists():
        print(f"AVISO: {env_path} nao existe. Variaveis ja no os.environ serao usadas.")
        return
    for raw in env_path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        if k.strip() not in os.environ:
            os.environ[k.strip()] = v.strip().strip('"').strip("'")


_load_env()

# Import após carregar .env
from api.dashboard import _resolve_periodo, coletar_cached


PUBLIC_DIR = ROOT / "public"

MIME = {
    '.html': 'text/html; charset=utf-8',
    '.js':   'application/javascript; charset=utf-8',
    '.css':  'text/css; charset=utf-8',
    '.json': 'application/json; charset=utf-8',
    '.svg':  'image/svg+xml',
    '.png':  'image/png',
    '.ico':  'image/x-icon',
}


class LocalHandler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        # log mais curto que default
        print(f"[{time.strftime('%H:%M:%S')}] {self.command} {self.path} -> {args[1] if len(args)>1 else ''}")

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path == '/api/dashboard':
            self._handle_api(parsed.query)
            return

        # Static
        if path == '/' or path == '':
            path = '/index.html'

        fp = (PUBLIC_DIR / path.lstrip('/')).resolve()
        if not str(fp).startswith(str(PUBLIC_DIR)) or not fp.is_file():
            self._send(404, b'Not found', 'text/plain')
            return

        body = fp.read_bytes()
        mime = MIME.get(fp.suffix.lower(), 'application/octet-stream')
        self._send(200, body, mime)

    def _handle_api(self, qs: str):
        try:
            from datetime import datetime as _dt
            params = {k: v[0] if v else '' for k, v in parse_qs(qs).items()}
            ini, fim = _resolve_periodo(params)
            historico = params.get('historico', '1') != '0'
            refresh = params.get('refresh') == '1'

            t0 = time.time()
            data, was_cached, cached_at_ts = coletar_cached(ini, fim, historico=historico, refresh=refresh)
            tag = 'CACHE' if was_cached else 'FRESH'
            print(f"  |{tag} {ini}..{fim} hist={historico} -> {time.time()-t0:.2f}s")

            data['_meta'] = {
                'cached': was_cached,
                'cached_at': _dt.fromtimestamp(cached_at_ts).isoformat(timespec='seconds'),
            }
            body = json.dumps(data, ensure_ascii=False, default=str).encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Content-Length', str(len(body)))
            self.send_header('Cache-Control', 'no-store')
            self.send_header('X-Cache', 'HIT' if was_cached else 'MISS')
            self.end_headers()
            self.wfile.write(body)
        except Exception as e:
            traceback.print_exc()
            err = {'error': str(e), 'type': type(e).__name__}
            body = json.dumps(err).encode('utf-8')
            self._send(500, body, 'application/json; charset=utf-8')

    def _send(self, status: int, body: bytes, mime: str):
        self.send_response(status)
        self.send_header('Content-Type', mime)
        self.send_header('Content-Length', str(len(body)))
        self.send_header('Cache-Control', 'no-store')
        self.end_headers()
        self.wfile.write(body)


def main():
    port = int(os.environ.get('PORT', 8000))
    # Bind em 127.0.0.1 explicito + ThreadingHTTPServer (uma thread por request — evita
    # bloqueio de requests subsequentes quando uma conexao trava)
    server = ThreadingHTTPServer(('127.0.0.1', port), LocalHandler)
    server.daemon_threads = True
    print(f"\n  Dashboard CM (local) rodando em http://127.0.0.1:{port}", flush=True)
    print(f"  Press Ctrl+C pra parar.\n", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n  Tchau.", flush=True)


if __name__ == '__main__':
    main()
