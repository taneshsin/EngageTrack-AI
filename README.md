# 📊 EngageTrack AI – Smart Productivity Insights

**EngageTrack AI** is a simulated SaaS product analytics platform that visualizes user lifecycle insights, churn risk, engagement levels, and delivers AI-powered nudges and recommendations. Built using Streamlit, this project demonstrates product strategy, lifecycle personalization, and DevOps readiness.

---

## 🚀 Features

- ✅ Simulated user personas and engagement tracking
- ✅ AI-generated feature nudges via mock API
- ✅ Churn risk scoring and lifecycle analysis
- ✅ A/B test variant assignment and analysis
- ✅ User summary export (TXT download)
- ✅ Usage logging and audit trail
- ✅ Modular code structure for scaling
- ✅ Dashboard with bar charts for key metrics
- ✅ Dockerized environment for deployment
---

## 📦 Tech Stack

- **Frontend/UI**: Streamlit
- **Backend**: Python, Pandas
- **Mock AI Logic**: `mock_api.py`
- **DevOps**: Docker, Git, Modular `src/` layout
- **Data**: CSV-based user simulation
- **Dashboarding**: Streamlit Charts
---

## 📂 Folder Structure
```
EngageTrack-AI/
├── src/ # App logic
│ ├── app.py
│ ├── data_loader.py
│ ├── mock_api.py
│ ├── recommendation_engine.py
│
├── data/ # Input data
│ └── user_recommendations.csv
│
├── logs/ # Log output
│ └── usage.log
│
├── notebooks/ # Development notebooks
│ └── *.ipynb
│
├── docs/ # Documentation
│ └── PRD.md, changelog, etc.
│
├── Dockerfile
├── requirements.txt
├── assign_variants.py
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
Visit: http://localhost:8501
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
🔥 Engagement Level Distribution
🚨 Churn Risk Segmentation
📦 Plan Type Breakdown
🧪 A/B Variant Allocation
---

## 🧪 A/B Testing Support
Each user is randomly assigned a Variant A or B.
This simulates feature experiments and is visualized in the dashboard.
---

## 📄 Export & Logs
✅ User summary can be downloaded as a TXT file

✅ All user interactions are logged to /logs/usage.log
---

## 💼 Built By
Tanesh Singhal
MS Business Analytics @ University of Cincinnati
AI in Business · DevOps Enthusiast · Product Strategy
---

## 📄 License
MIT License – Free to use, fork, and expand.

