from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from transformers import pipeline
import logging
import requests
from  dotenv import load_dotenv
import os

# Import MLflow to load models
import mlflow
import mlflow.pyfunc
from mlflow.exceptions import MlflowException

# --- Configure logging ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

global sentiment_model, summarization_model, stat
load_dotenv()
mlflow_tracking_uri = os.environ.get("MLFLOW_TRACKING_URI")
os.environ["MLFLOW_TRACKING_USERNAME"] = os.environ.get["MLFLOW_TRACKING_USERNAME"]
os.environ["MLFLOW_TRACKING_PASSWORD"] = os.environ.get["MLFLOW_TRACKING_PASSWORD"]
news_api_key = os.environ.get("NEWS_API_KEY")

if not news_api_key:
    logger.warning("NEWS_API_KEY environment variable not set. News fetching will fail.")


# --- App Initialization and CORS Configuration ---
app = FastAPI(
    title="Financial News Analyzer API",
    description="API for sentiment analysis and summarization.",
    version="1.0.0"
)

# Allow all origins for simplicity in development. For production, restrict this.
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- NLP Model Loading ---
# Load models on startup for efficiency. This can take a moment.
try:
    if not mlflow_tracking_uri:
        raise MlflowException("MLFLOW_TRACKING_URI environment variable is not set. Skipping MLflow.")

    logger.info(f"Setting MLflow tracking URI to {mlflow_tracking_uri}...")
    mlflow.set_tracking_uri(mlflow_tracking_uri)

    logger.info("Loading 'Production' sentiment analysis model from MLflow...")
    # Use mlflow.pyfunc.load_model, which should be a unified model handler
    sentiment_model = mlflow.pyfunc.load_model("models:/finbert-sentiment-model/Production")
        
    logger.info("Loading 'Production' summarization model from MLflow...")
    summarization_model = mlflow.pyfunc.load_model("models:/bart-summarization-model/Production")
    
    stat = 1
    logger.info("Models loaded successfully from MLflow registry.")
except Exception as e:
    logger.info("Loading sentiment analysis model...")
    sentiment_analyzer = pipeline("sentiment-analysis", model="ProsusAI/finbert")
    logger.info("Loading summarization model...")
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    logger.info("Models loaded successfully.")
    stat = 2

# --- Pydantic Models for Data Validation ---
class TextRequest(BaseModel):
    text: str

class SentimentResponse(BaseModel):
    label: str
    score: float

class SummaryResponse(BaseModel):
    summary: str

# --- API Endpoints ---
@app.get("/", tags=["Health Check"])
def read_root():
    """Health check endpoint to confirm the API is running."""
    return {"status": "API is online", "models_loaded": all([sentiment_analyzer, summarizer])}

# Load environment variables to get the API key
load_dotenv()
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

@app.get("/fetch-news/{ticker}", tags=["News Fetcher"])
def fetch_live_news(ticker: str):
    """
    Fetches live news for a given stock ticker from Alpha Vantage.
    """
    if not NEWS_API_KEY:
        raise HTTPException(status_code=500, detail="News API key is not configured on the server.")
    
    url = f"https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers={ticker.upper()}&apikey={NEWS_API_KEY}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if "Note" in data or "feed" not in data or not data["feed"]:
            logger.info(f"No news found for {ticker} or API limit reached.")
            return []

        # Reformat the data, now INCLUDING the summary
        formatted_news = []
        for article in data.get("feed", []):
            formatted_news.append({
                "title": article.get("title"),
                "url": article.get("url"),
                "publishedDate": article.get("time_published"),
                "site": article.get("source"),
                "summary": article.get("summary") # <-- ADD THIS LINE
            })
        
        return formatted_news[:20]

    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching news from external API: {e}")
        raise HTTPException(status_code=502, detail="Failed to fetch news from the provider.")

    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching news from external API: {e}")
        raise HTTPException(status_code=502, detail="Failed to fetch news from the provider.")
    


@app.post("/analyze", response_model=dict, tags=["Analysis"])
def analyze_text(request: TextRequest):
    """
    Performs both sentiment analysis and summarization on the provided text.
    """
    if not request.text or not request.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty.")
    
    if not sentiment_analyzer or not summarizer:
        raise HTTPException(status_code=503, detail="Models are not available.")

    try:
        if stat == 1:
            sentiment_result = sentiment_model.predict([request.text])[0]
            summary_result = summarization_model.predict([request.text])[0]
        else:   
            # Sentiment Analysis
            sentiment_result = sentiment_analyzer(request.text)[0]
            # Summarization
            summary_result = summarizer(request.text, max_length=150, min_length=40, do_sample=False)[0]

        return {
            "sentiment": {
                "label": sentiment_result['label'],
                "score": sentiment_result['score']
            },
            "summary": summary_result['summary_text']
        }
    except Exception as e:
        logger.error(f"Error during analysis: {e}")
        raise HTTPException(status_code=500, detail="An error occurred during text analysis.")