# 📊 EngageTrack AI – Smart Productivity Insights

**EngageTrack AI** is a simulated SaaS product analytics platform that visualizes user lifecycle insights, churn risk, engagement levels, and delivers AI-powered nudges. It mimics how modern AI-enabled SaaS platforms use behavioral signals and personalization to drive engagement.

Built with **Streamlit + XGBoost + Docker + GitHub Actions + Azure AKS**, this project showcases **product strategy, DevOps maturity, and full-stack delivery**.

---

## 🌐 Live Demo

▶️ **Try it now:** [http://172.171.188.153/](http://172.171.188.153/)  
> No login required – select a user to view insights instantly

---

## 🚀 Features


- ✅ Real churn prediction using XGBoost classifier
- ✅ AI-generated feature nudges via mock logic
- ✅ Per-user churn probability score with insights
- ✅ A/B variant assignment (`churn.csv`) for simulation
- ✅ Model input preview for every user
- ✅ Summary export as `.txt`
- ✅ Logging audit trail (`/tmp/usage.log`)
- ✅ Dashboard charts: engagement, contract, churn, variants
- ✅ Modular Streamlit UI with sidebar branding
- ✅ Deployed via Docker + GitHub Actions → Azure AKS
- ✅ Notebook with SHAP-based explainability
---

## 📦 Tech Stack

| Layer         | Tech                                      |
|---------------|--------------------------------------------|
| UI / Frontend | Streamlit                                 |
| Backend       | Python, Pandas                            |
| ML Model      | XGBoost (churn classifier)                |
| Preprocessing | LabelEncoder, StandardScaler              |
| DevOps        | Docker, GitHub Actions, Azure AKS         |
| Infra         | NGINX reverse proxy, LoadBalancer ingress |
| Data Source   | `churn.csv` (simulated SaaS behavior)     |

---

## 🖼 Screenshots

### 🔍 User Overview
![User Insights](screenshots/user_tab.png)

### 📊 Dashboard Visuals
![Dashboard](screenshots/dashboard_tab.png)

## 📂 Folder Structure

```bash
EngageTrack-AI/
├── src/ # App logic  
│ ├── app.py  
│ ├── data_loader.py  
│ ├── mock_api.py  
│ ├── recommendation_engine.py  
│  
├── logs/ # Logs are redirected to /tmp in cloud  
│  
├── data/ # Input data  
│ └── churn.csv  
│  
├── notebooks/
│ └── churn_model.ipynb
│  
├── docs/ # Documentation  
│ └── PRD.md, Features.md, etc.  
│  
├── Dockerfile  
├── requirements.txt  
├── assign_variants.py  
├── Security.md  
├── docker-compose.yml  
├── engagetrack-deploy.yaml  
├── engagetrack-ingress.yaml  
├── engagetrack-service.yaml  
├── nginx.conf  
├── .gitignore
├── .dockerignore
└── README.md  
```
---

## ▶️ How to Run

### 🔧 Option 1: Local (without Docker)
```bash
pip install -r requirements.txt
streamlit run src/app.py
```

### 🐳 Option 2: Dockerized
```bash
docker build -t engagetrack .
docker run -p 8501:8501 engagetrack
```
  
🌐 Visit the app: [http://localhost:8501](http://localhost:8501)

---

## 🧠 System Logic
```bash
User selects ID → Loads behavior & metadata
   ↳ Churn model (XGBoost) predicts risk
   ↳ AI nudge generated via mock_api
   ↳ Metadata + prediction shown in UI
   ↳ Optional export as summary .txt
   ↳ Dashboard shows aggregated insights
```
✅ If variant is missing in dataset, manually add it using assign_variants.py  
✅ Payment Delay is log-transformed for ML stability
---

## 📊 Dashboard Insights

🔥 **Usage Frequency Distribution** <br>  
📅 **Contract Length Segmentation** <br>  
📞 **Support Call Frequency** <br>  
⏳ **Payment Delay Breakdown** <br>  
🧪 **A/B Variant Split** (if column present)  
---

## 🧪 A/B Testing Support

- Users are randomly tagged with A/B via assign_variants.py
- Variant shows in user insights and dashboard
- Demonstrates simple experimentation workflow

---

## 📄 Export & Logging

✅ Per-user summary export as .txt  
✅ Logs user activity to /tmp/usage.log (container-safe)

---

## 🔐 Security Highlights

- Runs under a non-root Docker user
- Redirected logs to /tmp/ (write-safe in Docker)
- No secrets or credentials pushed
- .gitignore covers logs, system files, and config
- NGINX + IP controls + rate limiting available  

See Security.md for full details.

---

## 🧪 Model Explainability

A Jupyter notebook with:  

- Model training
- ROC + confusion matrix
- SHAP explainability plot  

File: notebooks/churn_model.ipynb

---

## 💼 Built By

Tanesh Singhal  
MS Business Analytics @ University of Cincinnati  
📌 Product • DevOps • AI Strategy

---

## 📄 License

MIT License — Free to use, fork, and extend for educational or demo purposes.

