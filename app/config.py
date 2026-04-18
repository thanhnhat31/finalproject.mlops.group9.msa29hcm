

import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# ========================
# MODEL SETTINGS
# ========================

MODEL_DIR = BASE_DIR / "models"

MODEL_PATH = os.getenv("MODEL_PATH", str(MODEL_DIR / "svd_model.pkl"))

MODEL_VERSION = os.getenv("MODEL_VERSION", "1.0.0")

# ========================
# DATA SETTINGS
# ========================

DATA_PATH = str(BASE_DIR / "data" / "Telco-Customer-Churn.csv")

# ========================
# API SETTINGS
# ========================

API_TITLE = "Customer Churn Prediction API"
API_DESCRIPTION = "API for predicting customer churn with ML Pipeline and monitoring"
API_VERSION = "1.0.0"

# ========================
# SERVER SETTINGS
# ========================

HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 8000))
DEBUG = os.getenv("DEBUG", "false").lower() == "true"


DEFAULT_THRESHOLD = 0.5
# ========================
# MONITORING SETTINGS
# ========================

METRICS_ENABLED = os.getenv("METRICS_ENABLED", "true").lower() == "true"
