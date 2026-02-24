import requests

SLF_BULLETIN_URL = "PASTE_YOUR_WORKING_SLF_JSON_ENDPOINT_HERE"

def fetch_slf_bulletin(lang: str = "en") -> dict:
    headers = {"User-Agent": "alps-briefing-agent/1.0 (learning project)"}
    r = requests.get(SLF_BULLETIN_URL, params={"lang": lang}, headers=headers, timeout=20)
    r.raise_for_status()
    return r.json()