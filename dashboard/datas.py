"""datas.py — calculo de periodos sab-sex para a dashboard semanal de Content Marketing."""
from __future__ import annotations

from datetime import date, timedelta


def calcular_periodos(ate: date | None = None) -> dict:
    """
    Retorna dict com periodos calculados a partir de `ate` (default = hoje).

    Convencao: semana de sabado a sexta. A semana "atual" reportada e sempre
    a ultima semana sab-sex COMPLETA anterior a `ate` (nao inclui dias parciais
    da semana corrente, pra evitar reportar dados incompletos).

    Exemplo (ate=2026-05-18, segunda):
        ini_atual = 2026-05-09 (sab), fim_atual = 2026-05-15 (sex)
        ini_ant   = 2026-05-02 (sab), fim_ant   = 2026-05-08 (sex)
        mtd_ini   = 2026-05-01,        mtd_fim  = 2026-05-15
        ytd_ini   = 2026-01-01,        ytd_fim  = 2026-05-15
        semanas_decorridas_ytd = 18
    """
    hoje = ate or date.today()

    # weekday: seg=0, ter=1, qua=2, qui=3, sex=4, sab=5, dom=6
    wd = hoje.weekday()

    # ultima sexta-feira ESTRITAMENTE anterior a hoje (ou hoje, se hoje for sexta?)
    # convencao: se hoje for sex/sab/dom da semana corrente, a "semana atual reportada"
    # ainda e a anterior, pra ficar consistente (relatorio rodado em sex/sab/dom
    # ainda fecha a semana anterior, nao a corrente).
    if wd == 4:    # sexta: pega sexta da semana passada
        fim_atual = hoje - timedelta(days=7)
    elif wd == 5:  # sabado: comeca semana nova, mas reporta anterior
        fim_atual = hoje - timedelta(days=1)
    elif wd == 6:  # domingo
        fim_atual = hoje - timedelta(days=2)
    else:          # seg/ter/qua/qui — voltar pra sexta anterior
        fim_atual = hoje - timedelta(days=(wd - 4) % 7)

    ini_atual = fim_atual - timedelta(days=6)
    fim_ant = ini_atual - timedelta(days=1)
    ini_ant = fim_ant - timedelta(days=6)

    mtd_ini = date(fim_atual.year, fim_atual.month, 1)
    mtd_fim = fim_atual

    ytd_ini = date(fim_atual.year, 1, 1)
    ytd_fim = fim_atual

    # Semanas completas decorridas entre ytd_ini e ini_atual (exclusivo)
    # Denominador da media semanal YtD (mostrada no foot dos KPIs semanais)
    semanas_decorridas = max(1, (ini_atual - ytd_ini).days // 7)

    return {
        'hoje': hoje,
        'ini_atual': ini_atual,
        'fim_atual': fim_atual,
        'ini_ant': ini_ant,
        'fim_ant': fim_ant,
        'mtd_ini': mtd_ini,
        'mtd_fim': mtd_fim,
        'ytd_ini': ytd_ini,
        'ytd_fim': ytd_fim,
        'semanas_decorridas_ytd': semanas_decorridas,
    }


# ============ FORMATADORES ============

_MESES = ['Jan', 'Fev', 'Mar', 'Abr', 'Maio', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
_DIAS = ['seg', 'ter', 'qua', 'qui', 'sex', 'sab', 'dom']
_DIAS_ACENTO = ['seg', 'ter', 'qua', 'qui', 'sex', 'sáb', 'dom']


def fmt_data_longa(d: date) -> str:
    """Ex: '09 de Maio (sab)'. Usado no header do relatorio."""
    return f"{d.day:02d} de {_MESES[d.month-1]} ({_DIAS_ACENTO[d.weekday()]})"


def fmt_data_curta(d: date) -> str:
    """Ex: '09/05'. Usado em datas dentro de tabelas."""
    return f"{d.day:02d}/{d.month:02d}"


def fmt_data_iso(d: date) -> str:
    """Ex: '2026-05-15'. Usado em SQL."""
    return d.isoformat()


def fmt_periodo_curto(ini: date, fim: date) -> str:
    """Ex: '09-15 Mai 2026'. Usado em tags e sub-heads."""
    if ini.month == fim.month:
        return f"{ini.day:02d}-{fim.day:02d} {_MESES[fim.month-1]} {fim.year}"
    return f"{fmt_data_curta(ini)}-{fmt_data_curta(fim)} {fim.year}"


# ============ CLI ============

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        p = calcular_periodos(date.fromisoformat(sys.argv[1]))
    else:
        p = calcular_periodos()
    print(f"Periodos calculados a partir de {p['hoje']}:")
    print(f"  Semana atual:  {p['ini_atual']} -> {p['fim_atual']}")
    print(f"  Semana ant.:   {p['ini_ant']} -> {p['fim_ant']}")
    print(f"  MtD:           {p['mtd_ini']} -> {p['mtd_fim']}")
    print(f"  YtD:           {p['ytd_ini']} -> {p['ytd_fim']}")
    print(f"  Semanas decorridas YtD: {p['semanas_decorridas_ytd']}")
