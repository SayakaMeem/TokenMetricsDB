from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import random
from datetime import datetime, timedelta

app = FastAPI(title="TokenMetrics API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/v1/metrics/summary")
def get_metrics_summary():
    # Dynamic KPI aggregates
    total_tokens = random.randint(1_100_000, 1_500_000)
    total_cost = round(total_tokens * 0.000012 + random.uniform(1.0, 3.0), 2)
    avg_latency = random.randint(95, 145)
    
    # 24-hour time-series data for line chart
    now = datetime.now()
    hourly_trends = []
    for i in range(24):
        timestamp = (now - timedelta(hours=23 - i)).strftime("%H:00")
        hourly_trends.append({
            "time": timestamp,
            "tokens": random.randint(30_000, 85_000),
            "cost": round(random.uniform(0.4, 1.2), 2),
            "latency": random.randint(80, 180)
        })

    # Model usage distribution for pie/donut chart
    model_breakdown = [
        {"model": "GPT-4o", "usage_pct": 45, "cost": round(total_cost * 0.55, 2)},
        {"model": "Claude 3.5 Sonnet", "usage_pct": 30, "cost": round(total_cost * 0.30, 2)},
        {"model": "Gemini 1.5 Pro", "usage_pct": 15, "cost": round(total_cost * 0.10, 2)},
        {"model": "Llama 3 70B", "usage_pct": 10, "cost": round(total_cost * 0.05, 2)},
    ]

    return {
        "summary": {
            "total_tokens": total_tokens,
            "total_cost": total_cost,
            "avg_latency_ms": avg_latency,
            "active_models": 4,
            "system_status": "Healthy"
        },
        "hourly_trends": hourly_trends,
        "model_breakdown": model_breakdown
    }