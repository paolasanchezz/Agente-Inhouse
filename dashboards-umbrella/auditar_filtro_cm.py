#!/usr/bin/env python3
"""auditar_filtro_cm.py — o filtro CM do buzz-br esta igual nas duas copias?

O filtro de Content Marketing do Buzzmonitor Brasil vive em duas superficies sincronizadas a mao:
dashboard/queries.py (a oficial, da dash local) e dashboard-pessoal/lib/queries.py (o espelho, que
e o que dashboard-buzz-br-vercel/exportar_dados.py importa de fato). Se divergirem, a dashboard no
ar sobe deals com o filtro errado e nada reclama — foi o caso ECHEF ROBOT (2026-07-01).

A /dashboard-atualizar rodava esta conferencia antes de todo export do buzz-br. Quando a atualizacao
virou noturna no GitHub Actions (2026-10-21), ela ficou de fora; agora o workflow roda este script
antes de exportar, e a skill tambem. So stdlib: importa os dois modulos e compara constantes e SQL.

Uso: py dashboards-umbrella/auditar_filtro_cm.py      (exit 1 = dessincronizado)
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
OFICIAL = REPO / "dashboard" / "queries.py"
ESPELHO = REPO / "dashboard-pessoal" / "lib" / "queries.py"

CONJUNTOS = ["CM_UTM_SOURCES", "CM_UTM_SOURCE_PREFIXOS", "EMAIL_WHITELIST", "EMAIL_BLACKLIST",
             "INTERNOS_EXCLUIR", "HERANCA_SOURCES_INTERNAS", "CM_SLUGS_PREFIXES"]
VALORES = ["CM_DEALS_FORCADOS", "FECHAMENTOS_FORCADOS", "RECONVERSOES_MANUAIS",
           "DEALS_EXCLUIDOS_URL_DATA"]
FUNCOES_SQL = ["filtro_cm", "filtro_inbound", "_sem_outbound"]


def carregar(caminho: Path, nome: str):
    spec = importlib.util.spec_from_file_location(nome, caminho)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main() -> int:
    o, e = carregar(OFICIAL, "oficial"), carregar(ESPELHO, "espelho")
    diferencas = []
    for a in CONJUNTOS:
        A, B = set(getattr(o, a)), set(getattr(e, a))
        if A ^ B:
            diferencas.append(f"{a}: so na oficial={sorted(A - B)} · so no espelho={sorted(B - A)}")
    for a in VALORES:
        if getattr(o, a) != getattr(e, a):
            diferencas.append(f"{a}: valores diferentes")
    for fn in FUNCOES_SQL:
        if getattr(o, fn)() != getattr(e, fn)():
            diferencas.append(f"{fn}(): SQL diferente entre oficial e espelho")
    if diferencas:
        print("FILTRO CM DESSINCRONIZADO — o exportador do buzz-br usa o ESPELHO "
              "(dashboard-pessoal/lib/queries.py). Replique a mudanca nele antes de exportar:")
        for d in diferencas:
            print(f"  - {d}")
        return 1
    print("filtro CM sincronizado (dashboard/queries.py = dashboard-pessoal/lib/queries.py)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
