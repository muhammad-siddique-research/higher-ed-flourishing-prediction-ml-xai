"""End-to-end ML / SHAP demonstration with SYNTHETIC records only.

The synthetic data-generating formula is pedagogical, not fitted from an
institutional study. No synthetic result is evidence about actual students.

Usage: python -m examples.synthetic_demo [--shap]
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from src.train_and_evaluate import run_benchmarks, run_shap_explanation

NOTICE = "SYNTHETIC DEMONSTRATION — NOT STUDENT RESEARCH RESULTS"

def make_synthetic_sample(n: int = 240, seed: int = 42) -> pd.DataFrame:
    if n < 60:
        raise ValueError("At least 60 synthetic records required.")
    rng = np.random.default_rng(seed)
    community = rng.uniform(1, 6, n)
    integrity = rng.uniform(1, 6, n)
    spirituality = rng.uniform(1, 6, n)
    fit = rng.uniform(1, 6, n)
    tuition = rng.integers(1, 7, n)
    firstgen = rng.integers(0, 2, n)
    gender = rng.integers(0, 2, n)
    income = rng.integers(1, 6, n)
    # Mathematical assumptions, NOT estimates of psychosocial effects.
    y = (2.05 + .32 * community + .11 * integrity + .13 * spirituality
         + .10 * fit + .035 * tuition - .08 * firstgen
         + .08 * np.sin(2 * community) + rng.normal(0, .38, n))
    return pd.DataFrame({
        "SCOMM": community, "INTEGRITY": integrity, "SPIR": spirituality,
        "FIT": fit, "TUITION": tuition, "FIRSTGEN": firstgen,
        "GENDER": gender, "FAMINCOME": income,
        "TQ_MEAN": np.clip(y, 1, 6),
        "CAMPUS_ID": [f"FAKE_CAMPUS_{j % 12:02d}" for j in range(n)],
    })

def run_demo(output_dir: Path, n: int = 240, seed: int = 42, shap: bool = False):
    synthetic = make_synthetic_sample(n, seed)
    scores = run_benchmarks(synthetic, folds=3, seed=seed,
                            group_column="CAMPUS_ID")
    output_dir.mkdir(parents=True, exist_ok=True)
    scores.insert(0, "provenance", "SYNTHETIC_ONLY")
    scores.to_csv(output_dir / "SYNTHETIC_model_metrics.csv", index=False)
    if "fold_metrics" in scores.attrs:
        scores.attrs["fold_metrics"].to_csv(
            output_dir / "SYNTHETIC_fold_metrics.csv", index=False)
    fig, ax = plt.subplots(figsize=(9.5, 5))
    order = scores.sort_values("rmse_mean", ascending=False)
    ax.barh(order["model"], order["rmse_mean"], xerr=order["rmse_sd"],
            capsize=3, color="#286D88")
    ax.set_xlabel("RMSE on simulated outcome (1–6 scale)")
    ax.set_title("Group-held-out model comparison | Synthetic experiment")
    fig.text(.5, .01, NOTICE, color="#9A2323", ha="center", weight="bold")
    fig.tight_layout(rect=[0, .04, 1, 1])
    fig.savefig(output_dir / "SYNTHETIC_models.png", dpi=160)
    plt.close(fig)
    manifest = {"provenance": NOTICE, "n": n, "seed": seed,
                "folds": 3, "groups": "12 synthetic campus identifiers",
                "interpretation": "Software verification; not empirical validation"}
    (output_dir / "SYNTHETIC_manifest.json").write_text(
        json.dumps(manifest, indent=2), encoding="utf-8")
    if shap:
        dest = run_shap_explanation(synthetic, output_dir / "SYNTHETIC_SHAP")
        print("Synthetic feature attribution:", dest)
    print(NOTICE)
    print(scores.to_string(index=False))
    return scores

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=Path("demo_outputs"))
    parser.add_argument("--n", type=int, default=240)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--shap", action="store_true")
    args = parser.parse_args()
    run_demo(args.output_dir, n=args.n, seed=args.seed, shap=args.shap)

if __name__ == "__main__":
    main()
