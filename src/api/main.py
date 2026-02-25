import warnings
# Suppress Pydantic v2 warnings from transitive dependencies (e.g., LangChain)
warnings.filterwarnings("ignore", message=".*protected namespace.*", category=UserWarning)

from fastapi import FastAPI, HTTPException
from src.api.models import CustomerFeatures, PredictionResponse
from src.api import predict as predict_module
from datetime import datetime

app = FastAPI(
    title="Telco Customer Churn Prediction API",
    description="Api for predicting customer churn (churn)",
    version="1.0.0",
    docs_url="/docs",      # ← enable Swagger
)

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "churn-prediction-api",
        "timestamp": datetime.utcnow().isoformat(),
        "model_loaded": "yes" if predict_module.model is not None else "no"
    }

@app.post("/predict", response_model=PredictionResponse)
def predict(features: CustomerFeatures):
    """
    Predict the probability of customer churn. Send customer features in JSON format.
    """
    result = predict_module.predict_churn(features.dict())
    
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    
    return PredictionResponse(
        churn_probability=result["churn_probability"],
        churn_prediction=result["churn_prediction"],
        features_used=result["features_used"]
    )