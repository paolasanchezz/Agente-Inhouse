"""sync_sibling.py — Cxpress: sincroniza a sibling de deploy com o codigo desta pasta.

> APOSENTADO em 2026-09-09: as dashboards viraram um guarda-chuva unico
> (`dashboards-elife`). Quem monta a pasta de deploy agora e
> `dashboards-umbrella/build_umbrella.py`, chamado pela skill `/dashboard-atualizar` (v4).
> Este script so serve pra recovery do modelo antigo de sibling por projeto.

Copia os 5 estaticos (index.html, estilo.css, motor.js, render.js, dados-cxpress.json) para a
sibling fora do repo e (re)gera middleware.js (Basic Auth com a MESMA credencial do Buzz BR —
lida do middleware dele, sem digitar a senha), vercel.json e robots.txt identicos ao Buzz BR.

NAO deploya. Rode antes de `vercel deploy`. Passo do runbook em dashboard/DEPLOY-cxpress.md.

Uso:
    uv run --python 3.12 --with "psycopg[binary]" python dashboard-cxpress-vercel/exportar_dados.py
    uv run --python 3.12 python dashboard-cxpress-vercel/sync_sibling.py
"""
import re
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
CLAUDE = HERE.parent.parent               # .../Claude
BUZZ_SIB = CLAUDE / "dashboard-buzzmonitor-brasil"
SIBLING = CLAUDE / "dashboard-cxpress-brasil"
DADOS = "dados-cxpress.json"
MARCA = "Cxpress Brasil"
REALM = "Cxpress Dashboard Brasil"

MW = """// Edge Middleware — Basic Auth para a dashboard CM __MARCA__.
// Credencial identica a do Buzzmonitor Brasil (mesma senha forte).

export const config = {
  matcher: '/((?!_next/static|_next/image|favicon.ico|robots.txt).*)',
};

const USER = '__USER__';
const PASS = '__PASS__';
const REALM = '__REALM__';

export default function middleware(req) {
  const auth = req.headers.get('authorization');
  if (auth) {
    const [scheme, encoded] = auth.split(' ');
    if (scheme === 'Basic' && encoded) {
      try {
        const decoded = atob(encoded);
        const idx = decoded.indexOf(':');
        const user = decoded.slice(0, idx);
        const pass = decoded.slice(idx + 1);
        if (user === USER && pass === PASS) {
          return; // autorizado — segue pro asset
        }
      } catch {
        // fall through ao 401
      }
    }
  }
  return new Response('Authentication required', {
    status: 401,
    headers: {
      'WWW-Authenticate': `Basic realm="${REALM}"`,
      'Content-Type': 'text/plain; charset=utf-8',
      'Cache-Control': 'no-store',
    },
  });
}
"""


def main() -> None:
    if not (HERE / DADOS).exists():
        raise SystemExit(f"ERRO: {DADOS} nao existe — rode exportar_dados.py primeiro.")
    mw_buzz = (BUZZ_SIB / "middleware.js").read_text(encoding="utf-8")
    user = re.search(r"const USER = '([^']*)'", mw_buzz).group(1)
    pw = re.search(r"const PASS = '([^']*)'", mw_buzz).group(1)

    SIBLING.mkdir(exist_ok=True)
    for f in ("index.html", "estilo.css", "motor.js", "render.js", DADOS):
        shutil.copy2(HERE / f, SIBLING / f)
    mw = MW.replace("__MARCA__", MARCA).replace("__USER__", user).replace("__PASS__", pw).replace("__REALM__", REALM)
    (SIBLING / "middleware.js").write_text(mw, encoding="utf-8")
    shutil.copy2(BUZZ_SIB / "vercel.json", SIBLING / "vercel.json")
    shutil.copy2(BUZZ_SIB / "robots.txt", SIBLING / "robots.txt")

    m = (SIBLING / "middleware.js").read_text(encoding="utf-8")
    assert "inhouse@77" not in m and pw in m, "credencial nao aplicada corretamente"
    print(f"[{MARCA}] sibling sincronizada -> {SIBLING}")
    print(f"  auth: USER={user!r} · senha forte (== Buzz BR) · REALM={REALM!r}")
    print("  Proximo: vercel deploy --prod --yes --scope team_nC991VqUuSU2jXZN152xqqEg --cwd", str(SIBLING))


if __name__ == "__main__":
    main()
