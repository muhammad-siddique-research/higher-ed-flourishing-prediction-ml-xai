"""Unit tests use fully synthetic observations; not study validation."""
import numpy as np
import pandas as pd
import pytest
from sklearn.dummy import DummyRegressor
from examples.synthetic_demo import make_synthetic_sample
from src.train_and_evaluate import run_benchmarks
from src.policy_diagnostics import aggregate_error_audit

def test_synthetic_generation_is_deterministic():
    a = make_synthetic_sample(72, seed=7)
    pd.testing.assert_frame_equal(a, make_synthetic_sample(72, seed=7))
    assert a["TQ_MEAN"].between(1, 6).all()
    assert a["CAMPUS_ID"].nunique() == 12

def test_foldwise_metrics_are_preserved():
    result = run_benchmarks(
        make_synthetic_sample(72), folds=3,
        models={"synthetic_dummy": DummyRegressor()})
    assert len(result.attrs["fold_metrics"]) == 3
    assert np.isclose(result["rmse_mean"].iat[0],
                      result.attrs["fold_metrics"]["rmse"].mean())

def test_out_of_fold_subgroup_audit():
    frame = make_synthetic_sample(120)
    result = aggregate_error_audit(frame, folds=3, min_group_n=20)
    assert "ALL_OBSERVATIONS" in result["group"].tolist()
    assert result["n"].max() == 120
    assert result["RMSE"].ge(0).all()
    assert "individual_prediction" not in result.columns

def test_small_group_suppression():
    frame = make_synthetic_sample(72)
    frame["FIRSTGEN"] = 0
    frame.loc[:9, "FIRSTGEN"] = 1
    result = aggregate_error_audit(frame, folds=3, min_group_n=20)
    assert not result["group"].str.contains("FIRSTGEN=1").any()

def test_small_cell_limit_enforced():
    with pytest.raises(ValueError, match="at least 20"):
        aggregate_error_audit(make_synthetic_sample(72), min_group_n=10)
