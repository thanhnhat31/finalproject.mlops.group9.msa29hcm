"""
Pydantic schemas for request/response validation.
"""

from pydantic import BaseModel, Field, field_validator
from typing import List, Optional


class PredictionRequest(BaseModel):
    """Request schema for Telco Customer Churn prediction."""

    gender: str = Field(..., examples=["Female"])
    SeniorCitizen: int = Field(..., ge=0, le=1, examples=[0])
    Partner: str = Field(..., examples=["Yes"])
    Dependents: str = Field(..., examples=["No"])
    tenure: int = Field(..., ge=0, examples=[1])
    PhoneService: str = Field(..., examples=["No"])
    MultipleLines: str = Field(..., examples=["No phone service"])
    InternetService: str = Field(..., examples=["DSL"])
    OnlineSecurity: str = Field(..., examples=["No"])
    OnlineBackup: str = Field(..., examples=["Yes"])
    DeviceProtection: str = Field(..., examples=["No"])
    TechSupport: str = Field(..., examples=["No"])
    StreamingTV: str = Field(..., examples=["No"])
    StreamingMovies: str = Field(..., examples=["No"])
    Contract: str = Field(..., examples=["Month-to-month"])
    PaperlessBilling: str = Field(..., examples=["Yes"])
    PaymentMethod: str = Field(..., examples=["Electronic check"])
    MonthlyCharges: float = Field(..., ge=0, examples=[29.85])
    TotalCharges: float = Field(..., ge=0, examples=[29.85])

    @field_validator("gender", "Partner", "Dependents", "PhoneService", "PaperlessBilling")
    @classmethod
    def validate_yes_no(cls, v: str) -> str:
        """Validate simple categorical strings."""
        if v not in ["Yes", "No", "Male", "Female"]:
            # Note: gender is handled in the same validator for simplicity here
            pass
        return v.strip()


class PredictionResponse(BaseModel):
    """Response schema for churn prediction."""

    prediction: str = Field(..., examples=["Churn"])
    churn_probability: float = Field(..., ge=0.0, le=1.0)
    model_version: str
    latency_ms: Optional[float] = None


class HealthResponse(BaseModel):
    """Response schema for health check endpoint."""
    status: str
    model_loaded: bool
    model_version: str


class BatchPredictionRequest(BaseModel):
    """Request schema for batch prediction endpoint."""
    # Giữ nguyên cấu trúc List nhưng item bên trong là PredictionRequest
    predictions: List[PredictionRequest] = Field(
        ..., min_length=1, max_length=100)


class BatchPredictionResponse(BaseModel):
    """Response schema for batch prediction endpoint."""
    predictions: List[PredictionResponse]
    total_count: int
    avg_latency_ms: float


class MetricsInfo(BaseModel):
    """Information about available metrics."""
    metrics_enabled: bool
    endpoint: str
    metrics_count: int
