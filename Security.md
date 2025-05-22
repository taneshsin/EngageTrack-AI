# 🔒 EngageTrack AI – Security Overview

**EngageTrack AI** is a portfolio-grade, simulated SaaS analytics platform demonstrating AI-powered churn prediction, engagement nudges, and DevOps capabilities. While it uses mock or anonymized data, it incorporates real-world security practices suitable for scalable, cloud-native deployments.

> 🧠 Note: The threat model here is simulated. The purpose is to showcase secure engineering workflows — not to protect real customer data.

---

## ✅ Security Measures Implemented

| Area                        | Security Practice                                                                 |
|-----------------------------|------------------------------------------------------------------------------------|
| 🔐 Containerization         | Dockerized app runs as a **non-root user** (`appuser`)                             |
| 🔁 CI/CD Secrets            | **GitHub Secrets** used for AKS + ACR credentials in deployment pipeline          |
| 📁 Log Safety               | Logs are written to `/tmp/usage.log` (safe write in containerized environments)   |
| 📄 Git Hygiene              | `.gitignore` and `.dockerignore` protect credentials, logs, build files           |
| 🔧 NGINX Ingress            | Reverse proxy with **rate limiting (RPS + burst)** via annotations                |
| 🧪 Variant Isolation        | A/B testing logic handled with isolated, simulated variants                       |
| 🚫 No Hardcoded Secrets     | No `.env` files or API tokens committed; simulated logic only                     |
| 🧱 Modular Architecture     | Separated logic (`mock_api`, `recommendation_engine`, `model training`) reduces attack surface |
| 📂 Minimal Data Exposure    | Only anonymized churn features used; no user-identifiable info shown              |

---

## 🔒 Optional (Not Yet Activated)

| Security Control            | Status       | Notes                                                                 |
|-----------------------------|--------------|-----------------------------------------------------------------------|
| ✅ HTTPS / TLS              | ❌ Skipped    | Can be configured with **cert-manager + Let's Encrypt** for AKS      |
| 🔐 Basic Authentication     | ❌ Not enabled| For demo environments; can be added via NGINX ingress auth            |
| 📦 Vulnerability Scanning   | ❌ Planned    | Tools like **Trivy**, **Snyk**, or ACR image scan can be used         |
| 🔍 Audit Logging Extension  | ❌ Optional   | Current log covers usage; full nudge tracking can be added            |
| 📡 Network Policies         | ❌ Skipped    | Not required for this small-scale public deployment                   |

---

## 🔐 Deployment Stack & Hardening Summary

- **CI/CD:** GitHub Actions with secret tokens → ACR → AKS rollout
- **Ingress:** NGINX with rate limit annotations and L7 proxy protection
- **Container:** Docker image follows best practices (non-root, minimal image size, secure file access)
- **Logging:** Streamlit logs usage securely, without overwriting files

---

## 📌 Takeaway

Although EngageTrack AI is not a production system, it models:

- Clean separation of concerns
- Secure deployment workflows (CI/CD + AKS + Docker)
- Safe logging and API practices
- Scalable security thinking for SaaS ML apps

---

🛡️ *Built with security best practices by Tanesh Singhal – May 2025*
