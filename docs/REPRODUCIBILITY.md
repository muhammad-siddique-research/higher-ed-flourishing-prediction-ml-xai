# Reproducibility protocol

## What is reproducible without restricted student records?

- Source-code parsing and synthetic-only unit tests, using GitHub Actions.
- Dataset contract and preprocessing logic.
- Train-only folds, model candidates, evaluation metric computations, and
  optional exploratory XGBoost SHAP generation **when authorized data are supplied**.

This repository does **not** contain the original student-level CSV,
trained model artifacts, executed performance plots, or an externally validated
evaluation report. The historical R²/RMSE/MAE figures in an older README
therefore cannot be reproduced from the current files alone.

## Setup

```bash
git clone https://github.com/muhammad-siddique-research/higher-ed-flourishing-prediction-ml-xai.git
cd higher-ed-flourishing-prediction-ml-xai
python -m venv .venv
# activate the environment before installing
python -m pip install -r requirements.txt
python -m pip install pytest
python -m pytest -q
```

## Authorized data analysis

Keep the original CSV in an approved, non-public location. Use the documented
schema in [data/README.md](../data/README.md).

```bash
python -m src.train_and_evaluate --data /secure/path/student_thriving.csv --folds 10
```

If students or institutions recur across observations, prefer:

```bash
python -m src.train_and_evaluate --data /secure/path/student_thriving.csv --folds 5 --group-column STUDENT_ID
```

To generate an *exploratory, full-sample* SHAP plot, append `--shap`. This
plot explains a fitted model; it is **not** an out-of-sample performance metric
or a causal estimate. Results go to `results/cross_validation_metrics.csv`,
`results/run_metadata.json`, and optionally `results/figures/shap_summary.png`.

## Benchmark specifications

- Missing numeric values: median imputation; continuous/ordinal predictors
  standardized in each training fold.
- Missing categorical values: most-frequent imputation; one-hot coding
  with unknown-category handling inside each training fold.
- Candidate regressors: mean-only baseline, ElasticNetCV (inner five-fold
  tuning), Random Forest, XGBoost, and LightGBM.
- Outer evaluation: ten shuffled folds, fixed random state 42, unless
  group-disjoint evaluation is specifically requested.
- Summary: fold-wise averages and standard deviations for R², RMSE, and MAE.

**Caution:** A random split is insufficient if the same student, instructor,
institution, or cohort appears on both sides of a fold. Outer ten-fold CV is
not a test of prediction at a new campus or in a future academic year.
The comparison is not nested hyperparameter optimization across all models;
only ElasticNetCV includes automatic inner tuning here.

## Reporting checklist

Specify dataset provenance, license, IRB/authorization status, sample size,
target scoring, missingness, actual category labels, preprocessing, group
structure, benchmark code version, fold-level uncertainty, baseline comparison,
and limitations. Report SHAP with measurement and dependence caveats.
Do not reuse historical values without matching artifacts.
