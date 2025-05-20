def get_engagement_color(usage_frequency):
    """
    Map usage frequency to a color.
    """
    if usage_frequency >= 20:
        return "green"
    elif 10 <= usage_frequency < 20:
        return "orange"
    else:
        return "red"


def get_churn_color(probability_or_label):
    """
    Map churn probability (0 to 1) or binary label to a risk color.
    - If float: assumes probability
    - If int (0 or 1): maps directly
    """
    if isinstance(probability_or_label, float):
        if probability_or_label >= 0.7:
            return "red"     # High risk
        elif probability_or_label >= 0.4:
            return "orange"  # Medium risk
        else:
            return "green"   # Low risk
    elif isinstance(probability_or_label, int):
        return "red" if probability_or_label == 1 else "green"
    else:
        return "gray"  # fallback for unknown input
