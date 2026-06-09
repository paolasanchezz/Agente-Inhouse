"""Mostra amostras representativas dos campos descritivos de dor e feature de Cxpress BR."""
import csv
import random
from pathlib import Path

random.seed(42)

base = Path(__file__).parent.parent / "conhecimento" / "clientes-fechados" / "dor-features-cxpress-brasil.csv"
with base.open(encoding="utf-8-sig") as f:
    rows = list(csv.DictReader(f))

print(f"Total deals: {len(rows)}\n")

# Amostra 15 deals com qualquer dor + qualquer feature preenchido
def has_dor(r):
    return any((r.get(c) or "").strip() for c in ["dor_principal_queixa", "dor_bant_needs", "dor_spin_problema", "dor_spin_implicacao"])

def has_feat(r):
    return any((r.get(c) or "").strip() for c in ["feature_canais_a_integrar", "feature_necessidade_lead", "feature_prioridade_implementacao", "feature_spin_necessidade"])

filtered = [r for r in rows if has_dor(r) and has_feat(r)]
print(f"Deals com dor E feature: {len(filtered)}")
sample = random.sample(filtered, min(15, len(filtered)))

for i, r in enumerate(sample, 1):
    print(f"\n--- #{i} | {r.get('title', '')[:60]} | {r.get('data_fechamento', '')} | {r.get('valor_fee', '')} {r.get('currency', '')} ---")
    print(f"DOR (principal_queixa): {(r.get('dor_principal_queixa') or '')[:400]}")
    print(f"DOR (bant_needs):       {(r.get('dor_bant_needs') or '')[:300]}")
    print(f"DOR (spin_problema):    {(r.get('dor_spin_problema') or '')[:300]}")
    print(f"FEATURE (canais):       {(r.get('feature_canais_a_integrar') or '')[:200]}")
    print(f"FEATURE (necessidade):  {(r.get('feature_necessidade_lead') or '')[:300]}")
    print(f"FEATURE (prioridade):   {(r.get('feature_prioridade_implementacao') or '')[:120]}")
    print(f"FEATURE (spin_necess):  {(r.get('feature_spin_necessidade') or '')[:300]}")
    print(f"AREA: {(r.get('area_atendida') or '')[:120]}")
    print(f"VOLUME: {(r.get('volume_atendimentos') or '')[:80]}")
    print(f"CONCORRENTE: {(r.get('concorrente_avaliado') or '')[:120]}")
