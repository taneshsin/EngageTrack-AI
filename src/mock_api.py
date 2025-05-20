import random

def generate_mock_nudge(user_id, usage_frequency, support_calls, payment_delay, contract_length):
    """
    Generate a single rule-based engagement nudge for a customer
    based on real behavioral indicators from the churn dataset.

    Returns one personalized recommendation.
    """

    nudges = []

    # Engagement level
    if usage_frequency < 10:
        nudges.extend([
            "Explore our weekly engagement tools to build a habit.",
            "Set reminders to revisit features you used before.",
            "Check out our Quick Start guide to get back on track."
        ])

    # Support burden
    if support_calls > 5:
        nudges.extend([
            "We noticed you’ve contacted support frequently — try our Help Center for quick answers.",
            "Join our next onboarding webinar for tips and tricks.",
            "Schedule a success call to streamline your experience."
        ])

    # Payment friction
    if payment_delay > 15:
        nudges.extend([
            "Update your billing info to avoid any service interruptions.",
            "Enable auto-pay to never miss a billing cycle.",
            "Check out our billing support FAQ if you’re facing delays."
        ])

    # Contract length
    if contract_length.strip().lower() == "monthly":
        nudges.extend([
            "Switch to an annual plan and save up to 20%.",
            "Annual subscribers receive premium support and loyalty rewards.",
            "Consider long-term plans for uninterrupted access at better rates."
        ])

    # Fallback nudge if no triggers
    if not nudges:
        nudges.append("Thanks for being with us! Try our newest features for enhanced productivity.")

    return f"Hi {user_id}, {random.choice(nudges)}"
