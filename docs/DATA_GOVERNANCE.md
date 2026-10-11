# Privacy, fairness, and institutional governance

This is a public **research code repository**, not a warehouse for identifiable
student information or an approved institutional decision engine.

## Student-level data safeguards

- Confirm lawful and institutionally authorized data use, applicable IRB review,
  FERPA/other privacy obligations, research consent, and data agreements.
- Remove direct identifiers before analytical use; evaluate indirect reidentification
  risks before releasing small-group summaries or machine-learning artifacts.
- Apply least-privilege access, encryption at rest/in transit, retention limits,
  audit logging, and documented deletion procedures in the approved environment.
- Keep raw data, source notebooks with exposed records, fitted models, and
  interactive student-level results outside this public repository.
- Avoid assuming publicly available code provides permission to reuse study data.

## Fairness and construct-validity safeguards

- Explain the population sampled and nonresponse, survey administration,
  missingness, and psychometric scale properties.
- Audit subgroup error metrics where legally/ethically appropriate and where
  sample sizes support meaningful uncertainty statements.
- Avoid treating gender, income, or first-generation status as inherent risks.
- Obtain stakeholder feedback, including students, instructors, support staff,
  and disability/accessibility specialists.
- Monitor model drift and unintended consequences, and make human oversight
  and appeal paths explicit before any consequential policy use.

## Research-to-policy guardrails

**Permissible:** aggregate, appropriately protected descriptive research;
evaluation of learning-support programs; exploration of uncertainty.

**Not justified:** automated student labeling, admissions decisions,
financial-aid decisions, withholding services, mental-health diagnosis,
or targeting interventions solely from SHAP or predictive rankings.

A policy recommendation must be supported by program-effectiveness evidence,
institutional feasibility, equity assessment, and transparent governance.
