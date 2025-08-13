from pydantic import BaseModel, Field
from typing import Optional, List, Dict

class SummarizeRequest(BaseModel):
    text: str = Field(..., min_length=10)

class SummarizeResponse(BaseModel):
    summary: str

class PolicySearchRequest(BaseModel):
    query: str
    top_k: int = 3

class PolicySearchResult(BaseModel):
    id: str
    score: float
    snippet: str

class FeedbackRequest(BaseModel):
    category: str
    description: str
    location: Optional[str] = None

class FeedbackResponse(BaseModel):
    status: str
    id: str

class ChatRequest(BaseModel):
    question: str

class ChatResponse(BaseModel):
    answer: str

class EcoTipsResponse(BaseModel):
    tips: List[str]

class ForecastResponse(BaseModel):
    predictions: List[float]
    note: Optional[str] = None

class AnomalyResponse(BaseModel):
    anomalies: List[Dict]