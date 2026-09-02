import httpx

BASE_URL = "https://aviationweather.gov/api/data"


async def get_metar(station: str, hours: int = 3) -> list[dict]:
    url = f"{BASE_URL}/metar"
    params = {"ids": station, "format": "json", "hours": str(hours)}
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            r = await client.get(url, params=params)
        if r.status_code == 204 or r.status_code != 200:
            return []  # no data in window, or upstream error
        data = r.json()
    except Exception:
        return []  # timeout / network / parsing error -> treat as no data
    return data if isinstance(data, list) else []


async def get_taf(station: str) -> list[dict]:
    url = f"{BASE_URL}/taf"
    params = {"ids": station, "format": "json"}
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            r = await client.get(url, params=params)
        if r.status_code == 204 or r.status_code != 200:
            return []
        data = r.json()
    except Exception:
        return []
    return data if isinstance(data, list) else []
