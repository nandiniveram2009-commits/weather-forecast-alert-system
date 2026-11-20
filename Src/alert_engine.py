"""
Risk Alert Rule Engine
Evaluates meteorological measurements against configurable thresholds.
"""

DEFAULT_THRESHOLDS = {
    "max_temp_c": 35.0,
    "min_temp_c": 2.0,
    "max_rain_mm": 7.5,
    "max_wind_kmh": 45.0,
    "max_humidity_pct": 85.0,
    "max_aqi": 150,
}


def evaluate_weather_alerts(current: dict, thresholds: dict = None) -> list:
    """Compare current readings against risk thresholds and return structured alerts."""
    rules = thresholds or DEFAULT_THRESHOLDS
    alerts = []

    temp = current["temperature_c"]
    humidity = current["humidity_pct"]
    rain = current["precipitation_mm"]
    wind = current["wind_kmh"]
    aqi = current.get("us_aqi", 0)

    if temp >= rules["max_temp_c"]:
        severity = "Severe" if temp >= rules["max_temp_c"] + 5 else "Warning"
        alerts.append({
            "metric": "Temperature",
            "severity": severity,
            "title": "Extreme Heat Alert",
            "message": f"Temperature {temp} °C exceeds threshold {rules['max_temp_c']} °C.",
        })

    if temp <= rules["min_temp_c"]:
        alerts.append({
            "metric": "Temperature",
            "severity": "Warning",
            "title": "Freeze Advisory",
            "message": f"Temperature {temp} °C dropped below {rules['min_temp_c']} °C.",
        })

    if rain >= rules["max_rain_mm"]:
        severity = "Severe" if rain >= rules["max_rain_mm"] * 2 else "Warning"
        alerts.append({
            "metric": "Precipitation",
            "severity": severity,
            "title": "Heavy Rain & Flood Risk",
            "message": f"Rainfall rate {rain} mm/h exceeds {rules['max_rain_mm']} mm/h.",
        })

    if wind >= rules["max_wind_kmh"]:
        severity = "Severe" if wind >= rules["max_wind_kmh"] * 1.4 else "Warning"
        alerts.append({
            "metric": "Wind",
            "severity": severity,
            "title": "High Wind Advisory",
            "message": f"Wind speed {wind} km/h exceeds {rules['max_wind_kmh']} km/h.",
        })

    if humidity >= rules["max_humidity_pct"]:
        alerts.append({
            "metric": "Humidity",
            "severity": "Advisory",
            "title": "High Humidity Alert",
            "message": f"Relative humidity {humidity}% exceeds {rules['max_humidity_pct']}%.",
        })

    if aqi >= rules["max_aqi"]:
        severity = "Severe" if aqi >= 200 else "Warning"
        alerts.append({
            "metric": "Air Quality",
            "severity": severity,
            "title": "Unhealthy Air Quality Alert",
            "message": f"US AQI {aqi} exceeds safety limit {rules['max_aqi']}.",
        })

    return alerts
