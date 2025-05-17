import random

def generate_mock_nudge(user_id, engagement_level, persona):
    nudges = {
        "Student": [
            "Check out our interactive tutorials to get ahead.",
            "Try the daily challenge to stay engaged.",
            "Join study groups using the collab tool!",
            "Use Smart Notes to retain key topics."
        ],
        "Marketer": [
            "Try the campaign performance dashboard today!",
            "Use smart segmentation to target better.",
            "Analyze your latest funnel with one click.",
            "Check your top-performing channel insights."
        ],
        "Analyst": [
            "Explore advanced filters for deeper insights.",
            "Try predictive dashboards to boost forecasting.",
            "Use cohort analysis to track user patterns.",
            "Export raw data for custom analysis."
        ],
        "Writer": [
            "Use the content suggestion tool to brainstorm ideas.",
            "Try distraction-free mode while writing.",
            "Check readability score before publishing!",
            "Draft faster using AI-assisted writing."
        ]
    }

    options = nudges.get(persona, ["Explore new features to stay productive!"])
    chosen = random.choice(options)
    return f"Hi {user_id}, {chosen}"
