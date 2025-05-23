# src/nudge_api.py

import os
import requests
from dotenv import load_dotenv

# Load your Together AI key (still via HF_TOKEN env var)
load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")

# Together AI free Llama Vision + FLUX.1 completion endpoint
TG_URL = "https://api.together.xyz/v1/completions"
MODEL_NAME = "together-llama-11b-flux.1"  # the free-tier model

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
    Generate a personalized engagement nudge via Together AI’s free Llama Vision 11B + FLUX.1 model.
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
        "Authorization": f"Bearer {HF_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "max_tokens": 100,
        "temperature": 0.7
    }

    resp = requests.post(TG_URL, headers=headers, json=payload, timeout=30)
    if resp.status_code != 200:
        raise RuntimeError(f"Together API error {resp.status_code}: {resp.text}")

    data = resp.json()
    # Expect {"choices":[{"text":"..."}], ...}
    choices = data.get("choices", [])
    if choices and isinstance(choices[0], dict) and "text" in choices[0]:
        return choices[0]["text"].strip()

    return "Unable to generate suggestion."
