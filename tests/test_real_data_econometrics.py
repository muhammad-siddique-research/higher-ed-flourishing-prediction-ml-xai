"""Econometrics test using generated values only (never manuscript replication)."""
import numpy as np
import pandas as pd
import pytest
from src.real_data_econometrics import assess_ols


def example(n=95, seed=9):
    rng = np.random.default_rng(seed)
    c = rng.uniform(2, 5.7, n)
    i = rng.uniform(2, 5.7, n)
    p = rng.uniform(2, 5.7, n)
    y = np.clip(1.9 + .30 * c + .10 * p
                + rng.normal(0, .24, n), 1, 6)
    return pd.DataFrame({
        "SCOMM": c, "INTEGRITY": i, "SPIR": p, "TQ_MEAN": y,
    })


def test_robust_coefficients_and_nested_decomposition():
    results = assess_ols(example(), bootstrap=55, seed=42)
    assert results["n_complete"] == 95
    assert 0 < results["R2"] < 1
    assert len(results["coefficients"]) == 4
    assert all(x["SE_HC3"] > 0 for x in results["coefficients"])
    assert results["nested_R2"]["SCOMM"]["delta_R2_same_cases"] > 0
    assert results["bootstrap"]["n_valid"] >= 50


def test_missingness_changes_complete_case_n():
    a = example()
    a.loc[:3, "SPIR"] = np.nan
    r = assess_ols(a, bootstrap=0)
    assert r["n_complete"] == len(a) - 4
    assert r["missing_by_variable"]["SPIR"] == 4


def test_invalid_scale_rejected():
    data = example()
    data.loc[0, "TQ_MEAN"] = 8
    with pytest.raises(ValueError, match="1–6"):
        assess_ols(data, bootstrap=0)


def test_small_cluster_count_rejected():
    data = example()
    data["CAMPUS"] = ["only_campus"] * len(data)
    with pytest.raises(ValueError, match="10 independent"):
        assess_ols(data, bootstrap=0, cluster_column="CAMPUS")
