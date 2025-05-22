# 📊 EngageTrack AI – Smart Productivity Insights

**EngageTrack AI** is a simulated SaaS analytics platform that visualizes user lifecycle insights, churn risk, engagement levels, and delivers AI-powered nudges. It mimics how modern AI-enabled SaaS products use behavioral signals and personalization to drive engagement.

Built with **Streamlit + XGBoost + Docker + GitHub Actions + Azure AKS**, this project showcases **product strategy, DevOps maturity, and full-stack delivery**.

---

## 🌐 Live Demo

▶️ **Try it now:** [http://172.171.188.153/](http://172.171.188.153/)  
> No login required – select a user to view insights instantly

---

## 🚀 Features

- ✅ Real churn prediction using XGBoost (Telco dataset)  
- ✅ AI-generated nudges via rule-based mock API  
- ✅ Per-user churn probability with risk level  
- ✅ A/B variant assignment stored in `data/churn.csv`  
- ✅ SHAP global explainability visualization  
- ✅ **Per-user SHAP waterfall plots** in the “Why this prediction?” expander  
- ✅ One-click user summary export (TXT)  
- ✅ Logs lifecycle activity to `logs/usage.log`  
- ✅ Dashboard with contract, delay, engagement & variant charts  
- ✅ Clean Streamlit UI with tabs and sidebar branding  
- ✅ Fully Dockerized + CI/CD to AKS  

---

## 📦 Tech Stack

| Layer         | Tech Used                                   |
|---------------|----------------------------------------------|
| UI / Frontend | Streamlit                                   |
| ML Model      | XGBoost (binary churn classifier)           |
| Preprocessing | Pandas, LabelEncoder, StandardScaler        |
| Backend       | Modular Python (`app.py`, `data_loader.py`) |
| DevOps        | Docker, GitHub Actions, Azure AKS           |
| Infra         | NGINX Ingress + AKS Load Balancer            |
| Dataset       | IBM Telco Customer Churn (+ `variant` flag) |

---

## 🖼 Screenshots

### 🔍 User Overview
![User Insights](screenshots/user_tab.png)

### 📊 Dashboard Visuals
![Dashboard](screenshots/dashboard_tab.png)

### 📊 SHAP Plot
![SHAP](screenshots/shap.png)


## 📂 Folder Structure

```bash
EngageTrack-AI/
├── data/ # Input data  
│ └── churn.csv       # Updated Telco dataset with variant column
├── logs/
│   └── .gitkeep             # Keeps logs/ in Git; actual usage.log is ignored
├── notebooks/
│   └── churn_model.ipynb    # Training & explainability notebook
├── src/ # Streamlit App & Modules
│ ├── app.py  
│ ├── data_loader.py  
│ ├── mock_api.py  
│ └── recommendation_engine.py
├── docs/
│   ├── PRD.md
│   ├── Features.md
│   ├── Help_Center.md
│   ├── Security.md
│   └── Release_Notes.md
├── Dockerfile  
├── requirements.txt 
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
docker build -t engagetrack-ai .
docker run -p 8501:8501 engagetrack-ai
# then browse http://localhost:8501
```
---

## 🧠 System Logic
```bash
Select user → load user data (including A/B variant)
  ↳ Preprocess (label-encode, log-transform)
  ↳ Predict churn (XGBoost + scaler + encoders)
  ↳ Generate nudge (rule-based)
  ↳ Display churn % & risk level
  ↳ Show per-user SHAP waterfall to explain that prediction
  ↳ Export summary & log to logs/usage.log
```
---

## 📊 Dashboard Insights

🔥 **Usage Frequency Distribution**  
🧮 **Contract Type Distribution**  
📞 **Support Call Frequency**  
⏳ **Payment Delay Breakdown**  
🧪 **A/B Variant Assignment**  
❌ **Churn Rate by Variant**  

---

## 🧪 A/B Testing Support

- Users are assigned A or B via the variant column in data/churn.csv  
- Variants appear in both the User Insights view and the Dashboard  
- Demonstrates a simple experimentation workflow

---

## 📄 Export & Logging

✅ Per-user summary export as .txt  
✅ Logs user activity to logs/usage.log (directory tracked via .gitkeep)



---

## 🧪 Model Explainability

A Jupyter notebook with:  

- ✅ Churn model training (XGBoost)
- ✅ ROC curve and confusion matrix
- ✅ SHAP global explainability plot

File: notebooks/churn_model.ipynb

---

## 📄 Docs & Support Files

- PRD.md – Product Requirements Document  
- Features.md – Detailed feature overview  
- Help_Center.md – UI usage instructions  
- Security.md – Security best practices  
- Release_Notes.md – Version history & releases  

---

## 🔐 Security Highlights

- Runs as a non-root Docker user
- Logs written to logs/usage.log (directory persisted via .gitkeep, log file ignored)
- No secrets or credentials in repo
- .gitignore and .dockerignore protect sensitive files
- GINX ingress supports rate limiting and TLS

See docs/Security.md for full details.

---

## 💼 Built By

Tanesh Singhal  
MS Business Analytics @ University of Cincinnati  
📌 Product • DevOps • AI Strategy

---

## 📄 License

MIT License — Free to use, fork, and extend for educational or demo purposes.

