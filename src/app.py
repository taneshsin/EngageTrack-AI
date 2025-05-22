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
import os
import numpy as np
import shap
import matplotlib.pyplot as plt

from data_loader import load_user_data
from mock_api import generate_mock_nudge
from recommendation_engine import get_engagement_color, get_churn_color

from sklearn.preprocessing import LabelEncoder, StandardScaler
import xgboost as xgb

# Load real user data
df = load_user_data()

# ✅ Churn model training
@st.cache_resource
def train_churn_model():
    churn_df = pd.read_csv("data/churn.csv").copy()
    churn_df = churn_df.drop(columns=["customerID"])

    churn_df.replace("No internet service", "No", inplace=True)
    churn_df.replace("No phone service", "No", inplace=True)

    binary_cols = ["Partner", "Dependents", "PhoneService", "PaperlessBilling", "Churn"]
    for col in binary_cols:
        churn_df[col] = churn_df[col].map({"Yes": 1, "No": 0})

    churn_df["TotalCharges"] = pd.to_numeric(churn_df["TotalCharges"], errors="coerce")
    churn_df.dropna(inplace=True)

    cat_cols = ["gender", "MultipleLines", "InternetService", "OnlineSecurity",
                "OnlineBackup", "DeviceProtection", "TechSupport", "StreamingTV",
                "StreamingMovies", "Contract", "PaymentMethod"]
    le_dict = {}
    for col in cat_cols:
        le = LabelEncoder()
        churn_df[col] = le.fit_transform(churn_df[col])
        le_dict[col] = le

    features = [col for col in churn_df.columns if col != "Churn"]
    X = churn_df[features]
    y = churn_df["Churn"]

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    model = xgb.XGBClassifier(
        use_label_encoder=False,
        eval_metric='logloss',
        max_depth=4,
        learning_rate=0.1,
        subsample=0.8,
        colsample_bytree=0.8,
        reg_lambda=1.0,
        reg_alpha=0.2,
        n_estimators=100,
        scale_pos_weight=2.5
    )
    model.fit(X_scaled, y)

    return model, scaler, le_dict, features

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
    if st.button("🔄 Generate New Nudge"):
        st.session_state["mock_nudge"] = generate_mock_nudge(
            user_id=user_id,
            usage_frequency=user_data["MonthlyCharges"],
            support_calls=user_data["tenure"],
            payment_delay=user_data["TotalCharges"],
            contract_length=user_data["Contract"]
        )
    if "mock_nudge" not in st.session_state:
        st.session_state["mock_nudge"] = generate_mock_nudge(
            user_id=user_id,
            usage_frequency=user_data["MonthlyCharges"],
            support_calls=user_data["tenure"],
            payment_delay=user_data["TotalCharges"],
            contract_length=user_data["Contract"]
        )
    st.info(st.session_state["mock_nudge"])

    st.markdown(f"**🧾 Gender:** {user_data['gender']}")
    st.markdown(f"**📶 Internet Service:** {user_data['InternetService']}")
    st.markdown(f"**📞 Tenure:** {user_data['tenure']} months")
    st.markdown(f"**💵 Monthly Charges:** ${user_data['MonthlyCharges']}")
    st.markdown(f"**💰 Total Charges:** ${user_data['TotalCharges']}")
    st.markdown(f"**📄 Contract:** {user_data['Contract']}")

    st.divider()
    st.subheader("🔮 Real Churn Prediction (Model-Based)")

    input_row = user_data.to_frame().T.copy()
    for col in churn_encoders:
        input_row[col] = churn_encoders[col].transform(input_row[col])

    X_input = input_row[churn_features]
    X_input_scaled = churn_scaler.transform(X_input)

    pred = churn_model.predict(X_input_scaled)[0]
    proba = churn_model.predict_proba(X_input_scaled)[0][1]

    if proba > 0.75:
        risk_label = "High"
        risk_color = "red"
    elif proba > 0.5:
        risk_label = "Medium"
        risk_color = "orange"
    else:
        risk_label = "Low"
        risk_color = "green"

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
    st.subheader("📈 System-wide Metrics")

    st.markdown("### 📄 Contract Type Distribution")
    st.bar_chart(df["Contract"].value_counts(), use_container_width=True)

    st.markdown("### 💵 Monthly Charges Distribution")
    st.bar_chart(df["MonthlyCharges"].value_counts().sort_index(), use_container_width=True)

    st.markdown("### 📶 Internet Service Types")
    st.bar_chart(df["InternetService"].value_counts(), use_container_width=True)

# ---------------------------
# TAB 3: SHAP Explainability
# ---------------------------
with tab3:
    st.subheader("🧠 SHAP Summary Plot – Global Feature Impact")

    full_input = df.copy()
    for col in churn_encoders:
        full_input[col] = churn_encoders[col].transform(full_input[col])

    X_full = full_input[churn_features]
    X_scaled = churn_scaler.transform(X_full)

    explainer = shap.Explainer(churn_model)
    shap_values = explainer(X_scaled)

    fig, ax = plt.subplots()
    shap.summary_plot(shap_values, features=X_scaled, feature_names=churn_features, show=False)
    st.pyplot(fig)
