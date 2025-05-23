import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")

# Validate environment variable
if not HF_TOKEN:
    raise EnvironmentError("HF_TOKEN is not set. Please check your .env file.")

TG_URL = "https://api.together.xyz/v1/completions"
MODEL_NAME = "mistralai/Mixtral-8x7B-Instruct-v0.1"  # Update this if needed

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
    Generate a personalized engagement nudge using Together AI text generation model.
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
        "Write a brief, friendly message in 30 words to help this user engage more and avoid churn. Don't provide any link. Just give direct message"
    )

    headers = {
        "Authorization": f"Bearer {HF_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "max_tokens": 50,
        "temperature": 0.7
    }

    resp = requests.post(TG_URL, headers=headers, json=payload, timeout=30)
    if resp.status_code != 200:
        raise RuntimeError(f"Together API error {resp.status_code}: {resp.text}")

    data = resp.json()
    choices = data.get("choices", [])
    if choices and isinstance(choices[0], dict) and "text" in choices[0]:
        return choices[0]["text"].strip()

    return "Unable to generate suggestion."
