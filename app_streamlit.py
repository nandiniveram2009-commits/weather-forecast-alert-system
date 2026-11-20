"""
Streamlit Weather & Alert Dashboard
Run locally: streamlit run app_streamlit.py
"""

import streamlit as st
import pandas as pd
from src.weather_api import fetch_weather_for_city
from src.simulator import load_simulated_weather
from src.alert_engine import evaluate_weather_alerts

st.set_page_config(page_title="Weather Forecast & Alert App", layout="wide")
st.title("Weather Forecast & Alert Application")

with st.sidebar:
    st.header("Configuration")
    city = st.text_input("City Name", value="New Delhi")
    mode = st.radio("Data Mode", ["Live Public API", "Virtual Simulation"])
    scenario = st.selectbox("Simulation Scenario", ["heatwave", "monsoon", "smog"])
    max_temp = st.slider("Heat Alert Threshold (°C)", 25, 50, 35)
    max_rain = st.slider("Rain Alert Threshold (mm/h)", 1, 30, 8)
    max_wind = st.slider("Wind Alert Threshold (km/h)", 20, 100, 45)
    max_aqi = st.slider("AQI Alert Threshold", 50, 300, 150)

data = (
    load_simulated_weather(city, scenario)
    if mode == "Virtual Simulation"
    else fetch_weather_for_city(city)
)

thresholds = {
    "max_temp_c": max_temp,
    "min_temp_c": 2.0,
    "max_rain_mm": max_rain,
    "max_wind_kmh": max_wind,
    "max_humidity_pct": 85.0,
    "max_aqi": max_aqi,
}

alerts = evaluate_weather_alerts(data["current"], thresholds)

c1, c2, c3, c4 = st.columns(4)
c1.metric("Temperature", f"{data['current']['temperature_c']} °C")
c2.metric("Humidity", f"{data['current']['humidity_pct']} %")
c3.metric("Rainfall", f"{data['current']['precipitation_mm']} mm/h")
c4.metric("US AQI", f"{data['current'].get('us_aqi', 'N/A')}")

st.subheader("Risk Alert Status")
if not alerts:
    st.success("All meteorological metrics are within safe thresholds.")
else:
    for alert in alerts:
        st.error(f"[{alert['severity']}] {alert['title']} — {alert['message']}")

st.subheader("24-Hour Temperature Trend")
df = pd.DataFrame({
    "Time": data["hourly"]["time"],
    "Temperature (°C)": data["hourly"]["temperature_c"],
    "Precipitation (mm)": data["hourly"]["precipitation_mm"],
})
st.line_chart(df.set_index("Time")["Temperature (°C)"])
