"""
FastAPI REST API Server
Run locally: uvicorn app_fastapi:app --reload --port 8000
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.weather_api import fetch_weather_for_city
from src.alert_engine import evaluate_weather_alerts, DEFAULT_THRESHOLDS

app = FastAPI(title="Weather Forecast & Alert API", version="1.0.0")


class SimulationPayload(BaseModel):
    city: str = "Virtual Station"
    temperature_c: float
    humidity_pct: float
    precipitation_mm: float
    wind_kmh: float
    us_aqi: int = 50


@app.get("/weather/{city}")
def get_city_weather(city: str):
    try:
        data = fetch_weather_for_city(city)
        alerts = evaluate_weather_alerts(data["current"], DEFAULT_THRESHOLDS)
        return {"telemetry": data, "alerts": alerts}
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@app.post("/simulate")
def simulate_weather(payload: SimulationPayload):
    current = payload.model_dump()
    alerts = evaluate_weather_alerts(current, DEFAULT_THRESHOLDS)
    return {"city": payload.city, "simulated": current, "alerts": alerts}
