import joblib
import pandas as pd
import os
from typing import Dict

MODEL_PATH = os.getenv("MODEL_PATH", "models/churn_model.pkl")

# Завантажуємо модель один раз при старті
try:
    model = joblib.load(MODEL_PATH)
    print(f"Модель успішно завантажена з {MODEL_PATH}")
except Exception as e:
    print(f"Помилка завантаження моделі: {e}")
    model = None

def preprocess_features(features: Dict) -> pd.DataFrame:
    """Перетворюємо вхідні дані в DataFrame, готовий для моделі"""
    df = pd.DataFrame([features])
    
    # Мінімальна обробка (додайте те, що було в train.py)
    categorical_cols = [
        'gender', 'Partner', 'Dependents', 'PhoneService', 'MultipleLines',
        'InternetService', 'OnlineSecurity', 'OnlineBackup', 'DeviceProtection',
        'TechSupport', 'StreamingTV', 'StreamingMovies', 'Contract',
        'PaperlessBilling', 'PaymentMethod'
    ]
    
    for col in categorical_cols:
        if col in df.columns:
            df[col] = df[col].astype('category').cat.codes
    
    return df

def predict_churn(features: Dict) -> Dict:
    if model is None:
        return {"error": "Модель не завантажена"}

    try:
        X = preprocess_features(features)
        prob = model.predict_proba(X)[0][1]  # ймовірність churn=1
        pred = 1 if prob >= 0.5 else 0
        
        return {
            "churn_probability": round(float(prob), 4),
            "churn_prediction": int(pred),
            "features_used": list(X.columns)
        }
    except Exception as e:
        return {"error": str(e)}