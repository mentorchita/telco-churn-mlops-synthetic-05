# Enhanced Telco Dataset Generator with Text Data


# Telco Customer Churn – Synthetic Dataset with Data Drift

 [![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

 [![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue)](https://www.python.org/downloads/)


## Synthetic dataset for working through the full MLOps cycle:

- training churn classification models

- monitoring data drift / concept drift

- automated retraining

- shadow datasets, A/B testing models, etc.

 

 **Does not contain any real customer records** – completely generated programmatically.

 

### Source of inspiration

 The structure and statistical distributions are based on a public dataset:

 **Telco Customer Churn**

 https://www.kaggle.com/datasets/blastchar/telco-customer-churn

 Original license: CC BY-NC-SA 4.0

 

## This repository does not contain or distribute the original dataset.

 

### Synthetic Data Features

- 100,000+ records

- Period: 2023-01-01 → 2024-12-31

- Gradual conceptual drift (Fiber optic growth, Electronic check decline, churn decline, etc.)

- `RecordDate` column for time analysis

- Realistic dependencies between features (like in the real world)

 

## How to generate a dataset


## 1. Clone the repository

```sh
 git clone https://github.com/<your repo>/telco-churn-mlops-synthetic.git
```
```sh
 cd telco-churn-mlops-synthetic
```
 

## 2. Create a virtual environment and install dependencies

```sh
 python -m venv venv
```
```sh
 source venv/bin/activate # Windows: venv\\Scripts\\activate
```
```sh
 pip install -r requirements.txt
```
 

## 3. Generate a dataset


## Standatd generation
```sh
python generate_dataset.py
```
## Custom generation
```sh
python generate_dataset.py --samples 100000 --output-dir my_data/
```
## Custom generation with date

```sh
python generate_dataset.py --samples 50000 --start-date 2022-01-01 --end-date 2024-12-31
```

## Enhanced Custom generation

```sh
python generate_dataset_ext.py --samples 100000 --output-dir my_data/
```
## 📊 What will you get?

data/
├── telco_customers.csv           # 50,000 clients with drift
├── support_conversations.csv     # ~7,500 dialogs
├── knowledge_base.csv            # 8 documents
└── knowledge_base.json           # The same in json JSON
=======
# Telco Customer Churn – Synthetic Dataset with Data Drift

 [![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue)](https://www.python.org/downloads/)

 
 ### Synthetic dataset for working through the full MLOps cycle:

 - training churn classification models

 - monitoring data drift / concept drift

 - automated retraining

 - shadow datasets, A/B testing models, etc.

 

 **Does not contain any real customer records** – completely generated programmatically.

 

 ### Source of inspiration

 The structure and statistical distributions are based on a public dataset:

 **Telco Customer Churn**

 https://www.kaggle.com/datasets/blastchar/telco-customer-churn

 Original license: CC BY-NC-SA 4.0

 

 This repository does not contain or distribute the original dataset.

 

 ### Synthetic Data Features

 - 100,000+ records

 - Period: 2023-01-01 → 2024-12-31

 - Gradual conceptual drift (Fiber optic growth, Electronic check decline, churn decline, etc.)

 - `RecordDate` column for time analysis

 - Realistic dependencies between features (like in the real world)

 
 
