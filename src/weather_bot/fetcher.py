from __future__ import annotations

import httpx

AVIATIONWEATHER_BASE = "https://aviationweather.gov/api/data"

ICAO_REPORT_TYPES = {"metar", "taf"}
ALLOWED_FORMATS = {"xml", "json"}


def _parse_station_list(stations: str) -> list[str]:
    return [s.strip().upper() for s in stations.replace(",", " ").split() if s.strip()]


def build_params(
    stations: str,
    hours: int = 24,
    fmt: str = "json",
) -> dict[str, str]:
    if fmt not in ALLOWED_FORMATS:
        msg = f"format must be one of {ALLOWED_FORMATS}, got {fmt!r}"
        raise ValueError(msg)

    icaos = _parse_station_list(stations)
    return {
        "ids": ",".join(icaos),
        "format": fmt,
        "hours": str(max(1, min(hours, 72))),
    }


async def fetch_weather(
    report_type: str,
    stations: str,
    hours: int = 24,
    fmt: str = "json",
    client: httpx.AsyncClient | None = None,
) -> list[dict]:
    if report_type not in ICAO_REPORT_TYPES:
        msg = f"report_type must be one of {ICAO_REPORT_TYPES}, got {report_type!r}"
        raise ValueError(msg)

    url = f"{AVIATIONWEATHER_BASE}/{report_type}"
    params = build_params(stations, hours, fmt)
    close = client is None
    c = client or httpx.AsyncClient(timeout=30.0)

    try:
        r = await c.get(url, params=params)
        r.raise_for_status()
        data = r.json()
    finally:
        if close:
            await c.aclose()

    if isinstance(data, list):
        return data
    return []
