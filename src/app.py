
import streamlit as st

# ✅ Set page config immediately after import
st.set_page_config(page_title="EngageTrack AI", layout="centered")

import pandas as pd
import datetime
import os

# ✅ DEBUG: Show working directory and files in data/ using Streamlit
cwd = os.getcwd()
st.text(f"🛠 Working directory: {cwd}")

try:
    files = os.listdir("data")
    st.text(f"📁 Files in /data/: {files}")
except Exception as e:
    st.error(f"❌ Could not list /data/: {e}")


from data_loader import load_user_data
from mock_api import generate_mock_nudge
from recommendation_engine import get_engagement_color, get_churn_color

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
import xgboost as xgb

# Load real user data
df = load_user_data()

# Train churn model on load
@st.cache_resource
def train_churn_model():
    churn_df = pd.read_csv("data/customer_churn_dataset-testing-master.csv").copy()
    churn_df = churn_df.drop(columns=["CustomerID"])

    label_cols = ['Gender', 'Subscription Type', 'Contract Length']
    le_dict = {}
    for col in label_cols:
        le = LabelEncoder()
        churn_df[col] = le.fit_transform(churn_df[col])
        le_dict[col] = le

    X = churn_df.drop(columns=["Churn"])
    y = churn_df["Churn"]

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    model = xgb.XGBClassifier(use_label_encoder=False, eval_metric='logloss')
    model.fit(X_scaled, y)

    return model, scaler, le_dict, X.columns.tolist()

churn_model, churn_scaler, churn_encoders, churn_features = train_churn_model()

tab1, tab2 = st.tabs(["🔍 User Insights", "📈 Analytics Dashboard"])

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
            usage_frequency=user_data["Usage Frequency"],
            support_calls=user_data["Support Calls"],
            payment_delay=user_data["Payment Delay"],
            contract_length=user_data["Contract Length"]
        )

    if "mock_nudge" not in st.session_state:
        st.session_state["mock_nudge"] = generate_mock_nudge(
            user_id=user_id,
            usage_frequency=user_data["Usage Frequency"],
            support_calls=user_data["Support Calls"],
            payment_delay=user_data["Payment Delay"],
            contract_length=user_data["Contract Length"]
        )

    st.info(st.session_state["mock_nudge"])

    st.markdown(f"**📅 Contract Type:** {user_data['Contract Length']}")
    st.markdown(f"**🔥 Usage Frequency:** <span style='color:{get_engagement_color(user_data['Usage Frequency'])}'>{user_data['Usage Frequency']}</span>", unsafe_allow_html=True)
    st.markdown(f"**📞 Support Calls:** {user_data['Support Calls']}")
    st.markdown(f"**⏳ Payment Delay:** {user_data['Payment Delay']} days")
    st.markdown(f"**💰 Total Spend:** ${user_data['Total Spend']}")
    st.markdown(f"**🕒 Last Interaction:** {user_data['Last Interaction']} days ago")

    st.divider()

    st.subheader("🔮 Real Churn Prediction (Model-Based)")

    input_row = user_data.to_frame().T.copy()

    for col in ['Gender', 'Subscription Type', 'Contract Length']:
        input_row[col] = churn_encoders[col].transform(input_row[col])

    X_input = input_row.drop(columns=["CustomerID", "Churn"])
    X_input_scaled = churn_scaler.transform(X_input)

    pred = churn_model.predict(X_input_scaled)[0]
    proba = churn_model.predict_proba(X_input_scaled)[0][1]

    st.markdown(f"**Model Prediction:** {'🟥 Churn' if pred == 1 else '🟩 Retained'}")
    st.markdown(f"**Churn Probability:** `{proba * 100:.2f}%`")
    st.markdown(f"**Risk Color:** <span style='color:{get_churn_color(proba)}'>{get_churn_color(proba).capitalize()}</span>", unsafe_allow_html=True)

    st.caption("Built with ❤️ by Tanesh • Real ML-powered product analytics platform")

# ---------------------------
# TAB 2: Dashboard
# ---------------------------
with tab2:
    st.subheader("📊 System-wide Metrics")

    st.markdown("**Contract Type Segmentation**")
    st.bar_chart(df["Contract Length"].value_counts())

    st.markdown("**Support Call Frequency**")
    st.bar_chart(df["Support Calls"].value_counts().sort_index())

    st.markdown("**Payment Delay Distribution**")
    st.bar_chart(df["Payment Delay"].value_counts().sort_index())

    st.markdown("**Usage Frequency Distribution**")
    st.bar_chart(df["Usage Frequency"].value_counts().sort_index())
