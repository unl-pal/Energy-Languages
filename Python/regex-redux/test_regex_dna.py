from regex_dna import run_regex_dna, variants, subst

sample_input = """>SEQ_1
agggtaaa
tttaccct
aNDHaD
"""

results = run_regex_dna(sample_input)

# ===== Test input cleaning =====
assert results["original_length"] == len(sample_input)
assert results["cleaned_length"] < results["original_length"], "Cleaning should remove headers/newlines"

# ===== Test variant counts =====
variant_counts = dict(results["variant_counts"])
for v in variants:
    assert v in variant_counts, f"Missing variant: {v}"
    assert isinstance(variant_counts[v], int), "Each variant should return count as int"

# ===== Test substitutions applied =====
# Manually mimic substitution
from re import sub as re_sub
cleaned = re_sub('>.*\n|\n', '', sample_input)
for f, r in subst.items():
    cleaned = re_sub(f, r, cleaned)
assert len(cleaned) == results["final_length"], "Substitution result length mismatch"

print("✅ All regex_dna tests passed.")
