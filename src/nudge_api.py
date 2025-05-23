# src/nudge_api.py

import os
import requests
import re
from dotenv import load_dotenv

load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")
TG_URL = "https://api.together.xyz/v1/completions"
MODEL_NAME = "mistralai/Mixtral-8x7B-Instruct-v0.1"

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
        "Write a concise, friendly message (no more than 30 words) "
        "to encourage continued engagement and reduce churn. "
        "Do NOT include any user IDs, dates, phone numbers, links, "
        "or system-specific details. "
        "Use only “you” and general benefits."
    )

    headers = {
        "Authorization": f"Bearer {HF_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "max_tokens": 60,
        "temperature": 0.7
    }

    resp = requests.post(TG_URL, headers=headers, json=payload, timeout=30)
    resp.raise_for_status()
    data = resp.json()

    choices = data.get("choices", [])
    if choices and "text" in choices[0]:
        text = choices[0]["text"].strip()
        # Strip any trailing "User X" noise
        clean = re.sub(r"\s*User\s+\S+$", "", text).strip()
        return clean

    return "Unable to generate suggestion."
