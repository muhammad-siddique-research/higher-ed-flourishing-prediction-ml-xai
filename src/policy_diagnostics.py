"""Out-of-fold aggregate model diagnostics, with small-cell suppression.

This is NOT a certification of model fairness or permission for individual
student assessment. It never exports student-level predictions.
"""
from __future__ import annotations
import numpy as np
import pandas as pd
from sklearn.base import clone
from sklearn.dummy import DummyRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import GroupKFold, KFold
from sklearn.pipeline import Pipeline
from src.train_and_evaluate import FEATURES, TARGET, get_preprocessor, validate_dataset

AUDIT_FIELDS = ("FIRSTGEN", "GENDER", "FAMINCOME")

def aggregate_error_audit(df: pd.DataFrame, *, audit_field="FIRSTGEN",
                          grouping_id=None, estimator=None, folds=5,
                          min_group_n=20, seed=42):
    if audit_field not in AUDIT_FIELDS:
        raise ValueError("Unsupported audit field.")
    if min_group_n < 20:
        raise ValueError("Minimum reporting cell size must be at least 20.")
    frame = validate_dataset(df)
    if folds < 2 or folds > len(frame):
        raise ValueError("Invalid number of folds.")
    X, y = frame[FEATURES], frame[TARGET].to_numpy(dtype=float)
    model = DummyRegressor() if estimator is None else estimator
    pipe = Pipeline([("prep", get_preprocessor()), ("reg", model)])
    if grouping_id is None:
        splitter = KFold(n_splits=folds, shuffle=True, random_state=seed)
        splits = splitter.split(X, y)
    else:
        if grouping_id not in df.columns:
            raise ValueError("Unknown grouping identifier.")
        groups = df[grouping_id]
        if groups.isna().any() or groups.nunique() < folds:
            raise ValueError("Grouping identifiers missing/insufficient.")
        splits = GroupKFold(n_splits=folds).split(X, y, groups=groups)
    predictions = np.full(len(frame), np.nan)
    for train, test in splits:
        pipeline = clone(pipe).fit(X.iloc[train], y[train])
        predictions[test] = pipeline.predict(X.iloc[test])
    if not np.isfinite(predictions).all():
        raise RuntimeError("Out-of-fold prediction coverage is incomplete.")

    def summarize(label, mask):
        true, pred = y[mask], predictions[mask]
        return {"group": label, "n": int(mask.sum()),
                "MAE": float(mean_absolute_error(true, pred)),
                "RMSE": float(np.sqrt(mean_squared_error(true, pred))),
                "R2": float(r2_score(true, pred))}
    output = [summarize("ALL_OBSERVATIONS", np.ones(len(frame), dtype=bool))]
    categories = frame[audit_field].astype("string")
    for value in sorted(categories.dropna().unique()):
        mask = (categories == value).fillna(False).to_numpy(dtype=bool)
        if int(mask.sum()) >= min_group_n:
            output.append(summarize(f"{audit_field}={value}", mask))
    return pd.DataFrame(output)
