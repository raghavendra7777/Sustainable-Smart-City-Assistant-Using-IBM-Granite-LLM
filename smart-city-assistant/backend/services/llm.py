import os
from dotenv import load_dotenv

load_dotenv()

WATSONX_API_KEY = os.getenv("WATSONX_API_KEY")
WATSONX_PROJECT_ID = os.getenv("WATSONX_PROJECT_ID")
WATSONX_MODEL_ID = os.getenv("WATSONX_MODEL_ID", "granite-13b-chat-v2")

def has_cloud_llm() -> bool:
    return bool(WATSONX_API_KEY and WATSONX_PROJECT_ID and WATSONX_MODEL_ID)

def summarize(text: str) -> str:
    if has_cloud_llm():
        # Placeholder for real watsonx Granite call using ibm-watsonx-ai SDK
        # Here we just simulate: in production, replace with the official client
        return text[:400] + ("..." if len(text) > 400 else "")
    # Local fallback: trivial heuristic 'summary' by taking first and last sentences.
    sentences = [s.strip() for s in text.replace("\n", " ").split(".") if s.strip()]
    if not sentences:
        return text[:200]
    if len(sentences) == 1:
        return sentences[0]
    return sentences[0] + ". ... " + sentences[-1] + "."

def chat(question: str) -> str:
    if has_cloud_llm():
        # Placeholder for real Granite chat completion
        return f"[Granite simulated] Answer to: {question}"
    # Local rules-based fallback
    q = question.lower()
    if "carbon" in q or "emission" in q:
        return ("Ideas: expand public transit, EV charging, building efficiency retrofits, "
                "district cooling, green roofs, and stricter industrial standards.")
    if "water" in q:
        return ("Reduce non-revenue water via leak detection, smart meters, tiered pricing, "
                "rainwater harvesting, and wastewater reuse.")
    return ("For sustainable cities: compact zoning, mixed-use development, active mobility, "
            "renewables, circular waste systems, and transparent governance.")