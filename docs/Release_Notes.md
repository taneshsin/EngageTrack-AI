# 📦 Release Notes – EngageTrack AI

---

## 🚀 Version 1.0 – Initial Public Release  
📅 **Date:** May 2025  
🔧 **Maintainer:** [Tanesh Singhal](https://github.com/taneshsin)

### ✅ Features Implemented in v1.0

| Category                      | Description                                                                          |
|-------------------------------|--------------------------------------------------------------------------------------|
| 🧠 AI Nudges (Simulated)      | Rule-based nudges triggered by usage patterns, tailored by contract, delay, and variant |
| 🔮 Churn Prediction (ML)      | XGBoost model trained on IBM Telco Customer Churn dataset                            |
| 📊 Visual Dashboard           | Charts for contract, tenure, monthly/total charges, support calls, and A/B split     |
| 🧪 A/B Variant Assignment     | Users assigned via the `variant` column (A or B)                                      |
| 👤 User Detail View           | Per-user profile: plan, usage, churn probability, and nudge                          |
| 📥 Summary Export             | TXT download of per-user summary for reporting                                       |
| 🧾 Activity Logging           | Logs appended to `logs/usage.log` (tracked via `.gitkeep`, log file ignored)         |
| 🧱 Containerization           | Docker image with non-root user, `.dockerignore`, security best practices            |
| 📂 Modular Source Layout      | `src/` folder separating `app.py`, `data_loader.py`, `mock_api.py`, etc.             |
| 🌐 Streamlit UI               | Tabbed interface with sidebar, user insights, dashboard, and explainability tab       |
| 🧠 SHAP Global Explainability | SHAP summary plot showing global feature impact                                     |

---

## 🚀 Version 1.1 – AI Nudges & Per-User Explainability  
📅 **Date:** May 22, 2025  
🔧 **Maintainer:** [Tanesh Singhal](https://github.com/taneshsin)

### ✅ New in v1.1

| Category                         | Description                                                                                      |
|----------------------------------|--------------------------------------------------------------------------------------------------|
| 🧠 LLM-Powered Nudges             | On-demand real nudges via Together AI Mixtral-8x7B model                                        |
| 🧩 Per-User SHAP Explainability   | Waterfall SHAP plots in User Insights tab, showing top feature contributions for each user      |

---

### 🔧 DevOps & Deployment (unchanged)

- CI/CD via **GitHub Actions**  
- Containerized with **Docker**, deployed to **AKS**  
- **NGINX Ingress** with rate limiting  
- Secure logging to `logs/usage.log`  
- Repo contains `.gitignore`, `.dockerignore`, Helm/K8s manifests  

---

## 🛣️ Planned for v1.2

| Feature                         | Status     | Notes                                     |
|---------------------------------|------------|-------------------------------------------|
| 🔐 Basic Authentication          | 🕐 Planned | Add OAuth admin login                     |
| 🔄 Persistence (SQLite/CSV)      | 🕐 Planned | Store nudge feedback & logs persistently   |
| 📊 Cohort & Time-Series Analytics| 🕐 Planned | Trend analysis over time                  |
| 💬 Feedback Loop                 | 🕐 Planned | Capture user responses to improve nudges  |

---

📌 *EngageTrack AI v1.1 enhances personalization with real LLM nudges and per-user explainability, building on the robust analytics and DevOps foundation of v1.0.*  
