import requests

def fetch_weather(lat: float, lon: float) -> dict:
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum,wind_speed_10m_max",
        "timezone": "auto",
    }
    r = requests.get(url, params=params, timeout=20)
    r.raise_for_status()
    j = r.json()
    d = j["daily"]

    return {
        "date": d["time"][0],
        "t_max": d["temperature_2m_max"][0],
        "t_min": d["temperature_2m_min"][0],
        "precip_sum": d["precipitation_sum"][0],
        "wind_max": d["wind_speed_10m_max"][0],
    }