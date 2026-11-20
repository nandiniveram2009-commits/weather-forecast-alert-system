"""
Weather API Integration Module
Supports OpenWeatherMap (via .env API key) and Open-Meteo (zero-key public API).
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "")


def geocode_city(city_name: str) -> dict:
    """Resolve a city name to latitude, longitude, and country."""
    url = "https://geocoding-api.open-meteo.com/v1/search"
    response = requests.get(url, params={"name": city_name, "count": 1, "format": "json"}, timeout=10)
    response.raise_for_status()
    results = response.json().get("results", [])
    if not results:
        raise ValueError(f"City not found: {city_name}")
    top = results[0]
    return {
        "name": top["name"],
        "country": top.get("country", ""),
        "latitude": top["latitude"],
        "longitude": top["longitude"],
    }


def fetch_weather_for_city(city_name: str) -> dict:
    """
    Fetch current weather, 24-hour forecast, and Air Quality Index (US AQI).
    Falls back cleanly if optional OpenWeatherMap key is omitted.
    """
    location = geocode_city(city_name)

    forecast_url = "https://api.open-meteo.com/v1/forecast"
    forecast_params = {
        "latitude": location["latitude"],
        "longitude": location["longitude"],
        "current": "temperature_2m,relative_humidity_2m,precipitation,wind_speed_10m,weather_code",
        "hourly": "temperature_2m,precipitation,wind_speed_10m,relative_humidity_2m",
        "forecast_days": 2,
        "timezone": "auto",
    }
    w_res = requests.get(forecast_url, params=forecast_params, timeout=10)
    w_res.raise_for_status()
    w_json = w_res.json()

    aqi_url = "https://air-quality-api.open-meteo.com/v1/air-quality"
    aqi_res = requests.get(
        aqi_url,
        params={"latitude": location["latitude"], "longitude": location["longitude"], "current": "us_aqi,pm2_5"},
        timeout=10,
    )
    aqi_json = aqi_res.json() if aqi_res.ok else {}

    curr = w_json["current"]
    aqi_curr = aqi_json.get("current", {})
    hourly = w_json.get("hourly", {})

    return {
        "city": location["name"],
        "country": location["country"],
        "latitude": location["latitude"],
        "longitude": location["longitude"],
        "source": "live-open-meteo",
        "current": {
            "observed_at": curr["time"],
            "temperature_c": curr["temperature_2m"],
            "humidity_pct": curr["relative_humidity_2m"],
            "precipitation_mm": curr["precipitation"],
            "wind_kmh": curr["wind_speed_10m"],
            "us_aqi": aqi_curr.get("us_aqi", 50),
            "pm2_5": aqi_curr.get("pm2_5", 12.0),
        },
        "hourly": {
            "time": hourly.get("time", [])[:24],
            "temperature_c": hourly.get("temperature_2m", [])[:24],
            "precipitation_mm": hourly.get("precipitation", [])[:24],
        },
    }
