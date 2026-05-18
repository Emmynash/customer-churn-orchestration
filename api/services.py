import joblib
import pandas as pd
from datetime import datetime
from api.schema import PredictionRequest, PredictionResponse
from api.config import MODEL_PATH, FEATURES

model = joblib.load(MODEL_PATH)

def map_risk(prob: float) -> str:
    """Maps churn probability to risk band."""
    if prob >= 0.7:
        return "High Risk"
    elif prob >= 0.4:
        return "Medium Risk"
    else:
        return "Low Risk"
    
def predict_churn(request: PredictionRequest):
    input_dict = request.features.dict()
    input_df = pd.DataFrame([input_dict])[FEATURES]

    prob = model.predict_proba(input_df)[0][1]

    return PredictionResponse(
        customer_id=request.customer_id,
        churn_probability=prob,
        risk_band=map_risk(prob),
        confidence=round(abs(prob - 0.5) * 2, 2),
        reason_codes=[],
        model_version="rf_v1.0",
        scored_at=datetime.utcnow().isoformat()
    )