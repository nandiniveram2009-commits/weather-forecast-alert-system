"""
Visualization Module
Creates high-DPI Matplotlib charts saved into images/ for GitHub README documentation.
"""

from pathlib import Path
import matplotlib.pyplot as plt


def plot_temperature_and_rain_chart(weather_data: dict) -> str:
    output_dir = Path(__file__).resolve().parent.parent / "images"
    output_dir.mkdir(parents=True, exist_ok=True)

    times = [t[-5:] for t in weather_data["hourly"]["time"][:12]]
    temps = weather_data["hourly"]["temperature_c"][:12]
    rains = weather_data["hourly"]["precipitation_mm"][:12]

    fig, ax1 = plt.subplots(figsize=(10, 4.5), dpi=150)
    ax1.plot(times, temps, color="#2563EB", marker="o", linewidth=2, label="Temperature (°C)")
    ax1.set_ylabel("Temperature (°C)", color="#2563EB")
    ax1.tick_params(axis="x", rotation=35)
    ax1.grid(True, linestyle="--", alpha=0.3)

    ax2 = ax1.twinx()
    ax2.bar(times, rains, color="#06B6D4", alpha=0.35, width=0.5, label="Precipitation (mm)")
    ax2.set_ylabel("Precipitation (mm)", color="#0891B2")

    plt.title(f"12-Hour Weather Forecast — {weather_data['city']} ({weather_data['source']})")
    fig.tight_layout()

    safe_city = weather_data["city"].lower().replace(" ", "_")
    out_file = output_dir / f"{safe_city}_forecast.png"
    plt.savefig(out_file)
    plt.close(fig)
    return str(out_file)
