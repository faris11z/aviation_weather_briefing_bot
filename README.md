# Aviation Weather Briefing Bot

Free, CLI-based aviation weather briefing bot. Fetches **METAR** and **TAF** data from the [aviationweather.gov](https://aviationweather.gov/api/data) API — no API key required.

## Quick start

```bash
pip install -r requirements.txt
pip install -e .

weather-bot brief KLAX   # full briefing: METAR + TAF
weather-bot metar KLAX   # METAR only
weather-bot taf KLAX     # TAF only
```

## Commands

| Command | Description |
|---------|-------------|
| `brief <stations>` | Full weather briefing (METAR + TAF) |
| `metar <stations>` | Current METAR reports |
| `taf <stations>` | Terminal Aerodrome Forecasts |

### Options

| Flag | Default | Description |
|------|---------|-------------|
| `--hours / -h` | 12 (brief), 3 (metar), 24 (taf) | Lookback window (1–72h) |
| `--raw / -r` | off | Show raw report text |

### Examples

```bash
# Briefing for multiple airports
weather-bot brief KLAX,KLAS,KSEA

# Get raw METARs for the last 6 hours
weather-bot metar KLAX --hours 6 --raw

# TAF only
weather-bot taf EGLL
```

## Data source

Primary: [Aviation Weather Center API](https://aviationweather.gov/api/data) — US government, free, no key.

Alternatives (add your own integration):
- [CheckWX API](https://www.checkwxapi.com/) — free tier, global coverage, JSON
- [AVWX API](https://info.avwx.rest/) — free hobby tier, English-translated METARs