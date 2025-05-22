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

# ── Ensure logs directory exists ─────────────────────────────────────────
LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "usage.log")
os.makedirs(LOG_DIR, exist_ok=True)

# ── Page config ─────────────────────────────────────────────────────────
st.set_page_config(page_title="EngageTrack AI", layout="centered")

# ── Sidebar ───────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("📊 EngageTrack AI")
    st.markdown("Simulated user insights & churn prediction platform.")
    st.markdown("---")
    st.write("Built with Streamlit + XGBoost + Docker + AKS")

# ── Title & Description ───────────────────────────────────────────────────
st.title("🚀 EngageTrack AI – User Lifecycle & Churn Insight Platform")
st.caption("Simulated SaaS analytics tool with ML-based churn prediction, engagement nudging, and A/B experimentation.")
st.markdown("---")

# ── Load raw data for UI (keeps customerID, variant, etc.) ───────────────
raw_df = load_user_data(raw=True)
raw_df["customerID"] = raw_df["customerID"].astype(str)

# ── Train churn model ─────────────────────────────────────────────────────
@st.cache_resource
def train_churn_model():
    # load raw so we keep all columns
    churn_df = load_user_data(raw=True)
    X, y, scaler, encoders, features = preprocess_user_data(
        churn_df,
        fit=True,
        return_scaler=True
    )
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
        random_state=42
    )
    model.fit(X, y)
    return model, scaler, encoders, features

churn_model, churn_scaler, churn_encoders, churn_features = train_churn_model()

# ── Tabs ───────────────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["🔍 User Insights", "📈 Analytics Dashboard", "🧠 Explainability"])

# ---------------------------
# TAB 1: User Insights
# ---------------------------
with tab1:
    df_shuffled = raw_df.sample(frac=1, random_state=42).reset_index(drop=True)
    user_id = st.selectbox("Choose a user:", df_shuffled["customerID"].unique())

    user_row = df_shuffled[df_shuffled["customerID"] == user_id]
    if user_row.empty:
        st.error(f"No user found with ID: {user_id}")
        st.stop()
    user_data = user_row.iloc[0]

    raw_var = str(user_data.get("variant", "Unknown")).strip()
    variant = {"0": "A", "1": "B", "A": "A", "B": "B"}.get(raw_var, "Unknown")

    st.subheader("🧪 A/B Test Group")
    st.markdown(f"**Variant:** {'🅰️' if variant=='A' else '🅱️' if variant=='B' else '❓'}")
    st.caption(f"Raw variant value: `{raw_var}`")

    st.subheader("💡 AI-Generated Nudge")
    if st.button("🔄 Generate New Nudge") or "mock_nudge" not in st.session_state:
        msg, reasons = generate_mock_nudges(
            user_id=user_id,
            usage_frequency=user_data["tenure"],
            support_calls=0,
            payment_delay=int(float(user_data["TotalCharges"])),
            contract_length=user_data["Contract"],
            tech_support=user_data.get("TechSupport"),
            monthly_charges=user_data.get("MonthlyCharges"),
            paperless_billing=user_data.get("PaperlessBilling"),
            variant=variant,
            verbose=True
        )
        st.session_state["mock_nudge"] = (msg, reasons)

    message, reasons = st.session_state["mock_nudge"]
    st.info(message)
    st.caption(f"🔍 Triggered by: {', '.join(reasons)}")

    st.markdown(f"**📃 Contract Type:** {user_data['Contract']}")
    st.markdown(f"**💳 Payment Method:** {user_data['PaymentMethod']}")
    st.markdown(
        f"**🔥 Tenure:** <span style='color:{get_engagement_color(user_data['tenure'])}'>{user_data['tenure']}</span>",
        unsafe_allow_html=True
    )
    st.markdown(f"**💸 Monthly Charges:** ${user_data['MonthlyCharges']}")
    st.markdown(f"**💰 Total Charges:** ${user_data['TotalCharges']}")

    st.divider()
    st.subheader("🔮 Real Churn Prediction (Model-Based)")

    # build single-row for inference
    single = user_data.to_frame().T.copy()
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
        st.error("❌ Model predicts user will churn.")
    else:
        st.success("✅ Model predicts user will stay.")

    st.markdown(f"**Churn Probability:** {proba*100:.2f}%")
    st.markdown(f"**Risk Level:** <span style='color:{color}'>{label}</span>", unsafe_allow_html=True)

    with st.expander("🔍 View model input features"):
        st.write(X_single)

    summary = (
        f"User ID: {user_id}\n"
        f"Variant: {variant}\n"
        f"Prediction: {'Churn' if pred==1 else 'Retain'}\n"
        f"Probability: {proba*100:.2f}%\n"
        f"Risk Level: {label}\n"
    )
    st.download_button("📤 Export Summary", summary, file_name=f"summary_{user_id}.txt")

    # log to file
    with open(LOG_FILE, "a") as f:
        now = datetime.datetime.now().isoformat()
        f.write(f"{now}, user={user_id}, variant={variant}, pred={pred}, prob={proba:.3f}\n")

# ---------------------------
# TAB 2: Analytics Dashboard
# ---------------------------
with tab2:
    st.subheader("📈 System-wide Metrics")

    st.markdown("**📃 Contracts**")
    st.bar_chart(raw_df["Contract"].value_counts(), use_container_width=True)

    st.markdown("**⏳ Tenure Distribution**")
    st.bar_chart(raw_df["tenure"].value_counts().sort_index(), use_container_width=True)

    st.markdown("**💸 Monthly Charges Distribution**")
    st.bar_chart(raw_df["MonthlyCharges"].value_counts().sort_index(), use_container_width=True)

    st.markdown("**💰 Total Charges Distribution**")
    st.bar_chart(raw_df["TotalCharges"].value_counts().sort_index(), use_container_width=True)

    if "variant" in raw_df.columns:
        st.subheader("🧪 A/B Variant Distribution")
        st.bar_chart(raw_df["variant"].value_counts(), use_container_width=True)

        if "Churn" in raw_df.columns:
            st.subheader("❌ Churn Rate by Variant")
            summary = raw_df.groupby("variant")["Churn"].value_counts(normalize=True).unstack().fillna(0)
            if 1 in summary.columns:
                churn_rates = summary[1] * 100
                st.bar_chart(churn_rates, use_container_width=True)

# ---------------------------
# TAB 3: SHAP Explainability
# ---------------------------
with tab3:
    st.subheader("🧠 SHAP Summary Plot – Global Feature Impact")
    full_df = load_user_data(raw=True)
    X_full, _, _, _, _ = preprocess_user_data(full_df, label_encoders=churn_encoders, fit=False, return_scaler=True)
    X_full_scaled = churn_scaler.transform(X_full)

    explainer = shap.Explainer(churn_model)
    shap_values = explainer(X_full_scaled)

    fig, ax = plt.subplots()
    shap.summary_plot(shap_values, features=X_full_scaled, feature_names=churn_features, show=False)
    st.pyplot(fig)
