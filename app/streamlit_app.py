import streamlit as st
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Higher Ed Thriving AI Decision Engine",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 Undergraduate Thriving Predictor & Decision Engine")
st.markdown("Inference engine predicting student flourishing (**Thriving Quotient**) from psychosocial and environmental inputs.")

# Layout: 2 Columns for inputs
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Psychosocial & Relational Inputs")
    scomm = st.slider("Sense of Community (1.0 - 6.0)", 1.0, 6.0, 4.74, 0.1, help="Interpersonal belonging and peer support")
    integrity = st.slider("Institutional Integrity (1.0 - 6.0)", 1.0, 6.0, 4.58, 0.1, help="Transparency and mission alignment")
    spir = st.slider("Spirituality & Purpose (1.0 - 6.0)", 1.0, 6.0, 5.20, 0.1, help="Existential meaning and purpose")
    fit = st.slider("Perceived Institutional Fit (1.0 - 6.0)", 1.0, 6.0, 4.50, 0.1, help="Alignment with university goals")

with col2:
    st.subheader("Demographic & Background Attributes")
    tuition = st.slider("Tuition Value Perception (1.0 - 6.0)", 1.0, 6.0, 4.00, 0.1, help="Perceived return on educational investment")
    firstgen = st.selectbox("First-Generation Student Status", [0, 1], format_func=lambda x: "Yes (First-Gen)" if x == 1 else "No (Continuing-Gen)")
    gender = st.selectbox("Student Gender Identity", [0, 1], format_func=lambda x: "Female" if x == 1 else "Male")
    famincome = st.selectbox("Family Income Tier", [1, 2, 3, 4, 5], format_func=lambda x: f"Income Bracket {x}")

    # Model inference based on econometric parameter estimation
    predicted_tq = 2.293 + (0.405 * scomm) - (0.030 * integrity) + (0.110 * spir) + (0.040 * fit)

    st.markdown("---")
    st.metric(label="Predicted Thriving Quotient (TQ Score)", value=f"{predicted_tq:.2f} / 6.00")

    if predicted_tq >= 4.80:
        st.success("🟢 **Optimal Flourishing Tier:** Strong academic determination, cognitive engagement, and positive perspective.")
    elif predicted_tq >= 4.10:
        st.info("🟡 **Moderate Thriving Tier:** Stable baseline; benefits from peer-mentoring and living-learning communities.")
    else:
        st.warning("🔴 **Developmental Risk Tier:** Requires proactive advising and targeted relational intervention.")
