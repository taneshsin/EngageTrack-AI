# 🆘 Help Center – EngageTrack AI

Welcome to **EngageTrack AI** – a simulated SaaS analytics platform for demonstrating AI-powered insights, churn risk prediction, and feature nudging.

---

## 👤 1. Select a User

Use the **dropdown menu** to choose a simulated user. Their full profile — including subscription type, usage, support calls, and churn risk — will be displayed.

---

## 💡 2. Generate AI-Driven Recommendations

- Click 🔁 **Generate New Nudge** to simulate a fresh engagement tip
- Nudges are based on behavioral indicators such as low usage, frequent support calls, billing delays, and contract type
- You can see tailored suggestions that help reduce churn and improve retention

---

## 📥 3. Download User Summary

Click the **Download Summary** button to export user insights (plan type, delay, churn risk, and AI nudge) as a TXT file — useful for mock reporting or reviews.

---

## 📊 4. Explore the System Dashboard

Navigate to the **Analytics Dashboard tab** to view:

- 🔥 Usage Frequency Distribution
- 📞 Support Call Frequency
- ⏳ Payment Delay Distribution
- 📅 Contract Type Breakdown
- 🧪 A/B Variant Allocation (if available)

These charts reflect aggregated metrics across the simulated user base.

---

## 🧠 5. Understand Churn Prediction

On the **Explainability** tab:
- View SHAP summary plots explaining how each feature impacts churn risk
- Understand which features like usage, delay, or support calls influence predictions most

---

## 👩‍💻 For Developers

| Task                     | File/Module                |
|--------------------------|----------------------------|
| Modify user data         | `data/churn.csv`           |
| Tweak nudge responses    | `src/mock_api.py`          |
| Update ML model behavior | `src/app.py`               |
| Extend analytics         | `src/app.py` (tab logic)   |

All source code is modular under the `src/` directory. Streamlit runs the app from `src/app.py`.

---

## 📬 Support & Contributions

This project is for demo and portfolio use only. For improvements, feel free to fork the repo or open an issue.

Thanks for exploring **EngageTrack AI**!
