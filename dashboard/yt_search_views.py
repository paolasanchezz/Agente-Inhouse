"""
Busca resultados do YouTube para uma query e printa os videos ordenados por views.
Extrai o ytInitialData da pagina de resultados (sem API key).

Uso:
    python dashboard/yt_search_views.py "agente de ia whatsapp" pt BR
    python dashboard/yt_search_views.py "social listening" es MX
"""
import json
import re
import sys
import urllib.parse
import urllib.request

sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def fetch(query: str, hl: str, gl: str) -> str:
    url = "https://www.youtube.com/results?" + urllib.parse.urlencode(
        {"search_query": query, "hl": hl, "gl": gl}
    )
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36",
            "Accept-Language": f"{hl}-{gl},{hl};q=0.9",
            "Cookie": "CONSENT=YES+cb; SOCS=CAI",
        },
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8", errors="replace")


def extract_initial_data(html: str) -> dict:
    m = re.search(r"var ytInitialData = (\{.*?\});</script>", html, re.DOTALL)
    if not m:
        m = re.search(r'window\["ytInitialData"\] = (\{.*?\});', html, re.DOTALL)
    if not m:
        raise SystemExit("ytInitialData nao encontrado (consent wall?)")
    return json.loads(m.group(1))


def walk(obj, key):
    if isinstance(obj, dict):
        if key in obj:
            yield obj[key]
        for v in obj.values():
            yield from walk(v, key)
    elif isinstance(obj, list):
        for item in obj:
            yield from walk(item, key)


def parse_views(text: str) -> int:
    """'1,2 mi de visualizações' / '345 mil visualizações' / '12.345 vistas' / '1.2M views' -> int"""
    t = text.lower().replace("\xa0", " ")
    m = re.search(r"([\d.,]+)\s*(mi|m|mil|k|b)?", t)
    if not m:
        return 0
    num_s, suf = m.group(1), (m.group(2) or "")
    # normaliza decimal: '1,2' -> 1.2 ; '12.345' (milhar) -> 12345
    if suf in ("mi", "m", "k", "mil", "b"):
        num = float(num_s.replace(".", "").replace(",", ".")) if ("," in num_s) else float(num_s.replace(",", "."))
    else:
        num = float(num_s.replace(".", "").replace(",", ""))
    mult = {"mi": 1e6, "m": 1e6, "mil": 1e3, "k": 1e3, "b": 1e9}.get(suf, 1)
    return int(num * mult)


def text_of(node: dict) -> str:
    if not node:
        return ""
    if "simpleText" in node:
        return node["simpleText"]
    if "runs" in node:
        return "".join(r.get("text", "") for r in node["runs"])
    return ""


def main() -> None:
    query = sys.argv[1]
    hl = sys.argv[2] if len(sys.argv) > 2 else "pt"
    gl = sys.argv[3] if len(sys.argv) > 3 else "BR"

    html = fetch(query, hl, gl)
    data = extract_initial_data(html)

    vids = []
    for vr in walk(data, "videoRenderer"):
        vid = vr.get("videoId", "")
        title = text_of(vr.get("title", {}))
        views_txt = text_of(vr.get("viewCountText", {}))
        published = text_of(vr.get("publishedTimeText", {}))
        owner = text_of(vr.get("ownerText", {}))
        length = text_of(vr.get("lengthText", {}))
        views = parse_views(views_txt) if views_txt else 0
        vids.append((views, title, owner, published, length, f"https://youtu.be/{vid}"))

    vids.sort(key=lambda x: -x[0])
    print(f"### QUERY: {query} [{hl}-{gl}] — {len(vids)} videos")
    for views, title, owner, published, length, url in vids[:10]:
        print(f"{views:>10,} | {published:<14} | {length:>8} | {owner:<28} | {title[:95]} | {url}")


if __name__ == "__main__":
    main()
