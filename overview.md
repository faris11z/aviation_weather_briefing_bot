# Overview

## What this project is

A CLI tool that fetches aviation weather (METARs and TAFs) from the free US government API at `aviationweather.gov` and displays it in a formatted terminal briefing. No API key, no registration, no cost.

## What that output means

You ran `weather-bot brief KLAX` and got two panels:

**METAR** (Meteorological Aerodrome Report) — current observed conditions at KLAX (Los Angeles Intl):
- `Time: 290053Z` — observation time, 0053 UTC on the 29th
- `Wind: 27014KT` — 270° true at 14 knots
- `Vis: 10SM` — 10 statute miles visibility
- `Clouds: FEW010` — few clouds at 1000 ft
- `Temp/Dew: 24/19` — 24°C / 19°C dewpoint
- `Altimeter: A2980` — 29.80 inHg
- `Remarks: RMK AO2 SLP090 T02390189 $` — automated station, sea-level pressure 1009.0 hPa, temp/dew in tenths Celsius, $ = sensor may need maintenance

**TAF** (Terminal Aerodrome Forecast) — 24-30 hour forecast:
- `Issued: 291128Z` — issued 1128 UTC on the 29th
- `2912/3018 VRB04KT P6SM OVC012` — valid 12Z 29th to 18Z 30th, variable 4kt, 6+ SM vis, overcast 1200 ft
- `FM291900 26012KT P6SM SKC` — from 19Z, wind 260/12kt, clear skies
- `FM300600 VRB03KT 5SM BR BKN007` — from 06Z 30th, 5SM with mist, broken at 700 ft

## How the code is organized (4 modules)

```
cli.py          → entry point (typer CLI, 3 commands: brief/metar/taf)
fetcher.py      → async HTTP to aviationweather.gov API, returns JSON
parser.py       → raw METAR/TAF strings → structured dicts
formatter.py    → structured dicts → rich terminal tables + panels
```

**`cli.py`** — defines 3 commands using `typer`. Each command calls `asyncio.run()` on an async handler that fetches, parses, and formats. The `brief` command fetches both METAR and TAF for each station in parallel, groups results by ICAO, then passes them to `formatter.fmt_briefing()`.

**`fetcher.py`** — builds a URL like `https://aviationweather.gov/api/data/metar?ids=KLAX&format=json&hours=3` and calls it with `httpx.AsyncClient`. Returns a list of dicts from the JSON array. Supports `metar` and `taf` types, JSON/XML formats, and 1-72 hour lookback.

**`parser.py`** — two functions: `parse_metar()` and `parse_taf()`. Both walk the tokenized raw string sequentially, extracting fields by position and pattern recognition:
- METAR: detects `METAR`/`SPECI` prefix, 4-letter ICAO, `ddhhmmZ` time, wind (`dddf(f)G?ffKT`), visibility, weather codes (`-RA`, `BR`, `FG`...), cloud layers (`FEWnnn`, `SCTnnn`, `BKNnnn`, `OVCnnn`), temp/dew (`tt/dd`), altimeter (`Annnn` or `Qnnnn`), remarks.
- TAF: splits on change indicators (`FM`, `TEMPO`, `BECMG`, `PROB`) into forecast groups.

**`formatter.py`** — uses `rich.Table` and `rich.Panel` to render parsed data as terminal-formatted output.

## Similar existing projects

| Project | Language | Notes |
|---------|----------|-------|
| [metar-cli](https://pypi.org/project/metar-cli/) | Python | Same API, same concept, more mature (interactive mode, persistent config) |
| [qwx](https://github.com/iwyatt/qwx) | Rust | Fast, minimal, emoji-rich, also does zip/city lookups via Open-Meteo |
| [WxCraft](https://github.com/rmitchellscott/WxCraft) | Go | Decodes METAR/TAF into plain English, nearest-airport-by-IP, pipe support |
| [AviatorsBot](https://github.com/fvalka/AviatorsBot) | Scala | Telegram bot with METAR/TAF subscriptions, crosswind calc, SIGMET maps |
| [zdc](https://crates.io/crates/zdc) | Rust | vZDC-specific CLI (charts, preferred routes, weather) |

All the CLI tools above use the same `aviationweather.gov` API. This project is lighter-weight than most — no config files, no persistent state, just pass ICAO codes as arguments.

## What differentiates this project

- **Simplicity-first**: no config files, no interactive mode, no database. Pass ICAOs and get output. Three commands.
- **Briefing mode**: the `brief` command combines METAR + TAF in a single view, mimicking the structure of a standard aviation weather briefing.
- **Pure Python async**: uses `httpx` async for concurrent API calls across multiple stations.
- **No external API keys**: aviationweather.gov requires zero registration.

## Limitations

- No winds aloft, SIGMETs, AIRMETs, NOTAMs, or TFRs
- No plain-English decoding (unlike WxCraft)
- No persistent config or default stations (unlike metar-cli)
- Terminal-only, no Telegram/Discord integration (unlike AviatorsBot)
