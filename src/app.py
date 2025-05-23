import os
import datetime

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import shap
import xgboost as xgb

from data_loader import load_user_data, preprocess_user_data
from mock_api import generate_mock_nudges
from recommendation_engine import get_engagement_color, get_churn_color, get_churn_label

# Setup logs directory
LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "usage.log")
os.makedirs(LOG_DIR, exist_ok=True)

# Streamlit page config
st.set_page_config(page_title="EngageTrack AI", layout="centered")

with st.sidebar:
    st.header("EngageTrack AI")
    st.markdown("Simulated user insights and churn prediction platform.")
    st.markdown("---")
    st.write("Built with Streamlit, XGBoost, Docker, and AKS")

st.title("EngageTrack AI – User Lifecycle & Churn Insight Platform")
st.caption("Simulated SaaS analytics tool with ML-based churn prediction and engagement nudging.")
st.markdown("---")

# Load & normalize raw data
raw_df = load_user_data(raw=True)
raw_df["customerID"] = raw_df["customerID"].astype(str)
raw_df["variant"] = (
    raw_df["variant"]
    .astype(str)
    .str.strip()
    .str.upper()
    .replace({"0": "A", "1": "B"})
)

# Train model & precompute SHAP
@st.cache_resource(show_spinner=False)
def train_and_prepare():
    df_full = load_user_data(raw=True)
    X, y, scaler, encoders, features = preprocess_user_data(df_full, fit=True, return_scaler=True)

    model = xgb.XGBClassifier(
        use_label_encoder=False,
        eval_metric="logloss",
        max_depth=4,
        learning_rate=0.1,
        subsample=0.8,
        colsample_bytree=0.8,
        reg_lambda=1.0,
        reg_alpha=0.2,
        n_estimators=100,
        random_state=42,
    )
    model.fit(X, y)

    explainer = shap.Explainer(model, feature_names=features)
    X_scaled_full = scaler.transform(X)
    shap_vals = explainer(X_scaled_full)

    return model, scaler, encoders, features, explainer, shap_vals, X_scaled_full

(
    churn_model,
    churn_scaler,
    churn_encoders,
    churn_features,
    explainer,
    shap_values,
    X_full_scaled
) = train_and_prepare()

# Layout tabs
tab1, tab2, tab3 = st.tabs(["User Insights", "Analytics Dashboard", "Explainability"])

# ---------------------------
# TAB 1: User Insights
# ---------------------------
with tab1:
    st.subheader("Select a User")
    user_id = st.selectbox("Choose a user:", raw_df["customerID"].unique())

    user_row = raw_df[raw_df["customerID"] == user_id].iloc[0]
    variant = user_row.get("variant", "Unknown")

    st.markdown("### A/B Test Group")
    st.markdown(f"**Variant:** {variant}")
    st.caption(f"Raw variant value: {variant}")

    st.markdown("### AI-Generated Nudge")
    if st.button("Generate New Nudge") or "mock_nudge" not in st.session_state:
        msg, reasons = generate_mock_nudges(
            user_id=user_id,
            usage_frequency=user_row["tenure"],
            support_calls=0,
            payment_delay=int(float(user_row["TotalCharges"])),
            contract_length=user_row["Contract"],
            tech_support=user_row.get("TechSupport"),
            monthly_charges=user_row.get("MonthlyCharges"),
            paperless_billing=user_row.get("PaperlessBilling"),
            variant=variant,
            verbose=True,
        )
        st.session_state["mock_nudge"] = (msg, reasons)

    message, reasons = st.session_state["mock_nudge"]
    st.info(message)
    st.caption(f"Triggered by: {', '.join(reasons)}")

    st.markdown(f"**Contract:** {user_row['Contract']}")
    st.markdown(
        f"**Tenure:** <span style='color:{get_engagement_color(user_row['tenure'])}'>{user_row['tenure']}</span>",
        unsafe_allow_html=True,
    )
    st.markdown(f"**Monthly Charges:** ${user_row['MonthlyCharges']}")
    st.markdown(f"**Total Charges:** ${user_row['TotalCharges']}")

    st.markdown("### Model-Based Churn Prediction")

    single = user_row.to_frame().T.copy()
    single["TotalCharges"] = np.log1p(float(single["TotalCharges"]))
    for col, le in churn_encoders.items():
        if col in single.columns:
            single[col] = le.transform(single[col])

    X_single = single[churn_features]
    X_single_scaled = churn_scaler.transform(X_single)

    pred = churn_model.predict(X_single_scaled)[0]
    proba = churn_model.predict_proba(X_single_scaled)[0][1]
    color = get_churn_color(proba)
    label = get_churn_label(proba)

    if pred == 1:
        st.error("Model predicts user will churn.")
    else:
        st.success("Model predicts user will stay.")

    st.markdown(f"**Probability:** {proba * 100:.2f}%")
    st.markdown(f"**Risk Level:** <span style='color:{color}'>{label}</span>", unsafe_allow_html=True)

    with st.expander("Why this prediction? (Per-user SHAP)"):
        try:
            idx = raw_df.index[raw_df["customerID"] == user_id][0]
            user_shap = shap_values[idx]
            fig, ax = plt.subplots(figsize=(8, 4))
            shap.plots.waterfall(user_shap, max_display=10, show=False)
            st.pyplot(fig)
        except Exception as e:
            st.error(f"Failed to render SHAP plot: {e}")

    summary = (
        f"User ID: {user_id}\n"
        f"Variant: {variant}\n"
        f"Prediction: {'Churn' if pred==1 else 'Retain'}\n"
        f"Probability: {proba*100:.2f}%\n"
        f"Risk Level: {label}\n"
    )
    st.download_button("Export Summary", summary, file_name=f"summary_{user_id}.txt")

    with open(LOG_FILE, "a") as f:
        f.write(
            f"{datetime.datetime.now().isoformat()}, user={user_id}, "
            f"variant={variant}, pred={pred}, prob={proba:.3f}\n"
        )

# ---------------------------
# TAB 2: Analytics Dashboard
# ---------------------------
with tab2:
    st.subheader("System-wide Metrics")
    st.markdown("Contracts")
    st.bar_chart(raw_df["Contract"].value_counts(), use_container_width=True)

    st.markdown("Tenure Distribution")
    st.bar_chart(raw_df["tenure"].value_counts().sort_index(), use_container_width=True)

    st.markdown("Monthly Charges Distribution")
    st.bar_chart(raw_df["MonthlyCharges"].value_counts().sort_index(), use_container_width=True)

    st.markdown("Total Charges Distribution")
    st.bar_chart(raw_df["TotalCharges"].value_counts().sort_index(), use_container_width=True)

    st.markdown("A/B Variant Distribution")
    st.bar_chart(raw_df["variant"].value_counts(), use_container_width=True)

    st.markdown("Churn Rate by Variant")
    churn_rates = (
        raw_df.groupby("variant")["Churn"]
        .apply(lambda s: (s == "Yes").mean() * 100)
    )
    st.bar_chart(churn_rates, use_container_width=True)

# ---------------------------
# TAB 3: Explainability
# ---------------------------
with tab3:
    st.subheader("SHAP Summary Plot – Global Feature Impact")
    fig, ax = plt.subplots()
    shap.summary_plot(
        shap_values, features=X_full_scaled, feature_names=churn_features, show=False
    )
    st.pyplot(fig)
