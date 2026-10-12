# Evidence-to-policy brief | Undergraduate thriving

**Audience:** Institutional research, student-success leadership,
faculty, and higher education policy teams.

**Status:** Decision framework, **not** proof that a policy works.

## Why this research matters

Students' experiences of belonging, institutional trust, purpose, perceived
fit and affordability warrant thoughtful investigation. Internal predictive models may describe patterns in the privately analyzed original survey, while public reporting is restricted to approved aggregates.
A prediction does not establish which student-support intervention works.

## Empirical signals from original-data reanalysis

The original private SPSS survey contains **156 undergraduates** at a single
private Midwestern institution; the primary three-predictor model uses
**152 complete cases**. The replicated OLS explains 43.6% of variance in
thriving *within the observed sample* (adjusted R² = .424).

**HC3-robust conditional estimates:** sense of community B = .405,
95% CI [.267, .543]; spirituality B = .110, 95% CI [.008, .212];
institutional integrity B = −.030, 95% CI [−.125, .066].
Significant heteroskedasticity and specification diagnostics reinforce the
need for cautious inference; spirituality is sensitive to additional
institutional-perception controls.

**Exploratory predictive evidence:** XGBoost and Random Forest yielded
comparable held-out RMSEs (**.379 and .380**, respectively) on 25 overlapping
validation folds. Held-out Tree SHAP ranked community first in mean absolute
model attributions. This pattern **is not evidence that a community
intervention will cause thriving to increase**.

The research supports designing *evaluations* of inclusive mentoring,
faculty-student contact and welcoming campus communities, not using
algorithmic risk scores for individual decisions. Institutional integrity
and protected student autonomy remain responsibilities independently of
a model coefficient.

See the [original-data evidence report](REAL_DATA_VALIDATION.md) for
publication-safe figures and detailed methodological limitations.

### An implementable institutional learning agenda

1. **Co-design an inclusive belonging pilot.** Offer opt-in peer mentoring,
   faculty check-ins, transition support and accessible learning communities.
   Invite diverse students to define what meaningful belonging entails.
2. **Prespecify outcomes.** Track ethically administered flourishing scales,
   course engagement, students' perceived support, and program accessibility.
   Avoid turning composite TQ scores into disciplinary risk labels.
3. **Evaluate effects independently.** If feasible, use randomized invitation
   or phased rollout designs with appropriate consent and governance; report
   intent-to-treat outcomes, attrition, subgroup uncertainty and implementation
   costs. This evaluation is **proposed, not performed** in this repository.
4. **Maintain integrity and transparency.** Review student-facing commitments,
   timely services, equitable access, and grievance/feedback mechanisms even
   if multivariable correlations are not statistically significant.
5. **Respect religious and nonreligious diversity.** Meaning/purpose programs
   must be voluntary and inclusive; spirituality variables should not be
   used to infer beliefs or allocate student services.

### Decision dashboard for senior leadership

| Decision | Evidence available today | Responsible next evidence |
|---|---|---|
| Evaluate mentoring | Community strongly correlated with TQ | Controlled pilot and student input |
| Improve institutional trust | Correlations, no proven mediation | Governance assessment and longitudinal survey |
| Offer purpose exploration | Conditional correlation only | Voluntary, inclusive student support evaluation |
| Deploy ML risk scoring | **No validated original-data ML results** | Authorized data, external testing, privacy and equity approval |

See the [real-study empirical audit](EMPIRICAL_EVIDENCE.md) and
[advanced econometric protocol](ADVANCED_ECONOMETRICS.md). This is a
framework for learning from evidence, not a recommendation to automate
consequential student decisions.

## Evidence chain

| Stage | Required evidence | Practical decision |
|---|---|---|
| 1. Define constructs | Validated flourishing instrument and theory | What does thriving mean? |
| 2. Establish rights | Consent, purpose, governance, data minimization | Is analysis authorized? |
| 3. Benchmark models | Mean baseline, regularized regression, boosting | Does complexity add value? |
| 4. Examine portability | Campus/cohort holdouts and longitudinal tests | Will it generalize? |
| 5. Check equity | Error uncertainty and subgroup representation | Where might it fail? |
| 6. Explain predictions | Stable and clearly bounded SHAP attributions | What does the model use? |
| 7. Evaluate support | Separately designed program-effectiveness study | Does intervention help? |
| 8. Maintain oversight | Accessible appeals, drift monitoring, student voice | Should it be continued? |

## Three educational policy principles

**Student agency:** communicate intended uses and involve students in
measurement and governance.

**No automated disadvantage:** never deny services or assign high-stakes
labels from a single flourishing score or SHAP ranking.

**Fair access to support:** assess whether programs benefit students across
different access, socioeconomic and educational backgrounds; follow privacy
and small-cell suppression rules for reporting.

## Research-to-practice agenda

1. Does a properly evaluated belonging intervention improve validated
   flourishing outcomes across cohorts?
2. Do results replicate at other institutions and in future academic years?
3. Do constructs retain their psychometric meaning across student groups?
4. Which student supports offer measurable benefits without profiling?

## Selected conceptual foundations (APA 7)

Astin, A. W. (1984). Student involvement: A developmental theory for
higher education. *Journal of College Student Personnel, 25*(4), 297–308.

Tinto, V. (1975). Dropout from higher education: A theoretical synthesis of
recent research. *Review of Educational Research, 45*(1), 89–125.
https://doi.org/10.3102/00346543045001089

Ryan, R. M., & Deci, E. L. (2000). Self-determination theory and the
facilitation of intrinsic motivation, social development, and well-being.
*American Psychologist, 55*(1), 68–78.
https://doi.org/10.1037/0003-066X.55.1.68
