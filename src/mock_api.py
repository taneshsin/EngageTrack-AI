import random

def generate_mock_nudges(user_id, usage_frequency, support_calls, payment_delay, contract_length):
    """
    Generate multiple categorized nudges based on user behavior inputs.
    Returns a string containing category-tagged nudges.
    """
    categories = {
        "engagement": [],
        "support": [],
        "billing": [],
        "retention": []
    }

    # Engagement nudges
    if usage_frequency < 20:
        categories["engagement"].extend([
            "Try setting daily reminders to engage more consistently.",
            "Explore our guided tutorials to get the most out of your subscription.",
            "Low activity detected – try visiting new sections to discover features."
        ])

    # Support nudges
    if support_calls > 3:
        categories["support"].extend([
            "Frequent help requests? Our FAQ might save you time!",
            "Schedule a walkthrough call to reduce friction in usage.",
            "Try our AI chatbot for faster issue resolution."
        ])

    # Billing nudges
    if payment_delay > 15:
        categories["billing"].extend([
            "Enable auto-pay to avoid service interruptions.",
            "Consider switching to a more predictable payment method.",
            "Your billing info might be outdated — take a moment to check."
        ])

    # Retention nudges based on contract length
    if contract_length.strip().lower() == "month-to-month":
        categories["retention"].extend([
            "Save up to 20% by switching to a 12-month contract.",
            "Annual plans unlock premium support tiers.",
            "Loyalty bonuses apply for 6-month+ commitments."
        ])

    # Fallback if no rules triggered
    if all(len(lst) == 0 for lst in categories.values()):
        categories["engagement"].append("You're all set! Explore new features released this month.")

    # Sample one from each category (if available)
    final_nudges = []
    for cat, nudges in categories.items():
        if nudges:
            final_nudges.append(f"[{cat.upper()}] {random.choice(nudges)}")

    return "\n".join(final_nudges)
