# Sustainable Smart City Assistant (FastAPI + Streamlit)

This is a minimal **working** prototype of the Sustainable Smart City Assistant.  
It includes:
- **FastAPI backend** with endpoints for summarization, policy search (stub/optional Pinecone), citizen feedback, KPI forecasting, eco tips, anomaly detection, and chat.
- **Streamlit frontend** for an interactive dashboard that talks to the backend.
- **ML** demos: linear regression for forecasting, basic anomaly detection using z-scores/IQR.
- **Pluggable IBM watsonx Granite LLM** integration (fallback to local logic if env vars are not set).
- **.env** support via `python-dotenv`.

> Works out-of-the-box **without any external credentials** (uses local fallbacks). If you add IBM watsonx and Pinecone credentials, those features will automatically activate.

## Quickstart

### 1) Create a virtual environment
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
```

### 2) Install dependencies
```bash
pip install -r requirements.txt
```

### 3) Configure environment (optional for cloud features)
Copy `.env.example` to `.env` and fill values if you have credentials.
Without credentials, local fallbacks are used.
```bash
cp .env.example .env
```

### 4) Run the backend
```bash
uvicorn backend.main:app --reload --port 8000
```

### 5) Run the frontend
In a new terminal (same venv):
```bash
streamlit run frontend/app.py
```
Open the provided local URL in your browser.

## Endpoints (FastAPI)
- `POST /summarize` — Summarize text (Granite or local fallback)
- `POST /policy_search` — Optional Pinecone; otherwise simple keyword search stub
- `POST /feedback` — Accepts citizen issue reports
- `POST /forecast` — Upload CSV with two columns: `date,value` or `period,value`
- `POST /anomaly` — Upload CSV with `zone,value` or `date,value`
- `GET  /eco_tips?keyword=plastic` — Returns eco tips
- `POST /chat` — General Q&A (Granite or local rules-based fallback)

Check interactive docs at: `http://localhost:8000/docs`

## Sample data
A small CSV is included at `backend/data/sample_kpi.csv`.

## Structure
```
smart-city-assistant/
  backend/
    main.py
    models.py
    data/sample_kpi.csv
    services/
      llm.py
      pinecone_search.py
      forecasting.py
      anomaly.py
  frontend/
    app.py
  shared/
    utils.py
  .env.example
  requirements.txt
  README.md
```

## Notes
- The project uses **CORS** to allow the Streamlit app to call the API locally.
- The local LLM fallback uses simple heuristics so you can test UX without credentials.
- If you enable IBM watsonx: set `WATSONX_API_KEY`, `WATSONX_PROJECT_ID`, `WATSONX_MODEL_ID` in `.env`.
- If you enable Pinecone: set `PINECONE_API_KEY`, `PINECONE_INDEX` in `.env` (and build your index out-of-band).