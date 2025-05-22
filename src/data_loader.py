import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler

def load_user_data(raw=False):
    """
    Loads the enriched churn dataset with 'variant' column.
    If raw=True, returns the unprocessed raw dataframe.
    """
    df = pd.read_csv("data/churn.csv")
    if raw:
        return df
    else:
        return preprocess_user_data(df)[0]  # Return only preprocessed df for UI display


def preprocess_user_data(df, label_encoders=None, fit=False, return_scaler=False):
    """
    Preprocesses the churn dataset:
    - Cleans TotalCharges
    - Encodes categorical variables
    - Scales features
    Returns:
        X_scaled, y, (optional) scaler, encoders, feature_names
    """
    df = df.copy()

    # Drop customerID if present
    if "customerID" in df.columns:
        df.drop(columns=["customerID"], inplace=True)

    # Clean TotalCharges
    df = df[df["TotalCharges"] != " "]
    df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
    df.dropna(inplace=True)
    df["TotalCharges"] = np.log1p(df["TotalCharges"])

    # Label encoding
    if label_encoders is None:
        label_encoders = {}

    label_cols = df.select_dtypes(include="object").columns
    for col in label_cols:
        if col not in label_encoders or fit:
            le = LabelEncoder()
            df[col] = le.fit_transform(df[col])
            label_encoders[col] = le
        else:
            df[col] = label_encoders[col].transform(df[col])

    y = df.pop("Churn") if "Churn" in df.columns else None

    scaler = None
    if fit:
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(df)
    else:
        X_scaled = df.values  # Use externally fitted scaler

    if return_scaler:
        return X_scaled, y, scaler, label_encoders, df.columns.tolist()
    return X_scaled, y, label_encoders
