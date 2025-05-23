# src/nudge_api.py

import os
import requests
from dotenv import load_dotenv

load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")

# Use the DistilGPT-2 pipeline (always enabled)
INFERENCE_API_URL = "https://api-inference.huggingface.co/pipeline/text-generation/distilgpt2"

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
        "Content-Type": "application/json",
    }
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 100,
            "temperature": 0.7
        }
    }

    resp = requests.post(INFERENCE_API_URL, headers=headers, json=payload, timeout=30)
    resp.raise_for_status()
    data = resp.json()

    # Pipeline returns [[{"generated_text": "..."}]]
    if isinstance(data, list) and data and isinstance(data[0], list) and data[0] and "generated_text" in data[0][0]:
        return data[0][0]["generated_text"].strip()
    return str(data).strip()
