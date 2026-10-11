# Historical project figures — not independently verified

The repository originally displayed the following quantitative statements.
**They are preserved here for provenance, not endorsed as reproduced findings.**

## Historical econometric assertions

- OLS adjusted R²: 0.424; F(3, 148) = 38.11, p < .001
- Sense of community: B = 0.405, beta = 0.592, p < .001
- Institutional integrity: B = -0.030, p = .527
- Spirituality: B = 0.110, beta = 0.182, p = .009
- Correlation of institutional integrity and community: r = .629, p < .001
- Historical 2SLS claim: B = 0.256, p = .023

## Historical ML assertions

| Model | Reported ten-fold R² | RMSE | MAE |
|---|---:|---:|---:|
| XGBoost | 0.508 ± 0.04 | 0.358 | 0.282 |
| LightGBM | 0.501 ± 0.05 | 0.361 | 0.286 |
| Random Forest | 0.489 ± 0.04 | 0.366 | 0.291 |
| ElasticNet | 0.442 ± 0.03 | 0.381 | 0.302 |

## Why this separation matters

The accessible repository contains **no original data, detailed econometric
estimation scripts, experiment logs, fold-level outputs, or fitted models**
that establish these claims. This is not proof the numbers are wrong:
it is a reproducibility limit.

It would be scientifically inappropriate to restate the prior README's
"full mediation" or "active causal effect" conclusions as independently
established. Mediation and instrumental-variable claims require separate
identification assumptions and diagnostics; neither is implemented in
the available code.

These values should return to the main research results only after
original data provenance and authorized executable analyses validate them.
