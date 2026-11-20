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


## Architecture
```
User City / Thresholds
        │
        ▼
[ Weather API Client ] ──► Open-Meteo / OpenWeatherMap (or Virtual Simulator)
        │
        ▼
[ Alert Rule Engine ]  ──► Heat / Cold / Rain / Wind / Humidity / AQI Checks
        │
        ├──► FastAPI REST Service (/weather/{city}, /simulate)
        ├──► Streamlit / Web Dashboard (Charts + Station Map)
        └──► Pandas CSV Audit Report + Matplotlib PNG Charts
```

## Quick Start
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env

# Run CLI with live API
python main.py --city "Mumbai"

# Run Virtual Simulation safely offline
python main.py --city "New Delhi" --simulate --scenario heatwave

# Launch FastAPI server
uvicorn app_fastapi:app --reload --port 8000

# Launch Streamlit dashboard
streamlit run app_streamlit.py


## Authors

* **GitHub:** [nandiniverma2009](https://github.com)
* **LinkedIn:** [NandiniVerma](https://linkedin.com)

```
