# Model card | Student flourishing and responsible explainable ML

**Status:** Public research architecture. Software functionality is testable;
predictive performance on real undergraduate data **has not been independently verified**.

## Research objective and context

Explore whether an undergraduate Thriving Quotient (TQ) composite can be
predicted from sense of community, institutional integrity, purpose/spirituality,
institutional fit, tuition-value perceptions, and student background measures.
Predictive association is **not** causal identification.

## Intended use

Research-method demonstration, model benchmarking, scholarly collaboration,
and transparent discussion of institutional data governance. This repository
is *not* an operational risk scoring or automated student-support system.

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
| Real-data model scores | **Not independently reproduced** |
| External validation at other universities | **Not available** |
| Sensitivity to different survey measures | **Not assessed** |
| SHAP on the original student dataset | **Not available** |
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
