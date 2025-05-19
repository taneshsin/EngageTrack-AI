# 🔒 EngageTrack AI – Security Overview

EngageTrack AI is a simulated SaaS analytics platform designed to demonstrate best practices in DevOps, AI feature logic, and product lifecycle intelligence. While the project uses mock data and simulation features, several production-grade security practices have been implemented.

---

## ✅ Security Measures Implemented

| Area                        | Measure                                                                 |
|-----------------------------|--------------------------------------------------------------------------|
| 🔐 Containerization         | App runs in a **Docker container as a non-root user (`appuser`)**        |
| 🧾 Logging                  | All logs are written to `/tmp/usage.log` to avoid file permission issues |
| 🔁 CI/CD Pipeline           | GitHub Actions are used with secure secrets for ACR + AKS deployment     |
| 🧱 Ingress Protection       | Configured **NGINX Ingress rate limiting** (RPS + burst control)         |
| 🌍 Public Access Control    | Temporarily tested **IP whitelisting** and removed for broader access     |
| ⚠️ Secrets Management      | No API keys or `.env` files are pushed to GitHub (`.gitignore` enforced) |
| 🧪 A/B Variant Isolation    | All test variants are simulated without accessing sensitive data         |

---

## 🔒 Optional Security Measures (Not Yet Activated)

| Feature                     | Status     | Notes |
|----------------------------|------------|-------|
| HTTPS / TLS                | ❌ Skipped  | Not required for mock data demo; can be added via `cert-manager` |
| Basic Auth (Ingress)       | ❌ Not enabled | Can be added to restrict public demo access if needed |
| Kubernetes Network Policies| ❌ Skipped  | Not required for this scale |
| Vulnerability Scanning     | ❌ Not active | Could be added via DockerHub/ACR scanning or Trivy |

---

## 📌 Summary

While EngageTrack AI is a simulated analytics platform for demonstration and portfolio use, great care has been taken to reflect real-world engineering security patterns in Docker, Kubernetes, and CI/CD pipelines.

For full enterprise deployments or public domain exposure, additional protections (TLS, auth, firewall policies) are recommended.

---

🛡️ *Built by Tanesh Singhal – May 2025*
