"""server.py — dashboard **Content Marketing Cxpress Brasil** dinâmica (LOCAL).

Date-picker livre + presets (7d/15d/30d/90d/MtD/YtD), consulta o Supabase ao vivo.
Roda só localmente (o Vercel não conecta no Supabase com o user looker_readonly — mesmo
motivo da dashboard-pessoal e da dashboard-latam). Reaproveita o render do dashboard estático
(gerar_relatorio_cxpress): o servidor monta o HTML do período escolhido e o seletor troca via
fetch (iframe srcdoc).

Uso:
    uv run --python 3.12 --with "psycopg[binary]" python dashboard-cxpress/server.py
    # abre http://127.0.0.1:8020
"""
from __future__ import annotations

import os
import sys
import time
import threading
import traceback
from datetime import date, timedelta
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

ROOT = Path(__file__).resolve().parent
DASH = ROOT.parent / "dashboard"
sys.path.insert(0, str(DASH))

import psycopg
from gerar_relatorio_cxpress import load_url, colher, render_html  # reuso do render estático


# ============ PERÍODOS (range-based) ============

def calcular_periodos_range(ini: date, fim: date, periodo_nome: str = 'Período') -> dict:
    if fim < ini:
        raise ValueError(f"fim ({fim}) deve ser >= ini ({ini})")
    dias = (fim - ini).days + 1
    return {
        'hoje': date.today(),
        'ini_atual': ini, 'fim_atual': fim,
        'ini_ant': ini - timedelta(days=dias), 'fim_ant': ini - timedelta(days=1),
        'mtd_ini': date(fim.year, fim.month, 1), 'mtd_fim': fim,
        'ytd_ini': date(fim.year, 1, 1), 'ytd_fim': fim,
        'dias_periodo': dias,
        # render_html usa 'semanas_decorridas_ytd' como divisor da média
        'semanas_decorridas_ytd': max(1, ((fim - date(fim.year, 1, 1)).days + 1) // dias),
        'periodo_nome': periodo_nome,
    }


_PRESET_LABEL = {'7d': '7 dias', '15d': '15 dias', '30d': '30 dias',
                 '90d': '90 dias', 'mtd': 'MtD', 'ytd': 'YtD'}


def preset_periodo(preset: str, ate: date | None = None) -> tuple[date, date]:
    fim = ate or date.today()
    if preset == '7d':  return fim - timedelta(days=6), fim
    if preset == '15d': return fim - timedelta(days=14), fim
    if preset == '30d': return fim - timedelta(days=29), fim
    if preset == '90d': return fim - timedelta(days=89), fim
    if preset == 'mtd': return date(fim.year, fim.month, 1), fim
    if preset == 'ytd': return date(fim.year, 1, 1), fim
    raise ValueError(f"preset inválido: {preset}")


def resolver(params: dict) -> tuple[date, date, str]:
    if params.get('preset'):
        p = params['preset']
        ini, fim = preset_periodo(p)
        return ini, fim, _PRESET_LABEL.get(p, 'Período')
    ini, fim = params.get('ini'), params.get('fim')
    if ini and fim:
        return date.fromisoformat(ini), date.fromisoformat(fim), 'Período'
    ini, fim = preset_periodo('ytd')
    return ini, fim, 'YtD'


# ============ RENDER + CACHE ============

_CACHE: dict = {}
_LOCK = threading.Lock()


def render_periodo(ini: date, fim: date, nome: str, refresh: bool = False) -> tuple[str, bool]:
    key = (ini.isoformat(), fim.isoformat())
    if not refresh:
        with _LOCK:
            if key in _CACHE:
                return _CACHE[key], True
    per = calcular_periodos_range(ini, fim, nome)
    url = load_url()
    with psycopg.connect(url, autocommit=True) as conn, conn.cursor() as cur:
        cur.execute("SET statement_timeout = '120s'")
        d = colher(cur, per)
    html = render_html(d)
    with _LOCK:
        _CACHE[key] = html
    return html, False


# ============ SHELL (seletor + iframe) ============

SHELL = """<!DOCTYPE html><html lang="pt-BR"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Content Marketing Cxpress · dinâmico</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap" rel="stylesheet">
<style>
  :root{--blue:#0B63FF;--blue-d:#073FA3;--ink:#1F2937;--dim:#6B7280;--line:#E5E7EB;--bg:#F8FAFC}
  *{margin:0;padding:0;box-sizing:border-box}
  html,body{height:100%}
  body{font-family:'Inter',sans-serif;background:var(--bg);color:var(--ink);display:flex;flex-direction:column}
  .bar{background:#fff;border-bottom:1px solid var(--line);padding:12px 20px;display:flex;align-items:center;gap:16px;flex-wrap:wrap;box-shadow:0 1px 3px rgba(15,23,42,.05);z-index:5}
  .brand{font-weight:800;font-size:14px;color:var(--blue);letter-spacing:.02em;white-space:nowrap}
  .brand small{display:block;font-weight:600;color:var(--dim);font-size:11px;text-transform:uppercase;letter-spacing:.04em}
  .pgroup{display:flex;gap:6px;flex-wrap:wrap}
  .pbtn{border:1px solid var(--line);background:#fff;color:var(--ink);font:600 13px Inter,sans-serif;padding:7px 13px;border-radius:8px;cursor:pointer;transition:.15s}
  .pbtn:hover{border-color:var(--blue);color:var(--blue)}
  .pbtn.active{background:var(--blue);color:#fff;border-color:var(--blue)}
  .range{display:flex;align-items:center;gap:6px;font-size:13px;color:var(--dim)}
  .range input{border:1px solid var(--line);border-radius:8px;padding:6px 8px;font:600 13px Inter,sans-serif;color:var(--ink)}
  .apply{background:var(--blue-d);color:#fff;border:none;border-radius:8px;padding:7px 14px;font:700 13px Inter,sans-serif;cursor:pointer}
  .apply:hover{background:#052e7a}
  .refresh{background:#fff;border:1px solid var(--line);border-radius:8px;padding:7px 11px;cursor:pointer;font-size:14px}
  .status{margin-left:auto;font-size:12px;color:var(--dim);display:flex;align-items:center;gap:10px;white-space:nowrap}
  .pill{background:#EAF1FF;color:var(--blue-d);font-weight:700;padding:3px 10px;border-radius:999px}
  .pill.live{background:#FEF3C7;color:#92400E}
  #frame{flex:1;border:none;width:100%;background:var(--bg)}
  .loading{position:fixed;inset:53px 0 0 0;display:none;align-items:center;justify-content:center;background:rgba(248,250,252,.85);font-weight:700;color:var(--blue);z-index:4}
  .loading.on{display:flex}
</style></head><body>
  <div class="bar">
    <div class="brand">Cxpress Brasil<small>Content Marketing · dinâmico</small></div>
    <div class="pgroup" id="presets">
      <button class="pbtn" data-preset="7d">7d</button>
      <button class="pbtn" data-preset="15d">15d</button>
      <button class="pbtn" data-preset="30d">30d</button>
      <button class="pbtn" data-preset="90d">90d</button>
      <button class="pbtn" data-preset="mtd">MtD</button>
      <button class="pbtn active" data-preset="ytd">YtD</button>
    </div>
    <div class="range">
      <span>De</span><input type="date" id="ini">
      <span>Até</span><input type="date" id="fim">
      <button class="apply" id="apply">Aplicar</button>
    </div>
    <button class="refresh" id="refresh" title="Recarregar do banco (ignora cache)">&#x21bb;</button>
    <div class="status"><span id="rango">—</span><span class="pill" id="pill">—</span></div>
  </div>
  <div class="loading" id="loading">Carregando…</div>
  <iframe id="frame" title="dashboard"></iframe>
<script>
  const frame=document.getElementById('frame'), loading=document.getElementById('loading');
  const pill=document.getElementById('pill'), rango=document.getElementById('rango');
  let current='preset=ytd';
  function setActivePreset(p){ document.querySelectorAll('#presets .pbtn').forEach(b=>b.classList.toggle('active', b.dataset.preset===p)); }
  async function load(qs, refresh){
    loading.classList.add('on');
    try{
      const url='/render?'+qs+(refresh?'&refresh=1':'');
      const r=await fetch(url);
      const html=await r.text();
      if(!r.ok){ frame.srcdoc='<pre style=\"padding:24px;font:13px monospace;color:#b91c1c\">'+html.replace(/</g,'&lt;')+'</pre>'; return; }
      frame.srcdoc=html;
      current=qs;
      rango.textContent=r.headers.get('X-Periodo')||'';
      const cached=r.headers.get('X-Cache')==='HIT';
      pill.textContent=cached?'cache':'ao vivo'; pill.className='pill'+(cached?'':' live');
    }catch(e){ frame.srcdoc='<div style=\"font-family:Inter,system-ui,sans-serif;padding:40px;color:#b91c1c\"><h2 style=\"margin:0 0 8px\">Não foi possível carregar</h2><p style=\"color:#374151\">O servidor local não respondeu. Confira se ele está rodando numa janela do terminal:</p><pre style=\"background:#f8fafc;border:1px solid #e5e7eb;padding:12px;border-radius:8px;color:#1f2937;white-space:pre-wrap\">uv run --python 3.12 --with \"psycopg[binary]\" python dashboard-cxpress/server.py</pre><p style=\"color:#6b7280;font-size:13px\">Detalhe técnico: '+e+'</p></div>'; }
    finally{ loading.classList.remove('on'); }
  }
  document.querySelectorAll('#presets .pbtn').forEach(b=>b.addEventListener('click',()=>{
    setActivePreset(b.dataset.preset); load('preset='+b.dataset.preset);
  }));
  document.getElementById('apply').addEventListener('click',()=>{
    const i=document.getElementById('ini').value, f=document.getElementById('fim').value;
    if(!i||!f){ alert('Escolha as duas datas.'); return; }
    if(i>f){ alert('«De» tem que ser <= «Até».'); return; }
    setActivePreset(null); load('ini='+i+'&fim='+f);
  });
  document.getElementById('refresh').addEventListener('click',()=>load(current,true));
  const today=new Date().toISOString().slice(0,10);
  document.getElementById('fim').value=today;
  document.getElementById('ini').value=today.slice(0,4)+'-01-01';
  load('preset=ytd');
</script>
</body></html>"""


# ============ HTTP ============

class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        print(f"[{time.strftime('%H:%M:%S')}] {self.command} {self.path}")

    def _send(self, status, body, mime, extra=None):
        if isinstance(body, str):
            body = body.encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', mime)
        self.send_header('Content-Length', str(len(body)))
        self.send_header('Cache-Control', 'no-store')
        for k, v in (extra or {}).items():
            self.send_header(k, v)
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path in ('/', '/index.html'):
            self._send(200, SHELL, 'text/html; charset=utf-8')
            return
        if parsed.path == '/render':
            self._render(parse_qs(parsed.query))
            return
        self._send(404, 'Not found', 'text/plain')

    def _render(self, q):
        try:
            params = {k: v[0] if v else '' for k, v in q.items()}
            ini, fim, nome = resolver(params)
            refresh = params.get('refresh') == '1'
            t0 = time.time()
            html, cached = render_periodo(ini, fim, nome, refresh=refresh)
            print(f"  |{'CACHE' if cached else 'FRESH'} {nome} {ini}..{fim} -> {time.time()-t0:.2f}s")
            self._send(200, html, 'text/html; charset=utf-8', {
                'X-Cache': 'HIT' if cached else 'MISS',
                'X-Periodo': f'{nome}: {ini.isoformat()} a {fim.isoformat()}',
            })
        except Exception as e:
            traceback.print_exc()
            self._send(500, f'{type(e).__name__}: {e}', 'text/plain; charset=utf-8')


class _Server(ThreadingHTTPServer):
    # Windows + SO_REUSEADDR deixa DOIS servidores bindarem a mesma porta, com o trafego
    # indo pro processo antigo (incidente 2026-06-09: edicoes "nao apareciam" porque o server
    # velho do atalho seguia respondendo). False => segunda instancia falha com erro claro.
    allow_reuse_address = False


def main():
    port = int(os.environ.get('PORT', 8020))
    try:
        srv = _Server(('127.0.0.1', port), Handler)
    except OSError:
        print(f"\n  ERRO: a porta {port} ja esta em uso — ha outra janela do servidor aberta.")
        print("  Feche a janela antiga ('Dashboard CXPRESS LOCAL - feche para parar') e tente de novo.\n")
        raise SystemExit(1)
    srv.daemon_threads = True
    print(f"\n  Dashboard Content Marketing Cxpress (dinâmico, local) → http://127.0.0.1:{port}")
    print("  Presets + date-picker · consulta o Supabase ao vivo · Ctrl+C pra parar.\n", flush=True)
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print("\n  Tchau.")


if __name__ == '__main__':
    main()
