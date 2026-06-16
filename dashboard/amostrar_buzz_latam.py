"""Mostra amostras representativas de Buzzmonitor LATAM."""
import csv
import random
from pathlib import Path

random.seed(42)

base = Path(__file__).parent.parent / "conhecimento" / "clientes-fechados" / "dor-features-buzzmonitor-latam.csv"
with base.open(encoding="utf-8-sig") as f:
    rows = list(csv.DictReader(f))

print(f"Total deals: {len(rows)}\n")

def has_dor(r):
    return any((r.get(c) or "").strip() for c in ["dor_areas_oportunidade", "dor_problema_lead", "dor_spin_problema", "dor_spin_implicacao"])

def has_feat(r):
    return any((r.get(c) or "").strip() for c in ["feature_principais_modulos", "feature_objetivo", "feature_oportunidades_futuras", "feature_spin_necessidade"])

filtered = [r for r in rows if has_dor(r) and has_feat(r)]
print(f"Deals com dor E feature: {len(filtered)}")
sample = random.sample(filtered, min(15, len(filtered)))

for i, r in enumerate(sample, 1):
    print(f"\n--- #{i} | {r.get('title', '')[:60]} | {r.get('pais', '')} | {r.get('data_fechamento', '')} | {r.get('valor', '')} {r.get('currency', '')} ---")
    print(f"DOR (areas_oportunidade): {(r.get('dor_areas_oportunidade') or '')[:400]}")
    print(f"DOR (problema_lead):      {(r.get('dor_problema_lead') or '')[:300]}")
    print(f"DOR (spin_problema):      {(r.get('dor_spin_problema') or '')[:300]}")
    print(f"DOR (spin_implicacao):    {(r.get('dor_spin_implicacao') or '')[:300]}")
    print(f"FEAT (modulos):           {(r.get('feature_principais_modulos') or '')[:200]}")
    print(f"FEAT (objetivo):          {(r.get('feature_objetivo') or '')[:400]}")
    print(f"FEAT (oport_futuras):     {(r.get('feature_oportunidades_futuras') or '')[:300]}")
    print(f"PLATAFORMA ATUAL: {(r.get('plataforma_atual') or '')[:120]}")
    print(f"CANAIS: {(r.get('canais') or '')[:120]}")
    print(f"QUEM E O CLIENTE: {(r.get('quem_e_o_cliente') or '')[:200]}")
    print(f"DESCRIPTION: {(r.get('description') or '')[:200]}")
