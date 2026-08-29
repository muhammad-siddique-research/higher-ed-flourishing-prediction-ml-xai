# 🎓 Psychosocial Determinants of Higher Education Flourishing: Econometric Identification & Explainable Machine Learning (XAI)

An empirical framework bridging classical econometrics with machine learning (XGBoost, LightGBM, ElasticNet, and Tree SHAP interpretability) to model and forecast undergraduate student flourishing.

---

## 📌 Theoretical Framework & Path Architecture

Grounded in Tinto’s Interactionalist Model, Astin’s Student Involvement Theory, and Ryan & Deci’s Self-Determination Theory (SDT), this study models the predictive dynamics of relational community, institutional integrity, and intrapersonal purpose on the multidimensional **Thriving Quotient (TQ)**:

* **Institutional Integrity (Macro-Structural Enabler):** Establishes institutional trust ($r = .629, p < .001$) channeled into community belonging.
* **Sense of Community (Proximal Relational Mediator):** Serves as the primary direct engine of flourishing ($B = 0.405, \beta = .592, p < .001$).
* **Institutional Integrity Direct Path:** Statistically non-significant ($B = -0.030, p = .527$), fully absorbed by community belonging.
* **Spirituality (Intrapersonal Anchor):** Serves as an independent direct psychological buffer ($B = 0.110, \beta = .182, p = .009$).

---

## 📊 Feature Dictionary & Psychometric Scales

| Variable | Role | Type | Operational Definition |
| :--- | :--- | :--- | :--- |
| `TQ_MEAN` | **Target** | Float | Composite mean across 24 items (scale: 1.00–6.00) |
| `SCOMM` | **Predictor** | Float | Continuous scale assessing relational belonging and peer support |
| `INTEGRITY` | **Predictor** | Float | Continuous scale measuring institutional transparency and trust |
| `SPIR` | **Predictor** | Float | Continuous scale evaluating existential purpose and meaning |
| `FIT` | **Covariate** | Ordinal | Student-institution alignment perception |
| `TUITION` | **Instrument** | Ordinal | Perceived tuition value and return |
| `FIRSTGEN` | **Control** | Binary | First-generation student status (0 = No, 1 = Yes) |
| `GENDER` | **Control** | Binary | Gender identity (0 = Male, 1 = Female) |
| `FAMINCOME` | **Control** | Ordinal | Socioeconomic household income tier |

---

## 🔬 Econometric Benchmarks vs. Machine Learning Models

### 1. Econometric Robustness Suite
* **Multivariate Baseline (OLS):** Explains 42.4% of adjusted variance in student thriving ($F(3, 148) = 38.11, p < .001$).
* **Relational Primacy:** Sense of Community is the primary direct driver ($B = 0.405, \beta = .592, p < .001$).
* **Structural Absorption of Integrity:** Institutional Integrity is non-significant in multivariate estimation ($B = -0.030, p = .527$), fully mediated by community belonging ($r = .629$).
* **Intrapersonal Purpose:** Spirituality remains an independent, robust predictor ($B = 0.110, \beta = .182, p = .009$).
* **Endogeneity Control (2SLS):** Instrumenting `SCOMM` confirms that relational belonging exerts an active causal direct effect ($B = 0.256, p = .023$).

### 2. Machine Learning Benchmark (10-Fold Cross-Validation)

| Model Architecture | 10-Fold $R^2$ | RMSE | MAE |
| :--- | :---: | :---: | :---: |
| **XGBoost Regressor** | **0.508 ± 0.04** | **0.358** | **0.282** |
| **LightGBM Regressor** | 0.501 ± 0.05 | 0.361 | 0.286 |
| **Random Forest** | 0.489 ± 0.04 | 0.366 | 0.291 |
| **ElasticNet (L1/L2)** | 0.442 ± 0.03 | 0.381 | 0.302 |

---
## Streamlit App
https://higher-ed-flourishing-prediction-ml-xai-cj3qpcffjve46ochqrdtn9.streamlit.app/

## 👨‍🔬 Authors & Affiliation

* **Muhammad Siddique, PhD Candidate** — Department of Education & Computer Science, Judson University, Elgin, IL, USA.  
* **Dr. Chad Briggs, PhD** — Director of Institutional Research & Effectiveness, Academic Affairs, Judson University, Elgin, IL, USA.
