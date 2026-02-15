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

# Звичайний запуск (використовує config.yaml)
```sh
python src/generate_dataset_ext.py
```
# Перевизначити кількість клієнтів
```sh
python src/generate_dataset_ext.py --override-samples 20000
```
# Використати інший конфіг
```sh
python src/generate_dataset_ext.py --config config/my_experiment.yaml
```
# Full extended

```sh
python src/generate_dataset_ext.py --samples 20000 --conv-samples 3000
```

## 📊 What will you get?
```
data/
├── telco_customers.csv           # 50,000 clients with drift
├── support_conversations.csv     # ~7,500 dialogs
├── knowledge_base.csv            # 8 documents
└── knowledge_base.json           # The same in json JSON
```



# Recommendations for using make

- make help # see all available commands
- make install # first time
- make install-dev # if you want ruff, black, jupyter
- make generate-ext # main generation
- make explore # open Jupyter
- make lint # check style
- make format # fix style
- make clean-data # clean only data

# 1. Data generation (as before)
```sh
make docker-up
```
# or
```sh
docker compose up -d generator
```

# 2. Launch Jupyter
```sh
make jupyter-up
```

# 3. Let's look at the logs → there will be a link and a token
```sh
make jupyter-logs
```

# Example of output in the logs:
# http://127.0.0.1:8888/lab?token=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# 4. Stop Jupyter

```sh
make jupyter-down
```

If you want to launch Jupyter without docker-compose (one-time)
Add another target to the Makefile (alternative):
makefilejupyter-standalone: ​​## Run Jupyter in a single container without compose
```sh
	docker run -d \
		--name temp-jupyter \
		-p 8888:8888 \
		-v $(PWD)/notebooks:/home/jovyan/work \
		-v $(PWD)/data:/home/jovyan/data:ro \
		-e JUPYTER_ENABLE_LAB=yes \
		-e JUPYTER_TOKEN=secret123 \
		quay.io/jupyter/scipy-notebook:latest
```

jupyter-standalone-stop: ## Зупинити та видалити standalone Jupyter

```sh
	docker stop temp-jupyter && docker rm temp-jupyter 
```    

## ML Training
Запустіть `make train` для тренування моделі churn prediction.

## Deployment
Використовуйте Kubernetes manifests в deployment/ для production.

## Monitoring
Скрипти для дріфту в monitoring/.
