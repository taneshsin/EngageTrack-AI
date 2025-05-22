# 🆘 Help Center – EngageTrack AI

Welcome to **EngageTrack AI** – a simulated SaaS analytics platform for demonstrating AI-powered insights, churn risk prediction, per-user explainability, and feature nudging.

---

## 👤 1. Select a User

Use the **dropdown menu** to choose a simulated user. Their full profile — including subscription type, usage, support calls, A/B variant, and churn risk — will be displayed.

---

## 💡 2. Generate AI-Driven Recommendations

- Click 🔁 **Generate New Nudge** to simulate a fresh engagement tip  
- Nudges are based on behavioral indicators such as low usage, frequent support calls, billing delays, and contract type  
- You can see tailored suggestions that help reduce churn and improve retention  

---

## 📥 3. Download User Summary

Click the **Download Summary** button to export user insights (plan type, A/B variant, churn risk, and AI nudge) as a TXT file — useful for mock reporting or reviews.

---

## 🧩 4. Per-User Explainability

Under **User Insights**, open the **“Why this prediction? (Per-user SHAP)”** expander to see a waterfall plot that shows the top 10 features driving the churn prediction for the selected user. Each bar is labeled with its feature name and impact.

---

## 📊 5. Explore the System Dashboard

Navigate to the **Analytics Dashboard** tab to view:

- 🔥 Usage Frequency Distribution  
- 📞 Support Call Frequency  
- ⏳ Payment Delay Distribution  
- 📅 Contract Type Breakdown  
- 🧪 A/B Variant Distribution  
- ❌ Churn Rate by Variant  

These charts reflect aggregated metrics across the simulated user base.

---

## 🧠 6. Understand Churn Prediction

On the **Explainability** tab:

- View SHAP summary plots explaining how each feature impacts churn risk globally  
- Compare global feature impact against individual user explanations  

---

## 👩‍💻 For Developers

| Task                     | File/Module                        |
|--------------------------|------------------------------------|
| Modify user data         | `data/churn.csv`                   |
| Tweak nudge responses    | `mock_api.py`                      |
| Update ML preprocessing  | `data_loader.py`                   |
| Update ML model behavior | `app.py`                           |
| Extend analytics         | `app.py` (tab logic & visualizations) |

All source code lives in your project root. Streamlit runs the app from `app.py`, and the data loader logic is in `data_loader.py`.

---

## 📬 Support & Contributions

This project is for demo and portfolio use only. For improvements or bug reports, feel free to fork the repo or open an issue.

Thanks for exploring **EngageTrack AI**!  
