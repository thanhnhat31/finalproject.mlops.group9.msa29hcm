# AI in Production - Final project - Group 9

## Overview

This repository contains the Final Project for the **AI in Production** course (Group 9). The project implements an end-to-end Machine Learning system designed to predict user churn in real-time. It follows modern MLOps best practices by separating development (offline) from production (online) environments while ensuring high system reliability through a dedicated observability stack.

### Key Features:
*   **Real-time Prediction:** A FastAPI-based inference engine that provides instant churn probabilities for active users.
*   **Offline Development Pipeline:** Automated scripts for data preprocessing and model training to ensure reproducible results.
*   **Full Observability Stack:** Integrated **Prometheus** and **Grafana** for monitoring both system health (latency, throughput) and ML-specific performance (prediction distribution, model drift).
*   **Production Ready:** Deployment-ready configuration using **Docker Compose** for seamless orchestration of the API and monitoring services.
*   **CI/CD:** Automated testing and deployment pipeline using GitHub Actions.
*   **Responsible AI:** Implementation of fairness and bias detection mechanisms.

## Project Structure

```
finalproject.mlops.group9.msa29hcm/
├── app/
│   ├── __init__.py
│   ├── main.py             # FastAPI application with metrics
│   ├── model.py            # ML model with instrumentation
│   ├── schemas.py          # Pydantic schemas
│   ├── config.py           # Configuration
│   ├── metrics.py          # Prometheus metrics
│   └── middleware.py       # Metrics middleware
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
# Clone source code
git clone https://github.com/your-username/finalproject.mlops.group9.msa29hcm.git
cd finalproject.mlops.group9.msa29hcm

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt
```

### 2. Train Model (if not exists)

```bash
python scripts/train_model.py
```

### 3. Run the API

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 4. Test the API

```bash
# Health check
curl http://localhost:8000/health

# Predict
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{"user_id": "196", "movie_id": "242"}'
```

### 5. Run with Docker

```bash
docker-compose up -d
```

### 6. API Endpoints

| Service    | Method | URL                           | Credentials |
| ---------- | ------ | ----------------------------- | ----------- |
| API        | POST   | http://localhost:8000/predict | -           |
| Health     | GET    | http://localhost:8000/health  | -           |
| API Docs   | GET    | http://localhost:8000/docs    | -           |
| Metrics    | GET    | http://localhost:8000/metrics | -           |
| Prometheus | GET    | http://localhost:9090         | -           |
| Grafana    | GET    | http://localhost:3000         | admin/admin |

