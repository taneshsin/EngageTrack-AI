import pandas as pd
import random

df = pd.read_csv("data/user_recommendations.csv")
df["variant"] = [random.choice(["A", "B"]) for _ in range(len(df))]
df.to_csv("data/user_recommendations.csv", index=False)

print("✅ Variants A/B assigned and saved.")
