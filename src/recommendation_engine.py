def get_engagement_color(usage_frequency):
    if usage_frequency >= 50:
        return "green"
    elif 25 <= usage_frequency < 50:
        return "orange"
    else:
        return "red"

def get_churn_color(prob):
    if prob >= 0.75:
        return "red"
    elif prob >= 0.5:
        return "orange"
    else:
        return "green"

def get_churn_label(prob):
    if prob >= 0.75:
        return "High"
    elif prob >= 0.5:
        return "Medium"
    else:
        return "Low"
