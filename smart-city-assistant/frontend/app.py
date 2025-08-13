import os
import requests
import pandas as pd
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

BACKEND_HOST = os.getenv("BACKEND_HOST", "127.0.0.1")
BACKEND_PORT = os.getenv("BACKEND_PORT", "8000")
API = f"http://{BACKEND_HOST}:{BACKEND_PORT}"

st.set_page_config(page_title="Smart City Assistant", layout="wide")

st.title("🏙️ Sustainable Smart City Assistant")

tabs = st.tabs(["Policy Summarization", "Policy Search", "Citizen Feedback", "KPI Forecasting", "Eco Tips", "Anomaly Detection", "Chat"])

with tabs[0]:
    st.subheader("Policy Summarization")
    txt = st.text_area("Paste policy text")
    if st.button("Summarize"):
        if len(txt.strip()) < 10:
            st.warning("Please paste a longer text.")
        else:
            r = requests.post(f"{API}/summarize", json={"text": txt})
            st.success(r.json()["summary"])

with tabs[1]:
    st.subheader("Policy Search")
    q = st.text_input("Search query")
    k = st.number_input("Top K", min_value=1, max_value=10, value=3)
    if st.button("Search"):
        r = requests.post(f"{API}/policy_search", json={"query": q, "top_k": int(k)})
        st.write(pd.DataFrame(r.json()))

with tabs[2]:
    st.subheader("Citizen Feedback")
    cat = st.selectbox("Category", ["Water", "Roads", "Power", "Sanitation", "Parks", "Other"])
    desc = st.text_area("Describe the issue")
    loc = st.text_input("Location (optional)")
    if st.button("Submit Feedback"):
        r = requests.post(f"{API}/feedback", json={"category": cat, "description": desc, "location": loc})
        st.success(f"Submitted with ID: {r.json()['id']}")

with tabs[3]:
    st.subheader("KPI Forecasting")
    file = st.file_uploader("Upload CSV with columns date/value or period/value", type=["csv"])
    horizon = st.number_input("Forecast horizon (periods)", min_value=1, max_value=36, value=12)
    if st.button("Run Forecast") and file is not None:
        files = {"file": (file.name, file.getvalue(), "text/csv")}
        r = requests.post(f"{API}/forecast?horizon={int(horizon)}", files=files)
        preds = r.json()["predictions"]
        st.line_chart(preds)
        st.write(pd.DataFrame({"prediction": preds}))

with tabs[4]:
    st.subheader("Eco Tips")
    kw = st.text_input("Keyword (e.g., plastic, solar, water)", value="plastic")
    if st.button("Get Tips"):
        r = requests.get(f"{API}/eco_tips", params={"keyword": kw})
        st.write(r.json()["tips"])

with tabs[5]:
    st.subheader("Anomaly Detection")
    file2 = st.file_uploader("Upload CSV with columns (zone,value) or (date,value)", type=["csv"], key="anom")
    if st.button("Detect Anomalies") and file2 is not None:
        files = {"file": (file2.name, file2.getvalue(), "text/csv")}
        r = requests.post(f"{API}/anomaly", files=files)
        st.write(pd.DataFrame(r.json()["anomalies"]))

with tabs[6]:
    st.subheader("Chat Assistant")
    q = st.text_input("Ask a question")
    if st.button("Ask"):
        r = requests.post(f"{API}/chat", json={"question": q})
        st.info(r.json()["answer"])