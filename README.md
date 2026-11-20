# 🌦️ Weather Forecast & Alert Application

An end-to-end Python application that fetches real-time (or simulated) weather, forecast, and Air Quality Index (AQI) data, evaluates multi-hazard risk alerts, serves results via a **FastAPI** REST API, generates **Matplotlib** charts & CSV/Markdown reports, and visualizes interactive maps and warnings on a **Streamlit** dashboard.

## ✨ Features
- **Live & Virtual Simulation Modes:** Integrates with OpenWeatherMap API (`/weather`, `/forecast`, `/air_pollution`) with an offline JSON simulation fallback.
- **Multi-Hazard Alert Engine:** Evaluates Heat, Cold, Heavy Rain/Storm, High Wind, Humidity, and AQI thresholds.
- **FastAPI Backend:** Exposes `/health`, `/weather/{city}`, and `/alerts/{city}` endpoints with Swagger documentation.
- **Interactive Streamlit Dashboard:** Displays KPI cards, color-coded alert banners, trend charts, city maps, and CSV downloads.
- **Automated Reporting:** Exports forecast `.csv` files, `.md` alert reports, and `.png` Matplotlib visualizations.

## 🛠️ Tech Stack
- **Language:** Python 3.10+
- **Data & Visualization:** Pandas, Matplotlib, Streamlit
- **API & Networking:** FastAPI, Uvicorn, Requests, python-dotenv

## 🚀 Quick Start
```bash
git clone https://github.com/<your-username>/Weather-Forecast-Alert-Application.git
cd Weather-Forecast-Alert-Application
python -m venv venv
# Windows: venv\Scripts\activate | Mac/Linux: source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
