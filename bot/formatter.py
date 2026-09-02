from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

console = Console()


def print_metar(parsed: dict) -> None:
    """Print a parsed METAR as a nice table."""
    table = Table(title=f"METAR — {parsed.get('station', '?')}", box=None)
    table.add_column("Field", style="cyan")
    table.add_column("Value")

    table.add_row("Time", parsed.get("time", ""))
    table.add_row("Wind", parsed.get("wind", ""))
    table.add_row("Visibility", parsed.get("visibility", ""))
    table.add_row("Weather", " ".join(parsed.get("weather", [])))
    table.add_row("Clouds", " ".join(parsed.get("clouds", [])))
    table.add_row("Temp/Dew", f"{parsed.get('temp', '')}/{parsed.get('dewpoint', '')}")
    table.add_row("Altimeter", parsed.get("altimeter", ""))
    table.add_row("Remarks", parsed.get("remarks", ""))

    console.print(Panel(table, box=box.ROUNDED))


def print_taf(parsed: dict) -> None:
    """Print a parsed TAF as a nice table."""
    table = Table(title=f"TAF — {parsed.get('station', '?')}", box=None)
    table.add_column("Period", style="cyan")
    table.add_column("Forecast")

    table.add_row("Issued", parsed.get("issue_time", ""))
    for fc in parsed.get("forecast", []):
        table.add_row("→", fc.get("text", ""))

    console.print(Panel(table, box=box.ROUNDED))


def print_briefing(station: str, metar: dict, taf: dict) -> None:
    """Print a full weather briefing (METAR + TAF) for one station."""
    console.print(f"\n  ✈  WEATHER BRIEFING — {station}", style="bold yellow")
    print_metar(metar)
    print_taf(taf)
    console.print()
