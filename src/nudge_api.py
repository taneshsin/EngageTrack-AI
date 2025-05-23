# src/nudge_api.py
import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

load_dotenv()                            # local .env; no‐op in AKS
HF_TOKEN = os.getenv("HF_TOKEN")
client   = InferenceClient(token=HF_TOKEN)

def generate_hf_nudge(user_id, usage_frequency, support_calls,
                      payment_delay, contract_length,
                      tech_support, monthly_charges,
                      paperless_billing, variant):
    prompt = (
        f"User {user_id} profile:\n"
        f"- Tenure: {usage_frequency}\n"
        f"- Support calls: {support_calls}\n"
        f"- Payment delay (log days): {payment_delay}\n"
        f"- Contract: {contract_length}\n"
        f"- Tech support: {tech_support}\n"
        f"- Monthly charges: ${monthly_charges}\n"
        f"- Paperless billing: {paperless_billing}\n"
        f"- Variant: {variant}\n\n"
        "Write a concise, friendly suggestion to help this user increase engagement and reduce churn."
    )

    # Note: use `prompt=` instead of `inputs=`
    result = client.text_generation(
        model="gpt2-medium",
        prompt=prompt,
        parameters={"max_new_tokens": 100, "temperature": 0.7}
    )

    if hasattr(result, "generated_text"):
        return result.generated_text.strip()
    else:
        return result[0].get("generated_text", "").strip()
