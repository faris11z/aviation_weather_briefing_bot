from __future__ import annotations

import asyncio

import typer
from rich import print as rprint

from . import fetcher, parser, formatter

app = typer.Typer(
    name="weather-bot",
    help="Aviation weather briefing bot — free METAR/TAF from aviationweather.gov",
)


@app.command()
def brief(
    stations: str = typer.Argument(
        ...,
        help="ICAO station codes (comma/space-separated, e.g. KLAX,EGLL)",
    ),
    hours: int = typer.Option(
        12,
        "--hours", "-h",
        help="Lookback window in hours (1-72)",
        min=1,
        max=72,
    ),
    raw: bool = typer.Option(
        False,
        "--raw", "-r",
        help="Show raw METAR text instead of parsed table",
    ),
) -> None:
    asyncio.run(_brief(stations, hours, raw))


@app.command()
def metar(
    stations: str = typer.Argument(
        ...,
        help="ICAO station codes (comma/space-separated)",
    ),
    hours: int = typer.Option(
        3,
        "--hours", "-h",
        help="Lookback window in hours (1-72)",
        min=1,
        max=72,
    ),
    raw: bool = typer.Option(
        False,
        "--raw", "-r",
        help="Show raw METAR text",
    ),
) -> None:
    asyncio.run(_print_reports("metar", stations, hours, raw))


@app.command()
def taf(
    stations: str = typer.Argument(
        ...,
        help="ICAO station codes (comma/space-separated)",
    ),
    hours: int = typer.Option(
        24,
        "--hours", "-h",
        help="Lookback window in hours (1-72)",
        min=1,
        max=72,
    ),
) -> None:
    asyncio.run(_print_tafs(stations, hours))


async def _brief(stations: str, hours: int, raw: bool) -> None:
    station_list = _resolve_stations(stations)

    async with httpx_client() as client:
        metar_data = await fetcher.fetch_weather("metar", " ".join(station_list), hours, client=client)
        taf_data = await fetcher.fetch_weather("taf", " ".join(station_list), hours * 2, client=client)

    metar_by_station: dict[str, dict | str] = {}
    for m in metar_data:
        sid = _station_id(m)
        if sid:
            if raw:
                metar_by_station[sid] = m.get("rawOb", "")
            else:
                raw_text = m.get("rawOb", "")
                metar_by_station[sid] = parser.parse_metar(raw_text) if raw_text else {}

    taf_by_station: dict[str, str] = {}
    for t in taf_data:
        sid = _station_id(t)
        if sid:
            taf_by_station[sid] = t.get("rawTAF", "")

    for station in station_list:
        s = station.upper()
        m_raw = None
        m_parsed = None
        if s in metar_by_station:
            entry = metar_by_station[s]
            if isinstance(entry, str):
                m_raw = entry
            else:
                m_parsed = entry
                m_raw = entry.get("raw", "")

        t_raw = taf_by_station.get(s, "")
        formatter.fmt_briefing(m_raw, m_parsed, t_raw, s)


async def _print_reports(report_type: str, stations: str, hours: int, raw: bool = False) -> None:
    station_list = _resolve_stations(stations)

    async with httpx_client() as client:
        data = await fetcher.fetch_weather(report_type, " ".join(station_list), hours, client=client)

    for station in station_list:
        s = station.upper()
        found = [r for r in data if _station_id(r) == s]
        if not found:
            rprint(f"[red]No {report_type.upper()} data for {s}[/red]")
            continue
        for report in found:
            raw_text = report.get("rawOb", "")
            if report_type == "metar" and not raw:
                parsed = parser.parse_metar(raw_text) if raw_text else {}
                formatter.console.print(formatter.fmt_metar(parsed))
            else:
                formatter.console.print(formatter.fmt_metar_raw(raw_text, s))


async def _print_tafs(stations: str, hours: int) -> None:
    station_list = _resolve_stations(stations)

    async with httpx_client() as client:
        data = await fetcher.fetch_weather("taf", " ".join(station_list), hours, client=client)

    for station in station_list:
        s = station.upper()
        found = [r for r in data if _station_id(r) == s]
        if not found:
            rprint(f"[red]No TAF data for {s}[/red]")
            continue
        for report in found:
            raw_text = report.get("rawTAF", "")
            parsed = parser.parse_taf(raw_text) if raw_text else {}
            formatter.console.print(formatter.fmt_taf(parsed))


def _station_id(report: dict) -> str:
    return (report.get("icaoId") or report.get("stationId") or "").upper()


def _resolve_stations(stations: str) -> list[str]:
    return [s.strip().upper() for s in stations.replace(",", " ").split() if s.strip()]


def httpx_client():
    import httpx
    return httpx.AsyncClient(timeout=30.0)


if __name__ == "__main__":
    app()
