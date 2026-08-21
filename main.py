from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/v1/metrics/summary")
def get_metrics_summary():
    return {
        "total_tokens": 1250000,
        "total_cost": 15.42,
        "avg_latency_ms": 120,
        "active_models": 4
    }