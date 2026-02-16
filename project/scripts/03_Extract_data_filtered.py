import pandas as pd
from pathlib import Path
from collections import defaultdict

# =========================
# Configuration
# =========================
PROJECT_ROOT = Path.cwd()
RESULTS_DIR = PROJECT_ROOT / "results"
TOP_N = 20
SORT_COLUMN = "mean_score"

EXCLUDE_PREFIXES = ("03", "04", "05", "07")

OUTPUT_DIR = PROJECT_ROOT / "analysis" / "filtered"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# =========================
# Helpers
# =========================
def extract_residues_from_wt_positions(wt_positions):
    """
    "167,267" -> [167, 267]
    """
    return [int(x) for x in wt_positions.split(",")]


def load_top_variants(csv_path, top_n):
    df = pd.read_csv(csv_path)
    df = df[df["n_mutations"] == 2]
    df = df.sort_values(SORT_COLUMN, ascending=False).head(top_n)
    return df


# =========================
# Data containers
# =========================
variant_records = []
residue_records = []
scenario_variant_presence = defaultdict(set)
scenario_residue_counts = defaultdict(lambda: defaultdict(int))

# =========================
# Main loop (FILTERED)
# =========================
for scenario_dir in RESULTS_DIR.iterdir():
    if not scenario_dir.is_dir():
        continue

    scenario = scenario_dir.name

    if scenario.startswith(EXCLUDE_PREFIXES):
        continue

    csv_file = scenario_dir / "multi_mutation_variants.csv"
    if not csv_file.exists():
        continue

    print(f"Processing {scenario}")

    df = load_top_variants(csv_file, TOP_N)

    for _, row in df.iterrows():
        variant = row["variant"]
        mean_score = row["mean_score"]
        sum_score = row["sum_score"]

        residues = extract_residues_from_wt_positions(row["wt_positions"])

        # ---- Variant-level records
        variant_records.append({
            "variant": variant,
            "scenario": scenario,
            "mean_score": mean_score,
            "sum_score": sum_score
        })

        scenario_variant_presence[scenario].add(variant)

        # ---- Residue-level records
        for res in residues:
            residue_records.append({
                "residue": res,
                "variant": variant,
                "scenario": scenario,
                "mean_score": mean_score,
                "sum_score": sum_score
            })
            scenario_residue_counts[scenario][res] += 1

# =========================
# Variant statistics
# =========================
variant_df = pd.DataFrame(variant_records)

variant_stats = (
    variant_df
    .groupby("variant")
    .agg(
        n_appearances=("scenario", "count"),
        n_scenarios=("scenario", "nunique"),
        mean_mean_score=("mean_score", "mean"),
        std_mean_score=("mean_score", "std"),
        max_mean_score=("mean_score", "max"),
        mean_sum_score=("sum_score", "mean"),
        std_sum_score=("sum_score", "std"),
        max_sum_score=("sum_score", "max"),
    )
    .sort_values("n_appearances", ascending=False)
)

variant_stats.to_csv(OUTPUT_DIR / "variant_stats.csv")

# =========================
# Residue statistics
# =========================
residue_df = pd.DataFrame(residue_records)

residue_stats = (
    residue_df
    .groupby("residue")
    .agg(
        n_appearances=("variant", "count"),
        n_variants=("variant", "nunique"),
        n_scenarios=("scenario", "nunique"),
        mean_mean_score=("mean_score", "mean"),
        mean_sum_score=("sum_score", "mean"),
    )
    .sort_values("n_appearances", ascending=False)
)

residue_stats.to_csv(OUTPUT_DIR / "residue_stats.csv")

# =========================
# Scenario × Variant matrix
# =========================
scenario_variant_table = (
    pd.DataFrame.from_dict(
        {s: {v: 1 for v in vs} for s, vs in scenario_variant_presence.items()},
        orient="index"
    )
    .fillna(0)
    .astype(int)
)

scenario_variant_table.to_csv(OUTPUT_DIR / "scenario_variant_table.csv")

# =========================
# Scenario × Residue matrix
# =========================
scenario_residue_table = (
    pd.DataFrame.from_dict(
        scenario_residue_counts,
        orient="index"
    )
    .fillna(0)
    .astype(int)
    .sort_index(axis=1)
)

scenario_residue_table.to_csv(OUTPUT_DIR / "scenario_residue_table.csv")

print("Filtered variant and residue analysis complete.")