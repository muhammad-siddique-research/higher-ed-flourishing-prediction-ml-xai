# Data access and schema

Student-level flourishing observations are **not distributed** in this public repository.
No synthetic training dataset is presented as evidence, and no model evaluation
metrics have been certified by the current repository artifacts.

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
