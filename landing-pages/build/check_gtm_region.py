"""check_gtm_region.py — verifica se o GTM de cada LP bate com o container da
sua regiao, ANTES do deploy. Fecha o buraco do "traduz sem skill e esquece de
trocar o pixel" (incidente 2026-04-20, reaberto pelo caminho sem-skill).

Determinístico e stdlib-only, no estilo de build_umbrella.py / deploy_ci.py.

CONCEITO
--------
O tracking das LPs é via container do GTM, e o ID muda por marca+regiao
(brand/{marca}/tracking.json). Traduzir uma LP (BR -> PT, p.ex.) muda a regiao
mas costuma herdar o container da origem -> dados vão pra unidade errada.

Este script resolve a regiao pela cascata canônica (CONTEXT §5.1), lê o ID
esperado no tracking.json e compara com o(s) GTM presente(s) no index.html.

STAMP / GRANDFATHERING
----------------------
Cada LP pode ter um selo `.tracking.lock` (JSON) com o fingerprint do que
importa pra correção: regiao + GTM esperado + GTM(s) encontrado(s). Serve pra:
  1. Skip barato no nível da skill (agente não re-audita se nada relevante mudou).
  2. Grandfathering: uma LP já ERRADA hoje (ex.: as 3 -latam do Cxpress) recebe
     um selo `status: wrong` e NÃO bloqueia deploy enquanto seu fingerprint não
     mudar. No instante em que alguém mexe no GTM/regiao (fingerprint muda), ela
     é re-avaliada e passa a bloquear se ainda estiver errada.
Um `title` trocado não altera o fingerprint -> nunca re-bloqueia nem re-audita.

REGRA DE GATE (read-only nos selos em CI):
  OK                         -> passa.
  WRONG (container != regiao)-> bloqueia, EXCETO se houver selo grandfathered
                                com o mesmo fingerprint (aí só avisa).
  ABSENT (esperado mas sem GTM) -> só avisa (não bloqueia — LPs legadas).
  NO_EXPECTED (tracking null) mas tem GTM -> só avisa.
  NO_TRACKING (sem tracking.json)        -> passa (nada a checar).

USO
---
    py check_gtm_region.py <lp_dir | manifest.json>   # checa 1 LP ou 1 guarda-chuva
    py check_gtm_region.py --sweep [landing-pages]    # relatório de todas as LPs
    py check_gtm_region.py <lp_dir> --write-stamp      # grava selo OK (skills)
    py check_gtm_region.py <lp_dir> --grandfather      # aceita estado errado atual
    [--marca M]  força a marca (senão infere do path landing-pages/{marca}/{slug})
    [--json]     saída machine-readable

Exit 0 = nenhum bloqueio; 1 = ao menos um BLOQUEIO; 2 = erro de uso/interno.
"""
import hashlib
import json
import os
import re
import sys

MARCAS = ("buzzmonitor", "buzzcreators", "cxpress", "elife")
GTM_RE = re.compile(r"GTM-[A-Z0-9]+")
HTML_LANG_RE = re.compile(r"<html[^>]*\blang\s*=\s*[\"']([^\"']+)[\"']", re.I)
STAMP_NAME = ".tracking.lock"

# status
OK, WRONG, ABSENT, NO_EXPECTED, NO_TRACKING = (
    "ok", "wrong", "absent", "no_expected", "no_tracking")


def repo_root():
    return os.environ.get("REPO_ROOT") or os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", ".."))


def read_text(path):
    with open(path, "r", encoding="utf-8", newline="") as f:
        return f.read()


def resolve_region(slug, html):
    """Cascata canônica CONTEXT §5.1 — primeiro critério que resolver ganha."""
    s = (slug or "").lower()
    for suf, reg in (("-pt", "portugal"), ("-latam", "latam"),
                     ("-es", "latam"), ("-br", "brasil")):
        if s.endswith(suf):
            return reg, f"sufixo do slug '{suf}'"
    m = HTML_LANG_RE.search(html or "")
    if m:
        lang = m.group(1).lower()
        if lang.startswith("pt-pt"):
            return "portugal", f"<html lang='{m.group(1)}'>"
        if lang.startswith("es"):
            return "latam", f"<html lang='{m.group(1)}'>"
        if lang.startswith("pt-br"):
            return "brasil", f"<html lang='{m.group(1)}'>"
    return "brasil", "fallback"


def expected_gtm(repo, marca, regiao):
    """gtm.regions[{regiao}] || gtm.default || None. None se tracking.json ausente."""
    tj = os.path.join(repo, "brand", marca, "tracking.json")
    if not os.path.isfile(tj):
        return None, False  # (id, tracking_existe)
    gtm = (json.load(open(tj, encoding="utf-8")) or {}).get("gtm", {}) or {}
    return (gtm.get("regions", {}).get(regiao) or gtm.get("default") or None), True


def found_gtms(html):
    return sorted(set(GTM_RE.findall(html or "")))


def fingerprint(regiao, expected, found):
    h = hashlib.sha256()
    h.update("|".join([regiao, expected or "-", *found]).encode("utf-8"))
    return h.hexdigest()[:16]


def read_stamp(lp_dir):
    p = os.path.join(lp_dir, STAMP_NAME)
    if not os.path.isfile(p):
        return None
    try:
        return json.load(open(p, encoding="utf-8"))
    except (ValueError, OSError):
        return None


def evaluate(repo, lp_dir, slug=None, marca=None):
    """Avalia 1 LP. Retorna dict com status, regiao, esperado, encontrado, fingerprint."""
    slug = slug or os.path.basename(os.path.normpath(lp_dir))
    if marca is None:
        parts = os.path.normpath(lp_dir).replace("\\", "/").split("/")
        marca = next((p for p in parts if p in MARCAS), None)
    index = os.path.join(lp_dir, "index.html")
    if not os.path.isfile(index):
        return {"slug": slug, "marca": marca, "status": "no_html",
                "detail": f"sem index.html em {lp_dir}"}
    html = read_text(index)
    regiao, motivo = resolve_region(slug, html)
    expected, tracking_ok = (None, False)
    if marca in MARCAS:
        expected, tracking_ok = expected_gtm(repo, marca, regiao)
    found = found_gtms(html)

    if not tracking_ok:
        status = NO_TRACKING
    elif expected is None:
        status = NO_EXPECTED if found else OK
    elif not found:
        status = ABSENT
    elif expected in found and len(found) == 1:
        status = OK
    else:
        status = WRONG

    fp = fingerprint(regiao, expected, found)
    stamp = read_stamp(lp_dir)
    stamp_match = bool(stamp and stamp.get("fingerprint") == fp)
    return {
        "slug": slug, "marca": marca, "regiao": regiao, "regiao_motivo": motivo,
        "expected": expected, "found": found, "status": status,
        "fingerprint": fp, "lp_dir": lp_dir,
        # stamp_match: nada relevante mudou desde a última verificação (skill pula).
        # grandfathered: estado errado pré-existente aceito (CI não bloqueia).
        "stamp_match": stamp_match,
        "grandfathered": bool(stamp_match and stamp and stamp.get("grandfathered")),
    }


def is_blocking(res):
    """Só WRONG bloqueia — e apenas se não estiver grandfathered pelo selo."""
    return res.get("status") == WRONG and not res.get("grandfathered")


def human(res):
    st = res["status"]
    base = f"{res['marca']}/{res['slug']} [{res.get('regiao','?')}]"
    if st == WRONG:
        gf = "" if is_blocking(res) else " (grandfathered - nao bloqueia)"
        rot = "BLOQUEIO" if is_blocking(res) else "aviso"
        return (f"{rot} {base}: GTM errado - encontrado {res['found']}, "
                f"esperado {res['expected']} (regiao por {res['regiao_motivo']}){gf}")
    if st == ABSENT:
        return f"aviso {base}: GTM ausente, esperado {res['expected']}"
    if st == NO_EXPECTED:
        return f"aviso {base}: tem GTM {res['found']} mas tracking.json sem ID pra regiao"
    if st == "no_html":
        return f"aviso {res.get('slug')}: {res.get('detail')}"
    return f"ok {base}: GTM {res['expected']}"


def write_stamp(res, grandfather=False):
    from datetime import date
    stamp = {
        "regiao": res["regiao"], "expected_gtm": res["expected"],
        "found_gtm": res["found"], "fingerprint": res["fingerprint"],
        "status": res["status"], "grandfathered": grandfather,
        "verified_at": date.today().isoformat(),
    }
    if grandfather:
        stamp["note"] = ("estado pre-existente aceito — GTM diverge da regiao, "
                         "aguardando correção; não bloqueia deploy até o "
                         "fingerprint mudar")
    with open(os.path.join(res["lp_dir"], STAMP_NAME), "w",
              encoding="utf-8", newline="\n") as f:
        json.dump(stamp, f, ensure_ascii=False, indent=2)
        f.write("\n")


def lps_from_manifest(repo, manifest_path):
    man = json.load(open(manifest_path, encoding="utf-8"))
    out = []
    for lp in man["lps"]:
        out.append((os.path.join(repo, lp["source"]), lp["slug"], lp["marca"]))
    return out


def sweep_lps(repo, root=None):
    root = root or os.path.join(repo, "landing-pages")
    out = []
    for marca in MARCAS:
        base = os.path.join(root, marca)
        if not os.path.isdir(base):
            continue
        for slug in sorted(os.listdir(base)):
            lp_dir = os.path.join(base, slug)
            if os.path.isfile(os.path.join(lp_dir, "index.html")):
                out.append((lp_dir, slug, marca))
    return out


def gate(results):
    """(bloqueios[], avisos[], ok_count) — pronto pra deploy_ci / pr_check."""
    bloqueios, avisos, ok = [], [], 0
    for r in results:
        if is_blocking(r):
            bloqueios.append(human(r))
        elif r["status"] in (WRONG, ABSENT, NO_EXPECTED, "no_html"):
            avisos.append(human(r))
        else:
            ok += 1
    return bloqueios, avisos, ok


def main():
    args = sys.argv[1:]
    marca = None
    if "--marca" in args:
        i = args.index("--marca")
        marca = args[i + 1]
        del args[i:i + 2]
    write = "--write-stamp" in args
    grandfather = "--grandfather" in args
    as_json = "--json" in args
    sweep = "--sweep" in args
    positional = [a for a in args if not a.startswith("--")]
    repo = repo_root()

    if sweep:
        targets = sweep_lps(repo, positional[0] if positional else None)
    elif positional and positional[0].endswith("manifest.json"):
        targets = lps_from_manifest(repo, positional[0])
    elif positional:
        lp_dir = positional[0]
        targets = [(lp_dir, None, marca)]
    else:
        sys.stderr.write("uso: check_gtm_region.py <lp_dir|manifest.json|--sweep>\n")
        sys.exit(2)

    results = [evaluate(repo, d, s, m) for (d, s, m) in targets]

    for r in results:
        if r["status"] == "no_html":
            continue
        if grandfather and r["status"] == WRONG:
            write_stamp(r, grandfather=True)
            r["stamp_match"], r["grandfathered"] = True, True
        elif write and r["status"] == OK:
            write_stamp(r, grandfather=False)
            r["stamp_match"] = True

    bloqueios, avisos, ok = gate(results)

    if as_json:
        print(json.dumps({"bloqueios": bloqueios, "avisos": avisos,
                          "ok": ok, "resultados": results},
                         ensure_ascii=False, indent=2))
    else:
        for b in bloqueios:
            print(b)
        for a in avisos:
            print(a)
        print(f"-- {ok} OK, {len(avisos)} aviso(s), {len(bloqueios)} bloqueio(s)")

    sys.exit(1 if bloqueios else 0)


if __name__ == "__main__":
    main()
