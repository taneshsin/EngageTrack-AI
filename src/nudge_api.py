import os
import requests
from dotenv import load_dotenv

# Load TG_API_KEY from .env locally, or from environment (CI/CD, AKS)
load_dotenv()
TG_API_KEY = os.getenv("TG_API_KEY")

# Together AI text-generation endpoint (v1 completion)
TG_URL = "https://api.together.ai/api/v1/completions"

def generate_together_nudge(
    user_id,
    usage_frequency,
    support_calls,
    payment_delay,
    contract_length,
    tech_support,
    monthly_charges,
    paperless_billing,
    variant
):
    """
    Generate a friendly engagement nudge via Together AI.
    """
    prompt = (
        f"User {user_id} profile:\n"
        f"- Tenure (months): {usage_frequency}\n"
        f"- Support calls: {support_calls}\n"
        f"- Payment delay (log days): {payment_delay}\n"
        f"- Contract: {contract_length}\n"
        f"- Tech support: {tech_support}\n"
        f"- Monthly charges: ${monthly_charges}\n"
        f"- Paperless billing: {paperless_billing}\n"
        f"- Variant: {variant}\n\n"
        "Write a concise, friendly suggestion to help this user increase engagement and reduce churn."
    )

    headers = {
        "Authorization": f"Bearer {TG_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "together-vicuna-7b",
        "prompt": prompt,
        "max_tokens": 100,
        "temperature": 0.7,
    }

    resp = requests.post(TG_URL, headers=headers, json=payload, timeout=30)
    resp.raise_for_status()
    data = resp.json()

    # Response format: { "id": "...", "choices": [ { "text": "..." } ], ... }
    text = data.get("choices", [{}])[0].get("text", "").strip()
    return text or "Unable to generate suggestion."
