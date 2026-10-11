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

overview, scenario, governance = st.tabs([
    "Research overview", "Explore student-experience dimensions", "Policy & governance",
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
