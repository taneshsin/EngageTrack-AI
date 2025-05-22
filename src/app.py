import streamlit as st

# ✅ Page config
st.set_page_config(page_title="EngageTrack AI", layout="centered")

# ✅ Sidebar
with st.sidebar:
    st.header("\U0001F4CA EngageTrack AI")
    st.markdown("Simulated user insights & churn prediction platform.")
    st.markdown("---")
    st.write("Built with Streamlit + XGBoost + Docker + AKS")

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
from sklearn.model_selection import train_test_split
import xgboost as xgb

# Load real user data
df = load_user_data()

@st.cache_resource
def train_churn_model():
    churn_df = pd.read_csv("data/churn.csv").copy()

    # Clean and encode
    churn_df['TotalCharges'] = pd.to_numeric(churn_df['TotalCharges'], errors='coerce')
    churn_df = churn_df.dropna()

    churn_df['Churn'] = churn_df['Churn'].apply(lambda x: 1 if x == 'Yes' else 0)

    binary_cols = ['gender', 'Partner', 'Dependents', 'PhoneService', 'PaperlessBilling']
    for col in binary_cols:
        churn_df[col] = churn_df[col].apply(lambda x: 1 if x == 'Yes' else 0)

    # Drop unneeded columns
    churn_df = churn_df.drop(columns=['customerID'])
    if 'variant' in churn_df.columns:
        churn_df = churn_df.drop(columns=['variant'])

    # One-hot encode multi-category columns
    cat_cols = ['MultipleLines', 'InternetService', 'OnlineSecurity', 'OnlineBackup',
                'DeviceProtection', 'TechSupport', 'StreamingTV', 'StreamingMovies',
                'Contract', 'PaymentMethod']
    churn_df = pd.get_dummies(churn_df, columns=cat_cols)

    # Features + target
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

    return model, scaler, X.columns.tolist()

churn_model, churn_scaler, churn_features = train_churn_model()

# Tabs
tab1, tab2, tab3 = st.tabs(["\U0001F50D User Insights", "\U0001F4C8 Analytics Dashboard", "\U0001F9E0 Explainability"])

with tab1:
    user_id = st.selectbox("Choose a user:", df["customerID"].unique())
    user_data = df[df["customerID"] == user_id].iloc[0]

    # Logging
    try:
        with open("/tmp/usage.log", "a") as log_file:
            log_file.write(f"[{datetime.datetime.now()}] Viewed: {user_id}\n")
    except Exception as e:
        st.warning(f"⚠️ Logging failed: {e}")

    st.subheader("\U0001F4A1 AI-Generated Nudge")
    if st.button("\U0001F504 Generate New Nudge"):
        st.session_state["mock_nudge"] = generate_mock_nudges(
            user_id=user_id,
            usage_frequency=user_data["Usage Frequency"],
            support_calls=user_data["Support Calls"],
            payment_delay=int(float(user_data["Payment Delay"])),
            contract_length=user_data["Contract Length"]
        )

    if "mock_nudge" not in st.session_state:
        st.session_state["mock_nudge"] = generate_mock_nudges(
            user_id=user_id,
            usage_frequency=user_data["Usage Frequency"],
            support_calls=user_data["Support Calls"],
            payment_delay=int(float(user_data["Payment Delay"])),
            contract_length=user_data["Contract Length"]
        )
    st.info(st.session_state["mock_nudge"])

    st.markdown(f"**\U0001F4B0 Monthly Charges:** ${user_data['MonthlyCharges']}")
    st.markdown(f"**\U0001F4B3 Total Charges:** ${user_data['TotalCharges']}")
    st.markdown(f"**\U0001F4C5 Tenure:** {user_data['tenure']} months")
    st.markdown(f"**\U0001F4DD Contract Type:** {user_data['Contract']}")
    st.markdown(f"**\U0001F1FA\U0001F1F8 Payment Method:** {user_data['PaymentMethod']}")
    st.markdown(f"**\U0001F4DE Phone Service:** {user_data['PhoneService']}")

    st.divider()
    st.subheader("\U0001F52E Real Churn Prediction")

    input_row = user_data.to_frame().T.copy()
    input_row['TotalCharges'] = pd.to_numeric(input_row['TotalCharges'], errors='coerce')
    input_row = input_row.drop(columns=['customerID'])

    # Encode binary
    for col in ['gender', 'Partner', 'Dependents', 'PhoneService', 'PaperlessBilling']:
        input_row[col] = 1 if input_row[col].values[0] == 'Yes' else 0

    # One-hot encode same as training
    input_row = pd.get_dummies(input_row)
    for col in churn_features:
        if col not in input_row.columns:
            input_row[col] = 0
    input_row = input_row[churn_features]

    input_scaled = churn_scaler.transform(input_row)
    pred = churn_model.predict(input_scaled)[0]
    proba = churn_model.predict_proba(input_scaled)[0][1]

    risk_color = get_churn_color(proba)
    risk_label = get_churn_label(proba)

    if pred == 1:
        st.error("❌ Model predicts user will churn.")
    else:
        st.success("✅ Model predicts user will stay.")

    st.markdown(f"**Churn Probability:** {proba * 100:.2f}%")
    st.markdown(f"**Risk Level:** <span style='color:{risk_color}'>{risk_label}</span>", unsafe_allow_html=True)

with tab2:
    st.subheader("📈 System-wide Metrics")

    st.markdown("### 📅 Contract Type Distribution")
    st.bar_chart(df["Contract"].value_counts(), use_container_width=True)

    st.markdown("### 💳 Payment Method Usage")
    st.bar_chart(df["PaymentMethod"].value_counts(), use_container_width=True)

    st.markdown("### 🌐 Internet Service Types")
    st.bar_chart(df["InternetService"].value_counts(), use_container_width=True)

    st.markdown("### 💰 Monthly Charges Distribution")
    st.bar_chart(df["MonthlyCharges"].value_counts().sort_index(), use_container_width=True)

    st.markdown("### 🔒 Tech Support Availability")
    st.bar_chart(df["TechSupport"].value_counts(), use_container_width=True)

    if 'variant' in df.columns:
        st.markdown("### 🧪 A/B Variant Assignment")
        st.bar_chart(df["variant"].value_counts(), use_container_width=True)

with tab3:
    st.subheader("\U0001F9E0 SHAP Explainability")

    shap_df = df.copy()
    shap_df['TotalCharges'] = pd.to_numeric(shap_df['TotalCharges'], errors='coerce')
    shap_df = shap_df.dropna()

    for col in ['gender', 'Partner', 'Dependents', 'PhoneService', 'PaperlessBilling']:
        shap_df[col] = shap_df[col].apply(lambda x: 1 if x == 'Yes' else 0)

    shap_df = pd.get_dummies(shap_df)
    for col in churn_features:
        if col not in shap_df.columns:
            shap_df[col] = 0

    shap_X = shap_df[churn_features]
    shap_X_scaled = churn_scaler.transform(shap_X)

    explainer = shap.Explainer(churn_model)
    shap_values = explainer(shap_X_scaled)

    fig, ax = plt.subplots()
    shap.summary_plot(shap_values, features=shap_X_scaled, feature_names=churn_features, show=False)
    st.pyplot(fig)
