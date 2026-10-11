"""Unit tests use synthetic records ONLY; they do not verify research findings."""
import numpy as np
import pandas as pd
import pytest
from sklearn.dummy import DummyRegressor

from src.train_and_evaluate import (
    FEATURES, TARGET, get_preprocessor, run_benchmarks, validate_dataset,
)


def toy_frame(n=60):
    rng = np.random.default_rng(42)
    data = {
        "SCOMM": rng.uniform(1, 6, n),
        "INTEGRITY": rng.uniform(1, 6, n),
        "SPIR": rng.uniform(1, 6, n),
        "TUITION": rng.integers(1, 6, n),
        "FIT": rng.integers(1, 6, n),
        "FIRSTGEN": rng.integers(0, 2, n),
        "GENDER": rng.integers(0, 2, n),
        "FAMINCOME": rng.integers(1, 6, n),
        "TQ_MEAN": rng.uniform(2, 5.8, n),
        "STUDENT_ID": [f"student-{i // 2}" for i in range(n)],
    }
    return pd.DataFrame(data)


def test_expected_schema_and_bounds():
    valid = validate_dataset(toy_frame())
    assert set(FEATURES).issubset(valid.columns)
    assert valid[TARGET].between(1, 6).all()


def test_no_target_in_preprocessing_and_missing_predictor_imputed():
    df = toy_frame()
    df.loc[1, "SCOMM"] = np.nan
    df.loc[2, "GENDER"] = np.nan
    transformed = get_preprocessor().fit_transform(validate_dataset(df)[FEATURES])
    assert transformed.shape[0] == len(df)
    assert np.isfinite(transformed).all()


def test_missing_target_rejected():
    df = toy_frame()
    df.loc[0, TARGET] = np.nan
    with pytest.raises(ValueError, match="Target"):
        validate_dataset(df)


def test_cv_is_executable_without_fabricating_performance():
    results = run_benchmarks(
        toy_frame(), folds=3,
        models={"synthetic-test baseline": DummyRegressor()},
    )
    assert len(results) == 1
    assert results.iloc[0]["n_folds"] == 3
    assert np.isfinite(results.iloc[0]["rmse_mean"])


def test_group_disjoint_cv():
    results = run_benchmarks(
        toy_frame(), folds=3, group_column="STUDENT_ID",
        models={"synthetic-test baseline": DummyRegressor()},
    )
    assert len(results) == 1


def test_out_of_bounds_target_rejected():
    df = toy_frame()
    df.loc[0, TARGET] = 8.0
    with pytest.raises(ValueError, match="1-to-6"):
        validate_dataset(df)
