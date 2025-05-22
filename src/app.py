import streamlit as st

# ✅ Page config
st.set_page_config(page_title="EngageTrack AI", layout="centered")

# ✅ Sidebar
with st.sidebar:
    st.header("\ud83d\udcca EngageTrack AI")
    st.markdown("Simulated user insights & churn prediction platform.")
    st.markdown("---")
    st.write("Built with Streamlit + XGBoost + Docker + AKS")

# ✅ Title & Description
st.title("\ud83d\ude80 EngageTrack AI \u2013 User Lifecycle & Churn Insight Platform")
st.caption("Simulated SaaS analytics tool with ML-based churn prediction, engagement nudging, and A/B experimentation.")
st.markdown("---")

import pandas as pd
import datetime
import numpy as np
import shap
import matplotlib.pyplot as plt

from data_loader import load_user_data, preprocess_user_data
from mock_api import generate_mock_nudges
from recommendation_engine import get_engagement_color, get_churn_color, get_churn_label

import xgboost as xgb

# ✅ Load raw data for UI
df = load_user_data(raw=True)

# ✅ Train churn model
@st.cache_resource
def train_churn_model():
    churn_df = pd.read_csv("data/churn.csv")
    X_scaled, y, scaler, encoders, features = preprocess_user_data(
        churn_df, fit=True, return_scaler=True
    )
    model = xgb.XGBClassifier(
        use_label_encoder=False,
        eval_metric='logloss',
        max_depth=4,
        learning_rate=0.1,
        subsample=0.8,
        colsample_bytree=0.8,
        reg_lambda=1.0,
        reg_alpha=0.2,
        n_estimators=100
    )
    model.fit(X_scaled, y)
    return model, scaler, encoders, features

churn_model, churn_scaler, churn_encoders, churn_features = train_churn_model()

# Tabs
tab1, tab2, tab3 = st.tabs(["\ud83d\udd0d User Insights", "\ud83d\udcc8 Analytics Dashboard", "\ud83e\udde0 Explainability"])

# ---------------------------
# TAB 1: User Insights
# ---------------------------
with tab1:
    user_id = st.selectbox("Choose a user:", df["customerID"].unique())
    user_data = df[df["customerID"] == user_id].iloc[0]
    variant = user_data.get("variant", "Unknown")

    st.subheader("\ud83e\uddea A/B Test Group")
    st.markdown(f"**This user is in Variant:** `{variant}`")

    st.subheader("\ud83d\udca1 AI-Generated Nudge")
    if st.button("\ud83d\udd04 Generate New Nudge") or "mock_nudge" not in st.session_state:
        message, reasons = generate_mock_nudges(
            user_id=user_id,
            usage_frequency=user_data["tenure"],
            support_calls=0,
            payment_delay=int(float(user_data["TotalCharges"])),
            contract_length=user_data["Contract"],
            tech_support=user_data.get("TechSupport", None),
            monthly_charges=user_data.get("MonthlyCharges", None),
            paperless_billing=user_data.get("PaperlessBilling", None),
            variant=variant,
            verbose=True
        )
        st.session_state["mock_nudge"] = (message, reasons)

    message, reasons = st.session_state["mock_nudge"]
    st.info(message)
    st.caption(f"\ud83d\udd0d Triggered by: {', '.join(reasons)}")

    st.markdown(f"**\ud83d\udc7d Contract Type:** {user_data['Contract']}")
    st.markdown(f"**\ud83d\udcdc Payment Method:** {user_data['PaymentMethod']}")
    st.markdown(f"**\ud83d\udd25 Tenure (Engagement):** <span style='color:{get_engagement_color(user_data['tenure'])}'>{user_data['tenure']}</span>", unsafe_allow_html=True)
    st.markdown(f"**\ud83d\udcb3 Monthly Charges:** ${user_data['MonthlyCharges']}")
    st.markdown(f"**\ud83d\udcb8 Total Charges:** ${user_data['TotalCharges']}")

    st.divider()
    st.subheader("\ud83d\udd2e Real Churn Prediction (Model-Based)")

    input_row = user_data.to_frame().T.copy()
    input_row["TotalCharges"] = np.log1p(float(input_row["TotalCharges"]))
    for col in churn_encoders:
        if col in input_row.columns:
            input_row[col] = churn_encoders[col].transform(input_row[col])
    X_input = input_row[churn_features]
    X_input_scaled = churn_scaler.transform(X_input)

    pred = churn_model.predict(X_input_scaled)[0]
    proba = churn_model.predict_proba(X_input_scaled)[0][1]

    risk_color = get_churn_color(proba)
    risk_label = get_churn_label(proba)

    if pred == 1:
        st.error("\u274c Model predicts user will churn.")
    else:
        st.success("\u2705 Model predicts user will stay.")

    st.markdown(f"**Churn Probability:** {proba * 100:.2f}%")
    st.markdown(f"**Risk Level:** <span style='color:{risk_color}'>{risk_label}</span>", unsafe_allow_html=True)

    with st.expander("\ud83d\udd0d View model input features"):
        st.write(pd.DataFrame(X_input))

# ---------------------------
# TAB 2: Dashboard
# ---------------------------
with tab2:
    st.subheader("\ud83d\udcc8 System-wide Metrics")

    st.markdown("**\ud83d\udcc5 Contracts**")
    st.bar_chart(df["Contract"].value_counts(), use_container_width=True)

    st.markdown("**\u23f3 Tenure Distribution**")
    st.bar_chart(df["tenure"].value_counts().sort_index(), use_container_width=True)

    st.markdown("**\ud83d\udcb3 Monthly Charges Distribution**")
    st.bar_chart(df["MonthlyCharges"].value_counts().sort_index(), use_container_width=True)

    st.markdown("**\ud83d\udcb8 Total Charges Distribution**")
    st.bar_chart(df["TotalCharges"].value_counts().sort_index(), use_container_width=True)

    if 'variant' in df.columns:
        st.subheader("\ud83e\uddea A/B Variant Distribution")
        st.bar_chart(df["variant"].value_counts(), use_container_width=True)

        if "Churn" in df.columns:
            st.subheader("\u274c Churn Rate by Variant")
            churn_summary = df.groupby("variant")["Churn"].value_counts(normalize=True).unstack().fillna(0)
            if 1 in churn_summary.columns:
                churn_rate = churn_summary[1] * 100
                st.bar_chart(churn_rate)

# ---------------------------
# TAB 3: SHAP Explainability
# ---------------------------
with tab3:
    st.subheader("\ud83e\udde0 SHAP Summary Plot \u2013 Global Feature Impact")
    churn_df = pd.read_csv("data/churn.csv")

    X_scaled, _, _, _, _ = preprocess_user_data(
        churn_df, label_encoders=churn_encoders, fit=False, return_scaler=True
    )
    X_scaled = churn_scaler.transform(X_scaled)

    explainer = shap.Explainer(churn_model)
    shap_values = explainer(X_scaled)

    fig, ax = plt.subplots()
    shap.summary_plot(shap_values, features=X_scaled, feature_names=churn_features, show=False)
    st.pyplot(fig)
