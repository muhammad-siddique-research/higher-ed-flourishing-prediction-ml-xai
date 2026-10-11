"""Advanced, observational econometric robustness analyses on AUTHORIZED data.

This does NOT use the manuscript's unavailable raw dataset. Analysts must
supply a legally accessible CSV in a private environment. Outputs contain
aggregate coefficients and diagnostics only, never participant-level data.

Usage:
 python -m src.real_data_econometrics --data /secure/study.csv --output-dir results/ols
 python -m src.real_data_econometrics --data /secure/study.csv --bootstrap 1000
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.stats.diagnostic import het_breuschpagan, linear_reset
from statsmodels.stats.outliers_influence import variance_inflation_factor

OUTCOME = "TQ_MEAN"
PREDICTORS = ["SCOMM", "INTEGRITY", "SPIR"]
SEED = 42


def assess_ols(df: pd.DataFrame, *, bootstrap: int = 500,
               seed: int = SEED, cluster_column: str | None = None):
    """Fit complete-case OLS, HC3, sensitivity and influence diagnostics.

    Never treat coefficients as causal. The robust SE, quantile and bootstrap
    values require actual authorized participant-level data. Missingness is
    summarized; assumptions for missing-at-random are not claimed.
    """
    missing = sorted(set(PREDICTORS + [OUTCOME]) - set(df.columns))
    if missing:
        raise ValueError("Required survey composites missing: " + ", ".join(missing))
    if bootstrap < 0 or bootstrap > 10000:
        raise ValueError("bootstrap must be from 0 to 10000")
    frame = df.copy()
    for feature in PREDICTORS + [OUTCOME]:
        frame[feature] = pd.to_numeric(frame[feature], errors="coerce")
        frame[feature] = frame[feature].replace([np.inf, -np.inf], np.nan)
    available = frame[PREDICTORS + [OUTCOME]].notna().all(axis=1)
    complete = frame.loc[available].copy()
    if len(complete) < 30:
        raise ValueError("At least 30 complete cases required for this analysis.")
    for field in PREDICTORS + [OUTCOME]:
        if not complete[field].between(1, 6).all():
            raise ValueError(f"{field} contains values outside the documented 1–6 scale.")
        if complete[field].nunique() < 3:
            raise ValueError(f"{field} has insufficient variability.")

    y = complete[OUTCOME].to_numpy(dtype=float)
    X = sm.add_constant(complete[PREDICTORS].astype(float), has_constant="add")
    if np.linalg.matrix_rank(X.to_numpy()) != X.shape[1]:
        raise ValueError("Design matrix lacks full rank.")
    ols = sm.OLS(y, X).fit()
    hc3 = ols.get_robustcov_results(cov_type="HC3")
    ols_index = list(X.columns)
    base_results = []
    ci_ols = ols.conf_int()
    ci_hc3 = hc3.conf_int()
    for j, name in enumerate(ols_index):
        base_results.append({
            "predictor": name,
            "B": float(ols.params.iloc[j]),
            "SE_classical": float(ols.bse.iloc[j]),
            "p_classical": float(ols.pvalues.iloc[j]),
            "CI95_classical_low": float(ci_ols.iloc[j, 0]),
            "CI95_classical_high": float(ci_ols.iloc[j, 1]),
            "SE_HC3": float(hc3.bse[j]),
            "p_HC3": float(hc3.pvalues[j]),
            "CI95_HC3_low": float(ci_hc3[j, 0]),
            "CI95_HC3_high": float(ci_hc3[j, 1]),
        })
    vif = {
        feature: float(variance_inflation_factor(X.to_numpy(), j + 1))
        for j, feature in enumerate(PREDICTORS)
    }
    lm_stat, lm_p, f_stat, f_p = het_breuschpagan(
        ols.resid, ols.model.exog
    )
    # Ramsey RESET is a functional-form diagnostic, not a proof of truth.
    try:
        reset = linear_reset(ols, power=2, use_f=True)
        reset_p = float(reset.pvalue)
    except (ValueError, np.linalg.LinAlgError):
        reset_p = None
    influence = ols.get_influence()
    cooks = influence.cooks_distance[0]
    full_r2 = float(ols.rsquared)
    incremental = {}
    for feature in PREDICTORS:
        others = [f for f in PREDICTORS if f != feature]
        reduced = sm.OLS(y, sm.add_constant(complete[others],
                                          has_constant="add")).fit()
        incremental[feature] = {
            "R2_reduced": float(reduced.rsquared),
            "delta_R2_same_cases": float(full_r2 - reduced.rsquared),
        }
    out = {
        "provenance": "AUTHORIZED PRIMARY DATA — COMPLETE CASE ASSOCIATIONAL OLS",
        "data_source": "supplied privately by authorized researcher",
        "n_received": len(frame),
        "n_complete": len(complete),
        "missing_by_variable": {
            name: int(frame[name].isna().sum())
            for name in PREDICTORS + [OUTCOME]
        },
        "n_clusters": None,
        "R2": full_r2,
        "adjusted_R2": float(ols.rsquared_adj),
        "F": float(ols.fvalue),
        "F_p": float(ols.f_pvalue),
        "df_resid": int(ols.df_resid),
        "coefficients": base_results,
        "vif": vif,
        "nested_R2": incremental,
        "diagnostics": {
            "Breusch_Pagan_LM": float(lm_stat),
            "Breusch_Pagan_p": float(lm_p),
            "Breusch_Pagan_F_p": float(f_p),
            "RESET_p": reset_p,
            "Durbin_Watson_descriptive_only": float(
                sm.stats.stattools.durbin_watson(ols.resid)
            ),
            "max_Cooks_D": float(np.max(cooks)),
            "n_Cooks_D_above_4_over_n": int((cooks > 4 / len(complete)).sum()),
        },
        "limitations": (
            "Single-time-point observational survey. No causal identification, "
            "validated mediation, proof of missing at random, or transportability "
            "to other institutions is implied. Coefficients may depend on "
            "missingness, measurement and response selection. Residual ordering "
            "makes the Durbin-Watson statistic non-diagnostic for arbitrary "
            "cross-sectional records."
        ),
    }

    if cluster_column is not None:
        if cluster_column not in df.columns:
            raise ValueError(f"Unknown cluster column: {cluster_column}")
        groups = df.loc[available, cluster_column]
        if groups.isna().any():
            raise ValueError("Cluster identifiers must be observed on every complete case.")
        if groups.nunique() < 10:
            raise ValueError("At least 10 independent clusters required for this basic cluster-robust reporting option.")
        clustered = ols.get_robustcov_results(
            cov_type="cluster", groups=groups.to_numpy()
        )
        out["n_clusters"] = int(groups.nunique())
        out["cluster_robust"] = [
            {"predictor": name, "SE": float(clustered.bse[j]),
             "p": float(clustered.pvalues[j])}
            for j, name in enumerate(ols_index)
        ]
        out["cluster_warning"] = (
            "Conventional cluster-robust inference is approximate with modest "
            "cluster counts; consult small-sample adjusted or wild bootstrap "
            "methods if applicable."
        )

    if bootstrap:
        rng = np.random.default_rng(seed)
        matrix = X.to_numpy(dtype=float)
        replicates = []
        for _ in range(bootstrap):
            rowids = rng.integers(0, len(complete), len(complete))
            if np.linalg.matrix_rank(matrix[rowids]) == matrix.shape[1]:
                estimates = np.linalg.lstsq(matrix[rowids],
                                             y[rowids], rcond=None)[0]
                replicates.append(estimates)
        if len(replicates) < max(20, int(bootstrap * 0.90)):
            raise RuntimeError("Too few full-rank bootstrap samples.")
        distribution = np.asarray(replicates)
        out["bootstrap"] = {
            "method": "case-resampling, percentile confidence interval",
            "n_requested": bootstrap,
            "n_valid": len(distribution),
            "seed": seed,
            "coefficient_CI95": [
                {"predictor": name,
                 "low": float(np.percentile(distribution[:, j], 2.5)),
                 "high": float(np.percentile(distribution[:, j], 97.5))}
                for j, name in enumerate(ols_index)
            ],
            "limitations": "Resampling assumes observational rows are independent; bootstrap intervals are associational.",
        }
    return out


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, default=Path("results/ols"))
    parser.add_argument("--bootstrap", type=int, default=500)
    parser.add_argument("--cluster-column", default=None)
    args = parser.parse_args()
    if not args.data.is_file():
        parser.error("Original authorized student CSV not found. A manuscript summary is not participant-level data.")
    outcome = assess_ols(
        pd.read_csv(args.data), bootstrap=args.bootstrap,
        cluster_column=args.cluster_column,
    )
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "econometric_robustness.json").write_text(
        json.dumps(outcome, indent=2) + "\n", encoding="utf-8"
    )
    pd.DataFrame(outcome["coefficients"]).to_csv(
        args.output_dir / "econometric_coefficients.csv", index=False
    )
    print(json.dumps({
        "n": outcome["n_complete"],
        "R2": outcome["R2"],
        "adjusted_R2": outcome["adjusted_R2"],
        "coefficients": outcome["coefficients"],
        "notice": "Observational estimates only; no causal policy claims.",
    }, indent=2))


if __name__ == "__main__":
    main()
