"""
Weather Forecast & Alert Application - CLI Entry Point
Orchestrates live API fetching (or virtual simulation fallback),
risk alert evaluation, Matplotlib visualization, and CSV report export.
"""

import argparse
from src.weather_api import fetch_weather_for_city
from src.simulator import load_simulated_weather
from src.alert_engine import evaluate_weather_alerts, DEFAULT_THRESHOLDS
from src.visualizer import plot_temperature_and_rain_chart
from src.report_generator import save_weather_report_csv


def main():
    parser = argparse.ArgumentParser(description="Weather Forecast & Alert Application")
    parser.add_argument("--city", type=str, default="New Delhi", help="Target city name")
    parser.add_argument("--simulate", action="store_true", help="Use virtual simulation sample data")
    parser.add_argument("--scenario", type=str, default="heatwave", help="Simulation scenario key")
    args = parser.parse_args()

    print(f"\n[1/4] Fetching weather telemetry for: {args.city}")
    if args.simulate:
        weather_data = load_simulated_weather(args.city, args.scenario)
    else:
        weather_data = fetch_weather_for_city(args.city)

    current = weather_data["current"]
    print(f"      Temperature : {current['temperature_c']} °C")
    print(f"      Humidity    : {current['humidity_pct']} %")
    print(f"      Rainfall    : {current['precipitation_mm']} mm/h")
    print(f"      Wind Speed  : {current['wind_kmh']} km/h")
    print(f"      US AQI      : {current.get('us_aqi', 'N/A')}")

    print("\n[2/4] Evaluating risk alert thresholds...")
    alerts = evaluate_weather_alerts(current, DEFAULT_THRESHOLDS)
    if not alerts:
        print("      Status: NOMINAL — No weather thresholds breached.")
    else:
        for alert in alerts:
            print(f"      [{alert['severity'].upper()}] {alert['title']}: {alert['message']}")

    print("\n[3/4] Generating forecast chart...")
    chart_path = plot_temperature_and_rain_chart(weather_data)
    print(f"      Saved chart -> {chart_path}")

    print("\n[4/4] Exporting structured CSV audit report...")
    report_path = save_weather_report_csv(weather_data, alerts)
    print(f"      Saved report -> {report_path}\n")


if __name__ == "__main__":
    main()
