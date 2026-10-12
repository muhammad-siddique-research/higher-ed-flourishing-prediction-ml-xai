# Data access and schema

Student-level flourishing observations are **not distributed** in this public repository.
The original SPSS survey was reanalyzed in a private, authorized research setting;
only public **aggregate original-data ML/XAI metrics** and the separately labeled
synthetic software demonstrations are available here. See
[real-data validation](../docs/REAL_DATA_VALIDATION.md).
These results are internally cross-validated only; no external prediction claims
are supported.

To reproduce the benchmark, obtain the original dataset under appropriate
institutional authorization, privacy review, and data-use agreement.

Required CSV headers:

```text
SCOMM,INTEGRITY,SPIR,TUITION,FIT,FIRSTGEN,GENDER,FAMINCOME,TQ_MEAN
```

`TQ_MEAN` is the project-described composite outcome on a 1–6 scale.
Study instruments, construct reliability, scoring rules, and the provenance of
these variables must be independently documented before publication.

For records with repeated participants or institutional clusters, an optional
non-predictor grouping column (e.g., `STUDENT_ID`) can be provided using
`--group-column STUDENT_ID`. No student identifier is ever used as a feature.

Do **not** upload raw identifiable student records, free-text responses,
private survey exports, or individual-level predictions to GitHub. See
[Data Governance](../docs/DATA_GOVERNANCE.md).

## Empirical study to pipeline variable crosswalk (verification pending)

The author's 30-page manuscript presents a primary three-predictor
regression with Thriving Quotient (`TQ_MEAN`) as the target,
community (`SCOMM`), institutional integrity (`INTEGRITY`),
and spirituality (`SPIR`). The manuscript's appendix also describes
SPSS-style fields `TUT` (tuition value), `FIT`, `F-GEN`,
`GEND`, and `FM-INC`; whereas the expanded ML pipeline currently
expects `TUITION`, `FIT`, `FIRSTGEN`, `GENDER`,
and `FAMINCOME`.

**These are proposed name mappings—not confirmed original CSV headers.**
Inspect the actual restricted SPSS/CSV codebook before renaming columns,
especially whether variable values and missing-category codes are aligned.
A label such as `Spirituality` must not automatically be equated with
secular purpose without reviewing original items and construct validity.

The source draft reports `N=156`, complete-case OLS `n=152`;
correlation matrices rely on pairwise-valid samples. Neither a
real-data XGBoost result nor a LightGBM test has been independently
confirmed from the manuscript.

The econometric companion runs on **only four required columns**
(`TQ_MEAN`, `SCOMM`, `INTEGRITY`, `SPIR`) after authorized
data access. The more expansive machine-learning pipeline expects all
nine named fields and cannot be described as validated on the same
original sample until that source-data specification is checked.
