import random

def generate_mock_nudges(user_id, usage_frequency, support_calls, payment_delay, contract_length=None, tech_support=None, monthly_charges=None, paperless_billing=None):
    nudges = []

    if usage_frequency < 10:
        nudges.append("Explore our quick-start tips to boost your engagement.")

    if support_calls > 3:
        nudges.append("Try our Help Center to resolve common issues quickly.")

    if payment_delay > 15:
        nudges.append("Enable auto-pay to prevent billing interruptions.")

    if contract_length and contract_length.lower() == "month-to-month":
        nudges.append("Switch to a yearly plan and save on your monthly bill.")

    if monthly_charges and monthly_charges > 80:
        nudges.append("Review your active services — you might be paying for extras.")

    if tech_support and tech_support.lower() == "no":
        nudges.append("Enable tech support for hassle-free troubleshooting.")

    if paperless_billing and paperless_billing.lower() == "no":
        nudges.append("Switch to paperless billing for convenience and speed.")

    if not nudges:
        nudges.append("Thanks for being with us! Check out new features this month.")

    return f"Hi {user_id}, {random.choice(nudges)}"
