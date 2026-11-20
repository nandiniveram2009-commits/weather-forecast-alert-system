"""
Virtual Simulation Module
Replays realistic sample scenarios from data/sample_weather.json without API calls.
"""

import json
from pathlib import Path


def load_simulated_weather(city: str, scenario: str = "heatwave") -> dict:
    sample_path = Path(__file__).resolve().parent.parent / "data" / "sample_weather.json"
    with open(sample_path, "r", encoding="utf-8") as f:
        scenarios = json.load(f)

    chosen = scenarios.get(scenario, scenarios["heatwave"])
    return {
        "city": city,
        "country": "Simulated",
        "latitude": 28.6139,
        "longitude": 77.2090,
        "source": f"simulation-{scenario}",
        "current": chosen["current"],
        "hourly": chosen["hourly"],
    }
