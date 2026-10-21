#!/usr/bin/env python3
"""validar_contrato.py — camada de contrato das dashboards CM do guarda-chuva.

Por que existe
--------------
O painel de cada dashboard compara strings e le campos pelo nome, sem validar nada. Um campo
renomeado no exportador (`d_lead` -> `data_lead`) faz `_inRange(undefined, ...)` devolver false:
todos os KPIs viram 0 e a dashboard renderiza bonita e inteiramente zerada, sem erro nenhum.
Chave de topo ausente tambem e muda em pelo menos um lugar (`dashboard-pt-vercel/motor.js` faz
`new Set(DADOS.ganhas || [])` -> fechamento 0 em silencio). Este script e a rede que pega isso
ANTES do deploy, para que uma atualizacao noturna desassistida nunca suba numero errado.

O contrato de cada dashboard (`contratos/<contrato>.json`) declara o que o painel LE. Campo que
o painel parou de ler sai do contrato e o exportador pode larga-lo — o contrato congela o
acoplamento, nao o export.

Uso
---
    py dashboards-umbrella/validar_contrato.py [slug ...]          # valida (default: os 7)
        --raiz fonte|dist|url      onde ler os JSONs (default: fonte = pasta-fonte no repo)
        --dist DIR                 obrigatorio com --raiz dist
        --base-url URL             obrigatorio com --raiz url (Basic Auth do ambiente/.env.local)
        --baseline-url URL         catraca compara com o JSON que esta NO AR (modo do CI e da skill).
                                   So run verde deploya, entao producao = ultimo estado verde, sem
                                   precisar persistir baseline (o que obrigaria o CI a commitar na
                                   main toda noite)
        --baseline FILE            catraca compara com um arquivo (testes e inspecao local)
        --sem-catraca              so contrato, sem comparar com baseline nenhum
        --sem-frescor              nao exige gerado_em recente (inspecao manual de JSON antigo)
        --atualizar-baseline       grava as metricas de hoje no --baseline FILE (so se tudo passou)
        --aceitar-catraca SLUG     aceita uma queda legitima daquele slug ('tudo' = todos) nesta
                                   rodada. Exige --motivo. Nunca aceita violacao de contrato. Com
                                   --baseline-url, deixar a rodada deployar ja re-ancora: a noite
                                   seguinte compara contra o numero novo
        --motivo TEXTO             registrado na saida (e no arquivo, no modo --baseline FILE)
        --apenas-sync              nao le JSON: so confere exportador x contrato x painel
        --sugerir SLUG             imprime um rascunho de contrato inferido do JSON atual
        --json                     saida estruturada

Codigos de saida (o pior entre todos os slugs vence)
----------------------------------------------------
    0  ok (avisos permitidos)
    1  uso / IO / JSON ilegivel / contrato ausente
    2  violacao de contrato
    3  violacao de catraca — o UNICO que --aceitar-catraca destrava
    4  schema_version dessincronizado (exportador x contrato x painel x JSON)

Stdlib pura, sem rede (exceto --raiz url). Nunca imprime valor de campo de registro — so id,
nome de campo e tipo de violacao —, porque os JSONs tem PII de leads.
"""
from __future__ import annotations

import argparse
import base64
import json
import math
import os
import re
import sys
import urllib.request
from collections import Counter, defaultdict
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
UMB = REPO / "dashboards-umbrella"
MANIFEST = UMB / "manifest.json"
CONTRATOS = UMB / "contratos"
BASELINE = CONTRATOS / "baseline.json"
BRT = timezone(timedelta(hours=-3))
RE_DATA = re.compile(r"^\d{4}-\d{2}-\d{2}$")
RE_VER_EXPORTADOR = re.compile(r"^SCHEMA_VERSION\s*=\s*(\d+)", re.M)
RE_VER_PAINEL = re.compile(r"const\s+SCHEMA_ESPERADO\s*=\s*(\d+)")

OK, IO, CONTRATO, CATRACA, VERSAO = 0, 1, 2, 3, 4
# Precedencia do codigo final: IO > versao > contrato > catraca. A catraca e o menos grave de
# proposito — e o unico que um humano pode aceitar, entao nunca pode mascarar os outros.
GRAVIDADE = {OK: 0, CATRACA: 1, CONTRATO: 2, VERSAO: 3, IO: 4}
CATRACA_PADRAO = {"queda_pct": 2, "queda_abs": 5, "alta_aviso_pct": 25, "alta_fatal_pct": 100,
                  "alta_abs": 10}
MAX_EXEMPLOS = 3

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass


# ---------------------------------------------------------------- relatorio

class Relatorio:
    """Acumula achados de um slug. Codigo = o pior visto."""

    def __init__(self, slug: str, contrato: str):
        self.slug, self.contrato = slug, contrato
        self.fatais: list[tuple[int, str]] = []
        self.avisos: list[str] = []
        self.metricas: dict[str, int | None] = {}
        self.catraca: list[dict] = []
        self.codigo = OK
        self.aceito = False

    def fatal(self, msg: str, codigo: int = CONTRATO) -> None:
        self.fatais.append((codigo, msg))
        if GRAVIDADE[codigo] > GRAVIDADE[self.codigo]:
            self.codigo = codigo

    def aviso(self, msg: str) -> None:
        self.avisos.append(msg)


def pior(codigos) -> int:
    return max(codigos, key=lambda c: GRAVIDADE[c], default=OK)


# ---------------------------------------------------------------- tipos

def tipo_ok(v, tipo: str) -> bool:
    if tipo == "data":
        return isinstance(v, str) and bool(RE_DATA.match(v))
    if tipo == "int":
        return isinstance(v, int) and not isinstance(v, bool)
    if tipo == "num":
        return isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(v)
    if tipo == "str":
        return isinstance(v, str)
    if tipo == "bool":
        return isinstance(v, bool)
    if tipo == "objeto":
        return isinstance(v, dict)
    if tipo in ("lista", "pares"):
        return isinstance(v, list)
    return True


def nome_tipo(v) -> str:
    if v is None:
        return "null"
    if isinstance(v, bool):
        return "bool"
    if isinstance(v, str) and RE_DATA.match(v):
        return "data"
    return {int: "int", float: "num", str: "str", dict: "objeto", list: "lista"}.get(type(v), type(v).__name__)


def violacoes(v, spec: dict) -> list[str]:
    """Violacoes de um valor PRESENTE contra a spec. Nao devolve o valor (pode ser PII)."""
    if v is None:
        return [] if spec.get("nulo", False) else ["nulo nao permitido"]
    t = spec.get("tipo")
    if t and not tipo_ok(v, t):
        return [f"tipo {nome_tipo(v)}, esperava {t}"]
    out = []
    if "valor" in spec and v != spec["valor"]:
        out.append("valor fora do fixado")
    if "valores" in spec and v not in spec["valores"]:
        out.append("valor fora do dominio")
    return out


# ---------------------------------------------------------------- caminhos

def resolver(D, caminho: str):
    """'escopo.ini' -> D['escopo']['ini']. None se qualquer passo faltar."""
    cur = D
    for parte in caminho.split("."):
        if not isinstance(cur, dict) or parte not in cur:
            return None
        cur = cur[parte]
    return cur


RE_CAMINHO_LISTA = re.compile(r"^(\w+)\[\](?:\.(\w+)|\[(\d+)\])?$")


def valores_lista(D, caminho: str) -> set:
    """'deals[].e' | 'etapas[][0]' | 'ganhas[]' -> conjunto de valores."""
    m = RE_CAMINHO_LISTA.match(caminho)
    if not m:
        raise ValueError(f"caminho invalido: {caminho!r}")
    base = D.get(m.group(1))
    if not isinstance(base, list):
        return set()
    if m.group(2):
        return {r.get(m.group(2)) for r in base if isinstance(r, dict)}
    if m.group(3) is not None:
        i = int(m.group(3))
        return {r[i] for r in base if isinstance(r, list) and len(r) > i}
    return {x for x in base if not isinstance(x, (list, dict))}


def ref_valor(D, valor):
    """'@escopo.ini' / '@ganhas' referenciam o proprio JSON; o resto e literal."""
    if isinstance(valor, str) and valor.startswith("@"):
        return resolver(D, valor[1:])
    return valor


# ---------------------------------------------------------------- validacao estrutural

def checar_registros(lista: list, nome_lista: str, reg: dict, rel: Relatorio) -> None:
    campos: dict = reg.get("campos", {})
    obrigatorios = {c for c, s in campos.items() if s.get("obrigatorio", True)}
    faltando: Counter = Counter()
    extras: Counter = Counter()
    viol: dict[tuple, list] = defaultdict(list)       # (campo, violacao) -> ids de exemplo
    n = len(lista)
    nao_dict = 0

    for r in lista:
        if not isinstance(r, dict):
            nao_dict += 1
            continue
        rid = r.get("id", "?")
        for c in obrigatorios:
            if c not in r:
                faltando[c] += 1
        for k in r:
            if k not in campos:
                extras[k] += 1
        for c, spec in campos.items():
            if c in r:
                for v in violacoes(r[c], spec):
                    viol[(c, v)].append(rid)

    if nao_dict:
        rel.fatal(f"{nome_lista}: {nao_dict}/{n} itens nao sao objeto")
    for c, qtd in sorted(faltando.items()):
        cons = campos[c].get("consumidor")
        msg = f"{nome_lista}: campo obrigatorio '{c}' ausente em {qtd}/{n} registros"
        if cons:
            msg += f" — lido em {cons}"
        # Faltou em todos E sobrou outra chave em todos: quase sempre e rename no exportador.
        suspeitos = [k for k, q in extras.items() if q == qtd]
        if suspeitos:
            msg += f"\n        >>> provavel RENAME '{c}' -> {', '.join(repr(s) for s in suspeitos)}"
        rel.fatal(msg)
    for (c, v), ids in sorted(viol.items()):
        ex = ", ".join(str(i) for i in ids[:MAX_EXEMPLOS])
        rel.fatal(f"{nome_lista}.{c}: {v} em {len(ids)}/{n} registros (ex. id {ex})")
    modo_extra = reg.get("chaves_extras", "avisar")
    for k, qtd in sorted(extras.items()):
        if modo_extra == "avisar" and not any(qtd == q for q in faltando.values()):
            rel.aviso(f"{nome_lista}: chave nao declarada '{k}' em {qtd}/{n} registros "
                      "(campo novo? declare no contrato)")
    for c, spec in campos.items():
        if not spec.get("obrigatorio", True) and n and all(
                (not isinstance(r, dict)) or r.get(c) is None for r in lista):
            rel.aviso(f"{nome_lista}: campo opcional '{c}' ausente ou nulo em todos os registros")


def checar_series(obj: dict, sp: dict, nome: str, rel: Relatorio) -> None:
    rot = obj.get(sp["rotulos"])
    if not isinstance(rot, list):
        rel.fatal(f"{nome}.{sp['rotulos']}: ausente ou nao e lista")
        return
    n = len(rot)
    if n < sp.get("minimo", 1):
        rel.fatal(f"{nome}.{sp['rotulos']}: {n} rotulos, minimo {sp.get('minimo', 1)}")
    for s in sp["series"]:
        if s not in obj:
            rel.fatal(f"{nome}: serie '{s}' ausente")
        elif not isinstance(obj[s], list):
            rel.fatal(f"{nome}.{s}: nao e lista")
        elif len(obj[s]) != n:
            rel.fatal(f"{nome}.{s}: {len(obj[s])} pontos, mas '{sp['rotulos']}' tem {n} — series desalinhadas")
        elif any(x is not None and not tipo_ok(x, "num") for x in obj[s]):
            rel.fatal(f"{nome}.{s}: contem valor nao numerico")
    declaradas = set(sp["series"]) | {sp["rotulos"]}
    for k in obj:
        if k not in declaradas:
            rel.aviso(f"{nome}: serie nao declarada '{k}' (nova? declare no contrato)")


def checar_pares(v: list, spec: dict, nome: str, rel: Relatorio) -> None:
    item = spec.get("item", {})
    tam = item.get("tamanho", 2)
    vistos, malformados = set(), 0
    for p in v:
        if not isinstance(p, list) or len(p) != tam:
            malformados += 1
            continue
        for pos in range(tam):
            sub = item.get(str(pos))
            if sub and violacoes(p[pos], sub):
                malformados += 1
                break
        if item.get("0", {}).get("unico"):
            if p[0] in vistos:
                rel.fatal(f"{nome}: chave duplicada na posicao 0")
            vistos.add(p[0])
    if malformados:
        rel.fatal(f"{nome}: {malformados}/{len(v)} itens nao sao par posicional de {tam} "
                  "(o painel faz new Map() disto — formato errado vira Map vazio sem erro)")


def checar_topo(D: dict, contrato: dict, slug: str, rel: Relatorio) -> None:
    override = (contrato.get("por_slug") or {}).get(slug, {}).get("topo", {})
    topo = contrato["topo"]
    for chave, spec in topo.items():
        spec = {**spec, **override.get(chave, {})}
        if chave not in D:
            if spec.get("obrigatorio", True):
                msg = f"chave de topo '{chave}' ausente"
                if spec.get("consumidor"):
                    msg += f" — lida em {spec['consumidor']}"
                rel.fatal(msg)
            continue
        v = D[chave]
        for viol in violacoes(v, spec):
            rel.fatal(f"topo '{chave}': {viol}")
        t = spec.get("tipo")
        if t == "lista" and isinstance(v, list):
            if len(v) < spec.get("minimo", 0):
                rel.fatal(f"'{chave}': {len(v)} itens, minimo {spec['minimo']}")
            if "registro" in spec:
                checar_registros(v, chave, contrato["registros"][spec["registro"]], rel)
            if "tipo_item" in spec:
                ruins = sum(1 for x in v if not tipo_ok(x, spec["tipo_item"]))
                if ruins:
                    rel.fatal(f"'{chave}': {ruins}/{len(v)} itens nao sao {spec['tipo_item']}")
        elif t == "pares" and isinstance(v, list):
            if len(v) < spec.get("minimo", 0):
                rel.fatal(f"'{chave}': {len(v)} pares, minimo {spec['minimo']}")
            checar_pares(v, spec, chave, rel)
        elif t == "objeto" and isinstance(v, dict):
            for sub, sspec in (spec.get("campos") or {}).items():
                if sub not in v:
                    if sspec.get("obrigatorio", True):
                        rel.fatal(f"'{chave}.{sub}' ausente")
                    continue
                for viol in violacoes(v[sub], sspec):
                    rel.fatal(f"'{chave}.{sub}': {viol}")
            if "series_paralelas" in spec:
                checar_series(v, spec["series_paralelas"], chave, rel)
        elif t == "str" and isinstance(v, str) and len(v) < spec.get("minimo_chars", 0):
            rel.fatal(f"'{chave}': {len(v)} caracteres, minimo {spec['minimo_chars']}")
    for k in D:
        if k not in topo:
            rel.aviso(f"chave de topo nao declarada '{k}' (metadado novo? declare no contrato)")


def checar_regras(D: dict, contrato: dict, rel: Relatorio) -> None:
    def sev(regra: dict, msg: str) -> None:
        if regra.get("severidade", "fatal") == "fatal":
            rel.fatal(msg)
        else:
            rel.aviso(msg)

    for lit in contrato.get("literais", []):
        lista = D.get(lit["lista"]) if isinstance(D.get(lit["lista"]), list) else []
        n = sum(1 for r in lista if isinstance(r, dict) and r.get(lit["campo"]) == lit["valor"])
        minimo = lit.get("minimo_ocorrencias", 1)
        if n < minimo:
            sev(lit, f"literal {lit['valor']!r} aparece {n}x em {lit['lista']}[].{lit['campo']} "
                     f"(minimo {minimo}) — o painel compara essa string exata; mudou o literal, o KPI zera")

    for en in contrato.get("enums", []):
        lista = D.get(en["lista"]) if isinstance(D.get(en["lista"]), list) else []
        dom, nulo_ok = set(en["valores"]), en.get("permite_nulo", False)
        fora = Counter(r.get(en["campo"]) for r in lista if isinstance(r, dict)
                       and r.get(en["campo"]) not in dom
                       and not (r.get(en["campo"]) is None and nulo_ok))
        if fora:
            vals = ", ".join(f"{k!r}x{q}" for k, q in fora.most_common(5))
            sev(en, f"{en['lista']}[].{en['campo']} fora do dominio {sorted(dom)}: {vals}")

    for ref in contrato.get("referencias", []):
        de = valores_lista(D, ref["de"]) - {None}
        para = valores_lista(D, ref["para"])
        orfaos = de - para
        if orfaos:
            amostra = ", ".join(repr(x) for x in sorted(orfaos, key=str)[:5])
            sev(ref, f"{ref['de']} tem {len(orfaos)} valor(es) que nao existem em {ref['para']}: {amostra}")


# ---------------------------------------------------------------- catraca

def calcular_metrica(D: dict, m: dict) -> int | None:
    if m["tipo"] == "tamanho":
        v = resolver(D, m["caminho"])
        return len(v) if isinstance(v, list) else None
    lista = D.get(m["lista"])
    if not isinstance(lista, list):
        return None
    onde = m.get("onde")
    if not onde:
        return len(lista)
    campo, op, alvo = onde["campo"], onde["op"], ref_valor(D, onde.get("valor"))

    def casa(r: dict) -> bool:
        v = r.get(campo)
        if op == "nao_nulo":
            return v is not None and v != ""
        if op == "==":
            return v == alvo
        if op == ">=":
            return v is not None and alvo is not None and v >= alvo
        if op == "em":
            return v in (alvo or [])
        raise ValueError(f"operador desconhecido: {op}")

    return sum(1 for r in lista if isinstance(r, dict) and casa(r))


def piso(base: int, queda_pct: float, queda_abs: int) -> int:
    """Percentual manda em volume alto, absoluto manda em volume baixo."""
    return max(0, min(math.floor(base * (1 - queda_pct / 100)), base - queda_abs))


def checar_catraca(D: dict, contrato: dict, base: dict | None, rel: Relatorio,
                   aplicar: bool) -> None:
    cat = contrato.get("catraca") or {}
    padrao = {**CATRACA_PADRAO, **(cat.get("padrao") or {})}
    if aplicar and base and base.get("erro"):
        # Nunca em silencio: sem baseline a catraca nao protege nada nesta rodada.
        rel.aviso(f"sem baseline de producao ({base['erro']}) — catraca NAO aplicada nesta rodada")
    base_m = (base or {}).get("metricas", {})
    for m in cat.get("metricas", []):
        hoje = calcular_metrica(D, m)
        rel.metricas[m["nome"]] = hoje
        if hoje is None:
            rel.fatal(f"metrica '{m['nome']}' nao calculavel (lista/caminho ausente)")
            continue
        if "minimo" in m and hoje < m["minimo"]:
            rel.fatal(f"metrica '{m['nome']}' = {hoje}, minimo estrutural {m['minimo']}")
        if not aplicar:
            continue
        b = base_m.get(m["nome"])
        if b is None:
            continue                        # metrica nova ou primeiro run: nada a comparar
        cfg = {**padrao, **(m.get("catraca") or {})}
        p = piso(b, cfg["queda_pct"], cfg["queda_abs"])
        linha = {"metrica": m["nome"], "base": b, "hoje": hoje, "piso": p, "delta": hoje - b}
        rel.catraca.append(linha)
        if hoje < p:
            linha["estado"] = "QUEDA"
            rel.fatal(f"catraca: '{m['nome']}' caiu de {b} para {hoje} (piso {p})", CATRACA)
            continue
        alta = (hoje - b) / b * 100 if b else 0
        if b and (hoje - b) > cfg["alta_abs"]:
            if alta >= cfg["alta_fatal_pct"]:
                linha["estado"] = "EXPLOSAO"
                rel.fatal(f"catraca: '{m['nome']}' subiu {alta:.0f}% numa rodada ({b} -> {hoje}) — "
                          "JOIN duplicando linhas?", CATRACA)
                continue
            if alta >= cfg["alta_aviso_pct"]:
                linha["estado"] = "ALTA"
                rel.aviso(f"catraca: '{m['nome']}' subiu {alta:.0f}% ({b} -> {hoje})")
                continue
        linha["estado"] = "ok"


# ---------------------------------------------------------------- versao

def ler_texto(rel_path: str) -> str | None:
    p = REPO / rel_path
    return p.read_text(encoding="utf-8") if p.exists() else None


def checar_versao(contrato: dict, rel: Relatorio, D: dict | None) -> None:
    v = contrato["schema_version"]
    exp_txt = ler_texto(contrato["exportador"])
    m = RE_VER_EXPORTADOR.search(exp_txt or "")
    if not m:
        rel.fatal(f"exportador {contrato['exportador']} sem 'SCHEMA_VERSION = N'", VERSAO)
    elif int(m.group(1)) != v:
        rel.fatal(f"exportador declara SCHEMA_VERSION {m.group(1)}, contrato espera {v} — "
                  "bumpe os dois juntos", VERSAO)
    pai_txt = ler_texto(contrato["arquivo_painel"])
    mp = RE_VER_PAINEL.search(pai_txt or "")
    if mp and int(mp.group(1)) != v:
        rel.fatal(f"painel {contrato['arquivo_painel']} espera SCHEMA_ESPERADO {mp.group(1)}, "
                  f"contrato espera {v}", VERSAO)
    elif not mp and contrato.get("guard_painel"):
        rel.fatal(f"painel {contrato['arquivo_painel']} sem 'const SCHEMA_ESPERADO = N'", VERSAO)
    if D is not None:
        jv = D.get("schema_version")
        if jv != v:
            rel.fatal(f"JSON traz schema_version {jv!r}, contrato espera {v} — "
                      "o exportador rodou com codigo velho?", VERSAO)


# ---------------------------------------------------------------- leitura

def credencial_basic() -> str:
    user = os.environ.get("DASHBOARD_BASIC_AUTH_USER")
    pw = os.environ.get("DASHBOARD_BASIC_AUTH_PASS")
    env_local = REPO / ".env.local"
    if (not user or not pw) and env_local.exists():
        for linha in env_local.read_text(encoding="utf-8").splitlines():
            if not user and linha.startswith("DASHBOARD_BASIC_AUTH_USER="):
                user = linha.split("=", 1)[1].strip()
            if not pw and linha.startswith("DASHBOARD_BASIC_AUTH_PASS="):
                pw = linha.split("=", 1)[1].strip()
    if not user or not pw:
        raise SystemExit("ERRO: --raiz url precisa de DASHBOARD_BASIC_AUTH_USER/_PASS")
    return base64.b64encode(f"{user}:{pw}".encode()).decode()


def baixar(url: str, basic: str) -> bytes:
    req = urllib.request.Request(url, headers={
        "Authorization": f"Basic {basic}", "User-Agent": "dashboards-contrato/1.0",
        "Cache-Control": "no-cache"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read()


def baseline_de_producao(dashes: list[dict], base_url: str) -> dict:
    """Metricas calculadas do JSON que esta NO AR agora.

    So run verde chega a deployar, entao o que esta em producao e por definicao o ultimo estado
    verde — a catraca compara com ele sem precisar persistir baseline nenhum (o que exigiria o CI
    commitar na main toda noite). Aceitar uma queda legitima = deixar aquela rodada deployar; a
    noite seguinte ja compara contra o numero novo.
    """
    basic = credencial_basic()
    out: dict = {"origem": base_url, "dashboards": {}}
    for d in dashes:
        try:
            contrato = carregar_contrato(d.get("contrato", d["slug"]))
        except Exception:
            continue
        url = f"{base_url.rstrip('/')}/{d['slug']}/{d['dados']}"
        try:
            D = json.loads(baixar(url, basic).decode("utf-8"))
        except Exception as e:
            out["dashboards"][d["slug"]] = {"erro": f"{url}: {e}"}
            continue
        metricas = {m["nome"]: calcular_metrica(D, m)
                    for m in (contrato.get("catraca") or {}).get("metricas", [])}
        out["dashboards"][d["slug"]] = {"metricas": {k: v for k, v in metricas.items() if v is not None}}
    return out


def ler_json(d: dict, args) -> tuple[dict | None, int, str]:
    """(dados, tamanho_bytes, origem). dados=None se nao deu pra ler."""
    if args.raiz == "fonte":
        p = REPO / d["fonte"] / d["dados"]
        if not p.exists():
            return None, 0, f"{p} nao existe — o exportador rodou?"
        raw = p.read_bytes()
        origem = str(p.relative_to(REPO))
    elif args.raiz == "dist":
        p = Path(args.dist) / d["slug"] / d["dados"]
        if not p.exists():
            return None, 0, f"{p} nao existe na dist"
        raw = p.read_bytes()
        origem = str(p)
    else:
        url = f"{args.base_url.rstrip('/')}/{d['slug']}/{d['dados']}"
        try:
            raw = baixar(url, args._basic)
        except Exception as e:
            return None, 0, f"{url}: {e}"
        origem = url
    try:
        return json.loads(raw.decode("utf-8")), len(raw), origem
    except Exception as e:
        return None, len(raw), f"{origem}: JSON ilegivel ({e})"


def carregar_contrato(nome: str) -> dict:
    p = CONTRATOS / f"{nome}.json"
    if not p.exists():
        raise FileNotFoundError(f"contrato ausente: {p.relative_to(REPO)}")
    return json.loads(p.read_text(encoding="utf-8"))


# ---------------------------------------------------------------- validar um slug

def validar_slug(d: dict, args, baseline: dict) -> Relatorio:
    nome = d.get("contrato", d["slug"])
    rel = Relatorio(d["slug"], nome)
    try:
        contrato = carregar_contrato(nome)
    except Exception as e:
        rel.fatal(str(e), IO)
        return rel

    D, tamanho, origem = ler_json(d, args)
    rel.origem = origem
    if D is None:
        rel.fatal(origem, IO)
        return rel
    if not isinstance(D, dict):
        rel.fatal(f"{origem}: raiz do JSON nao e objeto", CONTRATO)
        return rel

    teto = contrato.get("tamanho_max_bytes", 3_400_000)
    if tamanho > teto:
        rel.fatal(f"JSON com {tamanho // 1024} KB, teto {teto // 1024} KB")
    elif tamanho > 0.8 * teto:
        rel.aviso(f"JSON com {tamanho // 1024} KB, ja passou de 80% do teto ({teto // 1024} KB)")

    # Versao primeiro: com versao errada, o resto e ruido.
    checar_versao(contrato, rel, D)
    if rel.codigo == VERSAO:
        return rel

    if not args.sem_frescor:
        g = D.get("gerado_em")
        if isinstance(g, str) and RE_DATA.match(g):
            dias = (datetime.now(BRT).date() - date.fromisoformat(g)).days
            if dias > contrato.get("frescor_dias", 1):
                rel.fatal(f"gerado_em {g} tem {dias} dias — exportador nao rodou? "
                          "(dado velho sobe como se fosse de hoje)")

    checar_topo(D, contrato, d["slug"], rel)
    checar_regras(D, contrato, rel)

    aceitar = args.aceitar_catraca in (d["slug"], "tudo")
    checar_catraca(D, contrato, baseline.get("dashboards", {}).get(d["slug"]), rel,
                   aplicar=not args.sem_catraca)
    if aceitar and rel.codigo == CATRACA:
        # So destrava a catraca: rebaixa os fatais dela a aviso. Contrato/versao seguem valendo
        # porque, se existissem, rel.codigo seria CONTRATO/VERSAO e nao entraria aqui.
        aceitos = [m for c, m in rel.fatais if c == CATRACA]
        rel.fatais = [(c, m) for c, m in rel.fatais if c != CATRACA]
        rel.avisos += [f"ACEITO por humano: {m}" for m in aceitos]
        rel.codigo = pior(c for c, _ in rel.fatais)
        rel.aceito = True
    elif aceitar:
        rel.aceito = rel.codigo == OK
    return rel


# ---------------------------------------------------------------- baseline

def gravar_baseline(baseline: dict, relatorios: list[Relatorio], args) -> None:
    agora = datetime.now(BRT).isoformat(timespec="seconds")
    run = None
    if os.environ.get("GITHUB_RUN_ID"):
        run = (f"{os.environ.get('GITHUB_SERVER_URL', 'https://github.com')}/"
               f"{os.environ.get('GITHUB_REPOSITORY', '')}/actions/runs/{os.environ['GITHUB_RUN_ID']}")
    baseline.setdefault("dashboards", {})
    for r in relatorios:
        ant = baseline["dashboards"].get(r.slug, {})
        ancora = ant.get("ancora_manual")
        if r.aceito and args.aceitar_catraca:
            ancora = {"em": agora[:10], "motivo": args.motivo, "run": run,
                      "metricas": [l["metrica"] for l in r.catraca if l.get("estado") != "ok"]}
        baseline["dashboards"][r.slug] = {
            "contrato": r.contrato,
            "metricas": r.metricas,
            "ancora_manual": ancora,
        }
    baseline["$comment"] = (
        "Metricas do ultimo run VERDE do validar_contrato.py. A CI reescreve no sucesso; queda "
        "abaixo do piso derruba o deploy. Para aceitar uma queda legitima: workflow_dispatch com "
        "aceitar_catraca=<slug> e motivo. Os dados em si sao gitignored — aqui so contagens.")
    baseline["atualizado_em"] = agora
    baseline["run"] = run
    BASELINE.write_text(json.dumps(baseline, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


# ---------------------------------------------------------------- sugerir

def inferir_campo(valores: list) -> dict:
    presentes = [v for v in valores if v is not None]
    spec: dict = {"tipo": "str", "obrigatorio": True, "nulo": len(presentes) < len(valores),
                  "consumidor": ""}
    if presentes:
        tipos = {nome_tipo(v) for v in presentes}
        if tipos == {"data"}:
            spec["tipo"] = "data"
        elif tipos <= {"int"}:
            spec["tipo"] = "int"
        elif tipos <= {"int", "num"}:
            spec["tipo"] = "num"
        elif tipos <= {"str", "data"}:
            spec["tipo"] = "str"
        elif len(tipos) == 1:
            spec["tipo"] = tipos.pop()
        else:
            spec["tipo"] = "?" + "|".join(sorted(tipos))
        if spec["tipo"] in ("str", "int") and len(set(presentes)) <= 8:
            spec["$valores_observados"] = sorted(set(presentes), key=str)
    return spec


def sugerir(d: dict, args) -> dict:
    D, _, origem = ler_json(d, args)
    if D is None:
        raise SystemExit(f"ERRO: {origem}")
    nome = d.get("contrato", d["slug"])
    topo: dict = {}
    registros: dict = {}
    metricas: list = []
    for k, v in D.items():
        if k == "schema_version":
            topo[k] = {"tipo": "int", "obrigatorio": True, "valor": v}
        elif isinstance(v, list) and v and all(isinstance(x, dict) for x in v):
            reg = k.rstrip("s") or k
            chaves = sorted({c for x in v for c in x})
            campos = {}
            for c in chaves:
                spec = inferir_campo([x.get(c) for x in v])
                if any(c not in x for x in v):
                    spec["obrigatorio"] = False
                campos[c] = spec
            registros[reg] = {"chaves_extras": "avisar", "campos": campos}
            topo[k] = {"tipo": "lista", "obrigatorio": True, "registro": reg, "minimo": 1,
                       "consumidor": ""}
            metricas.append({"nome": f"{k}_total", "lista": k, "tipo": "contagem"})
            for c, s in campos.items():
                if s["tipo"] == "data":
                    metricas.append({"nome": f"{k}_com_{c}", "lista": k, "tipo": "contagem",
                                     "onde": {"campo": c, "op": "nao_nulo"}})
        elif isinstance(v, list) and v and all(isinstance(x, list) and len(x) == 2 for x in v):
            topo[k] = {"tipo": "pares", "obrigatorio": True, "minimo": len(v),
                       "item": {"tamanho": 2, "0": {"tipo": nome_tipo(v[0][0]), "unico": True},
                                "1": {"tipo": nome_tipo(v[0][1])}},
                       "consumidor": ""}
            metricas.append({"nome": f"{k}_n", "caminho": k, "tipo": "tamanho", "minimo": len(v)})
        elif isinstance(v, list):
            tipos = {nome_tipo(x) for x in v} or {"str"}
            topo[k] = {"tipo": "lista", "obrigatorio": True,
                       "tipo_item": tipos.pop() if len(tipos) == 1 else "str",
                       "minimo": 1 if v else 0, "consumidor": ""}
        elif isinstance(v, dict) and isinstance(v.get("labels"), list):
            series = [s for s, x in v.items() if s != "labels" and isinstance(x, list)]
            topo[k] = {"tipo": "objeto", "obrigatorio": True,
                       "series_paralelas": {"rotulos": "labels", "series": series, "minimo": 4},
                       "consumidor": ""}
            metricas.append({"nome": f"{k}_semanas", "caminho": f"{k}.labels", "tipo": "tamanho",
                             "minimo": 4})
        elif isinstance(v, dict):
            topo[k] = {"tipo": "objeto", "obrigatorio": True,
                       "campos": {s: {"tipo": nome_tipo(x)} for s, x in v.items()},
                       "consumidor": ""}
        else:
            spec = inferir_campo([v])
            spec["nulo"] = v is None
            topo[k] = spec
    return {
        "$comment": f"RASCUNHO gerado por --sugerir a partir de {origem}. Preencha os 'consumidor' "
                    "(grep no motor.js/render.js/index.html), marque obrigatorio:false no que o "
                    "painel nao le, transforme $valores_observados em enums/literais onde o painel "
                    "compara string, e apague este comentario.",
        "contrato": nome,
        "schema_version": D.get("schema_version", 1),
        "exportador": f"{d['fonte']}/exportar_dados.py",
        "arquivo_painel": f"{d['fonte']}/index.html",
        "guard_painel": False,
        "frescor_dias": 1,
        "tamanho_max_bytes": 3_400_000,
        "topo": topo,
        "registros": registros,
        "literais": [],
        "enums": [],
        "referencias": [],
        "catraca": {"padrao": dict(CATRACA_PADRAO), "metricas": metricas},
    }


# ---------------------------------------------------------------- saida

def imprimir(relatorios: list[Relatorio], final: int) -> None:
    rotulo = {OK: "OK", CATRACA: "CATRACA", CONTRATO: "CONTRATO", VERSAO: "VERSAO", IO: "IO"}
    for r in relatorios:
        print(f"\n== {r.slug}  (contrato {r.contrato})  -> {rotulo[r.codigo]}"
              + ("  [catraca aceita]" if r.aceito else ""))
        if getattr(r, "origem", None):
            print(f"   {r.origem}")
        for c, m in r.fatais:
            print(f"   FATAL[{rotulo[c]}] {m}")
        for m in r.avisos:
            print(f"   aviso  {m}")
        quedas = [l for l in r.catraca if l.get("estado") != "ok"]
        if r.catraca:
            ok_n = len(r.catraca) - len(quedas)
            print(f"   catraca: {ok_n}/{len(r.catraca)} metricas dentro do piso")
            for l in quedas:
                print(f"     {l['metrica']:22s} base {l['base']:>6}  hoje {l['hoje']:>6}  "
                      f"piso {l['piso']:>6}  delta {l['delta']:+d}  {l.get('estado')}")
    print(f"\nRESULTADO: {rotulo[final]} (exit {final})")
    if final == CATRACA:
        slugs = [r.slug for r in relatorios if r.codigo == CATRACA]
        print("Se a queda for legitima (limpeza de CRM, recategorizacao), destrave com:\n"
              f"  validar_contrato.py --aceitar-catraca {slugs[0] if len(slugs) == 1 else 'tudo'} "
              "--motivo \"<por que caiu>\"")


def resumo_github(relatorios: list[Relatorio], final: int) -> None:
    alvo = os.environ.get("GITHUB_STEP_SUMMARY")
    if not alvo:
        return
    rot = {OK: "✅", CATRACA: "⚠️ catraca", CONTRATO: "❌ contrato", VERSAO: "❌ versão", IO: "❌ leitura"}
    linhas = ["## Contrato das dashboards", "", "| dashboard | resultado | fatais | avisos |",
              "|---|---|---|---|"]
    for r in relatorios:
        linhas.append(f"| {r.slug} | {rot[r.codigo]} | {len(r.fatais)} | {len(r.avisos)} |")
    for r in relatorios:
        if r.fatais:
            linhas += ["", f"### {r.slug}", ""] + [f"- `{m.splitlines()[0]}`" for _, m in r.fatais]
    with open(alvo, "a", encoding="utf-8") as f:
        f.write("\n".join(linhas) + "\n")


# ---------------------------------------------------------------- main

def main() -> int:
    global BASELINE
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("slugs", nargs="*")
    ap.add_argument("--raiz", choices=["fonte", "dist", "url"], default="fonte")
    ap.add_argument("--dist")
    ap.add_argument("--base-url")
    ap.add_argument("--sem-catraca", action="store_true")
    ap.add_argument("--sem-frescor", action="store_true")
    ap.add_argument("--atualizar-baseline", action="store_true")
    ap.add_argument("--aceitar-catraca", metavar="SLUG")
    ap.add_argument("--motivo")
    ap.add_argument("--apenas-sync", action="store_true")
    ap.add_argument("--sugerir", metavar="SLUG")
    ap.add_argument("--baseline", help=f"arquivo de baseline (default: {BASELINE.relative_to(REPO)})")
    ap.add_argument("--baseline-url", metavar="URL",
                    help="calcula o baseline do JSON que esta no ar (modo do CI e da skill)")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    if args.baseline:
        BASELINE = Path(args.baseline).resolve()

    if args.raiz == "dist" and not args.dist:
        ap.error("--raiz dist exige --dist DIR")
    if args.raiz == "url":
        if not args.base_url:
            ap.error("--raiz url exige --base-url URL")
        args._basic = credencial_basic()
    if args.aceitar_catraca and not args.motivo:
        ap.error("--aceitar-catraca exige --motivo (fica registrado no baseline)")
    if args.aceitar_catraca and not args.baseline_url:
        args.atualizar_baseline = True     # modo arquivo: aceitar = re-ancorar o arquivo
    if args.baseline_url and args.atualizar_baseline:
        ap.error("--atualizar-baseline nao se aplica a --baseline-url: o baseline e o que esta no ar")

    man = json.loads(MANIFEST.read_text(encoding="utf-8"))
    dashes = man["dashboards"]
    por_slug = {d["slug"]: d for d in dashes}

    if args.sugerir:
        if args.sugerir not in por_slug:
            ap.error(f"slug desconhecido: {args.sugerir}")
        print(json.dumps(sugerir(por_slug[args.sugerir], args), ensure_ascii=False, indent=2))
        return OK

    if args.slugs:
        desconhecidos = [s for s in args.slugs if s not in por_slug]
        if desconhecidos:
            ap.error(f"slug(s) desconhecido(s): {', '.join(desconhecidos)}")
        dashes = [por_slug[s] for s in args.slugs]

    if args.apenas_sync:
        relatorios, vistos = [], set()
        for d in dashes:
            nome = d.get("contrato", d["slug"])
            if nome in vistos:
                continue
            vistos.add(nome)
            rel = Relatorio(d["slug"], nome)
            try:
                checar_versao(carregar_contrato(nome), rel, None)
            except Exception as e:
                rel.fatal(str(e), IO)
            relatorios.append(rel)
        final = pior(r.codigo for r in relatorios)
        imprimir(relatorios, final)
        return final

    baseline = {}
    if not args.sem_catraca:
        if args.baseline_url:
            baseline = baseline_de_producao(dashes, args.baseline_url)
        elif BASELINE.exists():
            baseline = json.loads(BASELINE.read_text(encoding="utf-8"))
        else:
            print("nota: sem --baseline-url nem --baseline — a catraca so calcula as metricas, "
                  "nao compara com nada. No CI e na skill, use --baseline-url.")

    relatorios = [validar_slug(d, args, baseline) for d in dashes]
    final = pior(r.codigo for r in relatorios)

    if args.json:
        print(json.dumps([{"slug": r.slug, "contrato": r.contrato, "codigo": r.codigo,
                           "fatais": [m for _, m in r.fatais], "avisos": r.avisos,
                           "metricas": r.metricas, "catraca": r.catraca, "aceito": r.aceito}
                          for r in relatorios], ensure_ascii=False, indent=2))
    else:
        imprimir(relatorios, final)
    resumo_github(relatorios, final)

    if args.atualizar_baseline:
        if final == OK:
            # Base nova parte da existente: slugs nao validados nesta rodada ficam como estavam.
            base_atual = json.loads(BASELINE.read_text(encoding="utf-8")) if BASELINE.exists() else {}
            gravar_baseline(base_atual, relatorios, args)
            try:
                mostrar = BASELINE.relative_to(REPO)
            except ValueError:
                mostrar = BASELINE
            print(f"baseline atualizado: {mostrar}")
        else:
            print("baseline NAO atualizado: a rodada nao foi verde (a catraca nao pode escorregar "
                  "junto com a degradacao)")
    return final


if __name__ == "__main__":
    sys.exit(main())
