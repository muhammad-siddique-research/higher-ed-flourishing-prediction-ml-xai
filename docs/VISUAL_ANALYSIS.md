# Visual evidence | Flourishing ML and explainability laboratory

> **RESEARCH DEMONSTRATION — SIMULATED DATA ONLY.**
> These outputs reflect a reproducible simulation, **not** an empirical sample
> of undergraduates, validated Thriving Quotient scores, or a deployed policy model.

## 1. Model evaluation: regularization and gradient-boosted trees

![SYNTHETIC model comparison: ElasticNet, XGBoost, LightGBM, Random Forest and mean-only baseline](figures/SYNTHETIC_model_comparison.png)

**Figure 1.** Out-of-group, three-fold RMSE comparison across five regression
configurations on 240 generated records distributed across 12 fictitious
campuses. Lower RMSE indicates smaller prediction errors; bars and uncertainty
whiskers describe only the predefined synthetic experiment.

| Model | Mean cross-validated R² | RMSE | MAE |
|---|---:|---:|---:|
| **ElasticNet (fixed-penalty; grouped CV)** | **0.641** | **0.417** | **0.338** |
| Random Forest | 0.601 | 0.440 | 0.349 |
| LightGBM | 0.585 | 0.449 | 0.365 |
| XGBoost | 0.579 | 0.453 | 0.355 |
| Mean-only baseline | −0.009 | 0.700 | 0.571 |

**Interpretation:** On the *mathematically specified synthetic signal*,
ElasticNet performs best by RMSE. This does not imply ElasticNet is preferable
for observed students. It illustrates why an advanced computational analysis
should include a simple baseline, regularized regression, and an evaluation
of complexity rather than assume boosted trees must win.

[Inspect the reproducible summary metrics](figures/SYNTHETIC_model_metrics.csv) ·
[Inspect the fold-level results](figures/SYNTHETIC_fold_metrics.csv)

## 2. Tree SHAP: explanations of synthetic XGBoost predictions

![SYNTHETIC XGBoost Tree SHAP beeswarm demonstrating feature attribution](figures/SYNTHETIC_tree_shap.png)

**Figure 2.** XGBoost Tree SHAP summary from the **full synthetic example**.
Each dot represents a generated observation and a feature contribution to
the fitted model output. The horizontal position is the SHAP value; color
indicates the corresponding feature level (for encoded binary features,
low/high correspond to the encoded feature value).

**Interpretation:** The widest attributions occur for simulated sense of
community (`SCOMM`) and selected institutional/purpose predictors. Those
patterns are expected because the simulation deliberately assigns these
variables larger predictive roles. The graph is **not an external-validation
figure** or proof of real-world psychosocial mechanisms.

SHAP quantifies how a model allocates predictions across supplied features.
It does not establish that changing belonging, spirituality, institutional
integrity, or any demographic measure will *cause* a change in flourishing.
Causal claims would require a separate research design.

## 3. From model diagnostics to higher-education policy

The code demonstrates three separable kinds of reasoning:

1. **Predictive validity** requires train-fold preprocessing, holdout results,
   mean-only baselines, and uncertainty across campuses or cohorts.
2. **Explanatory transparency** can diagnose a fitted model with SHAP,
   conditional on feature coding, dependence structure, and data provenance.
3. **Policy effectiveness** must be evaluated separately: a feature ranked
   highly by SHAP is not automatically an intervention target.

For genuine institutional research, document the original survey instrument,
psychometric validity, lawful use of student data, representativeness, missing
data, group-level uncertainty, external transportability, and accessibility
before deriving any student-support policy recommendations.

## 4. Provenance and reproducibility

- Generator: [`examples/synthetic_demo.py`](../examples/synthetic_demo.py).
- Machine-learning and SHAP implementation:
  [`src/train_and_evaluate.py`](../src/train_and_evaluate.py).
- Publication pipeline:
  [GitHub Actions synthetic demonstration](../.github/workflows/synthetic-demo.yml).
- Data: 240 generated records; 12 fake campuses; random seed 42.
- Methods: mean baseline, fixed-penalty ElasticNet under group-disjoint folds,
  Random Forest, XGBoost, LightGBM, and post-fit Tree SHAP.
- Artifact status: synthetic figures and summary CSVs committed by the
  verified CI workflow; no individual or real student data are published.

Also see the [model card](MODEL_CARD.md), [research design](RESEARCH_DESIGN.md),
[data governance protocol](DATA_GOVERNANCE.md), and
[educational policy brief](EDUCATION_POLICY_BRIEF.md).
