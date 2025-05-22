import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler

def load_user_data(raw=False, fit=False, label_encoders=None, scaler=None):
    """
    Loads the churn dataset.

    Parameters
    ----------
    raw : bool
        If True, returns the untouched DataFrame with all original columns
        (including 'customerID' and 'variant').
    fit : bool
        If raw=False, whether to fit new encoders & scaler (for training).
        If False, will reuse provided label_encoders & scaler (for inference).
    label_encoders : dict or None
        Existing LabelEncoder instances for each categorical column.
    scaler : StandardScaler or None
        Existing StandardScaler instance.

    Returns
    -------
    If raw=True:
        df_raw : pd.DataFrame
    Else:
        X : np.ndarray
        y : pd.Series
        scaler : StandardScaler
        label_encoders : dict
        feature_names : list of str
    """
    df = pd.read_csv("data/churn.csv")

    if raw:
        return df

    # Preprocess and return arrays + transformers
    X, y, fitted_scaler, fitted_encoders, feature_names = preprocess_user_data(
        df,
        label_encoders=label_encoders,
        fit=fit,
        return_scaler=True
    )
    return X, y, fitted_scaler, fitted_encoders, feature_names


def preprocess_user_data(df, label_encoders=None, fit=False, return_scaler=False):
    """
    Preprocesses the churn dataset:
      - Drops customerID
      - Cleans TotalCharges
      - Label-encodes categoricals (excludes 'variant')
      - (Optionally) fits or applies a StandardScaler

    Parameters
    ----------
    df : pd.DataFrame
    label_encoders : dict or None
    fit : bool
        If True, fits new encoders & scaler.
        If False, reuses provided label_encoders & scaler for transform.
    return_scaler : bool
        If True, returns (X_scaled, y, scaler, encoders, feature_names).

    Returns
    -------
    If return_scaler:
        X_scaled : np.ndarray
        y : pd.Series
        scaler : StandardScaler
        label_encoders : dict
        feature_names : list of str
    Else:
        X_scaled : np.ndarray
        y : pd.Series
        label_encoders : dict
    """
    df = df.copy()

    # Drop customerID (not a feature)
    if "customerID" in df.columns:
        df.drop(columns=["customerID"], inplace=True)

    # Clean TotalCharges: remove blanks, convert to numeric, take log1p
    df = df[df["TotalCharges"].str.strip() != ""]
    df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
    df.dropna(inplace=True)
    df["TotalCharges"] = np.log1p(df["TotalCharges"])

    # Initialize encoders dict if needed
    if label_encoders is None:
        label_encoders = {}

    # Identify object (categorical) columns except 'variant'
    label_cols = [c for c in df.select_dtypes(include="object").columns if c != "variant"]

    # Fit or transform each categorical column
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
    else:
        return X_scaled, y, label_encoders
