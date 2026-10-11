"""Tests reconstruct real-study *reported aggregates*, not primary observations."""
import json
from pathlib import Path

import numpy as np
import pytest

from src.reported_evidence_audit import audit_reported_summary


EVIDENCE = Path(__file__).resolve().parents[1] / "evidence" / "manuscript_summary.json"


def summary():
    return json.loads(EVIDENCE.read_text(encoding="utf-8"))


def test_ols_model_algebra_reconciles_to_report():
    result = audit_reported_summary(summary())
    assert result["sample_n"] == 152
    assert abs(result["r2_from_reported_F"] - .436) < .001
    assert abs(result["adjusted_r2_from_reported_F"] - .424) < .001
    assert abs(result["r2_from_rounded_pairwise_correlations_approx"] - .436) < .003


def test_vif_and_conditional_unique_information_are_reconstructable():
    d = {x["feature"]: x for x in audit_reported_summary(summary())["predictor_checks"]}
    assert abs(d["SCOMM"]["VIF_from_pairwise_corr_approx"] - 1.792) < .02
    assert .25 < d["SCOMM"]["partial_r2_from_reported_t"] < .26
    assert .002 < d["INTEGRITY"]["partial_r2_from_reported_t"] < .004
    assert .044 < d["SPIR"]["partial_r2_from_reported_t"] < .046
    assert d["INTEGRITY"]["incremental_r2_approx"] < .002


def test_malformed_summary_is_rejected():
    corrupted = summary()
    corrupted["model"]["df_residual"] = 100
    with pytest.raises(ValueError, match="degrees of freedom"):
        audit_reported_summary(corrupted)
