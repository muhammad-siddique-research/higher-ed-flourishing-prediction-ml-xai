# Reproducibility protocol

## What is reproducible without restricted student records?

- Source-code parsing and synthetic-only unit tests, using GitHub Actions.
- Dataset contract and preprocessing logic.
- Train-only folds, model candidates, evaluation metric computations, and
  optional exploratory XGBoost SHAP generation **when authorized data are supplied**.

This repository does **not** distribute the original participant-level
SPSS dataset, trained respondent-level models, or any externally validated
generalization report. It **does contain original-data aggregate cross-
validation metrics and aggregate SHAP figures**, obtained from the
author's private analysis and documented at
[REAL_DATA_VALIDATION.md](REAL_DATA_VALIDATION.md). The public
evidence CSVs can be inspected, but the original private data are required
to rerun their estimators independently. Older, historically unverified
README figures must not replace the newest aggregate evidence.

## Distinct original-data evidence and synthetic software benchmarks

- **Real, restricted observations:** N=156, complete-case n=152. Original
  study uses 5x-repeated 5-fold CV with fixed model configurations and
  held-out Tree SHAP on the first repetition; aggregates and method
  provenance are in [REAL_DATA_VALIDATION.md](REAL_DATA_VALIDATION.md)
  and `evidence/REAL_STUDY_*.csv`.
- **Synthetic CI demonstrations:** The checked-in runnable simulation
  uses fictitious observations and documents its own hyperparameters
  and group-disjoint validation. It does not validate the private study.
- **General authorized-data estimator:** The commands below are a
  separate implementation whose predictors/partitions may differ from
  the private original-data study. Running them with new data is
  **not** a replication of the paper unless the original documented
  specifications are matched.

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
or a causal estimate. Results go to `results/cross_validation_metrics.csv` and `results/fold_level_metrics.csv`,
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
The comparison is not nested hyperparameter optimization across all models. ElasticNetCV uses inner training CV only for ordinary KFold. For group-disjoint CV, the pipeline instead uses a documented fixed-penalty ElasticNet, avoiding ungrouped inner-model selection; future work can add explicitly grouped nested tuning.

## Reporting checklist

Specify dataset provenance, license, IRB/authorization status, sample size,
target scoring, missingness, actual category labels, preprocessing, group
structure, benchmark code version, fold-level uncertainty, baseline comparison,
and limitations. Report SHAP with measurement and dependence caveats.
Do not reuse historical values without matching artifacts.


## Clearly labeled synthetic demonstration

Run `python -m examples.synthetic_demo` and optionally add `--shap`.
Outputs are hypothetical and written under ignored `demo_outputs/`.
These test computational methods, not actual educational findings.

The `src/policy_diagnostics.py` utility reports aggregate out-of-fold
subgroup errors while suppressing any subgroup smaller than 20. Such
diagnostics do not establish model fairness or causal intervention effects.
