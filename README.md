# AI Revenue Leakage Detection System

An AI-powered system to detect and analyze revenue leakage in healthcare billing data.  
The system identifies underpayments, unpaid claims, and anomalies using machine learning and provides insights through a dashboard.

## Features
- Upload healthcare datasets (EHR, billing, claims)
- Detect revenue leakage automatically
- Identify underpayment and unpaid claims
- Machine Learning based anomaly detection
- LLM-based explanation for detected issues
- Interactive dashboard for analysis

## Tech Stack
- Python
- FastAPI (Backend API)
- Machine Learning (Scikit-learn)
- LLM Integration
- Streamlit Dashboard
- Pandas & Data Processing

## Project Structure


backend/
app.py

ml_model/
leakage_detector.py
predictor.py
llm_explainer.py

data/
ehr.csv
billing.csv
claims.csv

dashboard.py
requirements.txt


## How to Run

### 1 Install dependencies

pip install -r requirements.txt


### 2 Run backend API

uvicorn backend.app:app --reload


### 3 Run dashboard

streamlit run dashboard.py


## Dashboard
The dashboard provides:

- Leakage detection results
- Billed vs Paid analysis
- Provider-level leakage insights
- KPI metrics

## Future Improvements
- Advanced anomaly detection
- Real-time hospital billing monitoring
- Predictive revenue risk alerts

## Author
Haniiska
