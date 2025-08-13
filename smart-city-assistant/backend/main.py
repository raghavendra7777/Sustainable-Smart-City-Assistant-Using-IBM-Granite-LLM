import io
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd

from .models import (
    SummarizeRequest, SummarizeResponse,
    PolicySearchRequest, PolicySearchResult,
    FeedbackRequest, FeedbackResponse,
    ChatRequest, ChatResponse,
    EcoTipsResponse, ForecastResponse, AnomalyResponse
)
from .services import llm, pinecone_search, forecasting, anomaly

app = FastAPI(title="Sustainable Smart City Assistant", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

_FAKE_FEEDBACK_DB = {}

@app.post("/summarize", response_model=SummarizeResponse)
def summarize(req: SummarizeRequest):
    return SummarizeResponse(summary=llm.summarize(req.text))

@app.post("/policy_search", response_model=list[PolicySearchResult])
def policy_search(req: PolicySearchRequest):
    results = pinecone_search.search(req.query, req.top_k)
    return [PolicySearchResult(**r) for r in results]

@app.post("/feedback", response_model=FeedbackResponse)
def feedback(req: FeedbackRequest):
    new_id = f"fb-{len(_FAKE_FEEDBACK_DB)+1}"
    _FAKE_FEEDBACK_DB[new_id] = req.model_dump()
    return FeedbackResponse(status="received", id=new_id)

@app.post("/forecast", response_model=ForecastResponse)
async def forecast(file: UploadFile = File(...), horizon: int = 12):
    content = await file.read()
    df = pd.read_csv(io.BytesIO(content))
    preds = forecasting.fit_linear_forecast(df, horizon=horizon)
    return ForecastResponse(predictions=preds, note="Linear regression baseline")

@app.post("/anomaly", response_model=AnomalyResponse)
async def anomaly_detect(file: UploadFile = File(...)):
    content = await file.read()
    df = pd.read_csv(io.BytesIO(content))
    anomalies = anomaly.detect_anomalies(df)
    return AnomalyResponse(anomalies=anomalies)

@app.get("/eco_tips", response_model=EcoTipsResponse)
def eco_tips(keyword: str):
    tips_map = {
        "plastic": [
            "Carry a reusable bottle and bag.",
            "Choose products with minimal packaging.",
            "Run neighborhood plastic collection drives."
        ],
        "solar": [
            "Install rooftop solar with net metering.",
            "Use solar water heaters.",
            "Educate RWAs on group purchase programs."
        ],
        "water": [
            "Fix leaks and install aerators.",
            "Harvest rainwater in buildings.",
            "Adopt drought-tolerant landscaping."
        ]
    }
    tips = tips_map.get(keyword.lower(), [
        "Switch to LEDs and efficient appliances.",
        "Use public transport or cycle for short trips.",
        "Segregate waste at source and compost organics."
    ])
    return EcoTipsResponse(tips=tips)

@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    return ChatResponse(answer=llm.chat(req.question))