# 📦 Release Notes – EngageTrack AI

---

## 🚀 Version 1.0 – Initial Public Release  
📅 **Date:** May 2025  
🔧 **Maintainer:** [Tanesh Singhal](https://github.com/taneshsin)

---

### ✅ Features Implemented

| Category                 | Description |
|--------------------------|-------------|
| 🧠 AI Nudges (Simulated) | Rule-based nudges triggered by real usage patterns, tailored by contract, delay, and usage |
| 🔮 Churn Prediction (ML) | Real XGBoost model trained on IBM Telco Customer Churn dataset |
| 📊 Visual Dashboard       | Interactive charts on contract type, support calls, payment delay, engagement, and variants |
| 🧪 A/B Variant Assignment | Users randomly bucketed into Variant A or B (via preprocessing) |
| 👤 User Detail View       | Lifecycle info: usage, delay, plan, churn probability, nudge |
| 📥 Summary Export         | TXT download of per-user summary for analysis/reporting |
| 🧾 Activity Logging       | User view logs appended to `/tmp/usage.log` (container-safe) |
| 🧱 Containerization       | Docker with non-root user, `.dockerignore`, and security configs |
| 📂 Modular Source Layout  | `src/` directory with separation of concerns (`app.py`, `mock_api.py`, etc.) |
| 🌐 Streamlit UI           | Modern tabbed layout with dropdowns, visualizations, and explainability tab |
| 🧠 SHAP Global Explainability | Summary plot for global feature contributions from trained XGBoost model |

---

### 🔧 DevOps & Deployment

- CI/CD automated via **GitHub Actions**
- App containerized with **Docker** and deployed to **Azure Kubernetes Service (AKS)**
- **NGINX Ingress** with LoadBalancer and rate-limiting
- Logs safely redirected to `/tmp` for write-access compliance
- GitHub repo configured with:
  - `.dockerignore`, `.gitignore`, non-root Dockerfile
  - `engagetrack-deploy.yaml`, `engagetrack-ingress.yaml`, `docker-compose.yml`
  - Environment-safe variable management

---

### 🛣️ Planned for v1.1

| Feature                         | Status     | Notes                                |
|----------------------------------|------------|--------------------------------------|
| 🔐 Basic Authentication          | 🕐 Planned | Restrict access to dashboards        |
| 🔄 SQLite or CSV Persistence     | 🕐 Planned | Store feedback and nudge logs        |
| 🌐 OpenAI/GPT Nudging (Real API) | 🕐 Planned | Replace rule-based with real LLM     |
| 📈 Historical Usage Trends       | 🕐 Planned | Time-series tracking of usage/churn  |
| 🧠 Per-user SHAP Explanations    | 🕐 Planned | Drilldown-level explainability       |
| 💬 Feedback Capture              | 🕐 Planned | Collect real-time feedback from UI   |

---

📌 *EngageTrack AI v1.0 is fully deployed, functional, and aligned with MS-BANA capstone standards. Designed for DevOps, ML, and product management demonstrations.*

