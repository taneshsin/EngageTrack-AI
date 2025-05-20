import pandas as pd
import random

def load_user_data():
    df = pd.read_csv("data/churn.csv")

    # ✅ Fallback: If 'variant' column is missing, generate and add
    if 'variant' not in df.columns:
        df['variant'] = [random.choice(['A', 'B']) for _ in range(len(df))]

    return df
