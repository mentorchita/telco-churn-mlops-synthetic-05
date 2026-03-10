# Telco Customer Churn - Synthetic Dataset with MLOps Pipeline

## Overview
This repository provides a synthetic dataset generator for Telco Customer Churn prediction, along with a full MLOps pipeline. It includes tools for data generation with built-in data drift, model training, experiment tracking using MLflow, API serving with FastAPI, monitoring, and deployment. The dataset is entirely synthetic (no real customer data) and is inspired by the public Telco Customer Churn dataset on Kaggle, licensed under CC BY-NC-SA 4.0.
Key features:

Generate 100,000+ records spanning 2023-01-01 to 2024-12-31.
Simulate gradual concept drift (e.g., growth in fiber optic adoption, decline in electronic checks, reducing churn rates).
Realistic feature dependencies and a RecordDate column for time-based analysis.
MLOps integration: Data Version Control (DVC), Airflow for orchestration, MLflow for experiment tracking and model registry, Kubernetes for deployment, and monitoring for drift detection.

## Repository Structure

.dvc/: DVC configuration for data and pipeline tracking.
airflow/dags/: Airflow DAGs for ML workflows.
conf/ and config/: Configuration files for experiments and pipelines.
data/: Generated synthetic data (e.g., telco_customers.csv).
deployment/: Kubernetes manifests for production deployment.
docs/: Additional documentation and diagrams.
mlflow/: MLflow configurations, registration scripts, and setup guide.
mlflow_db/: Persistent storage for MLflow database.
models/: Trained model artifacts.
monitoring/: Scripts for data/concept drift detection, A/B testing, and shadow datasets.
notebooks/: Jupyter notebooks for data exploration and analysis.
pipelines/: Training and prediction pipelines (e.g., train.py, predict.py).
src/: Source code for data generation (e.g., generate_dataset_ext.py).
tests/: Unit tests (e.g., test_api_predict.py).
Dockerfile and Dockerfile.api: Docker images for the project and API.
docker-compose.yml: Composes services like data generator, Jupyter, API, and MLflow.

## Installation

Clone the repository:textgit clone https://github.com/mentorchita/telco-churn-mlops-synthetic-05.git
cd telco-churn-mlops-synthetic-05
Create a virtual environment and install dependencies:textpython -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
pip install -r requirements-ml.txt  # For MLflow and training dependencies
pip install -r requirements-api.txt  # For FastAPI
pip install -r requirements-dev.txt  # Optional: For linting, Jupyter, etc.

## Usage
### Data Generation

Generate synthetic data using the provided scripts.

Standard generation:textpython src/generate_dataset.py
Custom generation:textpython src/generate_dataset.py --samples 100000 --output-dir data/ --start-date 2022-01-01 --end-date 2024-12-31
Enhanced generation (using config.yaml):textpython src/generate_dataset_ext.py --samples 20000 --conv-samples 3000

Output files will be placed in data/ (e.g., telco_customers.csv, support_conversations.csv).

### Makefile Commands

Use make for streamlined workflows:

make help: List all commands.
make install: Install base dependencies.
make install-dev: Install development tools (e.g., Ruff, Black, Jupyter).
make generate-ext: Generate extended dataset.
make explore: Launch Jupyter.
make lint: Check code style.
make format: Fix code style.
make clean-data: Clean generated data.
make train: Train the churn model (logs to MLflow).
make docker-up: Start all services via Docker Compose.
make jupyter-up: Launch Jupyter container.
make jupyter-down: Stop Jupyter.
make jupyter-logs: View Jupyter logs (includes access token).

## ML Training
Train a churn prediction model using pipelines/train.py, which is instrumented with MLflow for logging parameters, metrics, and artifacts.

Start the MLflow tracking server (locally or via Docker Compose).
Set environment variables:textexport MLFLOW_TRACKING_URI=http://localhost:5000
export MLFLOW_EXPERIMENT=telco_churn_experiment
export MLFLOW_REGISTER_MODEL=true  # Optional: Register model in registry
Run training:textmake train  # Or python pipelines/train.py

The script loads data from data/, trains a model (e.g., RandomForest or similar), logs to MLflow, and optionally registers the model.

## MLflow Integration

MLflow is central to experiment tracking, model registry, and serving in this project.

Setup: Use mlflow/ for configurations. Start the server:textmlflow server --backend-store-uri sqlite:///mlflow.db --default-artifact-root ./mlartifacts --host 0.0.0.0 --port 5000Or via Docker Compose (service defined in docker-compose.yml with volumes for mlruns/ and database).
Tracking: During training (pipelines/train.py), parameters (e.g., n_estimators), metrics (e.g., accuracy), and the model are logged using mlflow.start_run(), mlflow.log_param(), mlflow.log_metric(), and mlflow.sklearn.log_model().
Model Registry: Register models programmatically with mlflow/mlflow_register.py or directly in training via registered_model_name. Promote models from staging to production.
Viewing Experiments: Access the MLflow UI at http://localhost:5000.
API Integration: The FastAPI service (src/api/) can load registered models from MLflow (e.g., mlflow.pyfunc.load_model("models:/churn@production")).
Configurations: See mlflow/mlflow_config.yaml for sample values like tracking URI and experiment name.

## API Serving
Serve predictions via FastAPI.

Start the API:textuvicorn src.api.main:app --host 0.0.0.0 --port 8000 --reloadOr via Docker: docker compose up api (depends on MLflow service).
### Endpoints:
/health: Check service status and model loading.
/predict: POST customer features (JSON) for churn probability.


Example curl test:
textcurl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"tenure": 12, "MonthlyCharges": 65.5, "TotalCharges": 786.0, "gender": "Male", "SeniorCitizen": 0, "Partner": "Yes", "Dependents": "No", "PhoneService": "Yes", "MultipleLines": "No", "InternetService": "Fiber optic", "OnlineSecurity": "No", "OnlineBackup": "No", "DeviceProtection": "No", "TechSupport": "No", "StreamingTV": "No", "StreamingMovies": "No", "Contract": "Month-to-month", "PaperlessBilling": "Yes", "PaymentMethod": "Electronic check"}'

## Testing: 
Run python tests/test_api_predict.py for automated checks.

## Deployment
Use deployment/ for Kubernetes manifests to deploy the API and MLflow in production.
## Monitoring
Scripts in monitoring/ handle data/concept drift detection, A/B testing, and shadow datasets. Integrate with MLflow for comparing model versions.
## License
MIT License. See LICENSE for details.
dvc.yaml: DVC pipeline definitions.
Makefile: Convenience commands for setup, generation, training, and more.
requirements-*.txt: Python dependencies for base, API, dev, and ML.
