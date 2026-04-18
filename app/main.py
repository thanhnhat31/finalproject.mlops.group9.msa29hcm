"""
FastAPI application for Customer Churn Prediction with Prometheus Monitoring.

This application exposes:
- /predict - Make churn predictions
- /health - Health check
- /metrics - Prometheus metrics endpoint
"""

from fastapi import FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
import logging

from app.config import (
    API_TITLE,
    API_DESCRIPTION,
    API_VERSION,
    MODEL_VERSION,
    METRICS_ENABLED,
)
from app.model import CustomerChurnModel
from app.schemas import (
    PredictionRequest,
    PredictionResponse,
    HealthResponse,
    MetricsInfo,
)
from app.middleware import MetricsMiddleware
from app.metrics import count_implemented_metrics

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title=API_TITLE,
    description=API_DESCRIPTION,
    version=API_VERSION,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add metrics middleware
if METRICS_ENABLED:
    app.add_middleware(MetricsMiddleware)

# Global model instance
model: CustomerChurnModel = None


@app.on_event("startup")
async def startup_event():
    """Load model when application starts."""
    global model
    try:
        model = CustomerChurnModel()
        logger.info("Churn Model loaded successfully at startup")
    except Exception as e:
        logger.error(f"Failed to load model: {e}")


# =============================================================================
# Info Endpoints
# =============================================================================

@app.get("/", tags=["Info"])
async def root():
    """Root endpoint with API information."""
    implemented, total = count_implemented_metrics()
    return {
        "name": API_TITLE,
        "version": API_VERSION,
        "description": API_DESCRIPTION,
        "docs": "/docs",
        "health": "/health",
        "metrics": "/metrics",
        "metrics_implemented": f"{implemented}/{total}",
    }


@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """
    Health check endpoint.
    Returns the health status of the API and whether the model is loaded.
    """
    return HealthResponse(
        status="healthy" if model and model.is_loaded() else "unhealthy",
        model_loaded=model is not None and model.is_loaded(),
        model_version=MODEL_VERSION
    )


# =============================================================================
# Metrics Endpoint
# =============================================================================

@app.get("/metrics", tags=["Monitoring"])
async def metrics():
    """
    Prometheus metrics endpoint.
    Returns all collected metrics in Prometheus text format.
    """
    if not METRICS_ENABLED:
        raise HTTPException(status_code=503, detail="Metrics disabled")
    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST
    )


@app.get("/metrics/info", response_model=MetricsInfo, tags=["Monitoring"])
async def metrics_info():
    """Get information about metrics configuration."""
    implemented, total = count_implemented_metrics()
    return MetricsInfo(
        metrics_enabled=METRICS_ENABLED,
        endpoint="/metrics",
        metrics_count=implemented
    )


# =============================================================================
# Prediction Endpoints
# =============================================================================

@app.post("/predict", response_model=PredictionResponse, tags=["Prediction"])
async def predict(request: PredictionRequest):
    """
    Predict customer churn.

    Args:
        request: PredictionRequest with customer features

    Returns:
        PredictionResponse with churn probability and status
    """
    if model is None or not model.is_loaded():
        raise HTTPException(status_code=503, detail="Model not loaded")

    try:
        # Thực hiện dự đoán từ dữ liệu đầu vào (request.dict() hoặc request.model_dump())
        prediction_results = model.predict(request)

        return PredictionResponse(
            churn_probability=prediction_results["probability"],
            prediction="Churn" if prediction_results["prediction"] == 1 else "No Churn",
            model_version=MODEL_VERSION,
            latency_ms=round(prediction_results["latency_ms"], 3)
        )
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# =============================================================================
# Model Info Endpoint
# =============================================================================

@app.get("/model/info", tags=["Info"])
async def model_info():
    """Get information about the loaded model."""
    if model is None:
        return {
            "model_version": MODEL_VERSION,
            "model_type": "Classification (Churn Prediction)",
            "is_loaded": False,
        }
    return model.get_info()


# =============================================================================
# Main entry point
# =============================================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
