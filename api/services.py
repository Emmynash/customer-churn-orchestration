import joblib
import uuid
import pandas as pd
from datetime import datetime
from api.schema import PredictionRequest, PredictionResponse
from api.config import MODEL_PATH, FEATURES

model = joblib.load(MODEL_PATH)

def map_risk(prob: float) -> str:
    """Maps churn probability to risk band."""
    if prob >= 0.6:
        return "High Risk"
    elif prob >= 0.3:
        return "Medium Risk"
    else:
        return "Low Risk"
    
def predict_churn(request: PredictionRequest):
    input_dict = request.features.dict()

    input_df = pd.DataFrame([input_dict])[FEATURES]

    prob = float(model.predict_proba(input_df)[0][1])

    # Risk mapping
    risk_band = map_risk(prob)

    # Lightweight heuristic explanations
    reason_codes = []

    if input_dict["contract"] == "Month-to-month":
        reason_codes.append("short_term_contract")

    if input_dict["tenure"] < 6:
        reason_codes.append("low_tenure")

    if input_dict["monthly_charges"] > 80:
        reason_codes.append("high_monthly_charges")

    if input_dict["payment_method"] == "Electronic check":
        reason_codes.append("manual_payment_risk")

    if input_dict["internet_service"] == "Fiber optic":
        reason_codes.append("premium_service_risk")

    return PredictionResponse(
        prediction_id=str(uuid.uuid4()),
        customer_id=request.customer_id,
        churn_probability=round(prob, 2),
        risk_band=risk_band,
        confidence=round(abs(prob - 0.5) * 2, 2),
        reason_codes=reason_codes,
        model_version="rf_v1.0",
        scored_at=datetime.utcnow().isoformat()
    )