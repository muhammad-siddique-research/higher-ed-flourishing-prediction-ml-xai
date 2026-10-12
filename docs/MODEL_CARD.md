# Model card | Student flourishing econometrics and explainable predictive modeling

**Status:** Original-data exploratory research results now documented through
private SPSS reanalysis and [published aggregate evidence](REAL_DATA_VALIDATION.md).
Cross-validation is internal to one small institutional cohort. **No validated
student-risk model, causal effect, external transportability, or deployed service.**

## Evidence tiers

- **Actual restricted survey:** N = 156 original cases; n = 152 complete
  cases. OLS replicated with HC3 sensitivity; seven-model predictive benchmark
  used 25 matched held-out folds and aggregate withheld-case SHAP. Source
  participant records are not distributed.
- **Aggregate public research:** Original-data regression summaries, CV
  metrics, SHAP feature-importance summary, and publication-safe SVG figures
  at [REAL_DATA_VALIDATION.md](REAL_DATA_VALIDATION.md).
- **Synthetic software demonstrations:** Source tests and GitHub Actions
  show that modeling and SHAP routines execute on generated example data.
  These results must not be confused with the original survey.
- **Further external work:** Instrument and fairness assessment, new cohorts
  and institutions, and prospective educational policy evaluation remain
  necessary.

## Research objective and context

Explore whether an undergraduate Thriving Quotient (TQ) composite can be
predicted from sense of community, institutional integrity, purpose/spirituality,
institutional fit, tuition-value perceptions, and student background measures.
Predictive association is **not** causal identification.

## Intended use

Research-method demonstration, model benchmarking, scholarly collaboration,
and transparent discussion of institutional data governance. This repository
is *not* an operational risk scoring or automated student-support system.

## Original-data analysis versus generic software pipeline

The original-data manuscript analysis compared seven configurations:
mean-only, OLS, Ridge, ElasticNet, Random Forest, XGBoost, LightGBM.
It used repeated 5-fold CV (5 repetitions) on n=152 complete cases,
and first-repetition held-out Tree SHAP. See
[original-data validation](REAL_DATA_VALIDATION.md). The generic software
pipeline below is a separate implementation with its own parameter and
fold settings; its outputs should not be identified as exact replications
of those private original-data results.

## Architecture and evaluation

- **Outcome:** Project-described TQ_MEAN, continuous 1–6 scale; original
  24-item survey scoring and psychometric properties are not provided.
- **Models:** mean-only benchmark, ElasticNetCV, Random Forest,
  XGBoost and LightGBM.
- **Preprocessing:** numeric median imputation and standardization,
  categorical most-frequent imputation and one-hot encoding,
  all fitted on training folds only.
- **Validation:** shuffled ten-fold CV, or group-disjoint CV where
  repeated people/institutions require it.
- **Outcomes:** R², RMSE and MAE with fold-level records.
- **Explainability:** optional Tree SHAP for XGBoost, which attributes
  model predictions, not causes or treatment effects.
- **Synthetic reproducibility example:** examples/synthetic_demo.py
  explicitly labels outputs as hypothetical.

## Evidence table

| Evidence category | Current verification |
|---|---|
| Data contracts and train-fold preprocessing | Code + synthetic unit tests |
| Real-data internal benchmark | Original private survey analyses summarized publicly; metrics from 25-fold CV (n=152) |
| External validation at other universities | **Not available** |
| Sensitivity of primary econometrics | HC3, model diagnostics, influence, and exploratory controls documented; psychometric invariance not assessed |
| SHAP on original study | Held-out first-repetition Tree SHAP aggregate summary available; respondent plots restricted |
| Causal effects or policy effectiveness | **Not established** |
| Subgroup-error reporting code | Available, minimum n=20 |

### Risks and ethical boundaries

Student perceptions are sensitive; a spirituality/purpose measure may reveal
protected or personal beliefs depending on survey wording. Coding for
gender, first-generation status, and income must be audited for validity,
inclusion and lawful purpose. Avoid stigmatizing students on the basis of
demographics or psychosocial scores. Student data require authorized
institutional access, purpose limitation, appropriate review, secure handling,
and transparent accountability.

## Strictly excluded uses

No automated admissions, scholarships, financial aid, academic probation,
mental-health screening, counseling allocation, or exclusion from services.
A statistical feature attribution is not an intervention recommendation.

## Publication-readiness prerequisites

Authorized source dataset and codebook; scale reliability and item scoring;
missing-data analysis; cohort/institution-level holdouts; subgroup uncertainty;
privacy and ethics approval as applicable; independent reproduction of
performance tables; and transparent student stakeholder engagement.

Related resources: [Research design](RESEARCH_DESIGN.md),
[Data governance](DATA_GOVERNANCE.md),
[Policy brief](EDUCATION_POLICY_BRIEF.md), and
[Reproducibility](REPRODUCIBILITY.md).
