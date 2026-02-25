# MLflow configuration and usage

This folder contains a simple MLflow configuration example and a small helper for
registering models. The training script `pipelines/train.py` has been instrumented
to log parameters, metrics and the trained model to MLflow.

Quick start:

- Run an MLflow tracking server (local example):

```bash
mlflow server --backend-store-uri sqlite:///mlflow.db --default-artifact-root ./mlartifacts --host 0.0.0.0 --port 5000
```

- Train and log a model (uses env vars or defaults):

```bash
export MLFLOW_TRACKING_URI=http://localhost:5000
export MLFLOW_EXPERIMENT=telco_churn_experiment
# optional: set to 'true' to register the model in the Model Registry
export MLFLOW_REGISTER_MODEL=false
python pipelines/train.py
```

The `mlflow_register.py` file shows a minimal example of how to programmatically
register a model in the registry. In most cases it's easier to use
`mlflow.sklearn.log_model(..., registered_model_name=...)` from the training run.

See `mlflow_config.yaml` for sample config values.
