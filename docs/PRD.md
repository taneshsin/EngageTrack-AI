# 📘 Product Requirements Document – EngageTrack AI

---

## 1. 🧭 Overview

**EngageTrack AI** is a full-stack AI-powered SaaS analytics simulation platform built to showcase product thinking, DevOps readiness, and applied machine learning. It blends **real churn prediction models** (using XGBoost) with **AI-generated nudges and per-user explainability**, offering a recruiter-friendly, production-style demo.

> 🧠 The AI nudges are served by Together AI’s Mixtral-8x7B model via REST, while churn prediction uses the IBM Telco churn dataset augmented with an A/B `variant` flag.

---

## 2. 🎯 Product Goals

- ✅ Demonstrate real-time AI-driven engagement suggestions  
- ✅ Deliver accurate churn risk predictions with explainability  
- ✅ Provide system-wide and per-variant analytics  
- ✅ Showcase end-to-end DevOps: Docker + CI/CD + AKS  
- ✅ Offer a live, interactive demo for interviews and portfolio reviews  

---

## 3. 👥 Target Users (Simulated Personas)

| Persona   | Behavioral Focus                             |
|-----------|-----------------------------------------------|
| Student   | Low usage, cost-sensitive, needs tips         |
| Marketer  | Visualizes engagement trends & A/B insights   |
| Analyst   | Seeks precise metrics and explainability      |
| Writer    | Prefers concise suggestions, avoids churn     |

---

## 4. 🧩 Core Features

| Feature                        | Description                                                                                           |
|--------------------------------|-------------------------------------------------------------------------------------------------------|
| 🧠 Real ML-Based Churn Model    | XGBoost classifier trained on Telco churn data, outputs calibrated probabilities                      |
| 🧠 AI Nudges                    | On-demand LLM nudges via Together AI Mixtral-8x7B, personalized per user profile                      |
| 📊 Interactive Dashboard        | Visuals for contract types, tenure, charges, support calls, and A/B variant distributions             |
| 🧩 Per-User Lifecycle Panel     | Detailed view of user metadata, churn score, risk label, and AI-generated nudge                        |
| 🧩 Per-User Explainability      | SHAP waterfall plots highlighting top feature impacts per selected user                              |
| 🧪 A/B Testing Simulation       | Dataset-driven assignment, with split analytics and churn rate comparison                             |
| 📥 Downloadable User Summary    | One-click TXT export with profile, churn metrics, and nudge text                                      |
| 🔐 Secure Logging               | App events logged to `logs/usage.log` (tracked via `.gitkeep`), running as non-root in containers      |

---

## 5. 📈 Success Metrics (MVP)

| Metric                       | Target Status       |
|------------------------------|---------------------|
| CI/CD (GitHub Actions)       | ✅ Green on push    |
| AKS Deployment                | ✅ Stable live URL  |
| Churn Model AUC > 0.80        | ✅ Achieved (0.83)  |
| Real-time Nudges Delivered    | ✅ Mixtral-8x7B API |
| SHAP Explainability Tab       | ✅ Global & per-user|
| Summary Export Works          | ✅ Generates .txt   |
| Variant A/B Split ~50/50      | ✅ Balanced         |

---

## 6. 🔮 Future Enhancements

| Feature                                   | Priority | Notes                                     |
|-------------------------------------------|----------|-------------------------------------------|
| 🔐 OAuth / Admin Login                    | Medium   | Add user authentication & role control    |
| 📊 Cohort & Time-Series Analytics         | Medium   | Track engagement trends over time         |
| 💬 Feedback Loop for Nudges               | Low      | Capture user responses to improve prompts |
| 📈 Multi-model Nudging (A/B LLMs)         | Low      | Compare performance of different LLMs     |

---

## 7. 📂 Dataset Summary

- **Source**: IBM Telco Customer Churn dataset  
- **Records**: ~7,000 customers  
- **Target**: `Churn` (0 = Stay, 1 = Churn)  
- **Features**: Demographics, contract, tenure, charges (log-scaled), support calls, **A/B variant**  
- **Preprocessing**: Label encoding, scaling, log transform, drop UI-only columns  

---

## 📌 Project Info

- **Live Demo**: http://your-app-url  
- **GitHub**: github.com/taneshsin/EngageTrack-AI  
- **Maintainer**: Tanesh Singhal (MS-BANA ’25)  
- **Tech Stack**: Streamlit, Python, XGBoost, Together AI, Docker, GitHub Actions, AKS  
- **Last Updated**: May 2025  

---

🧠 *EngageTrack AI integrates real AI nudges, churn modeling, and explainability within a cloud-native DevOps pipeline—ideal for product, ML, and engineering showcases.*  
