"""smoke_test.py — testa coletar() localmente sem subir API.

Uso:
    uv run --python 3.12 --with "psycopg[binary]" python dashboard-pessoal/smoke_test.py
"""
from __future__ import annotations

import json
import os
import sys
import time
from datetime import date, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))


def _load_env():
    env_path = Path(__file__).parent / ".env"
    if not env_path.exists():
        raise SystemExit(f"ERRO: {env_path} nao existe (copie de dashboard/.env)")
    for raw in env_path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        os.environ[k.strip()] = v.strip().strip('"').strip("'")


def main():
    _load_env()

    from api.dashboard import coletar

    fim = date.today() - timedelta(days=1)
    ini = fim - timedelta(days=6)
    print(f"=== Smoke test: ini={ini} fim={fim} historico=True ===")

    t0 = time.time()
    data = coletar(ini, fim, historico=True)
    dur = time.time() - t0

    print(f"\n[OK] Coleta completa em {dur:.1f}s")
    print(f"  KPIs atual: {data['kpis']['atual']}")
    print(f"  KPIs anterior: {data['kpis']['ant']}")
    print(f"  KPIs MtD: {data['kpis']['mtd']}")
    print(f"  KPIs YtD: {data['kpis']['ytd']}")
    print(f"  Lista leads: {len(data['listas']['leads'])} itens")
    print(f"  Lista ra: {len(data['listas']['ra'])} itens")
    print(f"  Lista fech: {len(data['listas']['fech'])} itens")
    print(f"  Rankings source atual: {len(data['rankings']['source']['atual'])} sources")
    print(f"  Serie 12m labels: {len(data['serie_12m']['labels'])} semanas")
    print(f"  Proporcao sources: {len(data['proporcao_sources'])} entradas")

    # Validacao basica
    assert 'periodos' in data
    assert 'kpis' in data
    assert data['kpis']['atual']['leads'] >= 0
    assert isinstance(data['kpis']['atual']['leads'], int)
    assert len(data['serie_12m']['labels']) == 52

    # Validar JSON-serializavel
    body = json.dumps(data, ensure_ascii=False)
    print(f"\n[OK] JSON size: {len(body):,} bytes")
    print(f"[OK] Tudo certo.")


if __name__ == '__main__':
    main()
