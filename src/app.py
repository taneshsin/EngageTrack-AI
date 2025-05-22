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
from recommendation_engine import get_engagement_color, get_churn_color, get_churn_label

from sklearn.preprocessing import LabelEncoder, StandardScaler
import xgboost as xgb

# Load real user data
df = load_user_data()

# ✅ Churn model training
@st.cache_resource
def train_churn_model():
    churn_df = pd.read_csv("data/churn.csv").copy()
    churn_df = churn_df.drop(columns=["CustomerID"])
    churn_df["Payment Delay"] = pd.to_numeric(churn_df["Payment Delay"], errors="coerce").fillna(0)
    churn_df["Payment Delay"] = np.log1p(churn_df["Payment Delay"])

    label_cols = ['Gender', 'Subscription Type', 'Contract Length']
    le_dict = {}
    for col in label_cols:
        le = LabelEncoder()
        churn_df[col] = le.fit_transform(churn_df[col])
        le_dict[col] = le

    if 'variant' in churn_df.columns:
        churn_df = churn_df.drop(columns=["variant"])

    X = churn_df.drop(columns=["Churn", "Last Interaction", "Subscription Type"])
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

    return model, scaler, le_dict, X.columns.tolist()

churn_model, churn_scaler, churn_encoders, churn_features = train_churn_model()

# Tabs
tab1, tab2, tab3 = st.tabs(["🔍 User Insights", "📈 Analytics Dashboard", "🧠 Explainability"])

# ---------------------------
# TAB 1: User Insights
# ---------------------------
with tab1:
    user_id = st.selectbox("Choose a user:", df["CustomerID"].unique())
    user_data = df[df["CustomerID"] == user_id].iloc[0]

    LOG_PATH = "/tmp/usage.log"
    try:
        with open(LOG_PATH, "a") as log_file:
            log_file.write(f"[{datetime.datetime.now()}] Viewed: {user_id}\n")
    except Exception as e:
        st.warning(f"⚠️ Logging failed: {e}")

    st.subheader("💡 AI-Generated Nudge")
    if st.button("🔄 Generate New Nudge"):
        st.session_state["mock_nudge"] = generate_mock_nudge(
            user_id="there",
            usage_frequency=user_data["Usage Frequency"],
            support_calls=user_data["Support Calls"],
            payment_delay=int(float(user_data["Payment Delay"])),
            contract_length=user_data["Contract Length"]
        )
    if "mock_nudge" not in st.session_state:
        st.session_state["mock_nudge"] = generate_mock_nudge(
            user_id="there",
            usage_frequency=user_data["Usage Frequency"],
            support_calls=user_data["Support Calls"],
            payment_delay=int(float(user_data["Payment Delay"])),
            contract_length=user_data["Contract Length"]
        )
    st.info(st.session_state["mock_nudge"])

    st.markdown(f"**📿 Subscription Type:** {user_data['Subscription Type']}")
    st.markdown(f"**🗕 Contract Type:** {user_data['Contract Length']}")
    st.markdown(f"**🔥 Usage Frequency:** <span style='color:{get_engagement_color(user_data['Usage Frequency'])}'>{user_data['Usage Frequency']}</span>", unsafe_allow_html=True)
    st.markdown(f"**📞 Support Calls:** {user_data['Support Calls']}")
    st.markdown(f"**⏳ Payment Delay:** {user_data['Payment Delay']} days")
    st.markdown(f"**💰 Total Spend:** ${user_data['Total Spend']}")
    st.markdown(f"**🕒 Last Interaction:** {user_data['Last Interaction']} days ago")
    if 'variant' in user_data:
        st.markdown(f"**🧪 Variant:** {user_data['variant']}")

    st.divider()
    st.subheader("🔮 Real Churn Prediction (Model-Based)")

    input_row = user_data.to_frame().T.copy()
    input_row["Payment Delay"] = np.log1p(float(input_row["Payment Delay"]))
    for col in ['Gender', 'Subscription Type', 'Contract Length']:
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

    summary_text = f"""
User ID: {user_id}
Contract: {user_data['Contract Length']}
Subscription Type: {user_data['Subscription Type']}
Usage: {user_data['Usage Frequency']}
Support Calls: {user_data['Support Calls']}
Payment Delay: {user_data['Payment Delay']} days
Total Spend: ${user_data['Total Spend']}
Last Interaction: {user_data['Last Interaction']} days ago
Variant: {user_data.get('variant', 'N/A')}
Churn Probability: {proba:.4f}
Nudge: {st.session_state["mock_nudge"]}
"""
    st.download_button(
        label="🗕 Download User Summary",
        data=summary_text,
        file_name=f"user_{user_id}_summary.txt",
        mime="text/plain"
    )

    st.caption("Built with ❤️ by Tanesh • Real ML-powered product analytics platform")

# ---------------------------
# TAB 2: Dashboard
# ---------------------------
with tab2:
    st.subheader("📈 System-wide Metrics")

    st.markdown("### 🗕 Contract Type Distribution")
    st.bar_chart(df["Contract Length"].value_counts(), use_container_width=True)

    st.markdown("### 📞 Support Call Frequency")
    st.bar_chart(df["Support Calls"].value_counts().sort_index(), use_container_width=True)

    st.markdown("### ⏳ Payment Delay Distribution (days)")
    st.bar_chart(df["Payment Delay"].value_counts().sort_index(), use_container_width=True)

    st.markdown("### 🔥 Usage Frequency Distribution")
    st.bar_chart(df["Usage Frequency"].value_counts().sort_index(), use_container_width=True)

    if 'variant' in df.columns:
        st.markdown("### 🧪 A/B Variant Assignment")
        st.bar_chart(df["variant"].value_counts(), use_container_width=True)

# ---------------------------
# TAB 3: SHAP Explainability
# ---------------------------
with tab3:
    st.subheader("🧠 SHAP Summary Plot – Global Feature Impact")

    full_input = df.copy()
    full_input["Payment Delay"] = pd.to_numeric(full_input["Payment Delay"], errors="coerce").fillna(0)
    full_input["Payment Delay"] = np.log1p(full_input["Payment Delay"])
    for col in ['Gender', 'Subscription Type', 'Contract Length']:
        full_input[col] = churn_encoders[col].transform(full_input[col])

    X_full = full_input[churn_features]
    X_scaled = churn_scaler.transform(X_full)

    explainer = shap.Explainer(churn_model)
    shap_values = explainer(X_scaled)

    fig, ax = plt.subplots()
    shap.summary_plot(shap_values, features=X_scaled, feature_names=churn_features, show=False)
    st.pyplot(fig)
