"""
<<<<<<< HEAD
Prometheus metrics definitions for the Movie Rating API.

This module defines all Prometheus metrics used for monitoring the application.

TODO: Complete the metric definitions below.

Metrics Types:
- Counter: Cumulative values that only increase (e.g., total requests)
- Gauge: Values that can go up or down (e.g., current temperature)
- Histogram: Distribution of values in buckets (e.g., request latency)
- Summary: Similar to histogram with quantiles
- Info: Key-value pairs for static information

Run the API and check metrics at: http://localhost:8000/metrics
=======
Prometheus metrics definitions for the Telco Customer Churn Prediction API.
>>>>>>> 5201525 (feat: Finish model churn & monitoring in dev branch)
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

<< << << < HEAD
# TODO 2: Define HTTP request latency histogram
# This histogram should track request duration in seconds with labels for:
# - method: HTTP method
# - endpoint: Request path
# Suggested buckets: [0.01, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0]

# REQUEST_LATENCY = Histogram(
#     'http_request_duration_seconds',
#     'HTTP request latency in seconds',
#     ['method', 'endpoint'],
#     buckets=[0.01, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0]
# )

# Placeholder - replace with your implementation
== == == =
# Track request duration in seconds
>>>>>> > 5201525 (feat: Finish model churn & monitoring in dev branch)
REQUEST_LATENCY = Histogram(
    'http_request_duration_seconds',
    'HTTP request latency in seconds',
    ['method', 'endpoint'],
    buckets=[0.01, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0]
)

<< << << < HEAD

== == == =
>>>>>> > 5201525 (feat: Finish model churn & monitoring in dev branch)
# =============================================================================
# ML-Specific Metrics
# =============================================================================

<< << << < HEAD
# TODO 3: Define prediction counter
# This counter should track total predictions with labels for:
# - model_version: Version of the model used

# PREDICTION_COUNT = Counter(
#     'ml_predictions_total',
#     'Total number of predictions made',
#     ['model_version']
# )

== == == =
# Track total predictions made
>>>>>> > 5201525 (feat: Finish model churn & monitoring in dev branch)
PREDICTION_COUNT = Counter(
    'ml_predictions_total',
    'Total number of predictions made',
    ['model_version']
)

<< << << < HEAD

# TODO 4: Define prediction latency histogram
# This histogram should track prediction duration in seconds
# Suggested buckets for ML predictions (faster than HTTP):
# [0.001, 0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5]

# PREDICTION_LATENCY = Histogram(
#     'ml_prediction_duration_seconds',
#     'Time to generate a prediction',
#     ['model_version'],
#     buckets=[0.001, 0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5]
# )

== == == =
# Track prediction latency (usually very fast)
>>>>>> > 5201525 (feat: Finish model churn & monitoring in dev branch)
PREDICTION_LATENCY = Histogram(
    'ml_prediction_duration_seconds',
    'Time to generate a prediction',
    ['model_version'],
    buckets=[0.001, 0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5]
)

<< << << < HEAD

# TODO 5: Define prediction value histogram
# This histogram should track the distribution of prediction values
# For movie ratings, use buckets: [1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0]

# PREDICTION_VALUE = Histogram(
#     'ml_prediction_value',
#     'Distribution of prediction values',
#     ['model_version'],
#     buckets=[1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0]
# )

PREDICTION_VALUE = Histogram(
    'ml_prediction_value',
    'Distribution of prediction values',
    ['model_version'],
    buckets=[1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0]
)


# TODO 6: Define prediction error counter
# This counter should track prediction errors with labels for:
# - error_type: Type of error (validation_error, model_error, unknown_error)
# - model_version: Version of the model

# PREDICTION_ERRORS = Counter(
#     'ml_prediction_errors_total',
#     'Total number of prediction errors',
#     ['error_type', 'model_version']
# )

== == == =
# (Rate: 0 -> 1)

PREDICTION_VALUE = Histogram(
    'ml_prediction_probability',
    'Distribution of churn probability predictions',
    ['model_version'],
    buckets=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
)

# Track errors during prediction
>>>>>> > 5201525 (feat: Finish model churn & monitoring in dev branch)
PREDICTION_ERRORS = Counter(
    'ml_prediction_errors_total',
    'Total number of prediction errors',
    ['error_type', 'model_version']
)

<< << << < HEAD

== == == =
>>>>>> > 5201525 (feat: Finish model churn & monitoring in dev branch)
# =============================================================================
# Model Status Metrics
# =============================================================================

<< << << < HEAD
# TODO 7: Define model loaded gauge
# This gauge should indicate if the model is loaded (1) or not (0)

# MODEL_LOADED = Gauge(
#     'ml_model_loaded',
#     'Whether the ML model is loaded (1) or not (0)'
# )

== == == =
# Indicator if the model is loaded (1) or not (0)
>>>>>> > 5201525 (feat: Finish model churn & monitoring in dev branch)
MODEL_LOADED = Gauge(
    'ml_model_loaded',
    'Whether the ML model is loaded (1) or not (0)'
)

<< << << < HEAD

# TODO 8: Define model info metric
# This info metric should provide static information about the model:
# - version: Model version
# - type: Model type (SVD, NMF, etc.)
# - path: Path to model file

# MODEL_INFO = Info(
#     'ml_model',
#     'Information about the loaded ML model'
# )

== == == =
# Static information about the model
>>>>>> > 5201525 (feat: Finish model churn & monitoring in dev branch)
MODEL_INFO = Info(
    'ml_model',
    'Information about the loaded ML model'
)

<< << << < HEAD

# TODO 9: Define model last reload timestamp gauge
# This gauge should track when the model was last loaded (Unix timestamp)

# MODEL_LAST_RELOAD = Gauge(
#     'ml_model_last_reload_timestamp',
#     'Unix timestamp of last model reload'
# )

== == == =
# Last load timestamp
>>>>>> > 5201525 (feat: Finish model churn & monitoring in dev branch)
MODEL_LAST_RELOAD = Gauge(
    'ml_model_last_reload_timestamp',
    'Unix timestamp of last model reload'
)

<< << << < HEAD

# =============================================================================
# Batch Prediction Metrics (BONUS)
# =============================================================================

# TODO 10 (BONUS): Define batch size histogram
# Track the size of batch prediction requests

# BATCH_SIZE = Histogram(
#     'ml_batch_prediction_size',
#     'Size of batch prediction requests',
#     buckets=[1, 5, 10, 25, 50, 100]
# )

== == == =
# =============================================================================
# Batch Prediction Metrics
# =============================================================================

>>>>>> > 5201525 (feat: Finish model churn & monitoring in dev branch)
BATCH_SIZE = Histogram(
    'ml_batch_prediction_size',
    'Size of batch prediction requests',
    buckets=[1, 5, 10, 25, 50, 100]
)

<< << << < HEAD

== == == =
>>>>>> > 5201525 (feat: Finish model churn & monitoring in dev branch)
# =============================================================================
# Helper Functions
# =============================================================================

<< << << < HEAD
== == == =

>>>>>> > 5201525 (feat: Finish model churn & monitoring in dev branch)


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
