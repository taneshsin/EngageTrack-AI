def get_engagement_color(usage_frequency):
    """
    Maps usage frequency to a traffic-light color code.

    Green: 20+ (high engagement)
    Orange: 10–19 (moderate)
    Red: <10 (low)
    """
    try:
        usage_frequency = float(usage_frequency)
    except:
        return "gray"

    if usage_frequency >= 20:
        return "green"
    elif 10 <= usage_frequency < 20:
        return "orange"
    else:
        return "red"


def get_churn_color(probability_or_label):
    """
    Maps churn risk (as a probability or a binary label) to a color code:
    
    - Input: float (probability between 0–1), str-convertible, or int (0 or 1)
    - Output: string "green", "orange", "red", or fallback "gray"

    Risk Bands:
    - Green: Low Risk (≤ 0.4)
    - Orange: Medium Risk (0.4 < p ≤ 0.7)
    - Red: High Risk (> 0.7)
    """
    try:
        if isinstance(probability_or_label, float):
            p = probability_or_label
        elif isinstance(probability_or_label, str):
            p = float(probability_or_label)
        elif isinstance(probability_or_label, int):
            return "red" if probability_or_label == 1 else "green"
        else:
            return "gray"

        if p >= 0.7:
            return "red"
        elif p >= 0.4:
            return "orange"
        else:
            return "green"

    except:
        return "gray"


def get_churn_label(prob):
    """
    Converts churn probability into a textual label.
    Useful for user-friendly display alongside color codes.

    - High Risk: > 0.7
    - Medium Risk: 0.4–0.7
    - Low Risk: ≤ 0.4
    """
    try:
        p = float(prob)
        if p >= 0.7:
            return "High Risk"
        elif p >= 0.4:
            return "Medium Risk"
        else:
            return "Low Risk"
    except:
        return "Unknown"
