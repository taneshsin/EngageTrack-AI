import pandas as pd
import random

# Load the real churn dataset
df = pd.read_csv("data/churn.csv")

# Assign A or B randomly
df["variant"] = [random.choice(["A", "B"]) for _ in range(len(df))]

# Save back to same file
df.to_csv("data/churn.csv", index=False)

print("✅ A/B variants assigned and saved to churn dataset.")
