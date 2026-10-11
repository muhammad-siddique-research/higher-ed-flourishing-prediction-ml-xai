"""Audit a *reported manuscript summary*, not student-level observations.

This script derives additional regression diagnostics from rounded published
aggregates. Derived checks are approximate when pairwise sample sizes differ.
No model, causal effect, robust standard error, or missing-data correction is
estimated from raw participant data in this module.

Run: python -m src.reported_evidence_audit
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path

import numpy as np
from scipy import stats


DEFAULT_PATH = Path(__file__).resolve().parents[1] / "evidence" / "manuscript_summary.json"


def audit_reported_summary(summary: dict) -> dict:
    sample = summary["sample"]
    model = summary["model"]
    n, k, resid = (sample["complete_case_ols_n"],
                    model["df_model"], model["df_residual"])
    if resid != n - k - 1:
        raise ValueError("OLS degrees of freedom mismatch.")
    f_stat = float(model["F"])
    r2_implied = (f_stat * k) / (f_stat * k + resid)
    adjusted_implied = 1 - (1 - r2_implied) * (n - 1) / resid

    corr = np.asarray(summary["correlation_pairwise"], dtype=float)
    if corr.shape != (4, 4) or not np.allclose(corr, corr.T):
        raise ValueError("Expected a symmetric 4x4 correlation matrix.")
    if not np.allclose(np.diag(corr), 1):
        raise ValueError("Correlation matrix diagonal must equal one.")
    if np.linalg.eigvalsh(corr).min() <= 0:
        raise ValueError("Correlation matrix must be positive definite.")
    predictors = corr[1:, 1:]
    corr_target = corr[1:, 0]
    implied_beta = np.linalg.solve(predictors, corr_target)
    r2_correlations = float(corr_target @ implied_beta)
    vifs = np.diag(np.linalg.inv(predictors))
    details = []
    for item, beta, vif in zip(summary["coefficients"][1:], implied_beta, vifs):
        t = float(item["t"])
        partial_r2 = t * t / (t * t + resid)
        # Incremental R² from omitting a single regressor in the SAME sample.
        delta_r2 = t * t * (1 - r2_implied) / resid
        details.append({
            "feature": item["variable"],
            "B_reported": float(item["B"]),
            "beta_reported": float(item["standardized_beta"]),
            "beta_implied_by_pairwise_corr_approx": float(beta),
            "VIF_from_pairwise_corr_approx": float(vif),
            "t_reported": t,
            "p_from_reported_t_approx": float(2 * stats.t.sf(abs(t), resid)),
            "partial_r2_from_reported_t": float(partial_r2),
            "incremental_r2_approx": float(delta_r2),
            "CI95_reported": item["CI95"],
        })
    return {
        "provenance": "AUTHOR-SUPPLIED MANUSCRIPT SUMMARY: DERIVED AUDIT, NO RAW DATA",
        "sample_n": n,
        "survey_n": sample["survey_n"],
        "r2_reported": model["R2"],
        "r2_from_reported_F": float(r2_implied),
        "adjusted_r2_from_reported_F": float(adjusted_implied),
        "r2_from_rounded_pairwise_correlations_approx": r2_correlations,
        "omnibus_p_from_reported_F_approx": float(stats.f.sf(f_stat, k, resid)),
        "predictor_checks": details,
        "caveat": (
            "OLS F/t algebra uses rounded manuscript figures. VIF and "
            "standardized coefficient reconstructions use pairwise "
            "correlations with potentially different sample sizes and "
            "should not be mistaken for exact complete-case diagnostics. "
            "No causality, mediation, or original-data replication is claimed."
        ),
    }


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--summary", type=Path, default=DEFAULT_PATH)
    p.add_argument("--output", type=Path, default=None)
    args = p.parse_args()
    audit = audit_reported_summary(json.loads(args.summary.read_text(encoding="utf-8")))
    serialized = json.dumps(audit, indent=2)
    print(serialized)
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(serialized + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
