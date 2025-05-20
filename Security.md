# 🔒 EngageTrack AI – Security Overview

EngageTrack AI is a simulated SaaS analytics platform designed to demonstrate best practices in DevOps, AI feature logic, and product lifecycle intelligence. While the project uses mock data and simulation features, several production-grade security practices have been implemented.

> 🧠 Note: The threat model is scoped to simulate strong engineering hygiene, not to secure production customer data.

---

## ✅ Security Measures Implemented

| Area                        | Measure                                                                 |
|-----------------------------|--------------------------------------------------------------------------|
| 🔐 Containerization         | App runs in a **Docker container as a non-root user (`appuser`)**        |
| 🧾 Logging                  | All logs are written to `/tmp/usage.log` to avoid file permission issues |
| 🔁 CI/CD Pipeline           | GitHub Actions used with **secure GitHub secrets** for ACR + AKS deploy  |
| 🧱 Ingress Protection       | Configured **NGINX Ingress with rate limiting (RPS + burst)**            |
| 🌍 Public Access Control    | IP whitelisting was temporarily enabled for testing, now disabled        |
| ⚠️ Secrets Management      | No API keys or `.env` files are committed (`.gitignore` enforced)        |
| 🧪 A/B Variant Isolation    | A/B testing logic is fully simulated; no sensitive user data is accessed |

---

## 🔒 Optional Security Measures (Not Yet Activated)

| Feature                     | Status     | Notes                                                  |
|----------------------------|------------|--------------------------------------------------------|
| HTTPS / TLS                | ❌ Skipped  | Not required for mock data demo; can be added via `cert-manager` |
| Basic Auth (Ingress)       | ❌ Not enabled | Can be added to restrict public demo access          |
| Kubernetes Network Policies| ❌ Skipped  | Not required for this demo scale                      |
| Vulnerability Scanning     | ❌ Not active | Can be enabled via tools like Trivy or ACR scans     |

---

## 📌 Summary

While EngageTrack AI is a simulated analytics platform built for learning and demonstration purposes, it reflects real-world engineering security patterns across Docker, Kubernetes, and CI/CD workflows.

For production-grade deployments, additional controls such as HTTPS, authentication, vulnerability scanning, and network policies are strongly recommended.

---

🛡️ *Built by Tanesh Singhal – May 2025*
