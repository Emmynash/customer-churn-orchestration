import joblib
import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_DIR = os.path.join(BASE_DIR, "models")

model = joblib.load(os.path.join(MODEL_DIR, "rf_v1.0_20260503_182152.joblib"))

sample = pd.DataFrame([{
    "tenure": 2,
    "monthly_charges": 85,
    "total_charges": 170,
    "contract": "Month-to-month",
    "payment_method": "Electronic check",
    "internet_service": "Fiber optic"
}])

print(model.predict_proba(sample))