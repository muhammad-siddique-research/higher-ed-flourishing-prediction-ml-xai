# Visualization provenance

## Two distinct evidence categories

**Reported real-world study:** SVGs named `REPORTED_*` visualize
coefficients and correlations transcribed from the author's actual survey
draft (N=156, OLS n=152). `DERIVED_unique_explanatory_contributions.svg`
is an algebraic reconstruction from those reported summary statistics.
None requires or reproduces the restricted participant-level CSV.
See [Real-study evidence](../EMPIRICAL_EVIDENCE.md).

**Executable synthetic ML/XAI demonstration:** Files beginning with
`SYNTHETIC_` are mathematical simulations and must not be interpreted
as observed student outcomes, causal effects or deployed model performance.

All **synthetic** figures below were automatically generated
by [the executable demonstration](../../examples/synthetic_demo.py) through
[the GitHub Actions workflow](../../.github/workflows/synthetic-demo.yml).

- `SYNTHETIC_model_comparison.png`: three-fold group-disjoint regression benchmark on 240 generated records from 12 fictitious campus groups.
- `SYNTHETIC_tree_shap.png`: XGBoost Tree SHAP beeswarm computed on those same simulated records. The plot is a *full-sample explanation*, **not an out-of-fold accuracy measure**.
- `SYNTHETIC_model_metrics.csv`: summary R², RMSE, and MAE for the five demonstration models.
- `SYNTHETIC_fold_metrics.csv`: per-fold evaluation metrics for the same synthetic benchmark.

**Important:** The data and coefficients are mathematical constructs. These
figures do not validate the Thriving Quotient scale, characterize real
undergraduates, or establish model superiority in actual institutional data.
Feature attribution is not a causal effect or student-support prescription.

The source student dataset is not distributed in this repository. Real-world
evidence requires permissioned empirical replication and external validation.
