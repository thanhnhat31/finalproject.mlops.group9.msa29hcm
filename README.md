<<<<<<< HEAD
# AI in Production - Final project - Group 9


## Overview

=======
# Lab 4: Monitoring & Production Deployment

## Overview

Implement comprehensive monitoring and observability for the movie rating prediction system using Prometheus for metrics collection and Grafana for visualization.
>>>>>>> 5201525 (feat: Finish model churn & monitoring in dev branch)

## Project Structure

```
<<<<<<< HEAD
finalproject.mlops.group9.msa29hcm/
=======
ddm501-lab4-starter/
>>>>>>> 5201525 (feat: Finish model churn & monitoring in dev branch)
├── app/
│   ├── __init__.py
│   ├── main.py             # FastAPI application with metrics
│   ├── model.py            # ML model with instrumentation
│   ├── schemas.py          # Pydantic schemas
│   ├── config.py           # Configuration
<<<<<<< HEAD
│   ├── metrics.py          # Prometheus metrics
│   └── middleware.py       # Metrics middleware
├── prometheus/
│   ├── prometheus.yml      # Prometheus config
│   └── alerts/
│       ├── api_alerts.yml  # API alerting rules
│       └── ml_alerts.yml   # ML alerting rules
=======
│   ├── metrics.py          # Prometheus metrics (TODO)
│   └── middleware.py       # Metrics middleware (TODO)
├── prometheus/
│   ├── prometheus.yml      # Prometheus config (TODO)
│   └── alerts/
│       ├── api_alerts.yml  # API alerting rules (TODO)
│       └── ml_alerts.yml   # ML alerting rules (TODO)
>>>>>>> 5201525 (feat: Finish model churn & monitoring in dev branch)
├── grafana/
│   ├── provisioning/
│   │   ├── datasources/
│   │   │   └── prometheus.yml  # Data source config
│   │   └── dashboards/
│   │       └── dashboards.yml  # Dashboard provisioning
│   └── dashboards/
<<<<<<< HEAD
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
=======
│       ├── system_dashboard.json   # System metrics (TODO)
│       └── ml_dashboard.json       # ML metrics (TODO)
├── scripts/
│   ├── train_model.py      # Model training
│   └── load_test.py        # Load testing script (TODO)
├── tests/
│   └── test_metrics.py     # Metrics tests
├── models/                 # Saved models
├── docker-compose.yml      # Full stack deployment (TODO)
├── Dockerfile
├── requirements.txt
└── README.md
>>>>>>> 5201525 (feat: Finish model churn & monitoring in dev branch)
```

## Quick Start

### 1. Clone and Setup

```bash
<<<<<<< HEAD
# Clone source code
git clone https://github.com/your-username/finalproject.mlops.group9.msa29hcm.git
cd finalproject.mlops.group9.msa29hcm
=======
unzip ddm501-lab4-starter.zip
cd ddm501-lab4-starter
>>>>>>> 5201525 (feat: Finish model churn & monitoring in dev branch)

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt
<<<<<<< HEAD

=======
>>>>>>> 5201525 (feat: Finish model churn & monitoring in dev branch)
```

### 2. Train Model (if not exists)

```bash
python scripts/train_model.py
```

<<<<<<< HEAD
### 3. Run the API
=======
### 3. Run API Locally
>>>>>>> 5201525 (feat: Finish model churn & monitoring in dev branch)

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

<<<<<<< HEAD
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
=======
### 4. Start Full Monitoring Stack
>>>>>>> 5201525 (feat: Finish model churn & monitoring in dev branch)

```bash
docker-compose up -d
```

<<<<<<< HEAD
### 6. API Endpoints

| Service    | Method | URL                           | Credentials |
| ---------- | ------ | ----------------------------- | ----------- |
| API        | POST   | http://localhost:8000/predict | -           |
| Health     | GET    | http://localhost:8000/health  | -           |
| API Docs   | GET    | http://localhost:8000/docs    | -           |
| Metrics    | GET    | http://localhost:8000/metrics | -           |
| Prometheus | GET    | http://localhost:9090         | -           |
| Grafana    | GET    | http://localhost:3000         | admin/admin |





=======
### 5. Access Services

| Service | URL | Credentials |
|---------|-----|-------------|
| API | http://localhost:8000 | - |
| API Docs | http://localhost:8000/docs | - |
| Metrics | http://localhost:8000/metrics | - |
| Prometheus | http://localhost:9090 | - |
| Grafana | http://localhost:3000 | admin/admin |

## TODO Tasks

Complete the following files:

### Metrics Implementation
- [ ] `app/metrics.py` - Define Prometheus metrics
- [ ] `app/middleware.py` - Implement metrics middleware
- [ ] Update `app/model.py` - Add ML metrics instrumentation

### Prometheus Configuration
- [ ] `prometheus/prometheus.yml` - Configure scrape targets
- [ ] `prometheus/alerts/api_alerts.yml` - API alerting rules
- [ ] `prometheus/alerts/ml_alerts.yml` - ML-specific alerts

### Grafana Dashboards
- [ ] `grafana/dashboards/system_dashboard.json` - System metrics dashboard
- [ ] `grafana/dashboards/ml_dashboard.json` - ML metrics dashboard

### Infrastructure
- [ ] `docker-compose.yml` - Add Prometheus and Grafana services
- [ ] `scripts/load_test.py` - Implement load testing

## Metrics to Implement

### Application Metrics
| Metric | Type | Description |
|--------|------|-------------|
| `http_requests_total` | Counter | Total HTTP requests |
| `http_request_duration_seconds` | Histogram | Request latency |

### ML Metrics
| Metric | Type | Description |
|--------|------|-------------|
| `ml_predictions_total` | Counter | Total predictions |
| `ml_prediction_duration_seconds` | Histogram | Prediction latency |
| `ml_prediction_value` | Histogram | Prediction distribution |
| `ml_model_loaded` | Gauge | Model status |
| `ml_prediction_errors_total` | Counter | Prediction errors |

## Alert Rules to Implement

| Alert | Condition | Severity |
|-------|-----------|----------|
| HighErrorRate | Error rate > 10% | Critical |
| HighLatency | P95 latency > 1s | Warning |
| ModelNotLoaded | Model status = 0 | Critical |
| PredictionLatencyHigh | P95 > 100ms | Warning |
| LowPredictionVolume | Rate < 0.1/s | Warning |

## Useful PromQL Queries

```promql
# Request rate
rate(http_requests_total[5m])

# Error rate percentage
rate(http_requests_total{status=~"5.."}[5m]) / rate(http_requests_total[5m]) * 100

# P95 latency
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))

# Prediction rate
rate(ml_predictions_total[5m])

# Average prediction value
histogram_quantile(0.5, rate(ml_prediction_value_bucket[5m]))
```

## Grading Rubric

| Criteria | Weight |
|----------|--------|
| Application Metrics | 25% |
| Monitoring Stack | 25% |
| Dashboards & Alerts | 30% |
| Documentation | 20% |

## Submission

1. Complete all TODO items
2. Take screenshots of Grafana dashboards with data
3. Run load test and capture metrics
4. Push to GitHub
5. Submit repository link
>>>>>>> 5201525 (feat: Finish model churn & monitoring in dev branch)
