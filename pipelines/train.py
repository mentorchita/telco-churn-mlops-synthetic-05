import mlflow
import pandas as pd
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier
from hydra import compose, initialize
from omegaconf import OmegaConf

initialize(version_base=None, config_path="../conf")
cfg = compose(config_name="config")

with mlflow.start_run():
    df = pd.read_csv(cfg.data.path)
    X = df.drop("Churn", axis=1)
    y = df["Churn"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=cfg.data.test_size)

    model = XGBClassifier(**cfg.model.params)
    model.fit(X_train, y_train)

    accuracy = model.score(X_test, y_test)
    mlflow.log_metric("accuracy", accuracy)
    mlflow.xgboost.log_model(model, "model")

    print(f"Accuracy: {accuracy:.4f}")
