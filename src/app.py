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
from mock_api import generate_mock_nudges
from recommendation_engine import get_engagement_color, get_churn_color, get_churn_label

from sklearn.preprocessing import LabelEncoder, StandardScaler
import xgboost as xgb

# Load real user data
df = load_user_data()

# ✅ Churn model training
@st.cache_resource
def train_churn_model():
    churn_df = pd.read_csv("data/churn.csv").copy()
    churn_df = churn_df.drop(columns=["customerID"], errors="ignore")
    churn_df = churn_df[churn_df["TotalCharges"] != " "]
    churn_df["TotalCharges"] = churn_df["TotalCharges"].astype(float)
    churn_df["TotalCharges"] = np.log1p(churn_df["TotalCharges"])

    label_cols = churn_df.select_dtypes(include="object").columns.tolist()
    label_encoders = {}
    for col in label_cols:
        le = LabelEncoder()
        churn_df[col] = le.fit_transform(churn_df[col])
        label_encoders[col] = le

    if "variant" in churn_df.columns:
        churn_df = churn_df.drop(columns=["variant"])

    X = churn_df.drop(columns=["Churn"])
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
        n_estimators=100
    )
    model.fit(X_scaled, y)

    return model, scaler, label_encoders, X.columns.tolist()

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
        st.session_state["mock_nudge"] = generate_mock_nudges(
            user_id=user_id,
            usage_frequency=user_data["tenure"],
            support_calls=0,
            payment_delay=int(float(user_data["TotalCharges"])),
            contract_length=user_data["Contract"]
        )
    if "mock_nudge" not in st.session_state:
        st.session_state["mock_nudge"] = generate_mock_nudges(
            user_id=user_id,
            usage_frequency=user_data["tenure"],
            support_calls=0,
            payment_delay=int(float(user_data["TotalCharges"])),
            contract_length=user_data["Contract"]
        )
    st.info(st.session_state["mock_nudge"])

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
    st.subheader("📈 System-wide Metrics")
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
    full_input = df.copy()
    full_input = full_input[full_input["TotalCharges"] != " "]
    full_input["TotalCharges"] = full_input["TotalCharges"].astype(float)
    full_input["TotalCharges"] = np.log1p(full_input["TotalCharges"])
    for col in churn_encoders:
        if col in full_input.columns:
            full_input[col] = churn_encoders[col].transform(full_input[col])

    X_full = full_input[churn_features]
    X_scaled = churn_scaler.transform(X_full)
    explainer = shap.Explainer(churn_model)
    shap_values = explainer(X_scaled)

    fig, ax = plt.subplots()
    shap.summary_plot(shap_values, features=X_scaled, feature_names=churn_features, show=False)
    st.pyplot(fig)
