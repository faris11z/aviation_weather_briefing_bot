from __future__ import annotations

import re

METAR_RE = re.compile(
    r"^(?P<type>SPECI|METAR)\s+"
    r"(?P<station>[A-Z0-9]{4})\s+"
    r"(?P<time>\d{6}Z)\s+"
    r"(?P<wind>\d{3,5}(G\d+)?(KT|MPS|KMH))\s+"
    r"(?P<vis>(\d+)?\s*\d/\d?SM|CAVOK|\d+)\s+"
    r"(?P<remainder>.*)",
    re.DOTALL,
)


def parse_metar(raw: str) -> dict:
    result: dict = {
        "raw": raw.strip(),
        "type": "METAR",
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
    }

    parts = raw.strip().split()
    if not parts:
        return result

    idx = 0
    if parts[idx] in ("METAR", "SPECI"):
        result["type"] = parts[idx]
        idx += 1

    if idx < len(parts) and len(parts[idx]) == 4 and parts[idx].isalpha():
        result["station"] = parts[idx]
        idx += 1

    if idx < len(parts) and parts[idx].endswith("Z") and len(parts[idx]) in (6, 7):
        result["time"] = parts[idx]
        idx += 1

    if idx < len(parts) and re.match(r"\d{3,5}(G\d+)?(KT|MPS|KMH)$", parts[idx]):
        result["wind"] = parts[idx]
        idx += 1

    if idx < len(parts):
        vis = parts[idx]
        if vis in ("CAVOK", "SKC", "CLR", "NSC"):
            result["visibility"] = vis
            idx += 1
        elif "SM" in vis or "KM" in vis or vis.replace("/", "").replace(".", "").replace("-", "").replace("M", "").isdigit():
            result["visibility"] = vis
            idx += 1

    weather_codes = []
    while idx < len(parts):
        p = parts[idx]
        if p in {"CAVOK", "SKC", "CLR", "NSC", "NSW"}:
            idx += 1
            continue
        if re.match(r"^[-+]?(TS|SH|FZ|DZ|RA|SN|SG|IC|PL|GR|GS|UP|BR|FG|FU|VA|DU|SA|HZ|PY|PO|SQ|FC|SS|DS|NSW|MI|BC|DR|BL)$", p) or re.match(r"^[-+]?[A-Z]{2,4}$", p):
            weather_codes.append(p)
            idx += 1
        else:
            break
    result["weather"] = weather_codes

    cloud_layers = []
    while idx < len(parts):
        p = parts[idx]
        if re.match(r"^(FEW|SCT|BKN|OVC|VV)\d{3}", p):
            cloud_layers.append(p)
            idx += 1
        elif p in ("SKC", "CLR", "NSC", "NCD", "VV"):
            cloud_layers.append(p)
            idx += 1
        else:
            break
    result["clouds"] = cloud_layers

    if idx < len(parts) and "/" in parts[idx]:
        temp_dew = parts[idx]
        if "/" in temp_dew:
            t, d = temp_dew.split("/", 1)
            result["temp"] = t
            result["dewpoint"] = d
            idx += 1

    if idx < len(parts) and parts[idx].startswith(("A", "Q")):
        result["altimeter"] = parts[idx]
        idx += 1

    if idx < len(parts):
        result["remarks"] = " ".join(parts[idx:])

    return result


TAF_FCST_RE = re.compile(r"^(FM|TEMPO|BECMG|PROB)")


def parse_taf(raw: str) -> dict:
    result: dict = {
        "raw": raw.strip(),
        "type": "TAF",
        "station": "",
        "issue_time": "",
        "valid_from": "",
        "valid_to": "",
        "forecast": [],
    }

    parts = raw.strip().split()
    if not parts:
        return result

    idx = 0
    if parts[idx] == "TAF":
        idx += 1

    if idx < len(parts) and len(parts[idx]) == 4 and parts[idx].isalpha():
        result["station"] = parts[idx]
        idx += 1

    if idx < len(parts) and parts[idx].endswith("Z"):
        result["issue_time"] = parts[idx]
        idx += 1

    if idx < len(parts) and re.match(r"\d{2}/\d{2} \d{2}:\d{2}", parts[idx]):
        pass

    fcst_groups = []
    current_group = [parts[idx]] if idx < len(parts) else []
    idx += 1

    while idx < len(parts):
        p = parts[idx]
        if TAF_FCST_RE.match(p):
            if current_group:
                fcst_groups.append(" ".join(current_group))
            current_group = [p]
        else:
            current_group.append(p)
        idx += 1

    if current_group:
        fcst_groups.append(" ".join(current_group))

    if fcst_groups:
        result["forecast"] = [{"text": g} for g in fcst_groups]

    return result
