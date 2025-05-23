# src/nudge_api.py

import os
import requests
from dotenv import load_dotenv

# Load HF_TOKEN from .env locally or from environment (CI/CD, AKS)
load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")
INFERENCE_API_URL = "https://api-inference.huggingface.co/models/gpt2-medium"

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
    Generate a personalized engagement nudge by calling
    the Hugging Face Inference API over HTTP.
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
        "Write a concise, friendly suggestion to help this user "
        "increase engagement and reduce churn."
    )

    headers = {
        "Authorization": f"Bearer {HF_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 100,
            "temperature": 0.7
        }
    }

    response = requests.post(INFERENCE_API_URL, headers=headers, json=payload, timeout=30)
    response.raise_for_status()
    data = response.json()

    # The API returns a list of dicts with "generated_text"
    if isinstance(data, list) and "generated_text" in data[0]:
        return data[0]["generated_text"].strip()
    # Otherwise return the whole payload
    return str(data).strip()
