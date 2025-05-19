# 🚀 EngageTrack AI – Feature Overview

EngageTrack AI is a simulated AI-powered productivity and engagement insight platform built for showcasing product thinking, DevOps workflows, and analytics skills.

This project mimics how modern SaaS products personalize user journeys using AI, lifecycle nudges, and A/B experimentation.

---

## 🔧 Core Features

### 1. 👤 Persona-Based Insights
- Simulated user personas (e.g., Student, Marketer, Writer, Analyst)
- Personalized plans and lifecycle states

### 2. 🧠 AI-Generated Nudges (Mocked)
- Simulates GPT-style nudges based on persona and engagement level
- Generated on login and refreshed on button click
- Demonstrates personalization + lifecycle marketing logic

### 3. 📊 Engagement & Churn Dashboard
- System-wide breakdown of:
  - Engagement levels (bar chart)
  - Churn risk distribution
  - Plan segmentation
  - A/B variant split

### 4. 🧪 A/B Test Simulation
- Users are randomly assigned to Variant A or B
- Visualizes distribution and allows for experimentation logic

### 5. 📥 Downloadable User Summary
- Export per-user engagement insights and AI recommendations

### 6. 🔁 Mock API & Logging
- Simulated mock API generation (`mock_api.py`)
- User interaction logs stored securely in `/tmp/usage.log`

---

## 🛠 Technical Highlights

| Stack              | Tool/Tech                         |
|-------------------|-----------------------------------|
| Frontend          | Streamlit                         |
| Backend Logic     | Python                            |
| Containerization  | Docker + Docker Compose           |
| Orchestration     | Azure Kubernetes Service (AKS)    |
| CI/CD             | GitHub Actions → ACR → AKS        |
| Hosting           | Azure Load Balancer + Ingress     |

---

🎯 *This feature set simulates a complete SaaS lifecycle with full-stack delivery, making it perfect for PM, DevOps, and strategy portfolios.*
