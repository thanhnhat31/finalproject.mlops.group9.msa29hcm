"""
Script to train and save the Customer Churn Prediction model.

Usage:
    python scripts/train_model.py
"""

from preprocess import load_data, clean_raw_data, get_preprocessor, encode_target
import os
import sys
import joblib
from datetime import datetime
import pandas as pd
from imblearn.over_sampling import SMOTE
from imblearn.pipeline import Pipeline as ImbPipeline
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix

# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
current_dir = os.path.dirname(os.path.abspath(__file__))

root_dir = os.path.abspath(os.path.join(current_dir, ".."))

if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

try:
    from app.config import DATA_PATH, MODEL_PATH
    from preprocess import load_data, clean_raw_data, get_preprocessor, encode_target
except ImportError as e:
    print(f"Error: {e}")
    print(f"Đường dẫn Python đang tìm: {sys.path[0]}")
    sys.exit(1)


def run_training_pipeline():
    """
    Execute the complete training workflow for Customer Churn.
    """

    # --- 1. Data Ingestion ---
    print(f"Loading data from: {DATA_PATH}")
    raw_df = load_data(DATA_PATH)

    if raw_df is None:
        print("Stopping training: Data could not be loaded.")
        return

    # --- 2. Data Cleaning & Label Encoding ---
    df = clean_raw_data(raw_df)
    X = df.drop('Churn', axis=1)
    y = encode_target(df)

    # Split data: 80% Train, 20% Test
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # --- 3. Build Integrated ML Pipeline ---
    # Using ImbPipeline
    model_pipeline = ImbPipeline(steps=[
        ('preprocessor', get_preprocessor()),
        ('smote', SMOTE(random_state=42)),
        ('classifier', LogisticRegression(
            C=0.1,
            max_iter=1000,
            random_state=42
        ))
    ])

    # --- 4. Model Training ---
    print("\nTraining the integrated pipeline...")
    model_pipeline.fit(X_train, y_train)
    print("Model training completed!")

    # --- 5. Evaluation ---
    y_pred = model_pipeline.predict(X_test)

    print("\n" + "="*30)
    print("MODEL PERFORMANCE REPORT")
    print("="*30)
    print(classification_report(y_test, y_pred))

    # --- 6. Model Export ---
    # Tạo thư mục models nếu chưa có
    model_dir = os.path.dirname(MODEL_PATH)
    if not os.path.exists(model_dir):
        os.makedirs(model_dir)

    # override file churn_pipeline_v1.pkl
    joblib.dump(model_pipeline, MODEL_PATH)

    print(f"\nSUCCESS: Full pipeline saved at {MODEL_PATH}")


if __name__ == "__main__":
    run_training_pipeline()
