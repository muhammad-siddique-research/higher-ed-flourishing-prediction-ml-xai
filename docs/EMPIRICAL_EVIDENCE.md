# Empirical evidence | Undergraduate flourishing in the actual study

> **Evidence provenance:** This page summarizes and independently checks
> numerical *aggregates reported in a researcher-supplied 30-page draft*
> by Muhammad Siddique and Chad Briggs. The research describes a real
> cross-sectional survey, but this public repository has **no original
> participant-level dataset, survey-item responses, data-use authorization,
> or SPSS estimation output**. These are *reported* results; the calculations
> below are mathematical **secondary checks**, not an independent
> replication from student records or external validation.

## A. Design, sample, and constructs

The manuscript describes **N = 156 traditional undergraduates** at a private
Midwestern US institution. The three-predictor complete-case OLS model uses
**n = 152**. This is a single-site, observational, cross-sectional survey:
neither a multi-university sample nor a quasi-experimental design.

| Measure | Reported N | Mean | SD | Minimum–maximum |
|---|---:|---:|---:|---:|
| Thriving Quotient (`TQ_MEAN`) | 156 | 4.65 | 0.51 | 3.29–6.00 |
| Sense of community (`SCOMM`) | 156 | 4.74 | 0.75 | 2.25–6.00 |
| Institutional integrity (`INTEGRITY`) | 152 | 4.58 | 0.88 | 2.00–6.00 |
| Spirituality and meaning (`SPIR`) | 154 | 5.20 | 0.85 | 3.00–6.00 |

Source: author-supplied draft, Table 1, §§4.1 and 3.2; transcribed in
[`evidence/manuscript_summary.json`](../evidence/manuscript_summary.json).
The original data file, study codebook, instrument items, reliability
coefficients, and institution-level metadata require separate authorization
and review. `TQ_MEAN` and other code identifiers are project-convention
names, not independently confirmed original SPSS variable labels.

## B. Reported bivariate relationships

![Correlation matrix from the real-study manuscript](figures/REPORTED_correlations.svg)

**Figure 1.** Pearson correlations from the manuscript's aggregate table.
Pairwise-valid N varies from 152 to 156. Sense of community and thriving
correlate at `r = .639`; integrity and thriving at `r = .385`;
spirituality and thriving at `r = .416`. Correlation neither establishes
temporal ordering nor identifies a manipulable policy lever.

## C. Simultaneous OLS and uncertainty

![Reported OLS coefficients with uncertainty intervals](figures/REPORTED_ols_coefficients.svg)

**Figure 2.** Multivariable associations with 95% confidence intervals
**transcribed from the author's draft**, not recomputed from microdata.

| Predictor | B | Standardized β | Reported 95% CI for B | Reported p |
|---|---:|---:|---|---:|
| Sense of community | 0.405 | .592 | [.293, .518] | < .001 |
| Institutional integrity | −0.030 | −.051 | [−.122, .063] | .527 |
| Spirituality / purpose | 0.110 | .182 | [.027, .193] | .009 |

Complete-case OLS: `n = 152`, `F(3, 148) = 38.11`, `p < .001`,
`R² = .436`, `adjusted R² = .424`. The reported coefficients describe
conditional differences on the 1–6 composite scale, *not* effects of an
intervention. Regression output does not validate measurement quality or
survey response representativeness.

## D. Additional econometric calculations from manuscript summaries

The accompanying [reproducible audit](../src/reported_evidence_audit.py)
derives and cross-checks quantities from the manuscript's rounded
regression `F`, `t` statistics and correlation matrix.

| Variable | Derived partial R² | Incremental full-model R² | VIF from pairwise correlations |
|---|---:|---:|---:|
| Sense of community | .2546 | .1927 | 1.79 |
| Institutional integrity | .0027 | .0015 | 1.68 |
| Spirituality / purpose | .0446 | .0264 | 1.23 |

![Derived unique contribution of manuscript predictors](figures/DERIVED_unique_explanatory_contributions.svg)

**Figure 3.** Approximate decline in `R²` when each predictor is removed
from the model (holding the remaining two predictors fixed).

The reported `F` and degrees of freedom imply `R² = .4358` and adjusted
`R² = .4244`, agreeing with the manuscript after rounding. The
rounded *pairwise* correlation matrix implies `R² ≈ .4361`, and
implied standardized coefficients approximately `(.595, −.054, .184)`,
close to the paper's `(.592, −.051, .182)`.

**Critical inference boundaries:**

- Partial `R²` means the fraction of *remaining conditional variation*
  explained by one predictor given the others; it is not the fraction of
  total study outcome variance, and it is not a causal contribution.
- Incremental full-model `R²` is the reduction in overall `R²` upon
  dropping the variable. It is not additive across shared predictors.
- The approximate VIFs use **pairwise correlations with different valid N**,
  not the exact 152-person complete-case correlation matrix. They cannot
  replace the original model's measured VIFs.
- A coefficient losing significance after adjustment **cannot establish
  full mediation**. Formal causal mediation requires temporal ordering,
  a mediator model, and defensible identification assumptions.
- The draft's suggestion of a Tobit model for a **ceiling-bound predictor**
  does not automatically follow from a bounded Likert response. Tobit is
  principally a censored-*outcome* model under specific data-generating
  assumptions; ceiling evidence alone cannot establish censoring.
- A Durbin–Watson statistic on arbitrarily ordered cross-sectional survey
  cases is not proof of error independence. Residual plots are not formal
  substitutes for all model diagnostics.
- The manuscript contains **duplicate reference lists and differing
  bibliographic details** for at least one entry; confirm final citations
  against authoritative records before submission.

## E. Decision translation: responsible institutional interpretation

The most defensible interpretation is **relational belonging is the
strongest unique covariate of thriving in this particular reported model**.
This motivates further examination of peer mentoring, connected
first-year experiences, faculty-student relationships, and inclusive advising.
It does **not** demonstrate that reallocating university budgets to these
programs raises TQ by `0.405` for every 1-point increase in belonging.

Perceived institutional integrity may matter through pathways that require
further study; an insignificant conditional slope is **not evidence that
ethics, equity, or transparent governance can be deprioritized**.

Spirituality and existential purpose should be framed inclusively with
respect for students' varied secular, religious, and nonreligious identities.
The research construct is not permission to profile individuals or
require belief-based programming.

A responsible research-to-policy sequence is **instrument validation →
secure data stewardship → external replication → optional/accessible student
supports → separately evaluated program effects**. See the
[policy brief](EDUCATION_POLICY_BRIEF.md).

## F. Reproducibility and restricted data

```bash
# Only the author's aggregate results; no student-level data required:
python -m src.reported_evidence_audit

# Execute HC3 OLS, nested R², robust diagnostics and bootstrap ONLY
# on researcher-authorized private individual-level data:
python -m src.real_data_econometrics \
    --data /secure/path/undergraduate_survey.csv \
    --output-dir results/real_study \
    --bootstrap 1000
```

Outputs from the second command are not supplied or represented as already
computed. Do not commit the microdata or privately derived artifacts without
data-owner authorization.

### Scholarly anchors

Schreiner, L. A. (2010). The “thriving quotient”: A new vision for student
success. *About Campus, 15*(2), 2–10.
https://doi.org/10.1002/abc.20016

Tinto, V. (1975). Dropout from higher education: A theoretical synthesis
of recent research. *Review of Educational Research, 45*(1), 89–125.
https://doi.org/10.3102/00346543045001089

Ryan, R. M., & Deci, E. L. (2000). Self-determination theory and the
facilitation of intrinsic motivation, social development, and well-being.
*American Psychologist, 55*(1), 68–78.
https://doi.org/10.1037/0003-066X.55.1.68

These external references supply conceptual frameworks, **not** independent
verification of this study's dataset or regression coefficients.
