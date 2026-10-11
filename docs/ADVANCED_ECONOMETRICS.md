# Advanced econometric validation | From reported OLS to auditable evidence

This protocol separates what is **already reported in an observational
undergraduate survey draft** from what is **implemented as executable code
pending authorized access to participant-level records**.

## I. Existing evidence

- Survey `N = 156`; complete-case regression `n = 152`.
- Outcome: composite Thriving Quotient, 1–6.
- Primary regressors: community belonging, institutional integrity,
  spirituality/meaning.
- Reported `R² = .436` and coefficient CIs.
- Conditional partial `R²`, incremental `R²`, model algebra and approximate
  VIF can be reconstructed from the author's summary tables.

These numbers are **reported from the author's draft**. They are not
replicated SPSS output or verified against the underlying private dataset.

## II. Implemented advanced econometric runner

[`src/real_data_econometrics.py`](../src/real_data_econometrics.py)
implements these checks **if and only if** the researcher supplies
permissioned primary observations:

1. **Complete-case baseline OLS.** Records whose outcome or one of the
   three pre-specified composites is missing are excluded. The script
   returns missingness counts and sample size. This design is not
   generally unbiased when data are missing not at random.
2. **Heteroskedasticity-consistent inference.** HC3 sandwich standard
   errors, p values and confidence intervals are reported alongside
   classical OLS inference. HC3 does not repair omitted confounders.
3. **Model form and variance diagnostics.** Breusch–Pagan and Ramsey
   RESET tests flag possible specification concerns; neither proves
   the model is causally identified.
4. **Collinearity and influence.** Predictor-specific VIFs and Cook's
   distance screening, with reported influence counts.
5. **Nested specification analysis.** Drop-one-variable changes in
   `R²` on the **same complete-case sample** distinguish unique
   incremental fit from marginal correlation.
6. **Nonparametric case bootstrap.** Percentile intervals from
   re-sampling individual records; validity depends on sampling and
   observational independence.
7. **Optional clustered inference.** At least 10 observed clusters
   required for a basic cluster-robust reporting option; small-cluster
   inference and any repeated measures require further scrutiny.

**No significant effect, mediation pathway, or new empirical estimate is
claimed until this code is actually run on the original authorized CSV.**

## III. Analytical enhancements recommended before journal submission

### Missing data and selection

Document the exact missingness pattern, whether the four missing integrity
values overlap with the two missing spirituality values, response
nonparticipation, and sensitivity to complete-case selection.
Multiple imputation by chained equations or likelihood methods should be
implemented only after choosing defensible imputation models and assessing
plausible missing-at-random assumptions. **MICE/FIML are not implemented here.**

### Psychometric construct evaluation

Obtain item-level responses, scale instructions, scoring key and permissions
before computing Cronbach's alpha/omega, confirmatory factor analyses, and
measurement invariance. Verify the three predictor scales are not
mathematical components of the TQ outcome, despite the manuscript's
description. Check ceiling clustering (notably `SPIR`) using distributions
and sensitivity analyses rather than automatically invoking a Tobit model.

### Causal mediation and endogeneity

Pre-specify a directed acyclic graph and explanatory estimand; identify
confounders; justify timing before mediation or causal inference.
No exclusion-valid instrument for `SCOMM` is shown here.
**Tuition-value perception alone is not a validated instrument.**
Avoid asserting *full mediation* from regression coefficient attenuation.

### External prediction and institutional transportability

High in-sample `R²` is **not** predictive generalization. Compare
ElasticNet/XGBoost/LightGBM to mean-only prediction with out-of-fold
validation, analyze leakage and missingness, and validate at new campuses
and cohorts as possible. The existing synthetic figures demonstrate
software; they are not student-level results.

## IV. Practical commands

```bash
# Recompute secondary checks from the manuscript's aggregate tables:
python -m src.reported_evidence_audit

# Actual data: researcher-authorized only, not a synthetic substitute.
python -m src.real_data_econometrics --data /secure/study.csv \
    --output-dir results/ols --bootstrap 1000

# Only if an ethically authorized cluster ID exists, with enough groups:
python -m src.real_data_econometrics --data /secure/study.csv \
    --cluster-column CLASS_SECTION --bootstrap 1000
```

The resulting `results/` files must stay under approved access controls.

## V. Research reporting standard

Report the analysis sample and missingness, original instrumentation,
model specification, conventional and HC3 standard errors, confidence
intervals, fit statistics, residual and influence diagnostics, observed
response ceiling behavior, exploratory analyses, preregistered hypotheses,
scope of generalization, governance, and all limitations. The project's
[reported-evidence audit](../src/reported_evidence_audit.py) and
[model card](MODEL_CARD.md) use explicit provenance labels.
