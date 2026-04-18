# System Architecture

## 1. Objective

Deliver a production-style ML service with monitoring, testing, and CI controls.

## 2. Logical Architecture

```text
Client
  |
  v
FastAPI Service (app/main.py)
  |- Request validation (app/schemas.py)
  |- Metrics middleware (app/middleware.py)
  |- Prediction service (app/model.py)
  |    |- Load model artifact: models/svd_model.pkl
  |    |- Emit ML metrics
  |
  v
Prometheus (/metrics scrape)
  |
  v
Grafana dashboards + alert visualization
```

## 3. Runtime Components

- API container
  - Exposes `8000`
  - Serves prediction and metrics endpoint
- Prometheus container
  - Exposes `9090`
  - Scrapes API metrics every configured interval
  - Evaluates alert rules from `prometheus/alerts/*.yml`
- Grafana container
  - Exposes `3000`
  - Uses provisioned Prometheus datasource
  - Loads dashboards from `grafana/dashboards/`

## 4. Data and Control Flow

### 4.1 Prediction Flow

1. Client sends `POST /predict` payload with `user_id` and `movie_id`.
2. FastAPI validates schema.
3. `MovieRatingModel` predicts score.
4. API returns response with rating and latency.

### 4.2 Monitoring Flow

1. Middleware records HTTP metrics.
2. Model layer records ML metrics.
3. Prometheus scrapes `/metrics`.
4. Grafana visualizes time series.
5. Alert rules trigger on thresholds.

## 5. Observability Coverage

HTTP metrics:
- `http_requests_total`
- `http_request_duration_seconds`

ML metrics:
- `ml_predictions_total`
- `ml_prediction_duration_seconds`
- `ml_prediction_value`
- `ml_prediction_errors_total`
- `ml_model_loaded`
- `ml_model_last_reload_timestamp`

## 6. Deployment Topology

Deployment is containerized using `docker-compose.yml` in a single host setup.

- Shared Docker network: `monitoring`
- Persistent volumes:
  - `prometheus_data`
  - `grafana_data`
- Model volume mount:
  - `./models:/app/models`

## 7. Risk and Mitigation

- Risk: model artifact missing or incompatible
  - Mitigation: startup health check + `ml_model_loaded` metric + alert
- Risk: API latency degradation
  - Mitigation: latency histogram + `HighLatency` alert
- Risk: low traffic or prediction failure spikes
  - Mitigation: volume and error-rate alerts
