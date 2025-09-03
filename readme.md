🤖 Financial News Analyzer: AI/ML Repository
This repository contains the core machine learning models and training pipelines for the Financial News Analyzer project. It is the single source of truth for model development, experimentation, and versioning.

📁 Repository Structure
ai_ml_repo/
├── .github/
│   └── workflows/
│       └── train_and_promote.yml
├── model_training/
│   ├── scripts/
│   │   ├── train_sentiment.py
│   │   └── train_summarization.py
│   └── requirements.txt
├── mlops/
│   └── promote_models.py
└── README.md

🎯 Purpose
The main goal of this repository is to train and version two key NLP models:
- A sentiment analysis model (based on FinBERT).
- A summarization model (based on BART).

When a new model is trained and meets performance criteria, it is automatically logged and promoted to the central MLflow Model Registry by our CI/CD pipeline. This model is then ready to be served by the separate Application API.

🚀 CI/CD Pipeline
The .github/workflows/train_and_promote.yml pipeline automates the entire process:
1. Triggers on a push to the main branch or a manual workflow_dispatch.
2. Installs all necessary dependencies.
3. Runs the training scripts, which log model performance and artifacts to our shared MLflow server.
4. Executes the promote_models.py script, which automatically transitions the best-performing model to the "Production" stage in the MLflow Model Registry.