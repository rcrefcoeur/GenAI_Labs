import matplotlib.pyplot as plt
from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path.cwd()
OUTPUT_DIR = PROJECT_ROOT / "analysis" / "filtered"
FIGURES_DIR = OUTPUT_DIR / "figures"

OUTPUT_DIR.mkdir(exist_ok=True)
FIGURES_DIR.mkdir(exist_ok=True)

# ---------------
variant_stats = pd.read_csv("analysis/filtered/variant_stats.csv", index_col=0)

top_variants = (
    variant_stats
    .sort_values("n_scenarios", ascending=False)
    .head(20)
)

plt.figure(figsize=(8, 6))
top_variants["n_scenarios"].plot(kind="barh")
plt.xlabel("Number of scenarios")
plt.ylabel("Variant")
plt.title("Robust variants across scenarios (Top 20)")
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig("analysis/filtered/figures/robust_variants.png")
plt.close()



# ------------------
residue_stats = pd.read_csv("analysis/filtered/residue_stats.csv", index_col=0)

top_residues = residue_stats.head(20)

plt.figure(figsize=(8, 6))
top_residues["n_appearances"].plot(kind="barh")
plt.xlabel("Appearances in top-20 sets")
plt.ylabel("Residue position")
plt.title("Dominant residues in top-20 variants")
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig("analysis/filtered/figures/dominant_residues.png")
plt.close()

# -----------------
import seaborn as sns

scenario_residue = pd.read_csv(
    "analysis/filtered/scenario_residue_table.csv", index_col=0
)

# Keep only residues that appear at least once
scenario_residue = scenario_residue.loc[:, scenario_residue.sum() > 0]

plt.figure(figsize=(12, 6))
sns.heatmap(
    scenario_residue,
    cmap="viridis",
    linewidths=0.5
)
plt.xlabel("Residue position")
plt.ylabel("Scenario")
plt.title("Residue usage per scenario (top-20 variants)")
plt.tight_layout()
plt.savefig("analysis/filtered/figures/scenario_residue_heatmap.png")
plt.close()
# -----------------

import numpy as np

scenario_variant = pd.read_csv(
    "analysis/filtered/scenario_variant_table.csv", index_col=0
)

scenarios = scenario_variant.index
jaccard = pd.DataFrame(
    np.zeros((len(scenarios), len(scenarios))),
    index=scenarios,
    columns=scenarios
)

for s1 in scenarios:
    for s2 in scenarios:
        v1 = scenario_variant.loc[s1].astype(bool)
        v2 = scenario_variant.loc[s2].astype(bool)
        intersection = (v1 & v2).sum()
        union = (v1 | v2).sum()
        jaccard.loc[s1, s2] = intersection / union if union > 0 else 0

plt.figure(figsize=(7, 6))
sns.heatmap(jaccard, annot=True, cmap="coolwarm", vmin=0, vmax=1)
plt.title("Scenario similarity (Jaccard index)")
plt.tight_layout()
plt.savefig("analysis/filtered/figures/scenario_similarity_heatmap.png")
plt.close()
