import streamlit as st
import pandas as pd
import datetime

from data_loader import load_user_data
from mock_api import generate_mock_nudge
from recommendation_engine import get_engagement_color, get_churn_color

# Load processed user data
df = load_user_data()

st.set_page_config(page_title="EngageTrack AI", layout="centered")
tab1, tab2 = st.tabs(["🔍 User Insights", "📈 Analytics Dashboard"])

# ---------------------------
# TAB 1: User Insights
# ---------------------------
with tab1:
    user_id = st.selectbox("Choose a user:", df["user_id"].unique())
    user_data = df[df["user_id"] == user_id].iloc[0]

    # Log user interaction
    with open("logs/usage.log", "a") as log_file:
        log_file.write(f"[{datetime.datetime.now()}] Viewed: {user_id}\n")

    # 🔄 AI Nudge (Session-based so it updates only on button click)
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

    # 👤 User Info
    st.markdown(f"**👤 Persona:** {user_data['persona']}")
    st.markdown(f"**🗓 Plan:** {user_data['plan_type']}")
    st.markdown(f"**🔥 Engagement Level:** <span style='color:{get_engagement_color(user_data['engagement_level'])}'>{user_data['engagement_level']}</span>", unsafe_allow_html=True)
    st.markdown(f"**⏱ Days Since Last Active:** {int(user_data['days_since_active'])}")
    st.markdown(f"**🚨 Churn Risk:** <span style='color:{get_churn_color(user_data['churn_risk'])}'>{user_data['churn_risk']}</span>", unsafe_allow_html=True)
    st.markdown(f"**🧪 A/B Test Variant:** `{user_data['variant']}`")

    st.divider()

    # 🌟 Recommendation
    st.subheader("🧠 AI Feature Recommendation")
    st.success(f"Try this next: **{user_data['recommended_feature']}**")

    # 🔔 Lifecycle Nudge
    st.subheader("💬 Lifecycle Nudge")
    nudge = user_data.get("nudge_action", "None")

    if pd.isna(nudge) or nudge == "None":
        st.info("No nudges needed — user is healthy!")
    else:
        st.warning(nudge)

    # 📥 Download Summary
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
    st.caption("Built with ❤️ by Tanesh • Simulated product analytics platform")

# ---------------------------
# TAB 2: Dashboard
# ---------------------------
with tab2:
    st.subheader("📊 System-wide Metrics")

    # Engagement Breakdown
    st.markdown("**Engagement Level Breakdown**")
    eng_dist = df['engagement_level'].value_counts()
    st.bar_chart(eng_dist)

    # Churn Risk Breakdown
    st.markdown("**Churn Risk Distribution**")
    churn_dist = df['churn_risk'].value_counts()
    st.bar_chart(churn_dist)

    # Plan Type
    st.markdown("**Plan Type Segmentation**")
    plan_dist = df['plan_type'].value_counts()
    st.bar_chart(plan_dist)

    # Variant Distribution
    st.markdown("**🧪 A/B Test Split**")
    variant_dist = df["variant"].value_counts()
    st.bar_chart(variant_dist)

