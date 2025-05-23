# 🆘 Help Center – EngageTrack AI

Welcome to **EngageTrack AI** – a simulated SaaS analytics platform for demonstrating AI-powered insights, churn risk prediction, per-user explainability, and real LLM nudges.

---

## 👤 1. Select a User

Use the **dropdown menu** to choose a simulated user. Their full profile — including subscription type, usage, support calls, A/B variant, and churn risk — will be displayed.

---

## 💡 2. Generate AI-Driven Recommendations

- Click **Generate New Nudge** to request a fresh engagement tip  
- Nudges are powered by Together AI’s Mixtral-8x7B model and personalized on tenure, support calls, billing delays, contract, and variant  
- If generation fails, you’ll see an error message explaining the issue  

---

## 📥 3. Download User Summary

Click the **Download Summary** button to export user insights (plan details, A/B variant, churn probability, risk level, and AI nudge) as a **TXT** file — handy for mock reporting or reviews.

---

## 🧩 4. Per-User Explainability

Under **User Insights**, expand **“Why this prediction? (Per-user SHAP)”** to view a waterfall plot showing the top 10 features driving churn risk for the selected user. Each bar is labeled with its feature name and impact.

---

## 📊 5. Explore the System Dashboard

In the **Analytics Dashboard** tab, you’ll find:

- 🔥 Usage Frequency Distribution  
- 📞 Support Call Volume  
- ⏳ Payment Delay Distribution  
- 📅 Contract Type Breakdown  
- 🧪 A/B Variant Split  
- ❌ Churn Rate by Variant  

These charts aggregate metrics across all users.

---

## 🧠 6. Understand Global Explainability

On the **Explainability** tab:

- See a SHAP summary plot showing global feature importance  
- Compare global impacts with individual user explanations  

---

## 👩‍💻 For Developers

| Task                         | File/Module              |
|------------------------------|--------------------------|
| Modify dataset               | `data/churn.csv`         |
| Generate nudges              | `src/nudge_api.py`       |
| Preprocess data              | `src/data_loader.py`     |
| Train/update churn model     | `src/app.py` (cache fn)  |
| Update visualizations/UI     | `src/app.py` (tab logic) |

Streamlit entrypoint: `src/app.py`. All LLM calls live in `src/nudge_api.py`.

---

## 📬 Support & Contributions

This project is for demonstration and portfolio purposes. To suggest improvements or report issues, please fork the repo or open an issue.

Thank you for using **EngageTrack AI**!  
