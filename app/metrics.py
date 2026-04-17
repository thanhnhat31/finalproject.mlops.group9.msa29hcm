"""
Prometheus metrics definitions for the Telco Customer Churn Prediction API.
"""

from prometheus_client import Counter, Histogram, Gauge, Info

# =============================================================================
# Application Metrics (HTTP Requests)
# =============================================================================

# Track total HTTP requests
REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total number of HTTP requests',
    ['method', 'endpoint', 'status']
)

# Track request duration in seconds
REQUEST_LATENCY = Histogram(
    'http_request_duration_seconds',
    'HTTP request latency in seconds',
    ['method', 'endpoint'],
    buckets=[0.01, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0]
)

# =============================================================================
# ML-Specific Metrics
# =============================================================================

# Track total predictions made
PREDICTION_COUNT = Counter(
    'ml_predictions_total',
    'Total number of predictions made',
    ['model_version']
)

# Track prediction latency (usually very fast)
PREDICTION_LATENCY = Histogram(
    'ml_prediction_duration_seconds',
    'Time to generate a prediction',
    ['model_version'],
    buckets=[0.001, 0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5]
)

# (Rate: 0 -> 1)

PREDICTION_VALUE = Histogram(
    'ml_prediction_probability',
    'Distribution of churn probability predictions',
    ['model_version'],
    buckets=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
)

# Track errors during prediction
PREDICTION_ERRORS = Counter(
    'ml_prediction_errors_total',
    'Total number of prediction errors',
    ['error_type', 'model_version']
)

# =============================================================================
# Model Status Metrics
# =============================================================================

# Indicator if the model is loaded (1) or not (0)
MODEL_LOADED = Gauge(
    'ml_model_loaded',
    'Whether the ML model is loaded (1) or not (0)'
)

# Static information about the model
MODEL_INFO = Info(
    'ml_model',
    'Information about the loaded ML model'
)

# Last load timestamp
MODEL_LAST_RELOAD = Gauge(
    'ml_model_last_reload_timestamp',
    'Unix timestamp of last model reload'
)

# =============================================================================
# Batch Prediction Metrics
# =============================================================================

BATCH_SIZE = Histogram(
    'ml_batch_prediction_size',
    'Size of batch prediction requests',
    buckets=[1, 5, 10, 25, 50, 100]
)

# =============================================================================
# Helper Functions
# =============================================================================


def get_all_metrics():
    """Return a dictionary of all defined metrics for inspection."""
    return {
        'request_count': REQUEST_COUNT,
        'request_latency': REQUEST_LATENCY,
        'prediction_count': PREDICTION_COUNT,
        'prediction_latency': PREDICTION_LATENCY,
        'prediction_value': PREDICTION_VALUE,
        'prediction_errors': PREDICTION_ERRORS,
        'model_loaded': MODEL_LOADED,
        'model_info': MODEL_INFO,
        'model_last_reload': MODEL_LAST_RELOAD,
        'batch_size': BATCH_SIZE,
    }


def count_implemented_metrics():
    """Count how many metrics have been implemented."""
    metrics = get_all_metrics()
    implemented = sum(1 for m in metrics.values() if m is not None)
    return implemented, len(metrics)
