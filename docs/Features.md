## 🔧 Core Features

### 1. 👤 Persona-Based Lifecycle Insights
- Simulated users with behavioural traits and engagement patterns  
- Contextual lifecycle data (e.g., subscription type, plan duration, churn history)

### 2. 🧠 AI-Generated Nudges (Powered by Together AI)
- Real-time LLM nudges driven by the **Together AI Mixtral-8x7B** model  
- Personalized suggestions based on each user’s tenure, support calls, billing delays, contract, and A/B variant

### 3. 📊 Engagement & Churn Analytics
- System dashboard visualizing:  
  - 🔥 Usage frequency breakdown  
  - ⏳ Payment delay distribution  
  - 📞 Support call volume  
  - 📅 Contract type segmentation  
  - 🧪 A/B variant split  

### 4. 🔮 Churn Prediction
- **XGBoost** classifier trained on the IBM Telco Customer Churn dataset  
- Outputs calibrated churn probabilities and binary predictions  
- Integrated SHAP for global feature importance

### 5. 🧩 Per-User Explainability
- **Waterfall SHAP plots** showing top feature contributions for each selected user  
- Accessible under **“Why this prediction?”** in the User Insights tab  
- Helps interpret exactly which factors increase or decrease churn risk  

### 6. 🧪 A/B Testing Simulation
- Users pre-assigned to Variant A or Variant B via the enriched dataset  
- Churn rate and engagement metrics compared side-by-side in the dashboard  
- Foundation for experimentation and feature rollout strategy  

### 7. 📥 Downloadable User Summary
- One-click export of per-user profile as a **TXT report**  
- Includes subscription details, behaviour metrics, churn score, and AI-generated nudge  

### 8. 🔐 Secure Logging & Audit
- All user interactions logged to `logs/usage.log` (tracked via `.gitkeep`, log file ignored in Git)  
- Non-root container user ensures safe write permissions in Docker/AKS  
- Supports audit and troubleshooting of engagement nudges  

---

## 🛠 Technical Stack Overview

| Layer             | Tech Used                                                                       |
|-------------------|---------------------------------------------------------------------------------|
| Frontend UI       | Streamlit                                                                       |
| ML Model          | XGBoost (Churn Classification)                                                  |
| LLM API           | Together AI Mixtral-8x7B via REST                                               |
| Backend Logic     | Python modular files (`app.py`, `data_loader.py`, `nudge_api.py`, etc.)         |
| Containerization  | Docker, Docker Compose                                                          |
| Orchestration     | Azure Kubernetes Service (AKS)                                                  |
| CI/CD Pipeline    | GitHub Actions → Azure Container Registry → AKS                                 |
| Networking        | NGINX Ingress + Azure Load Balancer                                             |

---

🎯 *EngageTrack AI now delivers real AI-powered nudges, end-to-end explainability, and robust DevOps controls—ideal for showcasing product strategy, ML, and cloud native deployment.*  
