import asyncio
import sys

import typer

from . import fetcher, parser, formatter

app = typer.Typer(help="Aviation weather briefing bot — free METAR/TAF from aviationweather.gov")


@app.command()
def brief(stations: str = typer.Argument(..., help="ICAO codes, comma-separated (e.g. KLAX,KJFK)"),
          hours: int = typer.Option(12, "--hours", "-h", min=1, max=72),
          raw: bool = typer.Option(False, "--raw", "-r")):
    """Show METAR + TAF for given airports."""
    asyncio.run(_brief(stations, hours, raw))


@app.command()
def metar(stations: str = typer.Argument(..., help="ICAO codes, comma-separated"),
          hours: int = typer.Option(3, "--hours", "-h", min=1, max=72),
          raw: bool = typer.Option(False, "--raw", "-r")):
    """Show current METAR reports."""
    asyncio.run(_metar(stations, hours, raw))


@app.command()
def taf(stations: str = typer.Argument(..., help="ICAO codes, comma-separated"),
        hours: int = typer.Option(24, "--hours", "-h", min=1, max=72)):
    """Show TAF forecasts."""
    asyncio.run(_taf(stations, hours))


def _parse_stations(stations: str) -> list[str]:
    """Turn 'KLAX,KJFK' or 'KLAX KJFK' into ['KLAX', 'KJFK']."""
    return [s.strip().upper() for s in stations.replace(",", " ").split() if s.strip()]


async def _brief(stations: str, hours: int, raw: bool) -> None:
    station_list = _parse_stations(stations)
    codes = " ".join(station_list)

    metar_data = await fetcher.get_metar(codes, hours)
    taf_data = await fetcher.get_taf(codes)

    metar_by_station = {m.get("icaoId", "").upper(): m for m in metar_data}
    taf_by_station = {t.get("icaoId", "").upper(): t for t in taf_data}

    for s in station_list:
        s = s.upper()
        m = metar_by_station.get(s)
        t = taf_by_station.get(s)

        if raw and m:
            console_metar = {"station": s, "time": "", "wind": "", "visibility": "",
                             "weather": [], "clouds": [], "temp": "", "dewpoint": "",
                             "altimeter": "", "remarks": "", "raw": m.get("rawOb", "")}
            formatter.print_metar(console_metar)
        elif m:
            parsed = parser.parse_metar(m.get("rawOb", ""))
            formatter.print_metar(parsed)
        else:
            print(f"No METAR data for {s}")

        if t:
            parsed = parser.parse_taf(t.get("rawTAF", ""))
            formatter.print_taf(parsed)
        else:
            print(f"No TAF data for {s}")

        print()


async def _metar(stations: str, hours: int, raw: bool) -> None:
    station_list = _parse_stations(stations)
    data = await fetcher.get_metar(" ".join(station_list), hours)

    for s in station_list:
        s = s.upper()
        found = [r for r in data if r.get("icaoId", "").upper() == s]
        if not found:
            print(f"No METAR data for {s}")
            continue
        for report in found:
            if raw:
                print(report.get("rawOb", ""))
            else:
                formatter.print_metar(parser.parse_metar(report.get("rawOb", "")))


async def _taf(stations: str, hours: int) -> None:
    station_list = _parse_stations(stations)
    data = await fetcher.get_taf(" ".join(station_list))

    for s in station_list:
        s = s.upper()
        found = [r for r in data if r.get("icaoId", "").upper() == s]
        if not found:
            print(f"No TAF data for {s}")
            continue
        for report in found:
            formatter.print_taf(parser.parse_taf(report.get("rawTAF", "")))


if __name__ == "__main__":
    app()
