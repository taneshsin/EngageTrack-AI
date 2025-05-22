# 🚀 EngageTrack AI – Feature Overview

**EngageTrack AI** is a simulated AI-powered productivity and lifecycle analytics platform built to showcase product strategy, DevOps maturity, and applied ML skills.

It demonstrates how modern SaaS products personalize engagement using nudges, churn prediction, and A/B experimentation — all fully deployed using containerized infrastructure and CI/CD workflows.

---

## 🔧 Core Features

### 1. 👤 Persona-Based Lifecycle Insights
- Simulated users with behavioral traits and engagement patterns
- Contextual lifecycle data (e.g., subscription type, plan duration, churn history)

### 2. 🧠 AI-Generated Nudges (Simulated)
- Multi-nudge system based on rules and mock personalization
- Context-aware suggestions to reduce churn or boost activity
- Nudges tagged with categories (e.g., billing, engagement, support)

### 3. 📊 Engagement & Churn Analytics
- Dashboard shows:
  - 🔥 Usage frequency breakdown
  - ⏳ Payment delays
  - 📞 Support calls
  - 📅 Contract segmentation
  - 🧪 A/B variant split

### 4. 🔮 Churn Prediction
- Real ML model (XGBoost) trained on Telco Churn dataset
- Probabilistic predictions with calibrated output
- SHAP-based global explainability included in UI

### 5. 🧪 A/B Testing Simulation
- Auto-generated variant assignment per user
- Dashboard chart to visualize split
- Basis for feature experimentation workflows

### 6. 📥 Downloadable User Summary
- TXT export includes:
  - Plan details, behavior metrics
  - Predicted churn score
  - Personalized nudges

### 7. 🔁 Mock API + Secure Logging
- Mock API generates nudges dynamically per user
- User interaction logs stored in `/tmp/usage.log` (Docker-safe)
- Supports behavior audit and engagement tracking

---

## 🛠 Technical Stack Overview

| Layer             | Tech Used                          |
|------------------|------------------------------------|
| Frontend UI       | Streamlit                          |
| ML Model          | XGBoost (Churn Classification)     |
| Backend Logic     | Python (modular `src/` structure)  |
| Containerization  | Docker, Docker Compose             |
| Orchestration     | Azure Kubernetes Service (AKS)     |
| CI/CD Pipeline    | GitHub Actions → ACR → AKS         |
| Networking        | NGINX Ingress + Azure Load Balancer|

---

🎯 *EngageTrack AI simulates the full product lifecycle of a modern SaaS app — from personalization to analytics — making it an ideal demo for product management, DevOps, and ML-focused roles.*
