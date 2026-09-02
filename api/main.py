import sys
import time
from pathlib import Path

import httpx
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

# so we can import bot/ from here
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from bot.parser import parse_metar, parse_taf
from bot.fetcher import get_metar, get_taf

from .models import (
    BatchResponse, BriefingResponse, MetarResponse,
    StationInfo, StationSearchResult, TafForecast, TafResponse,
)

BASE_URL = "https://aviationweather.gov/api/data"

# simple in-memory cache: key -> (timestamp, data)
cache: dict[str, tuple[float, object]] = {}
CACHE_TTL = 10  # seconds


def cached(key: str):
    """Return cached data if fresh enough, else None."""
    if key in cache:
        ts, data = cache[key]
        if time.time() - ts < CACHE_TTL:
            return data
        del cache[key]
    return None


def cache_set(key: str, data: object):
    cache[key] = (time.time(), data)


app = FastAPI(title="Aviation Weather API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def build_metar_response(data: dict) -> MetarResponse:
    raw = data.get("rawOb", "")
    parsed = parse_metar(raw) if raw else {}
    return MetarResponse(
        station=data.get("icaoId", ""),
        time=parsed.get("time", ""),
        wind=parsed.get("wind", ""),
        visibility=parsed.get("visibility", ""),
        weather=parsed.get("weather", []),
        clouds=parsed.get("clouds", []),
        temp=parsed.get("temp", ""),
        dewpoint=parsed.get("dewpoint", ""),
        altimeter=parsed.get("altimeter", ""),
        remarks=parsed.get("remarks", ""),
        raw=raw,
        flight_category=data.get("fltCat"),
    )


def build_taf_response(data: dict) -> TafResponse:
    raw = data.get("rawTAF", "")
    parsed = parse_taf(raw) if raw else {}
    return TafResponse(
        station=data.get("icaoId", ""),
        issue_time=parsed.get("issue_time", ""),
        forecast=[TafForecast(text=f["text"]) for f in parsed.get("forecast", [])],
        raw=raw,
    )


@app.get("/api/weather/brief")
async def brief(station: str = Query(...), hours: int = Query(12, ge=1, le=72)):
    key = f"brief:{station}:{hours}"
    cached_data = cached(key)
    if cached_data:
        return cached_data

    station_list = [s.strip().upper() for s in station.replace(",", " ").split() if s.strip()]
    codes = ",".join(station_list)

    metar_data = await get_metar(codes, hours)
    taf_data = await get_taf(codes)

    metar_map = {m.get("icaoId", "").upper(): m for m in metar_data}
    taf_map = {t.get("icaoId", "").upper(): t for t in taf_data}

    results = []
    for s in station_list:
        s = s.upper()
        metar = build_metar_response(metar_map[s]) if s in metar_map else None
        taf = build_taf_response(taf_map[s]) if s in taf_map else None
        results.append(BriefingResponse(station=s, metar=metar, taf=taf))

    resp = BatchResponse(stations=results)
    cache_set(key, resp)
    return resp


@app.get("/api/weather/metar")
async def metar(station: str = Query(...), hours: int = Query(3, ge=1, le=72)):
    key = f"metar:{station}:{hours}"
    cached_data = cached(key)
    if cached_data:
        return cached_data

    data = await get_metar(station, hours)
    resp = [build_metar_response(d) for d in data]
    cache_set(key, resp)
    return resp


@app.get("/api/weather/taf")
async def taf(station: str = Query(...), hours: int = Query(24, ge=1, le=72)):
    key = f"taf:{station}"
    cached_data = cached(key)
    if cached_data:
        return cached_data

    data = await get_taf(station)
    resp = [build_taf_response(d) for d in data]
    cache_set(key, resp)
    return resp


async def fetch_station_info(codes: list[str]) -> list[dict]:
    """Fetch station records from the government API for the given ICAO codes."""
    if not codes:
        return []
    params = {"format": "json", "stype": "all", "ids": ",".join(codes)}
    async with httpx.AsyncClient(timeout=20) as client:
        r = await client.get(f"{BASE_URL}/stationInfo", params=params)
    if r.status_code != 200:
        return []
    data = r.json()
    return data if isinstance(data, list) else []


@app.get("/api/airports/search")
async def search(q: str = Query(..., min_length=1), limit: int = Query(5, ge=1, le=20)):
    # The gov API no longer returns a full world list, so we do a direct
    # lookup on the query as an ICAO code.
    q_upper = q.strip().upper()
    if not (2 <= len(q_upper) <= 4 and q_upper.isalnum()):
        return []

    data = await fetch_station_info([q_upper])
    out = []
    for s in data:
        out.append(StationSearchResult(
            icao=s.get("icaoId", ""),
            name=s.get("site", ""),
            country=s.get("country", ""),
            lat=s.get("lat", 0.0), lon=s.get("lon", 0.0),
        ))
    return out[:limit]


@app.get("/api/airports/info")
async def airport_info(codes: str = Query(..., min_length=1)):
    """Return full-form details for one or more ICAO codes (worldwide)."""
    code_list = [s.strip().upper() for s in codes.replace(",", " ").split() if s.strip()]
    code_list = code_list[:10]  # safety cap

    data = await fetch_station_info(code_list)
    found = {}
    for s in data:
        found[s.get("icaoId", "").upper()] = s

    results = []
    for code in code_list:
        s = found.get(code)
        if s is None:
            results.append(StationInfo(icao=code, name="Not found"))
            continue
        results.append(StationInfo(
            icao=s.get("icaoId", code),
            name=s.get("site", ""),
            iata=s.get("iataId", "") or "",
            faa=s.get("faaId", "") or "",
            wmo=s.get("wmoId", "") or "",
            state=s.get("state", "") or "",
            country=s.get("country", "") or "",
            lat=s.get("lat", 0.0),
            lon=s.get("lon", 0.0),
        ))
    return results
