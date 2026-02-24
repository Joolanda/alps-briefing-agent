import requests
import xmltodict

SLF_CAAML_URL = "https://aws.slf.ch/api/bulletin/caaml"

HEADERS = {
    "User-Agent": "alps-briefing-agent/1.0 (learning project)",
    "Accept": "application/xml",
}

def fetch_slf_bulletin_parsed() -> dict:
    r = requests.get(SLF_CAAML_URL, headers=HEADERS, timeout=30)
    r.raise_for_status()

    content = r.content
    ct = (r.headers.get("content-type") or "").lower()
    first = content.lstrip()[:50].lower()

    # common case: HTML response (redirect/WAF/maintenance)
    if b"<html" in first or b"<!doctype html" in first:
        preview = content[:400].decode("utf-8", "replace")
        raise ValueError(
            f"SLF did not return XML (content-type={ct}, url={r.url}). Preview:\n{preview}"
        )

    try:
        return xmltodict.parse(content)
    except Exception as e:
        preview = content[:400].decode("utf-8", "replace")
        raise ValueError(
            f"Could not parse SLF response as XML (content-type={ct}, url={r.url}). Preview:\n{preview}"
        ) from e