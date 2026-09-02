from pydantic import BaseModel


class MetarResponse(BaseModel):
    station: str
    time: str = ""
    wind: str = ""
    visibility: str = ""
    weather: list[str] = []
    clouds: list[str] = []
    temp: str = ""
    dewpoint: str = ""
    altimeter: str = ""
    remarks: str = ""
    raw: str = ""
    flight_category: str | None = None


class TafForecast(BaseModel):
    text: str


class TafResponse(BaseModel):
    station: str
    issue_time: str = ""
    forecast: list[TafForecast] = []
    raw: str = ""


class BriefingResponse(BaseModel):
    station: str
    metar: MetarResponse | None = None
    taf: TafResponse | None = None


class BatchResponse(BaseModel):
    stations: list[BriefingResponse]


class StationSearchResult(BaseModel):
    icao: str
    name: str
    country: str
    lat: float
    lon: float
