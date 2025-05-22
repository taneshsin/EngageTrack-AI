import random

# Persona tone mapping (customizable)
PERSONA_TONE = {
    "Senior": "formal",
    "Young Professional": "friendly",
    "Techie": "helpful",
    "Default": "neutral"
}

# Tone-based sentence templates
TONE_WRAPPER = {
    "formal": lambda msg: f"We recommend: {msg}",
    "friendly": lambda msg: f"Hey there! {msg}",
    "helpful": lambda msg: f"Quick tip: {msg}",
    "neutral": lambda msg: msg
}


def generate_mock_nudges(user_id, usage_frequency, support_calls, payment_delay, contract_length, persona="Default"):
    """
    Generates a list of categorized, tone-adjusted engagement nudges for a customer.
    """

    nudges = []

    # Normalize contract length
    contract_length = contract_length.strip().lower() if isinstance(contract_length, str) else ""

    # Set tone style
    tone = PERSONA_TONE.get(persona, PERSONA_TONE["Default"])
    wrap = TONE_WRAPPER.get(tone, TONE_WRAPPER["neutral"])

    # Engagement-based nudges
    try:
        if float(usage_frequency) < 10:
            nudges.append({
                "category": "engagement",
                "message": wrap("Explore our weekly tools to build a habit.")
            })
            nudges.append({
                "category": "engagement",
                "message": wrap("Set reminders to revisit your favorite features.")
            })
    except:
        pass

    # Support-related nudges
    try:
        if float(support_calls) > 5:
            nudges.append({
                "category": "support",
                "message": wrap("You’ve reached out a few times — try our Help Center anytime.")
            })
            nudges.append({
                "category": "support",
                "message": wrap("Book a quick success call to improve your experience.")
            })
    except:
        pass

    # Payment delay nudges
    try:
        if float(payment_delay) > 15:
            nudges.append({
                "category": "payment",
                "message": wrap("Enable auto-pay to avoid billing issues.")
            })
            nudges.append({
                "category": "payment",
                "message": wrap("Check our billing FAQ if you’re running into problems.")
            })
    except:
        pass

    # Contract upgrade suggestion
    if contract_length == "month-to-month" or contract_length == "monthly":
        nudges.append({
            "category": "contract",
            "message": wrap("Upgrade to annual billing and enjoy up to 20% savings.")
        })
        nudges.append({
            "category": "contract",
            "message": wrap("Annual plans come with premium support benefits.")
        })

    # Fallback generic
    if not nudges:
        nudges.append({
            "category": "generic",
            "message": wrap("Thanks for being with us! Check out our latest features today.")
        })

    return nudges
