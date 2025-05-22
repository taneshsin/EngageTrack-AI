import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler

def load_user_data(raw=False, fit=False, label_encoders=None, scaler=None):
    """
    If raw=True:
        returns the untouched DataFrame (with customerID, variant, etc.).
    Else:
        returns X, y, scaler, label_encoders, feature_names.
        Pass fit=True on training to fit new encoders/scaler.
    """
    df = pd.read_csv("data/churn.csv")

    if raw:
        return df

    X, y, fitted_scaler, fitted_encoders, feature_names = preprocess_user_data(
        df,
        label_encoders=label_encoders,
        fit=fit,
        return_scaler=True
    )
    return X, y, fitted_scaler, fitted_encoders, feature_names


def preprocess_user_data(df, label_encoders=None, fit=False, return_scaler=False):
    """
    Cleans and encodes the churn DataFrame.
    - Drops customerID
    - Cleans TotalCharges + log1p
    - Label-encodes all categoricals except 'variant'
    - Fits or applies StandardScaler
    """
    df = df.copy()

    if "customerID" in df.columns:
        df.drop(columns=["customerID"], inplace=True)

    df = df[df["TotalCharges"].str.strip() != ""]
    df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
    df.dropna(inplace=True)
    df["TotalCharges"] = np.log1p(df["TotalCharges"])

    if label_encoders is None:
        label_encoders = {}

    label_cols = [c for c in df.select_dtypes(include="object").columns if c != "variant"]

    for col in label_cols:
        if fit or col not in label_encoders:
            le = LabelEncoder()
            df[col] = le.fit_transform(df[col])
            label_encoders[col] = le
        else:
            df[col] = label_encoders[col].transform(df[col])

    y = df.pop("Churn") if "Churn" in df.columns else None

    if fit:
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(df)
    else:
        scaler = None
        X_scaled = df.values

    feature_names = df.columns.tolist()

    if return_scaler:
        return X_scaled, y, scaler, label_encoders, feature_names
    return X_scaled, y, label_encoders
