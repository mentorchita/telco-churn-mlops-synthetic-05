from fastapi import FastAPI, HTTPException
from src.api.models import CustomerFeatures, PredictionResponse
from src.api.predict import predict_churn
from datetime import datetime

app = FastAPI(
    title="Telco Customer Churn Prediction API",
    description="API для передбачення відтоку клієнтів (churn)",
    version="1.0.0"
)
@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    # Вкажіть шлях до вашого файлу favicon.ico
    return FileResponse('static/favicon.ico')

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "churn-prediction-api",
        "timestamp": datetime.utcnow().isoformat(),
        "model_loaded": "yes" if predict_churn({}) else "no"
    }

@app.post("/predict", response_model=PredictionResponse)
def predict(features: CustomerFeatures):
    """
    Передбачення ймовірності відтоку клієнта.
    Надішліть ознаки клієнта в JSON-форматі.
    """
    result = predict_churn(features.dict())
    
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    
    return PredictionResponse(
        churn_probability=result["churn_probability"],
        churn_prediction=result["churn_prediction"],
        features_used=result["features_used"]
    )