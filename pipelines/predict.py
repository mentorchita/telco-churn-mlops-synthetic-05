import pickle
import pandas as pd

def predict(input_data_path: str, model_path: str = "models/churn_model.pkl"):
    with open(model_path, "rb") as f:
        model = pickle.load(f)
    df = pd.read_csv(input_data_path)
    # Приклад передбачення
    predictions = model.predict(df.drop("Churn", axis=1, errors="ignore"))
    print("Передбачені churn:", predictions)
