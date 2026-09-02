# Aviation Weather Briefing Bot

Free aviation weather briefing tool — CLI and web app. Fetches **METAR** and **TAF** data from the [aviationweather.gov](https://aviationweather.gov/api/data) API — no API key required.

## CLI

```bash
pip install -r requirements.txt
pip install -e .

weather-bot brief KLAX   # full briefing: METAR + TAF
weather-bot metar KLAX   # METAR only
weather-bot taf KLAX     # TAF only
```

| Flag | Default | Description |
|------|---------|-------------|
| `--hours / -h` | 12 (brief), 3 (metar), 24 (taf) | Lookback window (1–72h) |
| `--raw / -r` | off | Show raw report text |

## Web App

Two-part architecture: FastAPI backend (Render) + React frontend (Netlify).

### Backend

```bash
pip install -r api/requirements.txt
uvicorn api.main:app --reload
```

Endpoints: `/api/weather/brief`, `/api/weather/metar`, `/api/weather/taf`, `/api/airports/search`

### Frontend

```bash
cd web && npm install && npm run dev
```

Set `VITE_API_URL` env var to your backend URL in production.

### Deploy

- **Backend**: Push to GitHub → deploy on Render (free tier)
- **Frontend**: Push to GitHub → deploy on Netlify (free tier)

## Data source

Primary: [Aviation Weather Center API](https://aviationweather.gov/api/data) — US government, free, no key.