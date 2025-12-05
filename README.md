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

 

 ### How to generate a dataset

 

 ### 1. Clone the repository

```bash
 git clone https://github.com/twonick/telco-churn-mlops-synthetic.git

 cd telco-churn-mlops-synthetic
```
 

 ### 2. Create a virtual environment and install dependencies

```bash
 python -m venv venv
```

```bash
 source venv/bin/activate # Windows: venv\Scripts\activate
```
```bash
 pip install -r requirements.txt
```
 

 ### 3. Generate a dataset

```bash
 python generate\_dataset.py --samples 100000 --output data/telco_churn_full.csv
```

 ### or just run without parameters (default 100k)

```bash
 python generate\_dataset.py
```
