import pandas as pd

def load_user_data():
    """
    Loads the enriched churn dataset with 'variant' column.
    Returns the DataFrame for use in Streamlit app.
    """
    return pd.read_csv("data/churn.csv")
