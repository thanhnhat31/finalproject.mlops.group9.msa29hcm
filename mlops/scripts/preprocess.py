import pandas as pd
import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import RobustScaler, OneHotEncoder


def load_data(filepath, index_col=None):
    if not filepath or not isinstance(filepath, str):
        return None
    try:
        df = pd.read_csv(
            filepath, index_col=index_col) if index_col else pd.read_csv(filepath)
        return df
    except Exception as e:
        print(f"Error loading data: {e}")
        return None


def clean_raw_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    # Convert and handle missing values for TotalCharges
    df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
    df['TotalCharges'] = df['TotalCharges'].fillna(0)  # make sure data not NaN

    if 'customerID' in df.columns:
        df = df.drop('customerID', axis=1)
    return df


def get_preprocessor() -> ColumnTransformer:
    num_features = ['tenure', 'MonthlyCharges', 'TotalCharges']

    # Collect all the classification columns into a list
    cat_features = [
        'InternetService', 'Contract', 'PaymentMethod', 'MultipleLines',
        'OnlineSecurity', 'OnlineBackup', 'DeviceProtection',
        'TechSupport', 'StreamingTV', 'StreamingMovies',
        'gender', 'SeniorCitizen', 'Partner',
        'Dependents', 'PhoneService', 'PaperlessBilling'
    ]

    num_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', RobustScaler())
    ])

    cat_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
        ('onehot', OneHotEncoder(handle_unknown='ignore', drop='first'))
    ])

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', num_transformer, num_features),
            ('cat', cat_transformer, cat_features)
        ]
    )
    return preprocessor


def encode_target(df: pd.DataFrame):
    if 'Churn' in df.columns:
        return df['Churn'].map({'Yes': 1, 'No': 0})
    return None


def preprocess_full(df: pd.DataFrame, is_training: bool = True):
    df_cleaned = clean_raw_data(df)
    if is_training:
        X = df_cleaned.drop(
            'Churn', axis=1) if 'Churn' in df_cleaned.columns else df_cleaned
        y = encode_target(df_cleaned)
        return X, y
    return df_cleaned
