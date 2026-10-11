"""Education-policy-oriented exploration of the higher-ed flourishing project.

No fitted model or individual-student risk scoring is deployed here.
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Student Flourishing | Research & Policy Lab",
    page_icon="🎓",
    layout="wide",
)

ROOT = Path(__file__).resolve().parents[1]
st.title("Student Flourishing in Higher Education")
st.caption("Explainable ML research architecture · Educational evidence · Responsible policy design")
st.warning(
    "Research prototype—not a validated prediction service. The source student-level data, "
    "fitted model artifact, and independently reproducible performance report are not included. "
    "No individual risk score or intervention recommendation is generated."
)

overview, empirical, scenario, governance = st.tabs([
    "Research overview", "Reported empirical study", "Explore student-experience dimensions", "Policy & governance",
])

with overview:
    st.subheader("The research question")
    st.markdown(
        "How might sense of community, institutional integrity, meaning and purpose, "
        "perceived institutional fit, and tuition-value perceptions jointly predict "
        "undergraduate flourishing—and what evidence is needed before informing policy?"
    )
    a, b, c = st.columns(3)
    a.metric("Candidate ML methods", "4")
    b.metric("Recommended evaluation", "10-fold CV")
    c.metric("Validated deployed model", "None")
    st.markdown(
        "The repository contains an auditable scikit-learn pipeline with **ElasticNetCV, "
        "Random Forest, XGBoost, and LightGBM**, plus a mean-only baseline. "
        "Preprocessing occurs inside each training fold. SHAP plots can be created from "
        "authorized study data, but feature attribution is **not causal identification**."
    )
    st.info(
        "Model estimates in an earlier project description are archived as unverified historical "
        "claims. They should not be reused in reports until the original data, estimation "
        "specifications, and executable results are independently checked."
    )
    st.markdown(
        "See the repository's **README**, **research design**, **reproducibility protocol**, "
        "and **data governance** documents for analysis and decision boundaries."
    )

    st.markdown("---")
    st.subheader("Reproducible ML and Tree SHAP visualizations")
    st.caption(
        "SYNTHETIC-ONLY RESEARCH DEMONSTRATION: 240 mathematically generated "
        "records across 12 fictitious campuses. These are not results from "
        "actual undergraduates or an approved institutional scoring model."
    )
    figures = ROOT / "docs" / "figures"
    model_img = figures / "SYNTHETIC_model_comparison.png"
    shap_img = figures / "SYNTHETIC_tree_shap.png"
    metric_file = figures / "SYNTHETIC_model_metrics.csv"
    if model_img.is_file():
        st.image(
            str(model_img),
            caption="Synthetic out-of-group RMSE: ElasticNet, Random Forest, "
                    "XGBoost, LightGBM, and mean-only baseline.",
            use_container_width=True,
        )
    else:
        st.info("The automated research demonstration has not yet published its plot.")
    if metric_file.is_file():
        metrics = pd.read_csv(metric_file)
        st.dataframe(
            metrics[["model", "r2_mean", "rmse_mean", "mae_mean"]]
            .rename(columns={
                "model": "Synthetic model", "r2_mean": "R²",
                "rmse_mean": "RMSE", "mae_mean": "MAE",
            }).round(3),
            use_container_width=True, hide_index=True,
        )
    if shap_img.is_file():
        st.image(
            str(shap_img),
            caption="Synthetic XGBoost Tree SHAP on a full-sample fit; "
                    "attribution is not causation or policy effectiveness.",
            use_container_width=True,
        )
    st.caption(
        "Methodological caveat: these mathematical demonstration results "
        "cannot verify psychometric constructs, external validity or student "
        "outcomes. Research and policy decisions require authorized empirical evidence."
    )


with empirical:
    st.subheader("Actual undergraduate survey: published-in-draft aggregates")
    st.warning(
        "The reported figures below describe a real, single-site survey "
        "(N=156; complete-case OLS n=152), transcribed from an author-supplied "
        "research draft. Original participant-level data are not in this "
        "repository; estimates have NOT been independently re-estimated "
        "from raw records, and no intervention effects are claimed."
    )
    c1, c2, c3 = st.columns(3)
    c1.metric("Survey respondents", "156")
    c2.metric("Complete-case OLS", "152")
    c3.metric("Reported in-sample R²", "0.436")
    st.markdown(
        "**Reported model:** Thriving Quotient as a function of sense "
        "of community, institutional integrity, and spirituality/purpose. "
        "Adjusted R² = .424; F(3, 148) = 38.11."
    )
    df = pd.DataFrame([
        {"Predictor": "Sense of community", "B": 0.405,
         "Lower 95%": 0.293, "Upper 95%": 0.518,
         "Partial R² (derived)": 0.2546},
        {"Predictor": "Institutional integrity", "B": -0.030,
         "Lower 95%": -0.122, "Upper 95%": 0.063,
         "Partial R² (derived)": 0.0027},
        {"Predictor": "Spirituality / purpose", "B": 0.110,
         "Lower 95%": 0.027, "Upper 95%": 0.193,
         "Partial R² (derived)": 0.0446},
    ])
    st.dataframe(df, hide_index=True, use_container_width=True)
    for filename, caption in [
        ("REPORTED_ols_coefficients.svg",
         "Reported complete-case regression coefficients and confidence intervals"),
        ("REPORTED_correlations.svg",
         "Reported bivariate correlations from the author's research draft"),
        ("DERIVED_unique_explanatory_contributions.svg",
         "Algebraically derived incremental R² — not causal effects"),
    ]:
        file_path = ROOT / "docs" / "figures" / filename
        if file_path.exists():
            st.image(str(file_path), caption=caption, use_container_width=True)
    st.info(
        "Research-to-policy boundary: this single-institution observational "
        "study motivates testing inclusive mentoring and belonging supports. "
        "It does not prove those programs work, establish mediation, or "
        "justify individual student profiling."
    )
    st.markdown(
        "[Review evidence provenance and interpretation on GitHub]"
        "(https://github.com/muhammad-siddique-research/"
        "higher-ed-flourishing-prediction-ml-xai/blob/main/docs/EMPIRICAL_EVIDENCE.md)"
    )


with scenario:
    st.subheader("Illustrative perception profile")
    st.caption(
        "Adjust hypothetical scale responses to visualize the research constructs. "
        "These are NOT observed student data and NOT inputs to a trained model."
    )
    left, right = st.columns([1, 1.2])
    with left:
        community = st.slider("Sense of community", 1.0, 6.0, 4.0, 0.1)
        integrity = st.slider("Institutional integrity", 1.0, 6.0, 4.0, 0.1)
        purpose = st.slider("Meaning and purpose", 1.0, 6.0, 4.0, 0.1)
        fit = st.slider("Perceived institutional fit", 1.0, 6.0, 4.0, 0.1)
        tuition = st.slider("Perceived tuition value", 1.0, 6.0, 4.0, 0.1)
    with right:
        profile = pd.DataFrame({
            "Construct": [
                "Sense of community", "Institutional integrity",
                "Meaning and purpose", "Institutional fit", "Tuition value",
            ],
            "Illustrative response": [community, integrity, purpose, fit, tuition],
        }).set_index("Construct")
        st.bar_chart(profile, horizontal=True)
        st.caption(
            "The horizontal bars represent hypothetical responses on a 1–6 scale. "
            "They are not effect sizes, predicted thriving values, or policy thresholds."
        )
    st.markdown(
        "**Responsible use:** The profile can structure discussion of where institutional "
        "evidence is needed. No learner should be classified, penalized, or assigned services "
        "from these controls."
    )

with governance:
    st.subheader("Questions a policy-ready study must answer")
    checks = [
        "Are the flourishing construct and psychometric measures validated for this population?",
        "Were learners informed, and is use of student data authorized and privacy-protective?",
        "Does validation separate the same students, courses, or institutions across folds?",
        "Does the model generalize across time, departments, and institutions?",
        "Are errors and calibration assessed across relevant, ethically justifiable groups?",
        "Do interventions have independent educational effectiveness evidence?",
        "Is the analysis transparent to students, educators, and governance bodies?",
    ]
    for item in checks:
        st.checkbox(item, value=False, disabled=True)
    st.caption("Illustrative governance checklist; no completion or certification is implied.")
    st.markdown(
        "For institutional decisions, supplement predictive evaluation with stakeholder "
        "consultation, accessibility review, impact assessment, and appropriately designed "
        "causal research. Institution-wide aggregates are not a substitute for consent."
    )

st.divider()
st.caption(
    "Muhammad Siddique · Higher education research, explainable ML, and responsible policy. "
    "Open-source research prototype; not an admissions, advising, or student-risk system."
)
