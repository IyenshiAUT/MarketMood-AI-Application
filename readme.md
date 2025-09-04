# 🚀 MarketMood AI - Financial News Analyzer &  Summarizer: Application Repository

This repository contains the **production-ready FastAPI application** that serves the AI models. It is built to be lightweight and scalable, retrieving the latest **"Production" model** from the MLflow Model Registry at runtime.


## 📁 Repository Structure
```

application\_repo/
├── .github/
│   └── workflows/
│       └── build\_and\_deploy.yml   # CI/CD workflow
├── app/
│   ├── api/
│   │   └── main.py                # FastAPI entrypoint
│   └── requirements.txt           # Python dependencies
├── frontend/
|   ├── index.html
|   ├── script.js
|   ├── style.css                  # Frontend Developement
| 
├── tests/
|   ├── __init__.py
|   ├── testapi.py                 # Test cases
├── Dockerfile                     # Docker image definition
└── README.md                      # Documentation

```

---

## 🎯 Purpose
The main purpose of this repository is to provide a **robust API endpoint** for sentiment analysis and news summarization. 

It is designed with a **decoupled architecture**, meaning the application's code is independent of the model training process.

### The API performs the following functions:
- Initializes a connection to the **MLflow Model Registry** on startup.
- Fetches the latest **"Production" model versions** for both sentiment analysis and summarization.
- Serves these models via a **RESTful API endpoint**, ready to handle incoming requests.

---

## 🚀 CI/CD Pipeline
The `.github/workflows/build_and_deploy.yml` pipeline automates the deployment process:

1. **Triggers** on a push to the `main` branch or via `workflow_dispatch` (manual run).
2. **Builds** a new Docker image from the repository's `Dockerfile`.  
   - This image only contains the application code and dependencies (not the large model files).
3. **Pushes** the Docker image to a container registry (e.g., **Docker Hub**).
4. **Deploys** the image to the production server via SSH, passing MLflow server credentials as environment variables.
---
## ▶️ How to Run

### 1. Clone the Repository
```bash
git clone https://github.com/IyenshiAUT/MarketMood-AI-Application.git
cd marketmood-ai-application
```
### 2. Create and Activate Virtual Environment
```bash
python -m venv venv
source venv/bin/activate # On Linux/MacOS
venv\Scripts\activate # On Windows
```
### 3. Install Dependencies
```bash
python -m venv venv
source venv/bin/activate # On Linux/MacOS
venv\Scripts\activate # On Windows
```
### 4. Run Locally with Uvicorn
```bash
uvicorn app.api.main:app --host 0.0.0.0 --port 8000 --reload
```
## 🐳 Run with Docker
- Build Image
```bash
docker build -t financial-news-analyzer-app .
```
- Run Container
```bash
docker run -d -p 8000:8000 \
-e MLFLOW_TRACKING_URI=your_mlflow_server_url \
-e MLFLOW_TRACKING_USERNAME=your_username \
-e MLFLOW_TRACKING_PASSWORD=your_password \
```

## 📌 Future Enhancements
- Add request/response logging for better observability.
- Integrate monitoring and alerting (Prometheus/Grafana).
- Expand support for additional ML models.

---

## 🛠️ Tech Stack
- **FastAPI** – Web framework
- **MLflow** – Model registry & management
- **Docker** – Containerization
- **GitHub Actions** – CI/CD automation
