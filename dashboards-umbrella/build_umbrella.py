"""build_umbrella.py — monta a pasta de deploy do guarda-chuva de dashboards.

Uso:
    py dashboards-umbrella/build_umbrella.py <dist_dir> [--dry-run]

Le `dashboards-umbrella/manifest.json`, copia cada dashboard-fonte pra sua
subpasta (`dist/<slug>/`), injeta a barra de navegacao compartilhada e gera o
hub, o middleware de Basic Auth, o vercel.json, o robots.txt e o package.json.

Deterministico e stdlib-only. Mesmo papel do landing-pages/build/build_umbrella.py,
so que pras dashboards internas.

A credencial do Basic Auth vem de DASHBOARD_BASIC_AUTH_USER/_PASS (env ou
.env.local na raiz do repo) e so e escrita na dist — nunca no repo.

Exit 0 = OK; exit 1 = erro de validacao (mensagem no stderr).
"""
import json
import os
import re
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
MANIFEST = os.path.join(HERE, "manifest.json")
TPL = os.path.join(HERE, "templates")

HEAD_CLOSE = re.compile(r"</head>", re.I)
NAV_TAG = '<script defer src="/nav.js"></script>'

MIDDLEWARE = """// Edge Middleware — Basic Auth do guarda-chuva de dashboards internas.
// GERADO por dashboards-umbrella/build_umbrella.py. Nao editar a mao.
// Um unico login cobre TODAS as dashboards (era o motivo de unificar).

export const config = {
  matcher: '/((?!_next/static|_next/image|favicon.ico|robots.txt).*)',
};

const USER = '__USER__';
const PASS = '__PASS__';
const REALM = 'Dashboards internas - Grupo Elife';

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
      'WWW-Authenticate': 'Basic realm="' + REALM + '"',
      'Content-Type': 'text/plain; charset=utf-8',
      'Cache-Control': 'no-store',
    },
  });
}
"""

VERCEL_JSON = {
    "$schema": "https://openapi.vercel.sh/vercel.json",
    "cleanUrls": False,
    # true de proposito: as dashboards carregam motor.js/estilo.css/dados-*.json
    # por caminho RELATIVO. Sem a barra final, /buzz-br resolveria /motor.js e a
    # pagina subiria quebrada. O 308 acontece antes de renderizar.
    "trailingSlash": True,
    "headers": [
        {
            "source": "/(.*)",
            "headers": [
                {"key": "X-Frame-Options", "value": "DENY"},
                {"key": "X-Content-Type-Options", "value": "nosniff"},
                {"key": "Referrer-Policy", "value": "no-referrer"},
                {"key": "Permissions-Policy", "value": "geolocation=(), microphone=(), camera=()"},
                {"key": "Strict-Transport-Security", "value": "max-age=31536000; includeSubDomains"},
                {"key": "X-Robots-Tag", "value": "noindex, nofollow, noarchive, nosnippet"},
            ],
        }
    ],
}

ROBOTS = "# Dashboards internas — fora de buscadores.\nUser-agent: *\nDisallow: /\n"


def die(msg):
    sys.stderr.write("ERRO build_umbrella: %s\n" % msg)
    sys.exit(1)


def warn(msg):
    sys.stderr.write("AVISO build_umbrella: %s\n" % msg)


def read_text(path):
    with open(path, "r", encoding="utf-8", newline="") as f:
        return f.read()


def write_text(path, content):
    d = os.path.dirname(path)
    if d:
        os.makedirs(d, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(content)


def credenciais():
    user = os.environ.get("DASHBOARD_BASIC_AUTH_USER")
    pw = os.environ.get("DASHBOARD_BASIC_AUTH_PASS")
    env_local = os.path.join(REPO, ".env.local")
    if (not user or not pw) and os.path.exists(env_local):
        for line in read_text(env_local).splitlines():
            if line.startswith("DASHBOARD_BASIC_AUTH_USER=") and not user:
                user = line.split("=", 1)[1].strip()
            elif line.startswith("DASHBOARD_BASIC_AUTH_PASS=") and not pw:
                pw = line.split("=", 1)[1].strip()
    if not user or not pw:
        die("DASHBOARD_BASIC_AUTH_USER/_PASS ausentes (env ou .env.local).")
    if "'" in user or "'" in pw:
        die("credencial com aspa simples quebraria o middleware — troque a senha.")
    return user, pw


def injetar_nav(html, slug):
    """Insere a barra compartilhada antes de </head>. Idempotente."""
    if "/nav.js" in html:
        return html
    if not HEAD_CLOSE.search(html):
        die("%s: index.html sem </head> — nao da pra injetar a barra." % slug)
    return HEAD_CLOSE.sub(NAV_TAG + "\n</head>", html, count=1)


def esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;").replace('"', "&quot;"))


def hex_soft(cor):
    """Versao 10% do accent, pro badge da marca. Aceita #RRGGBB."""
    c = cor.lstrip("#")
    r, g, b = int(c[0:2], 16), int(c[2:4], 16), int(c[4:6], 16)
    return "rgba(%d,%d,%d,.10)" % (r, g, b)


def data_br(iso):
    if not iso or len(iso) < 10:
        return "—"
    return "%s/%s/%s" % (iso[8:10], iso[5:7], iso[0:4])


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    dry = "--dry-run" in sys.argv
    if len(args) != 1:
        die("uso: py build_umbrella.py <dist_dir> [--dry-run]")
    dist = os.path.abspath(args[0])

    repo_abs = os.path.abspath(REPO)
    if dist == repo_abs or dist.startswith(repo_abs + os.sep):
        die("dist dentro do repo (%s). A dist e a sibling FORA do repo." % dist)

    man = json.loads(read_text(MANIFEST))
    dashboards = man["dashboards"]
    if not dashboards:
        die("manifesto sem dashboards.")

    user, pw = credenciais()

    # ---- validacao + coleta ----
    plano = []
    for d in dashboards:
        slug, fonte = d["slug"], d["fonte"]
        src = os.path.join(REPO, fonte)
        if not os.path.isdir(src):
            die("%s: fonte inexistente: %s" % (slug, fonte))
        if "index.html" not in d["arquivos"]:
            die("%s: 'arquivos' precisa listar index.html." % slug)

        faltando = [f for f in d["arquivos"] if not os.path.exists(os.path.join(src, f))]
        reuso = False
        if faltando:
            # Unica falta tolerada: o JSON de dados, se a dist ja tiver um (evita
            # apagar os dados de uma dashboard ao deployar outra). Nunca silencioso.
            if faltando == [d["dados"]] and os.path.exists(os.path.join(dist, slug, d["dados"])):
                reuso = True
                warn("%s: %s ausente na fonte — REUSANDO o que ja esta na dist "
                     "(pode estar velho; rode exportar_dados.py)." % (slug, d["dados"]))
            else:
                die("%s: arquivos ausentes em %s: %s" % (slug, fonte, ", ".join(faltando)))

        gerado = "—"
        jpath = os.path.join(dist, slug, d["dados"]) if reuso else os.path.join(src, d["dados"])
        try:
            gerado = json.loads(read_text(jpath)).get("gerado_em", "—")
        except Exception:
            warn("%s: nao consegui ler gerado_em de %s." % (slug, d["dados"]))

        plano.append({"d": d, "src": src, "gerado": gerado, "reuso": reuso})

    if dry:
        print("DRY-RUN — dist: %s" % dist)
        for p in plano:
            print("  /%-14s <- %-32s dados de %s%s"
                  % (p["d"]["slug"] + "/", p["d"]["fonte"], p["gerado"],
                     "  (REUSADO)" if p["reuso"] else ""))
        print("  /%-14s <- hub gerado (%d cards)" % ("", len(plano)))
        print("  nav.js, middleware.js, vercel.json, robots.txt, package.json")
        return

    # ---- copia das dashboards ----
    os.makedirs(dist, exist_ok=True)
    for p in plano:
        d, src = p["d"], p["src"]
        alvo = os.path.join(dist, d["slug"])
        os.makedirs(alvo, exist_ok=True)
        for f in d["arquivos"]:
            if p["reuso"] and f == d["dados"]:
                continue
            shutil.copy2(os.path.join(src, f), os.path.join(alvo, f))
        idx = os.path.join(alvo, "index.html")
        write_text(idx, injetar_nav(read_text(idx), d["slug"]))
        # Sobra de build antigo (arquivo que saiu do manifesto) nao fica servida.
        for f in os.listdir(alvo):
            if f not in d["arquivos"]:
                os.remove(os.path.join(alvo, f))

    # ---- nav.js ----
    nav_data = [{"slug": d["slug"], "nome": d["nome"], "curto": d["curto"]} for d in dashboards]
    nav = read_text(os.path.join(TPL, "nav.js.tpl")).replace(
        "__DASHBOARDS_JSON__", json.dumps(nav_data, ensure_ascii=False))
    write_text(os.path.join(dist, "nav.js"), nav)

    # ---- hub ----
    cards = []
    for p in plano:
        d = p["d"]
        badges = "".join('<span class="badge">%s</span>' % esc(b)
                         for b in (d["regiao"], d["moeda"], d["idioma"]))
        cards.append(
            '    <a class="card" href="/%s/" style="--accent:%s;--accent-soft:%s">\n'
            '      <h2>%s</h2>\n'
            '      <p class="resumo">%s</p>\n'
            '      <div class="badges"><span class="badge brand">%s</span>%s</div>\n'
            '      <div class="foot"><span>Atualizada em %s</span>'
            '<span class="seta">Abrir &rarr;</span></div>\n'
            '    </a>'
            % (d["slug"], d["cor"], hex_soft(d["cor"]), esc(d["nome"]), esc(d["resumo"]),
               esc(d["marca"].capitalize()), badges, data_br(p["gerado"])))
    hub = (read_text(os.path.join(TPL, "hub.html.tpl"))
           .replace("__CARDS__", "\n".join(cards))
           .replace("__TITULO__", esc(man["titulo"]))
           .replace("__ORG__", esc(man["org"])))
    write_text(os.path.join(dist, "index.html"), hub)

    # ---- infra ----
    write_text(os.path.join(dist, "middleware.js"),
               MIDDLEWARE.replace("__USER__", user).replace("__PASS__", pw))
    write_text(os.path.join(dist, "vercel.json"),
               json.dumps(VERCEL_JSON, indent=2, ensure_ascii=False) + "\n")
    write_text(os.path.join(dist, "robots.txt"), ROBOTS)
    write_text(os.path.join(dist, "package.json"), json.dumps({
        "name": man["projeto"],
        "version": "1.0.0",
        "private": True,
        "description": "Guarda-chuva das dashboards internas de Content Marketing (Basic Auth)",
    }, indent=2) + "\n")
    write_text(os.path.join(dist, ".gitignore"), ".vercel\n")

    print("BUILD OK -> %s" % dist)
    for p in plano:
        print("  /%-14s dados de %s%s" % (p["d"]["slug"] + "/", p["gerado"],
                                          "  (REUSADO)" if p["reuso"] else ""))


if __name__ == "__main__":
    main()
