"""
Report Generator Module
Exports city telemetry and triggered alerts into structured CSV files using Pandas.
"""

from datetime import datetime
from pathlib import Path
import pandas as pd


def save_weather_report_csv(weather_data: dict, alerts: list) -> str:
    reports_dir = Path(__file__).resolve().parent.parent / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)

    curr = weather_data["current"]
    row = {
        "generated_at": datetime.utcnow().isoformat(),
        "city": weather_data["city"],
        "source": weather_data["source"],
        "temperature_c": curr["temperature_c"],
        "humidity_pct": curr["humidity_pct"],
        "precipitation_mm": curr["precipitation_mm"],
        "wind_kmh": curr["wind_kmh"],
        "us_aqi": curr.get("us_aqi", "N/A"),
        "alerts_count": len(alerts),
        "alert_titles": "; ".join([a["title"] for a in alerts]) or "None",
    }

    df = pd.DataFrame([row])
    filename = f"weather_report_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.csv"
    out_path = reports_dir / filename
    df.to_csv(out_path, index=False)
    return str(out_path)
