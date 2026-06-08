"""Mostra amostras representativas dos campos descritivos de dor e feature."""
import csv
import random
from pathlib import Path

random.seed(42)

base = Path(__file__).parent.parent / "conhecimento" / "clientes-fechados" / "dor-features-buzzmonitor-brasil.csv"
with base.open(encoding="utf-8-sig") as f:
    rows = list(csv.DictReader(f))

print(f"Total deals: {len(rows)}\n")

# Amostra 15 deals com objetivo e dor preenchidos
filtered = [r for r in rows if (r.get("feature_objetivo") or "").strip() and (r.get("dor_dores_atuais") or "").strip()]
sample = random.sample(filtered, min(15, len(filtered)))

for i, r in enumerate(sample, 1):
    print(f"--- #{i} | {r.get('title', '')[:60]} | {r.get('data_fechamento', '')} | {r.get('valor', '')} {r.get('currency', '')} ---")
    print(f"DOR (dores_atuais): {(r.get('dor_dores_atuais') or '')[:400]}")
    print(f"FEATURE (objetivo): {(r.get('feature_objetivo') or '')[:400]}")
    print(f"FEATURE (modulos): {(r.get('feature_principais_modulos') or '')[:200]}")
    print(f"PLATAFORMA ATUAL: {(r.get('plataforma_atual') or '')[:120]}")
    print(f"CONCORRENTES: {(r.get('concorrentes_avaliados') or '')[:120]}")
    print()
