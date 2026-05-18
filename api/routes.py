from fastapi import APIRouter, HTTPException
from api.schema import PredictionRequest, PredictionResponse
from api.services import predict_churn

router = APIRouter()

@router.get("/health")
def health_check():
    """Health check endpoint to verify that the API is running."""
    return {"status": "ok"}

@router.post("/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest):
    result = predict_churn(request)
    if not result:
        raise HTTPException(status_code=500, detail="Prediction failed")
    return result