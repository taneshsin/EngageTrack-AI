# 🚀 EngageTrack AI – Feature Overview

**EngageTrack AI** is a simulated AI-powered productivity and lifecycle analytics platform built to showcase product strategy, DevOps maturity, and applied ML skills.

It demonstrates how modern SaaS products personalize engagement using nudges, churn prediction, and A/B experimentation — all fully deployed using containerized infrastructure and CI/CD workflows.

---

## 🔧 Core Features

### 1. 👤 Persona-Based Lifecycle Insights
- Simulated users with distinct personas: *Student*, *Marketer*, *Analyst*, *Writer*
- Each user has custom lifecycle context (plan type, engagement level, churn risk)

### 2. 🧠 AI-Generated Nudges (Simulated)
- Rule-based nudging system mimicking GPT-style behavior
- Personalized nudges triggered on login or refresh
- Simulates feature discovery, habit formation, and user retention logic

### 3. 📊 Engagement & Churn Analytics
- Interactive dashboard showing:
  - 🔥 Engagement level distribution
  - 🚨 Churn risk levels
  - 💡 Plan segmentation (Free, Premium, etc.)
  - 🧪 A/B variant population split

### 4. 🧪 A/B Testing Simulation
- Randomized Variant A/B assignment per user
- Allows testing of differentiated UX or nudging strategies
- Variant split visualized on dashboard

### 5. 📥 Downloadable User Summary
- One-click export of the user’s:
  - Persona and plan
  - Churn risk and engagement score
  - Nudge and feature recommendations

### 6. 🔁 Mock API + Secure Logging
- `mock_api.py` simulates real-time nudge generation logic
- User activity securely logged to `/tmp/usage.log`
- Supports lifecycle observability without real data exposure

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

