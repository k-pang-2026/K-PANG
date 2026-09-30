from __future__ import annotations
import time
from fastapi import FastAPI

app = FastAPI(title="MM Search & Recommend")

@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}

@app.post("/api/search")
def search(payload: dict) -> dict:
    t0 = time.perf_counter()
    return {"search_type": "text", "results": [], "total_count": 0,
            "latency_ms": (time.perf_counter() - t0) * 1000}

@app.get("/api/recommend")
def recommend(user_id: str, top_n: int = 10) -> dict:
    return {"user_id": user_id, "recommendations": [],
            "pipeline_latency": {"candidate_ms": 0, "ranking_ms": 0,
                                 "reranking_ms": 0, "total_ms": 0},
            "session_context": {"recent_clicks": [], "session_interest": None}}
