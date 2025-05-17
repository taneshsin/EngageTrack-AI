# recommendation_engine.py

def get_engagement_color(level):
    return {
        "High": "green",
        "Medium": "orange",
        "Low": "red"
    }.get(level, "gray")

def get_churn_color(risk):
    return {
        "Low": "green",
        "Medium": "orange",
        "High": "red"
    }.get(risk, "gray")
