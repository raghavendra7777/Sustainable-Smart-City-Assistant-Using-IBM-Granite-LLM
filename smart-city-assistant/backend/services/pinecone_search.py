import os
from typing import List, Dict
from dotenv import load_dotenv
load_dotenv()

try:
    from pinecone import Pinecone
except Exception:
    Pinecone = None

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX = os.getenv("PINECONE_INDEX")

def available() -> bool:
    return bool(PINECONE_API_KEY and PINECONE_INDEX and Pinecone is not None)

def search(query: str, top_k: int = 3) -> List[Dict]:
    if not available():
        # Return stubbed matches
        return [
            {"id": "doc-1", "score": 0.9, "snippet": "Sample policy about renewable energy incentives."},
            {"id": "doc-2", "score": 0.86, "snippet": "Waste management guidelines for urban wards."},
        ][:top_k]
    pc = Pinecone(api_key=PINECONE_API_KEY)
    index = pc.Index(PINECONE_INDEX)
    # This is a placeholder; you must upsert embeddings separately
    res = index.query(
        vector=[0.1]*1536,  # Replace with real embedding of 'query'
        top_k=top_k,
        include_metadata=True
    )
    out = []
    for m in res.matches:
        out.append({
            "id": m.id,
            "score": float(m.score),
            "snippet": (m.metadata or {}).get("text", "")[:200]
        })
    return out