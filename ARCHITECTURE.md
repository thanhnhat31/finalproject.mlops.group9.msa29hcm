# AI in Production - Final project - Group 9

## I. System Architecture

### 1.1. System Overview

#### 1.1.1. Internal Components
The system is designed as a monolithic Machine Learning Application consisting of an offline training pipeline, a real-time online serving API, and an observability stack.

*   **Offline Training Pipeline (Local Scripts):** Reads `Raw Data`, processes features (`Data Processing`), and trains the model (`Model Training`) using `train_model.py`.
*   **Model Registry (Local Storage):** The trained model is saved as a `.pkl` file to a local volume (`./models`).
*   **Online Serving (FastAPI Container):** 
    *   **API Endpoints (`main.py`):** Exposes REST API endpoints to receive real-time prediction requests.
    *   **Inference Engine (`model.py`):** Loads the model into RAM on startup and generates predictions when triggered.
    *   **Instrumentation (`metrics.py` & middleware):** Intercepts API requests to record API metrics and captures ML metrics from the inference engine.
*   **Observability Stack (Docker Containers):** 
    *   **Prometheus:** Scrapes metrics from the FastAPI application via the `/metrics` endpoint.
    *   **Grafana:** Acts as a dashboard for metric visualization utilizing Prometheus as its data source.

#### 1.1.2. External Actors
*   **User:**
    *   Accesses the **API Endpoint** (e.g., via `POST /predict`) to query predictions.
    *   Accesses the **Grafana Dashboard** to administrate and monitor system health and metrics.
  
### 1.2. System Architecture

![System Architecture](./document/architecture.svg)



## Data Flow


## Tech Decisions & Trade-offs

