from __future__ import annotations

from rich.console import Console
from rich.table import Table
from rich.text import Text

console = Console()


def fmt_metar(report: dict) -> Table:
    table = Table(title=f"METAR — {report.get('station', '?')}", box=None)
    table.add_column("Field", style="cyan")
    table.add_column("Value", style="white")

    table.add_row("Time", report.get("time", ""))
    table.add_row("Wind", report.get("wind", ""))
    table.add_row("Vis", report.get("visibility", ""))
    table.add_row("Weather", " ".join(report.get("weather", [])))
    table.add_row("Clouds", " ".join(report.get("clouds", [])))

    temp = report.get("temp", "")
    dp = report.get("dewpoint", "")
    table.add_row("Temp/Dew", f"{temp}/{dp}" if dp else temp)

    table.add_row("Altimeter", report.get("altimeter", ""))
    table.add_row("Remarks", report.get("remarks", ""))

    return table


def fmt_metar_raw(raw: str, station: str) -> Table:
    table = Table(title=f"METAR — {station}", box=None)
    table.add_column("Raw", style="green")
    table.add_row(raw)
    return table


def fmt_taf(report: dict) -> Table:
    table = Table(title=f"TAF — {report.get('station', '?')}", box=None)
    table.add_column("Period", style="cyan")
    table.add_column("Forecast", style="white")

    table.add_row("Issued", report.get("issue_time", ""))
    for fc in report.get("forecast", []):
        label = fc.get("time", "") or fc.get("text", "")[:20]
        table.add_row(label, fc.get("text", ""))

    return table


def fmt_briefing(
    metar_raw: str | None,
    metar_parsed: dict | None,
    taf_raw: str | None,
    station: str,
) -> None:
    from rich.panel import Panel
    from rich import box

    header = Text(f"\n  ✈  WEATHER BRIEFING — {station}", style="bold yellow")
    console.print(header)

    if metar_parsed:
        console.print()
        console.print(Panel(fmt_metar(metar_parsed), box=box.ROUNDED))
    elif metar_raw:
        console.print()
        console.print(Panel(fmt_metar_raw(metar_raw, station), box=box.ROUNDED))
    else:
        console.print(f"\n  [red]No METAR data for {station}[/red]")

    if taf_raw:
        from .parser import parse_taf
        taf_parsed = parse_taf(taf_raw)
        console.print()
        console.print(Panel(fmt_taf(taf_parsed), box=box.ROUNDED))
    else:
        console.print(f"\n  [red]No TAF data for {station}[/red]")

    console.print()
