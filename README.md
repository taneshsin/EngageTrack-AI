# 📊 EngageTrack AI – Smart Productivity Insights

**EngageTrack AI** is a simulated SaaS product analytics platform that visualizes user lifecycle insights, churn risk, engagement levels, and delivers AI-powered nudges. It mimics how modern AI-enabled SaaS platforms use behavioral signals and personalization to drive engagement.

Built with **Streamlit + Docker + GitHub Actions + Azure AKS**, this project showcases **product strategy, DevOps maturity, and full-stack delivery**.

---

## 🌐 Live Demo

▶️ **Try it now:** [http://172.171.188.153/](http://172.171.188.153/)  
> No login required – select a user to view insights instantly

---

## 🚀 Features

- ✅ Simulated user personas (Writer, Analyst, Marketer, etc.)
- ✅ AI-generated feature nudges via mock GPT-style logic
- ✅ Churn risk detection and engagement scoring
- ✅ A/B variant assignment and experiment tracking
- ✅ Per-user report export as `.txt` file
- ✅ Usage logging and audit trail (`/tmp/usage.log`)
- ✅ Fully containerized and deployed on Azure AKS
- ✅ Bar chart dashboard: churn, engagement, variants
- ✅ Modularized `src/` architecture for scalability

---

## 📦 Tech Stack

| Layer         | Tech                                      |
|---------------|--------------------------------------------|
| UI / Frontend | Streamlit                                 |
| Backend       | Python, Pandas                            |
| AI Engine     | Simulated via `mock_api.py`               |
| DevOps        | Docker, GitHub Actions, Azure AKS         |
| Infra         | NGINX reverse proxy, LoadBalancer ingress |
| Data Source   | CSV-based simulated user behavior         |

---

## 🖼 Screenshots

(📸 To add: save UI screenshots and place them in `/screenshots/`)

```markdown
### 🔍 User Overview
![User Insights](screenshots/user_tab.png)

### 📊 Dashboard Visuals
![Dashboard](screenshots/dashboard_tab.png)

## 📂 Folder Structure
```
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
│ └── user_recommendations.csv
│
├── notebooks/ # Development notebooks
│ └── *.ipynb
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
User selects ID → Loads data
  ↳ Engagement + Churn Risk Calculated
  ↳ Mock AI generates feature nudge
  ↳ Lifecycle message shown
  ↳ Export report (TXT) enabled
  ↳ Dashboard visualizes trends
```
---

## 📊 Dashboard Insights

🔥 **Engagement Level Distribution** <br>
🚨 **Churn Risk Segmentation** <br>
📦 **Plan Type Breakdown** <br>
🧪 **A/B Variant Allocation**

---

## 🧪 A/B Testing Support

- Each user is randomly assigned Variant A or B
- View experiment results in the dashboard
- Demonstrates experimentation infrastructure simulation

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

## 💼 Built By

Tanesh Singhal  
MS Business Analytics @ University of Cincinnati  
📌 Product • DevOps • AI Strategy
🔗 LinkedIn • GitHub

---

## 📄 License

MIT License — Free to use, fork, and extend for educational or demo purposes.

