import pandas as pd

def load_user_data():
    """
    Load the real customer churn dataset for EngageTrack AI.
    Returns the full DataFrame with all features for dashboard use.
    """
    return pd.read_csv("data/customer_churn_dataset-testing-master.csv")
