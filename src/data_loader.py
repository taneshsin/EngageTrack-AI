# data_loader.py
import pandas as pd

def load_user_data():
    return pd.read_csv("data/user_recommendations.csv")
