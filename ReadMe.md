# Customer Churn Orchestration

Event-driven churn prediction system using FastAPI, scikit-learn, and n8n orchestration workflows.

---

## Overview

This project demonstrates a production-oriented churn prediction workflow that combines:

- A machine learning inference API built with FastAPI
- A trained scikit-learn churn prediction pipeline
- Event-driven workflow orchestration using n8n
- Human-in-the-loop customer retention review flows
- Google Sheets or external form ingestion
- LLM-powered intervention drafting (optional)

The goal is not to build a “toy AI demo,” but a realistic architecture where:

- ML handles prediction
- n8n handles orchestration
- Humans remain in control of customer communication

---

## Architecture

```
Customer Feedback Form / CRM / Survey Tool
                ↓
        Google Sheet / Webhook
                ↓
               n8n
                ↓
      FastAPI Churn API (/predict)
                ↓
     Churn Probability + Risk Band
                ↓
        LLM Enrichment (Optional)
                ↓
    Review Queue / Google Sheet
                ↓
      Human Review & Approval
                ↓
        Customer Retention Action
```

## Tech Stack

### Backend / ML
- Python
- FastAPI
- scikit-learn
- pandas
- joblib

### Workflow Automation
- n8n

### Data Source
- Google Sheets
- Kaggle Telco Customer Churn Dataset

### Optional AI Layer
- OpenAI API

---

## Project Structure

```
customer-churn-orchestration/
├── api/
│   ├── main.py
│   ├── config.py
│   ├── schema.py
│   └── services.py
├── src/
│   ├── __init__.py
│   ├── train.py
│   ├── preprocess.py
│   └── config.py
├── data/
│   └── telco_customer_churn_dataset.xlsx
├── models/
│   └── churn_pipeline.joblib
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Features

### Current Features
- Churn prediction API
- Random Forest classification pipeline
- Feature preprocessing pipeline
- Risk band classification
- Structured JSON responses
- Human review workflow architecture
- Event-driven orchestration design

### Planned Enhancements
- Probability calibration
- Model monitoring
- Explainability / SHAP integration
- CRM integrations
- Database persistence
- Docker deployment
- Authentication & API keys
- Retry-safe orchestration workflows

---

## ML Pipeline

The churn model is trained using a scikit-learn Pipeline containing:

- `ColumnTransformer`
- `StandardScaler`
- `OneHotEncoder`
- `RandomForestClassifier`

The serialized pipeline is saved as: `models/churn_pipeline.joblib`

This ensures:
- training-time preprocessing
- inference-time preprocessing
- feature consistency

remain aligned.

---

## Getting Started

### 1. Create Virtual Environment

```bash
python -m venv venv
```

**Activate:**

- **Windows:**
  ```
  venv\Scripts\activate
  ```
- **macOS/Linux:**
  ```bash
  source venv/bin/activate
  ```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Add Dataset

Place the dataset inside:

```
data/telco_customer_churn_dataset.xlsx
```

### 4. Train Model

Run from project root:

```bash
python -m src.train
```

**Expected output:**
- Classification metrics
- ROC AUC score
- Generated model artifact

---

## Running the FastAPI Service

Start the API:

```bash
uvicorn api.main:app --reload
```

---

## API Endpoints

### Health Check

**GET** `/health`

**Response:**
```json
{
  "status": "ok"
}
```

### Predict Churn

**POST** `/predict`

**Request:**
```json
{
  "customer_id": "C001",
  "features": {
    "tenure": 2,
    "monthly_charges": 85,
    "total_charges": 170,
    "contract": "Month-to-month",
    "payment_method": "Electronic check",
    "internet_service": "Fiber optic"
  }
}
```

**Response:**
```json
{
  "customer_id": "C001",
  "churn_probability": 0.99,
  "risk_band": "High Risk",
  "confidence": 0.98,
  "reason_codes": [],
  "model_version": "rf_v1.0",
  "scored_at": "2026-05-18T12:33:22.758972"
}
```

---

## Design Philosophy

This project intentionally separates responsibilities.

### ML API

**Responsible for:**
- Prediction
- Risk scoring
- Inference

**NOT responsible for:**
- Workflow orchestration
- Polling data sources
- Email sending
- Review management

### n8n

**Responsible for:**
- Workflow orchestration
- Google Sheets integration
- Retries
- Event triggers
- LLM enrichment
- Review queues
- Notifications

This separation keeps the system:
- **Maintainable**
- **Scalable**
- **Deployment-friendly**

---

## Why Not Build Everything Inside n8n?

n8n is an orchestration engine, not a data science platform.

Running full ML logic directly inside workflows introduces:
- Poor scalability
- Brittle logic
- Difficult debugging
- Inefficient processing

**Instead:**
- ML runs as a dedicated service
- n8n orchestrates events around it

---

## Example Real-World Workflow

1. Customer submits feedback form
2. Google Sheet updates
3. n8n detects new row
4. n8n calls `/predict`
5. API returns churn probability
6. n8n enriches output with LLM-generated draft response
7. Results are written to a review queue
8. Support staff manually review before customer outreach

---

## Deployment Recommendations

**Suggested deployment platforms:**
- Railway
- Render
- Fly.io

---

## Important Engineering Notes

**This project prioritizes:**
- Separation of concerns
- Deterministic API contracts
- Human review loops
- Event-driven architecture

**This project intentionally avoids:**
- Auto-emailing customers blindly
- Embedding ML directly into n8n
- Coupling orchestration with inference
- Over-engineered dashboards too early

---

## Future Directions

**Potential extensions:**
- Drift monitoring
- Batch scoring
- Feature stores
- Model registry integration
- Kafka/event streaming
- Customer segmentation
- Real-time CRM integrations
- A/B-tested retention interventions

---
Disclaimer

This project is intended as an educational and architectural demonstration of production-oriented ML orchestration patterns.

It is **not** financial, legal, or customer-retention advice.