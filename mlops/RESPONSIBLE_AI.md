# Responsible AI Plan

## 1. Scope

This document defines Responsible AI controls for the prediction service.

Goals:
- Reduce unfair model behavior across user groups
- Improve model transparency and explanation quality
- Protect user privacy and data integrity
- Document ethical risks and mitigation strategy

## 2. Fairness Strategy

### 2.1 Fairness Risks

Potential risk examples:
- Model quality differs by demographic segment
- Error rates are higher for minority groups
- Recommendation quality drifts over time for specific cohorts

### 2.2 Fairness Evaluation Framework

Evaluate metrics by protected or sensitive groups when data is available:
- Group-wise precision/recall/F1 (classification context)
- Group-wise MAE/RMSE (rating/regression context)
- Error gap between best and worst group

Fairness acceptance checks:
- Absolute group metric gap under agreed threshold
- No group with severe underperformance relative to global baseline

### 2.3 Fairness Mitigation Options

- Rebalance training data for underrepresented groups
- Add bias-aware thresholding or calibration
- Introduce post-processing constraints for high-risk outputs
- Retrain with updated features that reduce proxy bias

## 3. Explainability Strategy

### 3.1 Objectives

- Provide clear reasons for model output behavior
- Enable debugging when prediction quality degrades
- Support stakeholder review and audit

### 3.2 Techniques

- Global explainability: feature importance trend analysis
- Local explainability: per-prediction explanation using SHAP/LIME equivalent methods
- Drift context: compare explanation distribution over time windows

### 3.3 Explainability Operationalization

- Save explanation artifacts during evaluation cycles
- Track explanation drift in model review reports
- Include explainability checks in release checklist

## 4. Privacy and Data Governance

### 4.1 Data Handling Principles

- Minimize data fields collected by the API
- Avoid storing direct personal identifiers in logs
- Mask or hash user identifiers when persistence is required

### 4.2 Security Controls

- Restrict access to model artifacts and monitoring endpoints
- Rotate secrets and credentials regularly
- Use role-based access for Grafana and operational tools

### 4.3 Retention and Access

- Define retention window for logs and metrics
- Limit dataset access to project members by responsibility
- Record data access changes for auditability

## 5. Ethical Risk Register

| Risk | Impact | Likelihood | Mitigation |
| --- | --- | --- | --- |
| Bias against minority cohorts | High | Medium | Group-level evaluation + rebalancing + threshold review |
| Opaque model behavior | Medium | Medium | Explainability reporting in each release cycle |
| Leakage of sensitive IDs | High | Low | ID masking, secure storage, least privilege |
| Monitoring blind spots | Medium | Medium | Alert coverage for errors, latency, model status |

## 6. Monitoring Hooks for Responsible AI

Operational metrics already integrated:
- `ml_prediction_errors_total`
- `ml_prediction_value`
- `ml_model_loaded`
- prediction latency and request-level behavior

Recommended extensions:
- fairness metrics by group label
- explanation quality or drift indicators
- data quality counters (missingness, schema drift)

## 7. Release Checklist (Responsible AI)

Before promoting to `main`:
1. Fairness checks reviewed and approved
2. Explainability artifacts generated for sampled predictions
3. Privacy review completed for logging and data access
4. Ethical risk table reviewed and updated
5. Monitoring and alerts verified in staging

## 8. Ownership

Responsible AI owner for this project phase: Nguyen Van Nhat
