import streamlit as st

# ✅ Page config
st.set_page_config(page_title="EngageTrack AI", layout="centered")

# ✅ Sidebar
with st.sidebar:
    st.header("📊 EngageTrack AI")
    st.markdown("Simulated user insights & churn prediction platform.")
    st.markdown("---")
    st.write("Built with Streamlit + XGBoost + Docker + AKS")

# ✅ Title & Description
st.title("🚀 EngageTrack AI – User Lifecycle & Churn Insight Platform")
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

# ✅ FIXED: Load raw version so customerID exists for UI
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
tab1, tab2, tab3 = st.tabs(["🔍 User Insights", "📈 Analytics Dashboard", "🧠 Explainability"])

# ---------------------------
# TAB 1: User Insights
# ---------------------------
with tab1:
    user_id = st.selectbox("Choose a user:", df["customerID"].unique())
    user_data = df[df["customerID"] == user_id].iloc[0]

    LOG_PATH = "/tmp/usage.log"
    try:
        with open(LOG_PATH, "a") as log_file:
            log_file.write(f"[{datetime.datetime.now()}] Viewed: {user_id}\n")
    except Exception as e:
        st.warning(f"⚠️ Logging failed: {e}")

    st.subheader("💡 AI-Generated Nudge")
    if st.button("🔄 Generate New Nudge") or "mock_nudge" not in st.session_state:
        message, reasons = generate_mock_nudges(
            user_id=user_id,
            usage_frequency=user_data["tenure"],
            support_calls=0,
            payment_delay=int(float(user_data["TotalCharges"])),
            contract_length=user_data["Contract"],
            tech_support=user_data.get("TechSupport", None),
            monthly_charges=user_data.get("MonthlyCharges", None),
            paperless_billing=user_data.get("PaperlessBilling", None),
            verbose=True
        )
        st.session_state["mock_nudge"] = (message, reasons)

    message, reasons = st.session_state["mock_nudge"]
    st.info(message)
    st.caption(f"🔍 Triggered by: {', '.join(reasons)}")

    st.markdown(f"**📿 Contract Type:** {user_data['Contract']}")
    st.markdown(f"**📝 Payment Method:** {user_data['PaymentMethod']}")
    st.markdown(f"**🔥 Tenure (Engagement):** <span style='color:{get_engagement_color(user_data['tenure'])}'>{user_data['tenure']}</span>", unsafe_allow_html=True)
    st.markdown(f"**💳 Monthly Charges:** ${user_data['MonthlyCharges']}")
    st.markdown(f"**💸 Total Charges:** ${user_data['TotalCharges']}")
    if 'variant' in user_data:
        st.markdown(f"**🧪 Variant:** {user_data['variant']}")

    st.divider()
    st.subheader("🔮 Real Churn Prediction (Model-Based)")

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
        st.error("❌ Model predicts user will churn.")
    else:
        st.success("✅ Model predicts user will stay.")

    st.markdown(f"**Churn Probability:** {proba * 100:.2f}%")
    st.markdown(f"**Risk Level:** <span style='color:{risk_color}'>{risk_label}</span>", unsafe_allow_html=True)

    with st.expander("🔍 View model input features"):
        st.write(pd.DataFrame(X_input))

# ---------------------------
# TAB 2: Dashboard
# ---------------------------
with tab2:
    st.subheader("📊 System-wide Metrics")
    st.bar_chart(df["Contract"].value_counts(), use_container_width=True)
    st.bar_chart(df["tenure"].value_counts().sort_index(), use_container_width=True)
    st.bar_chart(df["MonthlyCharges"].value_counts().sort_index(), use_container_width=True)
    st.bar_chart(df["TotalCharges"].value_counts().sort_index(), use_container_width=True)
    if 'variant' in df.columns:
        st.bar_chart(df["variant"].value_counts(), use_container_width=True)

# ---------------------------
# TAB 3: SHAP Explainability
# ---------------------------
with tab3:
    st.subheader("🧠 SHAP Summary Plot – Global Feature Impact")
    churn_df = pd.read_csv("data/churn.csv")
    X_scaled, _, _, _, _ = preprocess_user_data(
        churn_df, label_encoders=churn_encoders, fit=False, return_scaler=False
    )
    X_scaled = churn_scaler.transform(X_scaled)

    explainer = shap.Explainer(churn_model)
    shap_values = explainer(X_scaled)

    fig, ax = plt.subplots()
    shap.summary_plot(shap_values, features=X_scaled, feature_names=churn_features, show=False)
    st.pyplot(fig)
