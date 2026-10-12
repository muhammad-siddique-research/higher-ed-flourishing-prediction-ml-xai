# Original-data evidence | *The Science of Student Thriving*

**Research manuscript:** *The Science of Student Thriving: Econometrics and Explainable AI Analysis* — Muhammad Siddique and Chad Briggs, revised working manuscript. **Publication status:** not represented as peer reviewed, accepted, or published.

This document summarizes aggregate analyses conducted on the **original restricted SPSS survey file** and reconciled with the revised research manuscript. The public repository includes **only aggregate numerical outputs and documentation**; it does **not** include original survey records or individual SHAP graphics. The internal results should not be confused with the separately labeled [synthetic demonstrations](VISUAL_ANALYSIS.md).

## Study design and econometric evidence

- **Setting:** one private Midwestern U.S. institution; cross-sectional observational undergraduate survey
- **Study size:** 156 survey cases; 152 complete cases for the three-predictor OLS model
- **Outcome:** Thriving Quotient mean (`TQ_MEAN`, 1–6 scale)
- **Theory-guided predictors:** sense of community (`SCOMM`), institutional integrity (`INTEGRITY`), and spirituality (`SPIR`)
- **Replication:** *F*(3, 148) = 38.11, *R²* = .4358, adjusted *R²* = .4244

| Predictor | OLS coefficient *B* | HC3 95% confidence interval | HC3 *p* |
|---|---:|---:|---:|
| Sense of community | .405 | [.267, .543] | < .001 |
| Institutional integrity | −.030 | [−.125, .066] | .541 |
| Spirituality | .110 | [.008, .212] | .035 |

**Model adequacy:** Breusch–Pagan *p* = .0085, White *p* < .001, and Ramsey RESET *p* = .0007. Accordingly, heteroskedasticity-robust HC3 uncertainty and cautious functional-form interpretation are emphasized. In a five-predictor exploratory specification incorporating perceived fit and tuition value, the conditional spirituality estimate was more sensitive to model choice (HC3 *p* ≈ .086). These are **observational associations**, not intervention effects.

## Seven-model internal predictive benchmark

Seven models were evaluated on the same 152 complete cases, using **5-fold cross-validation repeated five times (25 matched, overlapping held-out folds)**. Scores below average each fold's held-out metric. They are not estimates from an external institution.

| Model | Mean RMSE ↓ | Mean MAE ↓ | Mean fold R² ↑ |
|---|---:|---:|---:|
| **XGBoost** | **.3794** | **.2906** | .3814 |
| Random Forest | .3802 | .2931 | **.3840** |
| LightGBM | .3880 | .3031 | .3537 |
| ElasticNet | .3979 | .2995 | .3315 |
| Ridge | .3994 | .3001 | .3251 |
| OLS | .3995 | .3006 | .3183 |
| Mean-only baseline | .5126 | .4052 | −.0466 |

![Real-study internal CV model errors, aggregate only](figures/REAL_STUDY_model_errors.svg)

XGBoost's RMSE was about **5.0% lower than OLS** and **26.0% lower than the mean-only baseline**. Its difference from Random Forest was only **.0008 Thriving Quotient points**. Consequently, **XGBoost and Random Forest performed comparably in this sample**. Repeated-CV fold variability must not be treated as independent confidence intervals or as evidence of external generalization.

[Download the aggregate model comparison data](../evidence/REAL_STUDY_cv_summary.csv)

## Tree SHAP: held-out feature attribution

Five separately trained XGBoost models produced Tree SHAP values for **held-out survey cases within the first 5-fold repetition**. Only mean absolute attribution magnitudes—not individual response-level data—are released here.

| Predictor | Mean absolute out-of-fold SHAP | Relative share of total absolute SHAP |
|---|---:|---:|
| Sense of community | .2584 | 58.8% |
| Spirituality | .1300 | 29.6% |
| Institutional integrity | .0514 | 11.7% |

![Aggregate SHAP importance from original study; no respondent-level points](figures/REAL_STUDY_aggregate_SHAP.svg)

SHAP indicates which features the fitted model relies on when predicting the Thriving Quotient; it does **not** establish why students flourish, quantify causal effects, or validate an intervention strategy. Correlated perceptions can complicate the interpretation of attribution rankings.

[Download the aggregate SHAP importance data](../evidence/REAL_STUDY_shap_summary.csv)

## Research-to-policy contribution

The strongest convergent finding is the importance of **perceived sense of community** across conditional econometric associations and held-out model attribution. It motivates careful, student-centered evaluation of peer mentoring, inclusive academic communities, faculty–student interaction, and transition supports.

Institutional integrity remains an ethical and administrative responsibility irrespective of a nonsignificant *conditional slope*. Spirituality-related measures should be interpreted with attention to instrument wording, religious/nonreligious inclusion, and student autonomy.

**Policies should be evaluated independently** through appropriately governed longitudinal or experimental designs. Predictive models must not be used for admissions, sanctions, faith-based targeting, or automated student risk classification without a separate legal, ethical, and validity review.

## Provenance and permitted reuse

- Source materials: original locally analyzed SPSS survey and original SPSS outputs; revised author-supplied manuscript; aggregate cross-validation and SHAP tables.
- Public dataset: **none** (restricted student responses are not provided).
- Public materials: [ML summary CSV](../evidence/REAL_STUDY_cv_summary.csv), [SHAP summary CSV](../evidence/REAL_STUDY_shap_summary.csv), [aggregate provenance record](../evidence/REAL_STUDY_provenance.json), and privacy-preserving aggregate SVG charts.
- Original analyses: performed in a private research environment; public synthetic demonstrations and generic authorized-data code are separate and **must not** be mistaken for independent replication of the real-data outputs.
- Remaining submission requirements: confirm study approval/consent, recruitment details, survey-scale permissions/psychometrics, data rights, coauthor sign-off, and journal-specific research disclosures.

### Relevant scholarly context

- Schreiner, L. A. (2010). The “Thriving Quotient”: A new vision for student success. *About Campus, 15*(2), 2–10. https://doi.org/10.1002/abc.20016
- Shmueli, G. (2010). To explain or to predict? *Statistical Science, 25*(3), 289–310. https://doi.org/10.1214/10-STS330
- Chen, T., & Guestrin, C. (2016). XGBoost: A scalable tree boosting system. *Proceedings of the 22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining*, 785–794. https://doi.org/10.1145/2939672.2939785
- Lundberg, S. M., et al. (2020). From local explanations to global understanding with explainable AI for trees. *Nature Machine Intelligence, 2*, 56–67. https://doi.org/10.1038/s42256-019-0138-9
