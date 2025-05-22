import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler

def load_user_data(raw=False, fit=False, label_encoders=None, scaler=None):
    df = pd.read_csv("data/churn.csv")
    if raw:
        return df  # untouched, for UI
    # otherwise, preprocess and return arrays + transformers
    X, y, fitted_scaler, fitted_encoders, feature_names = preprocess_user_data(
        df,
        label_encoders=label_encoders,
        fit=fit,
        return_scaler=True
    )
    return X, y, fitted_scaler, fitted_encoders, feature_names


def preprocess_user_data(df, label_encoders=None, fit=False, return_scaler=False):
    df = df.copy()

    # Drop ID and UI-only column 'variant'
    df.drop(columns=["customerID", "variant"], inplace=True, errors="ignore")

    # Clean TotalCharges
    df = df[df["TotalCharges"].str.strip() != ""]
    df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
    df.dropna(inplace=True)
    df["TotalCharges"] = np.log1p(df["TotalCharges"])

    # Label-encode categoricals (all object dtypes now, excluding variant which was dropped)
    if label_encoders is None:
        label_encoders = {}
    label_cols = df.select_dtypes(include="object").columns.tolist()

    for col in label_cols:
        if fit or col not in label_encoders:
            le = LabelEncoder()
            df[col] = le.fit_transform(df[col])
            label_encoders[col] = le
        else:
            df[col] = label_encoders[col].transform(df[col])

    # Separate target
    y = df.pop("Churn") if "Churn" in df.columns else None

    # Scale features
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
