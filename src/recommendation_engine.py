# Threshold constants (optional tuning)
ENGAGEMENT_HIGH = 50
ENGAGEMENT_MEDIUM = 25

CHURN_HIGH = 0.75
CHURN_MEDIUM = 0.5

def get_engagement_color(usage_frequency):
    """
    Returns a color based on usage frequency.
    Green = High, Orange = Medium, Red = Low
    """
    if usage_frequency >= ENGAGEMENT_HIGH:
        return "green"
    elif ENGAGEMENT_MEDIUM <= usage_frequency < ENGAGEMENT_HIGH:
        return "orange"
    else:
        return "red"

def get_churn_color(prob):
    """
    Returns a color based on churn probability.
    Green = Low, Orange = Medium, Red = High
    """
    if prob >= CHURN_HIGH:
        return "red"
    elif prob >= CHURN_MEDIUM:
        return "orange"
    else:
        return "green"

def get_churn_label(prob):
    """
    Returns a risk label based on churn probability.
    High = ≥ 0.75, Medium = ≥ 0.5, Low = < 0.5
    """
    if prob >= CHURN_HIGH:
        return "High"
    elif prob >= CHURN_MEDIUM:
        return "Medium"
    else:
        return "Low"
