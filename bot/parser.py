import re


def parse_metar(raw: str) -> dict:
    """Turn a raw METAR string like 'METAR KLAX 021053Z 05004KT 10SM FEW020 18/14 A2998'
    into a dict with keys: type, station, time, wind, visibility, weather, clouds,
    temp, dewpoint, altimeter, remarks, raw."""

    result = {
        "type": "",
        "station": "",
        "time": "",
        "wind": "",
        "visibility": "",
        "weather": [],
        "clouds": [],
        "temp": "",
        "dewpoint": "",
        "altimeter": "",
        "remarks": "",
        "raw": raw.strip(),
    }

    parts = raw.strip().split()
    if not parts:
        return result

    idx = 0

    # METAR or SPECI (special report)
    if parts[idx] in ("METAR", "SPECI"):
        result["type"] = parts[idx]
        idx += 1

    # 4-letter ICAO station code
    if idx < len(parts) and len(parts[idx]) == 4 and parts[idx].isalpha():
        result["station"] = parts[idx]
        idx += 1

    # Time: ddhhmmZ (day, hour, minute, Zulu)
    if idx < len(parts) and parts[idx].endswith("Z") and len(parts[idx]) in (6, 7):
        result["time"] = parts[idx]
        idx += 1

    # Wind: dddssKT or dddssGggKT
    if idx < len(parts) and re.match(r"\d{3,5}(G\d+)?(KT|MPS|KMH)$", parts[idx]):
        result["wind"] = parts[idx]
        idx += 1

    # Visibility: 10SM, 1/2SM, CAVOK
    if idx < len(parts):
        vis = parts[idx]
        if vis in ("CAVOK", "SKC", "CLR", "NSC"):
            result["visibility"] = vis
            idx += 1
        elif "SM" in vis or "KM" in vis:
            result["visibility"] = vis
            idx += 1

    # Weather phenomena: -RA, +TS, BR, etc.
    weather_codes = []
    weather_pattern = re.compile(r"^[-+]?(RA|SN|TS|SH|FG|BR|HZ|DU|SA|FU|VA|PL|GR|GS|DZ|FZ|UP|SQ|FC|SS|DS|BC|PR|MI|DR|BL|NSW)$")
    while idx < len(parts) and weather_pattern.match(parts[idx]):
        weather_codes.append(parts[idx])
        idx += 1
    result["weather"] = weather_codes

    # Cloud layers: FEW020, SCT045, BKN008, OVC015, VV003
    clouds = []
    while idx < len(parts) and re.match(r"^(FEW|SCT|BKN|OVC|VV|SKC|CLR|NSC)\d{0,3}$", parts[idx]):
        clouds.append(parts[idx])
        idx += 1
    result["clouds"] = clouds

    # Temp/Dewpoint: 18/14 or M02/M05 (M = minus)
    if idx < len(parts) and "/" in parts[idx]:
        t, d = parts[idx].split("/", 1)
        result["temp"] = t
        result["dewpoint"] = d
        idx += 1

    # Altimeter: A2998 (inHg) or Q1013 (hPa)
    if idx < len(parts) and parts[idx][:1] in ("A", "Q"):
        result["altimeter"] = parts[idx]
        idx += 1

    # Everything after is remarks
    if idx < len(parts):
        result["remarks"] = " ".join(parts[idx:])

    return result


def parse_taf(raw: str) -> dict:
    """Turn a raw TAF string into a dict with station, issue_time, and forecast groups."""

    result = {
        "station": "",
        "issue_time": "",
        "forecast": [],
        "raw": raw.strip(),
    }

    parts = raw.strip().split()
    if not parts:
        return result

    idx = 0

    # Skip "TAF" prefix
    if parts[idx] == "TAF":
        idx += 1

    # Station code
    if idx < len(parts) and len(parts[idx]) == 4 and parts[idx].isalpha():
        result["station"] = parts[idx]
        idx += 1

    # Issue time
    if idx < len(parts) and parts[idx].endswith("Z"):
        result["issue_time"] = parts[idx]
        idx += 1

    # Split into forecast groups at FM, TEMPO, BECMG, PROB markers
    groups = []
    current = []
    while idx < len(parts):
        if re.match(r"^(FM|TEMPO|BECMG|PROB)", parts[idx]):
            if current:
                groups.append(" ".join(current))
            current = [parts[idx]]
        else:
            current.append(parts[idx])
        idx += 1
    if current:
        groups.append(" ".join(current))

    result["forecast"] = [{"text": g} for g in groups]
    return result
