#!/usr/bin/env python3
"""testar_contrato.py — prova que o validar_contrato.py PEGA cada modo de falha conhecido.

Um validador que nunca reclama pode simplesmente nao estar checando nada. Este script copia os
JSONs reais (precisam ter sido exportados antes) para uma dist temporaria, corrompe cada um de
um jeito especifico e confere se o validador sai com o codigo certo e a mensagem certa.

Cada caso e um modo de falha real das dashboards — os comentarios dizem o que o painel faria
com aquele dado se ele subisse.

Uso:
    py dashboards-umbrella/testar_contrato.py        # exige os dados-*.json exportados
Sai 1 se algum caso nao bater.
"""
from __future__ import annotations

import copy
import json
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
VALIDADOR = REPO / "dashboards-umbrella" / "validar_contrato.py"
MANIFEST = REPO / "dashboards-umbrella" / "manifest.json"
BRT = timezone(timedelta(hours=-3))
OK, IO, CONTRATO, CATRACA, VERSAO = 0, 1, 2, 3, 4

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass


# ---------------------------------------------------------------- mutacoes

def renomear_d_lead(D):
    # O assassino silencioso: _inRange(undefined) = false, todos os KPIs zeram, dash bonita e vazia.
    for r in D["deals"]:
        r["data_lead"] = r.pop("d_lead")


def tirar_ganhas(D):
    # motor.js faz new Set(DADOS.ganhas || []): fechamento 0 sem erro nenhum.
    del D["ganhas"]


def literal_perdido_minusculo(D):
    # motor.js compara status === 'Perdido'; 'perdido' zera o KPI de perdidos.
    for r in D["leads"]:
        if r["status"] == "Perdido":
            r["status"] = "perdido"


def enum_c_novo(D):
    # kpis[x.c] += 1 com valor novo cria kpis.parcial = NaN e some dos tres buckets.
    D["deals"][0]["c"] = "parcial"


def etapas_viram_objetos(D):
    # new Map([{chave,rotulo}]) nao da erro: vira Map vazio e a distribuicao esvazia.
    D["etapas"] = [{"chave": a, "rotulo": b} for a, b in D["etapas"]]


def versao_2(D):
    D["schema_version"] = 2


def data_com_hora(D):
    # Comparacao de string: '<= fim' falha so no ultimo dia do periodo. Erro sutil e eterno.
    D["deals"][0]["d_lead"] = D["deals"][0]["d_lead"] + "T00:00:00"


def etapa_orfa(D):
    D["deals"][0]["e"] = "etapa_que_nao_existe"


def dado_velho(D):
    # Exportador morreu, arquivo de 5 dias atras sobe como se fosse de hoje.
    D["gerado_em"] = (datetime.now(BRT).date() - timedelta(days=5)).isoformat()


def serie_desalinhada(D):
    D["serie"]["leads"] = D["serie"]["leads"][:-1]


def marca_trocada(D):
    # Arquivo da Cxpress PT servido na rota da Buzzmonitor PT (o bug do fallback mudo).
    D["marca"] = "cxpress"


def tirar_perdidos(D):
    del D["perdidos"]


def nulificar_d_lead(D):
    # Query quebrou e d_lead veio nulo em todo mundo: mesmo sintoma do rename (tudo zero),
    # mas cada registro isolado e "valido". So a catraca pega.
    for r in D["deals"]:
        r["d_lead"] = None


# ---------------------------------------------------------------- casos
# (nome, slug, mutacao | None, codigo esperado, trecho esperado na saida, baseline, args extras)
#   baseline: None = sem baseline | "real" = metricas atuais | callable(metricas) -> metricas

def mais_500(m):
    return {**m, "deals_total": m["deals_total"] + 500}


def um_terco(m):
    return {**m, "deals_total": m["deals_total"] // 3}


CASOS = [
    ("controle: dados reais, sem baseline",   "cxpress",  None,                     OK,       "RESULTADO: OK",   None,  []),
    ("controle: dados reais, com baseline",   "cxpress",  None,                     OK,       "RESULTADO: OK",   "real", []),
    ("rename d_lead -> data_lead",            "cxpress",  renomear_d_lead,          CONTRATO, "provavel RENAME", None,  []),
    ("chave de topo 'ganhas' ausente (PT)",   "bm-pt",    tirar_ganhas,             CONTRATO, "'ganhas' ausente", None, []),
    ("chave de topo 'perdidos' ausente",      "buzz-br",  tirar_perdidos,           CONTRATO, "'perdidos' ausente", None, []),
    ("literal 'Perdido' virou 'perdido'",     "latam",    literal_perdido_minusculo, CONTRATO, "literal 'Perdido'", None, []),
    ("enum novo em acumulador kpis[x.c]",     "bm-pt",    enum_c_novo,              CONTRATO, "fora do dominio", None,  []),
    ("etapas viram objetos (new Map vazio)",  "bm-pt",    etapas_viram_objetos,     CONTRATO, "par posicional",  None,  []),
    ("data com hora (erro no ultimo dia)",    "cxpress",  data_com_hora,            CONTRATO, "esperava data",   None,  []),
    ("etapa fora do vocabulario",             "bm-pt",    etapa_orfa,               CONTRATO, "nao existem em",  None,  []),
    ("gerado_em de 5 dias atras",             "cxpress",  dado_velho,               CONTRATO, "tem 5 dias",      None,  []),
    ("serie com um ponto a menos",            "cxpress",  serie_desalinhada,        CONTRATO, "desalinhadas",    None,  []),
    ("arquivo de outra marca na rota PT",     "bm-pt",    marca_trocada,            CONTRATO, "valor fora",      None,  []),
    ("JSON v2 com contrato v1",               "cxpress",  versao_2,                 VERSAO,   "schema_version 2", None, []),
    ("catraca: queda de 500 deals",           "cxpress",  None,                     CATRACA,  "caiu de",         mais_500, []),
    ("catraca: queda aceita por humano",      "cxpress",  None,                     OK,       "catraca aceita",  mais_500,
     ["--aceitar-catraca", "cxpress", "--motivo", "teste automatizado"]),
    ("aceitar catraca NAO mascara rename",    "cxpress",  renomear_d_lead,          CONTRATO, "provavel RENAME", mais_500,
     ["--aceitar-catraca", "cxpress", "--motivo", "teste automatizado"]),
    ("catraca: explosao (+200%, JOIN dobrado)", "cxpress", None,                    CATRACA,  "subiu",           um_terco, []),
    ("catraca: d_lead nulificado em massa",   "cxpress",  nulificar_d_lead,         CATRACA,  "deals_com_d_lead", "real", []),
]


# ---------------------------------------------------------------- execucao

def rodar(dist: Path, slug: str, baseline: Path | None, extras: list[str]) -> tuple[int, str]:
    cmd = [sys.executable, str(VALIDADOR), "--raiz", "dist", "--dist", str(dist), slug, *extras]
    if baseline:
        cmd += ["--baseline", str(baseline)]
    else:
        cmd += ["--sem-catraca"]
    p = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
    return p.returncode, p.stdout + p.stderr


def main() -> int:
    man = json.loads(MANIFEST.read_text(encoding="utf-8"))
    dash = {d["slug"]: d for d in man["dashboards"]}
    originais = {}
    for slug, d in dash.items():
        p = REPO / d["fonte"] / d["dados"]
        if not p.exists():
            print(f"ERRO: {p} nao existe — exporte as dashboards antes de testar")
            return 1
        originais[slug] = json.loads(p.read_text(encoding="utf-8"))

    tmp = Path(tempfile.mkdtemp(prefix="contrato-teste-"))
    try:
        # Metricas reais de cada slug, para montar baselines dos casos de catraca.
        dist = tmp / "dist"
        for slug, d in dash.items():
            (dist / slug).mkdir(parents=True)
            (dist / slug / d["dados"]).write_text(json.dumps(originais[slug]), encoding="utf-8")
        p = subprocess.run([sys.executable, str(VALIDADOR), "--raiz", "dist", "--dist", str(dist),
                            "--sem-catraca", "--json"], capture_output=True, text=True, encoding="utf-8")
        metricas_reais = {r["slug"]: r["metricas"] for r in json.loads(p.stdout)}

        falhas = 0
        for nome, slug, mut, esperado, trecho, base, extras in CASOS:
            d = dash[slug]
            dados = copy.deepcopy(originais[slug])
            if mut:
                mut(dados)
            (dist / slug / d["dados"]).write_text(json.dumps(dados), encoding="utf-8")
            baseline = None
            if base is not None:
                m = metricas_reais[slug] if base == "real" else base(metricas_reais[slug])
                baseline = tmp / "baseline.json"
                baseline.write_text(json.dumps({"dashboards": {slug: {"metricas": m}}}), encoding="utf-8")
            codigo, saida = rodar(dist, slug, baseline, extras)
            ok = codigo == esperado and trecho in saida
            falhas += not ok
            print(f"  {'ok  ' if ok else 'FALHOU'}  {nome:44s} exit {codigo} (esperado {esperado})")
            if not ok:
                faltou = "" if trecho in saida else f"  [faltou o trecho {trecho!r}]"
                print(f"          {faltou}\n" + "\n".join(f"          | {l}" for l in saida.splitlines()[-12:]))
            # Restaura o original para o proximo caso.
            (dist / slug / d["dados"]).write_text(json.dumps(originais[slug]), encoding="utf-8")

        print(f"\n{len(CASOS) - falhas}/{len(CASOS)} casos ok")
        return 1 if falhas else 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
