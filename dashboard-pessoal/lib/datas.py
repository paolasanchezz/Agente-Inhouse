"""datas.py — calculo de periodos arbitrarios para o dashboard pessoal.

Diferente do dashboard oficial (que fixa semana sab-sex), aqui o usuario
passa qualquer [ini, fim] e a funcao deriva os 4 periodos do report:
  - atual: [ini, fim]
  - anterior: mesmo numero de dias antes de ini
  - mtd: 1o do mes de fim ate fim
  - ytd: 1o de janeiro do ano de fim ate fim
"""
from __future__ import annotations

from datetime import date, timedelta


def calcular_periodos(ini: date, fim: date) -> dict:
    """
    Calcula todos os periodos derivados a partir do range [ini, fim].

    Exemplo (ini=2026-05-13, fim=2026-05-20, 8 dias):
        ini_atual = 2026-05-13, fim_atual = 2026-05-20
        ini_ant   = 2026-05-05, fim_ant   = 2026-05-12  (8 dias antes)
        mtd_ini   = 2026-05-01,  mtd_fim  = 2026-05-20
        ytd_ini   = 2026-01-01,  ytd_fim  = 2026-05-20
        dias_periodo = 8
        periodos_decorridos_ytd = 17 (140 dias YtD / 8 dias periodo)
    """
    if fim < ini:
        raise ValueError(f"fim ({fim}) deve ser >= ini ({ini})")

    dias = (fim - ini).days + 1

    return {
        'hoje': date.today(),
        'ini_atual': ini,
        'fim_atual': fim,
        'ini_ant': ini - timedelta(days=dias),
        'fim_ant': ini - timedelta(days=1),
        'mtd_ini': date(fim.year, fim.month, 1),
        'mtd_fim': fim,
        'ytd_ini': date(fim.year, 1, 1),
        'ytd_fim': fim,
        'dias_periodo': dias,
        # "quantos periodos do mesmo tamanho cabem no YtD" — denominador da media
        'periodos_decorridos_ytd': max(1, ((fim - date(fim.year, 1, 1)).days + 1) // dias),
    }


# ============ PRESETS ============

def preset_periodo(preset: str, ate: date | None = None) -> tuple[date, date]:
    """
    Retorna (ini, fim) para presets comuns. fim sempre = ate (default hoje).

    Presets:
      '7d' / '15d' / '30d' / '90d' — ultimos N dias inclusive ate
      'mtd' — 1o do mes ate ate
      'ytd' — 1o de jan ate ate
    """
    fim = ate or date.today()
    if preset == '7d':
        return fim - timedelta(days=6), fim
    if preset == '15d':
        return fim - timedelta(days=14), fim
    if preset == '30d':
        return fim - timedelta(days=29), fim
    if preset == '90d':
        return fim - timedelta(days=89), fim
    if preset == 'mtd':
        return date(fim.year, fim.month, 1), fim
    if preset == 'ytd':
        return date(fim.year, 1, 1), fim
    raise ValueError(f"preset invalido: {preset}")


# ============ FORMATADORES (server-side fallback; JS faz a maioria) ============

_MESES = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']


def fmt_iso(d: date) -> str:
    return d.isoformat()


def fmt_periodo_iso_curto(ini: date, fim: date) -> str:
    """'13-20 Mai 2026' ou '28 Abr - 04 Mai 2026' (cross-month)."""
    if ini.year == fim.year and ini.month == fim.month:
        return f"{ini.day:02d}-{fim.day:02d} {_MESES[fim.month-1]} {fim.year}"
    if ini.year == fim.year:
        return f"{ini.day:02d} {_MESES[ini.month-1]} - {fim.day:02d} {_MESES[fim.month-1]} {fim.year}"
    return f"{ini.day:02d} {_MESES[ini.month-1]} {ini.year} - {fim.day:02d} {_MESES[fim.month-1]} {fim.year}"
