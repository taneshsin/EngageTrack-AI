import pandas as pd

def load_user_data():
    return pd.read_csv("data/churn.csv")
