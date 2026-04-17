from app.metrics import (
    PREDICTION_COUNT,
    PREDICTION_LATENCY,
    PREDICTION_VALUE,
    PREDICTION_ERRORS,
    MODEL_LOADED,
    MODEL_LAST_RELOAD,
    MODEL_INFO
)
from app.config import MODEL_PATH, MODEL_VERSION
from typing import Tuple, Dict, Any
import joblib
import pandas as pd
from app.config import MODEL_PATH, MIN_RATING, MAX_RATING, MODEL_VERSION
from typing import List, Tuple, Optional
from pathlib import Path
import time
import logging
import pickle
<< << << < HEAD
"""
ML Model wrapper for movie rating prediction with metrics instrumentation.

TODO: Add metrics instrumentation to the model methods.
"""


== == == =

>>>>>> > 5201525 (feat: Finish model churn & monitoring in dev branch)

logger = logging.getLogger(__name__)


class CustomerChurnModel:
    def __init__(self):
        self.model = None
        self.version = MODEL_VERSION
        self.load_model()

    def load_model(self):
        """Load the scikit-learn pipeline from the .pkl file."""
        try:
            self.model = joblib.load(MODEL_PATH)

            # Update Prometheus metrics
            MODEL_LOADED.set(1)
            MODEL_LAST_RELOAD.set_to_current_time()
            MODEL_INFO.info({
                'version': self.version,
                'type': 'LogisticRegression_Pipeline',
                'path': str(MODEL_PATH)
            })

            logger.info(
                f"Model {self.version} loaded successfully from {MODEL_PATH}")
        except Exception as e:
            MODEL_LOADED.set(0)
            logger.error(f"Failed to load model: {e}")
            self.model = None

    def is_loaded(self) -> bool:
        return self.model is not None

    def predict_with_latency(self, input_data: Dict[str, Any]) -> Tuple[str, float, float]:
        """
        Predict churn and track performance metrics.
        Returns: (Result string, Probability, Latency in ms)
        """
        if not self.is_loaded():
            PREDICTION_ERRORS.labels(
                error_type="model_not_loaded", model_version=self.version).inc()
            raise RuntimeError("Model is not loaded")

        start_time = time.time()
        try:
            # Convert input dictionary to DataFrame for the pipeline
            df = pd.DataFrame([input_data])

            # 1. Predict Class (0 or 1)
            prediction = self.model.predict(df)[0]

            # 2. Predict Probability
            probability = self.model.predict_proba(df)[0][1]

            latency_ms = (time.time() - start_time) * 1000
            result_str = "Churn" if prediction == 1 else "No Churn"

            # --- Update ML Metrics ---
            PREDICTION_COUNT.labels(model_version=self.version).inc()
            PREDICTION_LATENCY.labels(
                model_version=self.version).observe(latency_ms / 1000)
            PREDICTION_VALUE.labels(
                model_version=self.version).observe(probability)

            return result_str, float(probability), latency_ms

        except Exception as e:
            PREDICTION_ERRORS.labels(
                error_type="prediction_error", model_version=self.version).inc()
            logger.error(f"Prediction error: {e}")
            raise e

    def get_info(self) -> Dict[str, Any]:
        return {
            "model_version": self.version,
            "model_type": "Logistic Regression (Standardized Pipeline)",
            "is_loaded": self.is_loaded(),
            "features_count": 19  # Numbers of feature in Telco dataset
        }
