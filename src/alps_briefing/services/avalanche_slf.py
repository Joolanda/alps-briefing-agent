import requests

SLF_BULLETIN_URL = "https://aws.slf.ch/api/bulletin/caaml/v4"


def fetch_slf_bulletin(lang: str = "en") -> dict:
    url = f"{SLF_BULLETIN_URL}/{lang}/geojson"
    headers = {"User-Agent": "alps-briefing-agent/1.0 (learning project)"}
    r = requests.get(url, headers=headers, timeout=20)
    r.raise_for_status()
    return r.json()


