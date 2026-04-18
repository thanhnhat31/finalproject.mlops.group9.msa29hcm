# AI in Production Final Project - Group 9

This repository contains the Final Project for the **AI in Production** course (Group 9). The project implements an end-to-end Machine Learning system designed to predict user churn in real-time. It follows modern MLOps best practices by separating development (offline) from production (online) environments while ensuring high system reliability through a dedicated observability stack.

### Key Features:
*   **Real-time Prediction:** A FastAPI-based inference engine that provides instant churn probabilities for active users.
*   **Offline Development Pipeline:** Automated scripts for data preprocessing and model training to ensure reproducible results.
*   **Full Observability Stack:** Integrated **Prometheus** and **Grafana** for monitoring both system health (latency, throughput) and ML-specific performance (prediction distribution, model drift).
*   **Production Ready:** Deployment-ready configuration using **Docker Compose** for seamless orchestration of the API and monitoring services.
*   **CI/CD:** Automated testing and deployment pipeline using GitHub Actions.
*   **Responsible AI:** Implementation of fairness and bias detection mechanisms.

## Project Structure

```text
finalproject.mlops.group9.msa29hcm/
├── app/
│   ├── __init__.py
│   ├── main.py             # FastAPI application with metrics
│   ├── model.py            # ML model with instrumentation
│   ├── schemas.py          # Pydantic schemas
│   ├── config.py           # Configuration
│   ├── metrics.py          # Prometheus metrics
│   └── middleware.py       # Metrics middleware
├── document/               # Save diagrams of systems
├── prometheus/
│   ├── prometheus.yml      # Prometheus config
│   └── alerts/
│       ├── api_alerts.yml  # API alerting rules
│       └── ml_alerts.yml   # ML alerting rules
├── grafana/
│   ├── provisioning/
│   │   ├── datasources/
│   │   │   └── prometheus.yml  # Data source config
│   │   └── dashboards/
│   │       └── dashboards.yml  # Dashboard provisioning
│   └── dashboards/
│       ├── system_dashboard.json   # System metrics
│       └── ml_dashboard.json       # ML metrics
├── scripts/
│   ├── train_model.py      # Model training
│   └── load_test.py        # Load testing script
├── tests/
│   ├── test_api.py         # API tests
│   └── test_metrics.py     # Metrics tests
├── models/                 # Saved models
├── .github/
│   └── workflows/
│       └── CICD.yml          # CI/CD workflow
├── docker-compose.yml      # Full stack deployment
├── Dockerfile
├── requirements.txt
├── README.md
├── ARCHITECTURE.md         # System architecture
└── CONTRIBUTING.md         # Contribution of members
```

## Quick Start

### 1. Clone and Setup

```bash
# Clone repository
git clone https://github.com/thanhnhat31/finalproject.mlops.group9.msa29hcm.git
cd finalproject.mlops.group9.msa29hcm

# Create virtual environment
python -m venv venv
# Activate virtual environment
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

Services:
- API: `http://localhost:8000`
- API docs: `http://localhost:8000/docs`
- Metrics: `http://localhost:8000/metrics`
- Prometheus: `http://localhost:9090`
- Grafana: `http://localhost:3000` (admin/admin)

### 3.3 Verify Model Loaded

```bash
curl http://localhost:8000/health
```

Expected:

```json
{"status":"healthy","model_loaded":true,"model_version":"1.0.0"}
```

### 3.4 Sample Prediction

```bash
curl -X 'POST' \
  'http://localhost:8000/predict' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "gender": "Female",
  "SeniorCitizen": 0,
  "Partner": "Yes",
  "Dependents": "No",
  "tenure": 1,
  "PhoneService": "No",
  "MultipleLines": "No phone service",
  "InternetService": "DSL",
  "OnlineSecurity": "No",
  "OnlineBackup": "Yes",
  "DeviceProtection": "No",
  "TechSupport": "No",
  "StreamingTV": "No",
  "StreamingMovies": "No",
  "Contract": "Month-to-month",
  "PaperlessBilling": "Yes",
  "PaymentMethod": "Electronic check",
  "MonthlyCharges": 29.85,
  "TotalCharges": 29.85
}'
```

## 4. Testing

Run tests in local Python environment:

```bash
python -m pytest tests/ -v --maxfail=1
```

If local Python is 3.13 and dependency issues occur, run tests in CI or use Python 3.10 virtual environment.

## 5. CI Workflow

Workflow file: `.github/workflows/CICD.yml`

Trigger policy:
- Push on `staging` or `main`: run test
- Pull request:
  - `dev -> staging`: run test + build image with `staging` tag
  - `staging -> main`: run test + build image with `main` tag

Image naming base:
- `nhatqkit/finalprojectmlops`

## 6. Documentation Index

- Architecture: `ARCHITECTURE.md`
- Team process and roles: `CONTRIBUTING.md`
- Responsible AI plan: `RESPONSIBLE_AI.md`

## 7. Notes

- `models/svd_model.pkl` is required for healthy prediction service.
- If you see `Model not loaded`, verify model file exists and restart API container:

```bash
docker compose restart api
```
