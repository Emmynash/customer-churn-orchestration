import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_DIR = os.path.join(BASE_DIR, "models")

FEATURES = [
    "tenure",
    "monthly_charges",
    "total_charges",
    "contract",
    "payment_method",
    "internet_service"
]

MODEL_PATH = os.path.join(MODEL_DIR, "churn_pipeline.joblib")