"""Reproducible, association-focused flourishing regression benchmark.

This module does not identify causal effects. No student dataset is distributed.
Run: python -m src.train_and_evaluate --data /secure/path/study.csv
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.dummy import DummyRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.linear_model import ElasticNet, ElasticNetCV
from sklearn.model_selection import GroupKFold, KFold, cross_validate
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

NUMERIC_FEATURES = ["SCOMM", "INTEGRITY", "SPIR", "TUITION", "FIT"]
CATEGORICAL_FEATURES = ["FIRSTGEN", "GENDER", "FAMINCOME"]
FEATURES = NUMERIC_FEATURES + CATEGORICAL_FEATURES
TARGET = "TQ_MEAN"
SEED = 42


def validate_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """Check schema and target without filling or inventing observations."""
    missing = sorted(set(FEATURES + [TARGET]) - set(df.columns))
    if missing:
        raise ValueError(f"Dataset missing required columns: {', '.join(missing)}")
    if len(df) < 30:
        raise ValueError("At least 30 labeled records required for this benchmark.")
    clean = df.copy()
    for col in NUMERIC_FEATURES + [TARGET]:
        clean[col] = pd.to_numeric(clean[col], errors="coerce")
    if clean[TARGET].isna().any():
        raise ValueError("Target contains missing/non-numeric values; resolve before modeling.")
    if not np.isfinite(clean[TARGET].to_numpy()).all():
        raise ValueError("Target contains non-finite values.")
    if not clean[TARGET].between(1, 6).all():
        raise ValueError("TQ_MEAN must lie in the documented 1-to-6 scale.")
    if clean[TARGET].nunique() < 2:
        raise ValueError("Target has no variation; R-squared cannot be evaluated.")
    for col in NUMERIC_FEATURES:
        clean[col] = clean[col].replace([np.inf, -np.inf], np.nan)
        if clean[col].isna().all():
            raise ValueError(f"Numeric predictor {col} has no observed values.")
    for col in CATEGORICAL_FEATURES:
        clean[col] = clean[col].astype("string").replace({"": pd.NA})
        if clean[col].isna().all():
            raise ValueError(f"Categorical predictor {col} has no observed values.")
        # str (not pandas extension NA) is required for some sklearn encoders.
        clean[col] = clean[col].astype(object).where(clean[col].notna(), np.nan)
    return clean


def get_preprocessor() -> ColumnTransformer:
    """Fit imputers and encoders inside each training fold to avoid leakage."""
    numeric = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler()),
    ])
    categorical = Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("encoder", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
    ])
    return ColumnTransformer([
        ("numeric", numeric, NUMERIC_FEATURES),
        ("categorical", categorical, CATEGORICAL_FEATURES),
    ])


def make_models(seed: int = SEED) -> dict:
    """Explicit baselines and candidate models; no unreported tuning claimed."""
    from lightgbm import LGBMRegressor
    from xgboost import XGBRegressor

    return {
        "Mean-only baseline": DummyRegressor(strategy="mean"),
        "ElasticNetCV": ElasticNetCV(cv=5, random_state=seed, max_iter=10000),
        "Random Forest": RandomForestRegressor(
            n_estimators=300, max_depth=6, random_state=seed, n_jobs=1
        ),
        "XGBoost": XGBRegressor(
            n_estimators=250, learning_rate=0.03, max_depth=4,
            random_state=seed, n_jobs=1, objective="reg:squarederror"
        ),
        "LightGBM": LGBMRegressor(
            n_estimators=250, learning_rate=0.03, max_depth=4,
            random_state=seed, verbosity=-1, n_jobs=1
        ),
    }


def run_benchmarks(
    df: pd.DataFrame,
    *,
    folds: int = 10,
    seed: int = SEED,
    group_column: str | None = None,
    models: dict | None = None,
) -> pd.DataFrame:
    """Evaluate by R2, RMSE, and MAE using identical held-out CV folds.

    For repeated students or institutions, provide --group-column. A single
    cross-validation result is not an external-site or temporal validation.
    """
    clean = validate_dataset(df)
    if folds < 2 or folds > len(clean):
        raise ValueError("Fold count must be between 2 and the number of records.")
    groups = None
    if group_column:
        if group_column not in df.columns:
            raise ValueError(f"Group column {group_column!r} not found.")
        groups = df[group_column]
        if groups.isna().any():
            raise ValueError("Group column contains missing IDs.")
        if groups.nunique() < folds:
            raise ValueError("Not enough distinct groups for GroupKFold.")
        cv = GroupKFold(n_splits=folds)
    else:
        cv = KFold(n_splits=folds, shuffle=True, random_state=seed)
    X, y = clean[FEATURES], clean[TARGET]
    candidates = make_models(seed) if models is None else models
    # Group-aware outer folds require group-aware inner selection, which
    # ElasticNetCV does not receive through this interface. Avoid leakage by
    # using a documented fixed-penalty ElasticNet for grouped experiments.
    if group_column and models is None:
        candidates.pop("ElasticNetCV")
        candidates["ElasticNet (fixed; group-safe)"] = ElasticNet(
            alpha=0.10, l1_ratio=0.5, max_iter=10000
        )
    rows = []
    fold_rows = []
    for name, estimator in candidates.items():
        pipeline = Pipeline([
            ("prep", get_preprocessor()),
            ("reg", estimator),
        ])
        metrics = cross_validate(
            pipeline, X, y, cv=cv, groups=groups, error_score="raise",
            scoring={
                "r2": "r2",
                "rmse": "neg_root_mean_squared_error",
                "mae": "neg_mean_absolute_error",
            },
        )
        r2 = metrics["test_r2"]
        rmse = -metrics["test_rmse"]
        mae = -metrics["test_mae"]
        fold_rows.extend({
            "model": name, "fold": j,
            "r2": float(r2[j]), "rmse": float(rmse[j]),
            "mae": float(mae[j]),
        } for j in range(folds))
        rows.append({
            "model": name,
            "n_records": len(clean),
            "n_folds": folds,
            "r2_mean": float(np.mean(r2)),
            "r2_sd": float(np.std(r2, ddof=1)),
            "rmse_mean": float(np.mean(rmse)),
            "rmse_sd": float(np.std(rmse, ddof=1)),
            "mae_mean": float(np.mean(mae)),
            "mae_sd": float(np.std(mae, ddof=1)),
        })
    table = pd.DataFrame(rows).sort_values("rmse_mean").reset_index(drop=True)
    table.attrs["fold_metrics"] = pd.DataFrame(fold_rows)
    return table


def run_shap_explanation(df: pd.DataFrame, output_dir: Path) -> Path:
    """Exploratory full-sample XGBoost attribution, NOT a causal effect."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import shap
    from xgboost import XGBRegressor

    clean = validate_dataset(df)
    X = clean[FEATURES]
    prep = get_preprocessor().fit(X)
    matrix = prep.transform(X)
    model = XGBRegressor(
        n_estimators=250, learning_rate=0.03, max_depth=4, random_state=SEED,
        objective="reg:squarederror", n_jobs=1,
    ).fit(matrix, clean[TARGET])
    explainer = shap.TreeExplainer(model)
    values = explainer.shap_values(matrix)
    output_dir.mkdir(parents=True, exist_ok=True)
    destination = output_dir / "shap_summary.png"
    shap.summary_plot(
        values, matrix, feature_names=prep.get_feature_names_out(),
        show=False, max_display=15,
    )
    plt.tight_layout()
    plt.savefig(destination, dpi=180, bbox_inches="tight")
    plt.close("all")
    return destination


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, required=True, help="Authorized private CSV")
    parser.add_argument("--output-dir", type=Path, default=Path("results"))
    parser.add_argument("--folds", type=int, default=10)
    parser.add_argument("--group-column", default=None,
                        help="Student/institution ID for group-disjoint folds")
    parser.add_argument("--shap", action="store_true",
                        help="Add EXPLORATORY full-data XGBoost SHAP plot")
    args = parser.parse_args()
    if not args.data.is_file():
        parser.error(
            f"Dataset not found: {args.data}. This repo intentionally has no student-level dataset. "
            "Provide an authorized CSV after reviewing the data-governance guidance."
        )
    raw = pd.read_csv(args.data)
    results = run_benchmarks(raw, folds=args.folds, group_column=args.group_column)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    results.to_csv(args.output_dir / "cross_validation_metrics.csv", index=False)
    results.attrs["fold_metrics"].to_csv(
        args.output_dir / "fold_level_metrics.csv", index=False
    )
    provenance = {
        "dataset_filename_only": args.data.name,
        "dataset_supplied_by_researcher": True,
        "row_count": int(len(raw)),
        "folds": args.folds,
        "seed": SEED,
        "validation": "group-disjoint GroupKFold" if args.group_column else "random KFold",
        "group_column": args.group_column,
        "regularization": (
            "fixed-penalty ElasticNet for grouped folds"
            if args.group_column else "ElasticNetCV tuned within training folds"
        ),
        "scoring": ["r2", "rmse", "mae"],
        "note": "Associational prediction only; outputs do not establish causal effects.",
    }
    (args.output_dir / "run_metadata.json").write_text(
        json.dumps(provenance, indent=2), encoding="utf-8"
    )
    print(results.to_string(index=False))
    if args.shap:
        path = run_shap_explanation(raw, args.output_dir / "figures")
        print(f"Exploratory SHAP plot saved to: {path}")


if __name__ == "__main__":
    main()
