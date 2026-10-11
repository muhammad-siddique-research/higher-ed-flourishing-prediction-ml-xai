# Research design | Student flourishing in higher education

## Problem and decision context

The project explores associations between undergraduate flourishing and
relational, institutional, and intrapersonal constructs. Its purpose is
methodological and research-oriented: a possible evidence base for future
student-success policy, **not** an operational risk-screening tool.

## Conceptual foundations

- **Astin's student involvement framework:** participation and engagement as
  central constructs in college experience.
- **Tinto's student persistence framework:** social and academic integration,
  alongside institutional context.
- **Self-determination theory (Ryan & Deci):** autonomy, competence, and
  relatedness as useful hypotheses for learning and well-being.

These theories motivate research questions; they do not prove that this dataset
supports any particular structural path, mediation, or causal mechanism.

## Variables and measurement

The repository expects eight predictors (`SCOMM`, `INTEGRITY`,
`SPIR`, `TUITION`, `FIT`, `FIRSTGEN`, `GENDER`, `FAMINCOME`) and one
outcome (`TQ_MEAN`). The target is described as the mean of 24 items
on a 1–6 scale. Item-level data, scale reliability, validity,
sample design, and missingness patterns are **not available in the repository**.

`TUITION` is treated as a predictor, not automatically as a valid instrumental
variable; relevance and the exclusion restriction would require identification
arguments and sensitivity analysis.

## Predictive objectives and safeguards

1. Compare mean-only regression with regularized linear and nonlinear models.
2. Evaluate R², RMSE, and MAE under the same train-only preprocessing protocol.
3. Use group-disjoint validation when repeated student or institution IDs exist.
4. Assess performance drift, subgroup errors, missing-data patterns, and
   external-site generalizability before real institutional consideration.
5. Generate SHAP explanations solely to describe **model attributions**, not
   interventions or causal effect magnitudes.

### Interpretation hierarchy

| Evidence type | Can support | Cannot establish alone |
|---|---|---|
| Correlations and regression coefficients | Conditional or marginal association | Causality |
| K-fold predictive cross-validation | In-sample-domain generalization estimate | Deployment validity |
| SHAP explanation | How a fitted model distributes predicted contributions | The effect of changing a student's circumstance |
| Quasi-experiment or randomized intervention | Potentially causal effects, subject to design assumptions | Universal transportability |

## Causal identification is separate research

Claims of mediation require an explicit causal graph, temporal ordering,
mediator/outcome identification assumptions, and inference appropriate to
the design. Instrumental-variable estimates demand a defensible instrument,
first-stage relevance, exclusion, and assessment of weak instruments.
**No causal identification is implemented by this repository.**

## Educational policy pathway

A policy-relevant study would first document construct validity and data
representativeness, then compare prediction quality against simple baselines,
validate across institutions and cohorts, review fairness and privacy, and
finally test specific opt-in supports through a separate evaluation design.
Predictive rankings must never be treated as clinical diagnoses or automatic
determinations of student access to educational support.

## Further reading

- Astin, A. W. (1984). Student involvement: A developmental theory for higher education. *Journal of College Student Personnel, 25*(4), 297–308.
- Tinto, V. (1975). Dropout from higher education: A theoretical synthesis of recent research. *Review of Educational Research, 45*(1), 89–125. https://doi.org/10.3102/00346543045001089
- Ryan, R. M., & Deci, E. L. (2000). Self-determination theory and the facilitation of intrinsic motivation, social development, and well-being. *American Psychologist, 55*(1), 68–78. https://doi.org/10.1037/0003-066X.55.1.68
- Lundberg, S. M., & Lee, S.-I. (2017). A unified approach to interpreting model predictions. *Advances in Neural Information Processing Systems, 30*. https://arxiv.org/abs/1705.07874
