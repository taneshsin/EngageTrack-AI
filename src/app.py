
import streamlit as st
import pandas as pd
import datetime
import os

from data_loader import load_user_data
from mock_api import generate_mock_nudge
from recommendation_engine import get_engagement_color, get_churn_color

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
import xgboost as xgb

# Load processed user data
df = load_user_data()

# Load churn model
@st.cache_resource
def train_churn_model():
    churn_df = pd.read_csv("data/customer_churn_dataset-testing-master.csv").copy()
    churn_df = churn_df.drop(columns=["CustomerID"])

    # Encode categoricals
    label_cols = ['Gender', 'Subscription Type', 'Contract Length']
    le_dict = {}
    for col in label_cols:
        le = LabelEncoder()
        churn_df[col] = le.fit_transform(churn_df[col])
        le_dict[col] = le

    # Prepare X, y
    X = churn_df.drop(columns=["Churn"])
    y = churn_df["Churn"]

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    model = xgb.XGBClassifier(use_label_encoder=False, eval_metric='logloss')
    model.fit(X_scaled, y)

    return model, scaler, le_dict, X.columns.tolist()

churn_model, churn_scaler, churn_encoders, churn_features = train_churn_model()

st.set_page_config(page_title="EngageTrack AI", layout="centered")
tab1, tab2 = st.tabs(["🔍 User Insights", "📈 Analytics Dashboard"])

# ---------------------------
# TAB 1: User Insights
# ---------------------------
with tab1:
    user_id = st.selectbox("Choose a user:", df["user_id"].unique())
    user_data = df[df["user_id"] == user_id].iloc[0]

    LOG_PATH = "/tmp/usage.log"

    try:
        with open(LOG_PATH, "a") as log_file:
            log_file.write(f"[{datetime.datetime.now()}] Viewed: {user_id}\n")
    except Exception as e:
        import pwd
        user = pwd.getpwuid(os.getuid()).pw_name
        st.warning(f"⚠️ Logging failed: {e}")
        st.warning(f"🧾 Running as user: {user}")
        st.warning(f"📁 Current directory: {os.getcwd()}")
        st.warning(f"📄 Files in /tmp/: {os.listdir('/tmp')}")

    st.subheader("💡 AI-Generated Nudge")
    if st.button("🔄 Generate New Nudge"):
        st.session_state["mock_nudge"] = generate_mock_nudge(
            user_id=user_id,
            engagement_level=user_data['engagement_level'],
            persona=user_data['persona']
        )

    if "mock_nudge" not in st.session_state:
        st.session_state["mock_nudge"] = generate_mock_nudge(
            user_id=user_id,
            engagement_level=user_data['engagement_level'],
            persona=user_data['persona']
        )

    st.info(st.session_state["mock_nudge"])

    st.markdown(f"**👤 Persona:** {user_data['persona']}")
    st.markdown(f"**🗓 Plan:** {user_data['plan_type']}")
    st.markdown(f"**🔥 Engagement Level:** <span style='color:{get_engagement_color(user_data['engagement_level'])}'>{user_data['engagement_level']}</span>", unsafe_allow_html=True)
    st.markdown(f"**⏱ Days Since Last Active:** {int(user_data['days_since_active'])}")
    st.markdown(f"**🚨 Churn Risk:** <span style='color:{get_churn_color(user_data['churn_risk'])}'>{user_data['churn_risk']}</span>", unsafe_allow_html=True)
    st.markdown(f"**🧪 A/B Test Variant:** {user_data['variant']}")

    st.divider()

    st.subheader("🧠 AI Feature Recommendation")
    st.success(f"Try this next: **{user_data['recommended_feature']}**")

    st.subheader("💬 Lifecycle Nudge")
    nudge = user_data.get("nudge_action", "None")

    if pd.isna(nudge) or nudge == "None":
        st.info("No nudges needed — user is healthy!")
    else:
        st.warning(nudge)

    summary_text = f"""
User: {user_id}
Persona: {user_data['persona']}
Plan: {user_data['plan_type']}
Engagement: {user_data['engagement_level']}
Churn Risk: {user_data['churn_risk']}
Recommended Feature: {user_data['recommended_feature']}
Lifecycle Nudge: {user_data.get("nudge_action", "None")}
"""
    st.download_button(
        label="📥 Download User Summary",
        data=summary_text,
        file_name=f"{user_id}_summary.txt",
        mime="text/plain"
    )

    st.divider()

    st.subheader("🔮 Real Churn Prediction (Model-Based)")

    row_selector = st.slider("Select reference row from churn dataset (0 to 999)", 0, 999, 0)
    churn_data = pd.read_csv("data/customer_churn_dataset-testing-master.csv")
    input_row = churn_data.iloc[row_selector:row_selector+1].copy()

    for col in ['Gender', 'Subscription Type', 'Contract Length']:
        input_row[col] = churn_encoders[col].transform(input_row[col])

    X_input = input_row.drop(columns=["CustomerID", "Churn"])
    X_input_scaled = churn_scaler.transform(X_input)

    pred = churn_model.predict(X_input_scaled)[0]
    proba = churn_model.predict_proba(X_input_scaled)[0][1]

    st.markdown(f"**Model Prediction:** {'🟥 Churn' if pred == 1 else '🟩 Retained'}")
    st.markdown(f"**Churn Probability:** `{proba * 100:.2f}%`")

    st.subheader("📣 Model-Based Nudge")
    if proba > 0.7:
        st.info("🚨 High Risk! Offer a special discount or loyalty program.")
    elif proba > 0.4:
        st.warning("⚠️ Medium Risk. Recommend sending a feature update email.")
    else:
        st.success("✅ Low Risk. Celebrate customer loyalty with a thank-you message!")

    st.caption("Built with ❤️ by Tanesh • Simulated product analytics platform")

# ---------------------------
# TAB 2: Dashboard
# ---------------------------
with tab2:
    st.subheader("📊 System-wide Metrics")

    st.markdown("**Engagement Level Breakdown**")
    eng_dist = df['engagement_level'].value_counts()
    st.bar_chart(eng_dist)

    st.markdown("**Churn Risk Distribution**")
    churn_dist = df['churn_risk'].value_counts()
    st.bar_chart(churn_dist)

    st.markdown("**Plan Type Segmentation**")
    plan_dist = df['plan_type'].value_counts()
    st.bar_chart(plan_dist)

    st.markdown("**🧪 A/B Test Split**")
    variant_dist = df["variant"].value_counts()
    st.bar_chart(variant_dist)
