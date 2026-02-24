from __future__ import annotations

from datetime import datetime, timezone
import requests

BASE = "https://aws.slf.ch/api/bulletin/caaml"
HEADERS = {
    "User-Agent": "alps-briefing-agent/1.0 (learning project)",
    "Accept": "application/json",
}


def fetch_slf_bulletin(lang: str = "en", active_at: datetime | None = None) -> dict:
    # IMPORTANT: lang is in the PATH (…/caaml/en/json), not as ?lang=en
    url = f"{BASE}/{lang}/json"

    params: dict[str, str] = {}
    if active_at is not None:
        params["activeAt"] = (
            active_at.astimezone(timezone.utc)
            .replace(microsecond=0)
            .strftime("%Y-%m-%dT%H:%M:%SZ")
        )

    r = requests.get(url, params=params, headers=HEADERS, timeout=30)
    r.raise_for_status()

    # guardrail: if it ever returns HTML, fail with a clear message
    ct = (r.headers.get("content-type") or "").lower()
    if "html" in ct:
        raise ValueError(f"SLF returned HTML, not JSON. content-type={ct} url={r.url}")

    return r.json()