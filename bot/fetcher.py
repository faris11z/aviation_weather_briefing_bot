import httpx

BASE_URL = "https://aviationweather.gov/api/data"


async def get_metar(station: str, hours: int = 3) -> list[dict]:
    url = f"{BASE_URL}/metar"
    params = {"ids": station, "format": "json", "hours": str(hours)}
    async with httpx.AsyncClient(timeout=30) as client:
        r = await client.get(url, params=params)
        if r.status_code == 204:
            return []  # API returns 204 when no data in window
        r.raise_for_status()
        data = r.json()
    return data if isinstance(data, list) else []


async def get_taf(station: str) -> list[dict]:
    url = f"{BASE_URL}/taf"
    params = {"ids": station, "format": "json"}
    async with httpx.AsyncClient(timeout=30) as client:
        r = await client.get(url, params=params)
        if r.status_code == 204:
            return []
        r.raise_for_status()
        data = r.json()
    return data if isinstance(data, list) else []
