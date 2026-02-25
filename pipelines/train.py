import os
import pandas as pd
import joblib
import mlflow
import mlflow.sklearn
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score

# path to data and model
DATA_PATH = 'data/telco_customers.csv'
MODEL_PATH = 'models/churn_model.pkl'

# MLflow configuration via environment variables
MLFLOW_TRACKING_URI = os.getenv('MLFLOW_TRACKING_URI', 'http://localhost:5000')
MLFLOW_EXPERIMENT = os.getenv('MLFLOW_EXPERIMENT', 'telco_churn_experiment')
MLFLOW_REGISTER = os.getenv('MLFLOW_REGISTER_MODEL', 'false').lower() == 'true'
MLFLOW_REGISTERED_NAME = os.getenv('MLFLOW_REGISTERED_NAME', 'ChurnModel')

# Load data
df = pd.read_csv(DATA_PATH)

# Preprocessing: delete customerID, convert TotalCharges to numeric, drop rows with missing values
df = df.drop(['customerID'], axis=1, errors='ignore')  # if customerID exists, drop it
df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')  # typical fix
df = df.dropna()

X = df.drop('Churn', axis=1)
y = df['Churn'].map({'Yes': 1, 'No': 0})  # target binarize

# Identify categorical and numerical columns
categorical_cols = X.select_dtypes(include=['object']).columns
numerical_cols = X.select_dtypes(include=['int64', 'float64']).columns

# Pipeline для preprocessing
preprocessor = ColumnTransformer(
    transformers=[
        ('num', 'passthrough', numerical_cols),
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_cols)
    ])

# Model pipeline
model = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('classifier', RandomForestClassifier(n_estimators=100, random_state=42))
])

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
mlflow.set_experiment(MLFLOW_EXPERIMENT)

with mlflow.start_run():
    # Log important parameters
    params = {
        'n_estimators': 100,
        'random_state': 42,
    }
    mlflow.log_params(params)

    # Train model
    model.fit(X_train, y_train)

    # Evaluate model
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f'Accuracy: {acc:.2f}')
    mlflow.log_metric('accuracy', float(acc))

    # Log and optionally register model
    try:
        if MLFLOW_REGISTER:
            mlflow.sklearn.log_model(model, 'model', registered_model_name=MLFLOW_REGISTERED_NAME)
        else:
            mlflow.sklearn.log_model(model, 'model')
    except Exception as e:
        # Fallback: still save local model and log exception
        print(f'Warning: failed to log/register model to MLflow: {e}')

    # Also save a local copy for compatibility
    os.makedirs('models/', exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    print(f'Model saved to {MODEL_PATH}')