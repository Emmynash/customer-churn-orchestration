TARGET = "churn"

NUMERICAL_FEATURES = [
    "tenure",
    "monthly_charges",
    "total_charges"
]

CATEGORICAL_FEATURES = [
    "contract",
    "payment_method",
    "internet_service"
]

FEATURES = NUMERICAL_FEATURES + CATEGORICAL_FEATURES

MODEL_VERSION = "rf_v1.0"