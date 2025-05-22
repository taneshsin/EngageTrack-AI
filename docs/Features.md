# 🚀 EngageTrack AI – Feature Overview

**EngageTrack AI** is a simulated AI-powered productivity and lifecycle analytics platform built to showcase product strategy, DevOps maturity, and applied ML skills.

It demonstrates how modern SaaS products personalize engagement using nudges, churn prediction, and A/B experimentation — all fully deployed using containerized infrastructure and CI/CD workflows.

---

## 🔧 Core Features

### 1. 👤 Persona-Based Lifecycle Insights
- Simulated users with behavioral traits and engagement patterns  
- Contextual lifecycle data (e.g., subscription type, plan duration, churn history)

### 2. 🧠 AI-Generated Nudges (Simulated)
- Multi-nudge system based on rule logic in `mock_api.py`  
- Context-aware suggestions to reduce churn or boost activity  
- Nudges tagged with categories (e.g., billing, engagement, support)

### 3. 📊 Engagement & Churn Analytics
- Dashboard shows:  
  - 🔥 Usage frequency breakdown  
  - ⏳ Payment delays  
  - 📞 Support calls  
  - 📅 Contract segmentation  
  - 🧪 A/B variant distribution

### 4. 🔮 Churn Prediction
- Real ML model (XGBoost) trained on Telco Churn dataset  
- Probabilistic predictions with calibrated outputs  
- SHAP-based global explainability integrated in UI

### 5. 🧩 Per-User Explainability (New)
- Waterfall plots showing top feature contributions for each selected user  
- Labels each bar with the actual feature name from the model’s feature set  
- Accessible via the “Why this prediction?” expander in the User Insights tab

### 6. 🧪 A/B Testing Simulation
- Dataset-driven variant assignment per user (A or B)  
- Dashboard chart to visualize split  
- Basis for feature experimentation workflows

### 7. 📥 Downloadable User Summary
- TXT export includes:  
  - Plan details, behavior metrics  
  - Predicted churn score  
  - Personalized nudges

### 8. 🔁 Mock API + Secure Logging
- Mock API generates nudges dynamically per user  
- User interaction logs written to `logs/usage.log` (directory tracked via `.gitkeep`, log file ignored)  
- Supports behavior audit and engagement tracking

---

## 🛠 Technical Stack Overview

| Layer             | Tech Used                                                                       |
|-------------------|---------------------------------------------------------------------------------|
| Frontend UI       | Streamlit                                                                       |
| ML Model          | XGBoost (Churn Classification)                                                  |
| Backend Logic     | Python modular files (`app.py`, `data_loader.py`, etc.)                         |
| Containerization  | Docker, Docker Compose                                                          |
| Orchestration     | Azure Kubernetes Service (AKS)                                                  |
| CI/CD Pipeline    | GitHub Actions → Azure Container Registry → AKS                                 |
| Networking        | NGINX Ingress + Azure Load Balancer                                             |

---

🎯 *EngageTrack AI simulates the full product lifecycle of a modern SaaS app — from personalization to analytics and per-user explainability — making it an ideal demo for product management, DevOps, and ML-focused roles.*  
