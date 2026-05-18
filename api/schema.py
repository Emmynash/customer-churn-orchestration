from pydantic import BaseModel
from typing import Optional, List

class Features(BaseModel):
    tenure: int
    monthly_charges: float
    total_charges: float
    contract: str
    payment_method: str
    internet_service: str

class PredictionRequest(BaseModel):
    features: Features
    customer_id: str
    feedback_text: Optional[str] = None

class PredictionResponse(BaseModel):
    customer_id: str
    churn_probability: float
    risk_band: str
    confidence: float
    reason_codes: List[str]
    model_version: str
    scored_at: str
