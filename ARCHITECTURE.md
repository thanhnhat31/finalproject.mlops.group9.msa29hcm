# AI in Production - Final project - Group 9

## System Architecture
The system is designed as a Batch Inference Pipeline to keep complexity low while meeting the daily update requirement.
*   Data Layer: Pulls raw data from the Production Database (PostgreSQL) containing user transactions, logs, and support history.
*   Data Processing Layer: A Python service cleans data and performs feature engineering (e.g., calculating "Average spend in last 3 months").
*   Model Registry (MLflow): Stores the trained model versions and keeps track of hyperparameters used during experiments.
*   Inference Engine: A scheduled job (Cron) that runs every night to generate predictions for all active users.
*   Output Layer: Saves results back to a "Churn Dashboard" for business users and triggers alerts for the marketing team.

## Data Flow
*   Step 1: Ingestion: Fetch user behavior data (Last login, purchase frequency) and profile data (Contract type, tenure).
*   Step 2: Preprocessing: Handle missing values (e.g., users with no recent purchases) and encode categorical variables (e.g., "Contract Type").
*   Step 3: Handling Imbalance: Since most users do not churn, use SMOTE (Synthetic Minority Over-sampling Technique) during training to help the model learn the "Churn" class better.
*   Step 4: Prediction: The model processes the daily features and outputs a list of User IDs with their churn probability.
*   Step 5: Consumption: The Marketing team receives a CSV or Dashboard update with the top 500 highest-risk users.

## Tech Decisions & Trade-offs
