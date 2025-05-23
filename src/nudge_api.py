# src/nudge_api.py

import os
import requests
from dotenv import load_dotenv

# Load TG_API_KEY from .env locally or from environment
load_dotenv()
TG_API_KEY = os.getenv("TG_API_KEY")

# Together AI completion endpoint
TG_URL = "https://api.together.xyz/v1/completions"

def generate_hf_nudge(
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
    Generate a personalized engagement nudge via Together AI.
    (Function name unchanged for compatibility with app.py.)
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
        "temperature": 0.7
    }

    response = requests.post(TG_URL, headers=headers, json=payload, timeout=30)
    response.raise_for_status()
    data = response.json()

    # Together AI returns {"choices":[{"text":"..."}], ...}
    choices = data.get("choices", [])
    if choices and "text" in choices[0]:
        return choices[0]["text"].strip()

    return "Unable to generate suggestion."
