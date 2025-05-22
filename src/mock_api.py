import random

def generate_mock_nudges(
    user_id,
    usage_frequency,
    support_calls,
    payment_delay,
    contract_length=None,
    tech_support=None,
    monthly_charges=None,
    paperless_billing=None,
    verbose=False
):
    nudges = []
    reasons = []

    if usage_frequency < 10:
        nudges.append("Explore our quick-start tips to boost your engagement.")
        reasons.append("Low usage frequency")

    if support_calls > 3:
        nudges.append("Try our Help Center to resolve common issues quickly.")
        reasons.append("Frequent support calls")

    if payment_delay > 15:
        nudges.append("Enable auto-pay to prevent billing interruptions.")
        reasons.append("Late payments")

    if isinstance(contract_length, str) and contract_length.lower() == "month-to-month":
        nudges.append("Switch to a yearly plan and save on your monthly bill.")
        reasons.append("Short-term contract")

    if monthly_charges and monthly_charges > 80:
        nudges.append("Review your active services — you might be paying for extras.")
        reasons.append("High monthly charges")

    if isinstance(tech_support, str) and tech_support.lower() == "no":
        nudges.append("Enable tech support for hassle-free troubleshooting.")
        reasons.append("No tech support enabled")

    if isinstance(paperless_billing, str) and paperless_billing.lower() == "no":
        nudges.append("Switch to paperless billing for convenience and speed.")
        reasons.append("Paper billing active")

    if not nudges:
        nudges.append("Thanks for being with us! Check out new features this month.")
        reasons.append("Default appreciation message")

    message = f"Hi {user_id}, {random.choice(nudges)}"
    
    return (message, reasons) if verbose else message
