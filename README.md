```markdown
# Alps Briefing Agent (Streamlit)

A small Streamlit app that generates a “mountain day briefing” and includes an MVP chat-style **avalanche gear Q&A**.

## What it does

- Geocodes a place name (e.g., “Andermatt”)
- Fetches weather (via the app’s weather service)
- Fetches avalanche bulletin data from SLF (WSL Institute for Snow and Avalanche Research)
- Answers an MVP question like: **“Do I need avalanche gear in Andermatt tomorrow?”**
  - Uses a minimal place → SLF region mapping (MVP)

> Educational demo only — always rely on the official avalanche bulletin and local guidance.

---

## Project structure (key files)

- `streamlit_app.py` — Streamlit UI
- `src/alps_briefing/services/avalanche_slf.py` — SLF bulletin fetch (`fetch_slf_bulletin`)
- `src/alps_briefing/services/avalanche_gear_qa.py` — MVP Q&A logic (parsing, region pick, gear advice)
- `src/alps_briefing/services/geocoding.py` — geocoding helper

---

## Setup

### 1) Create & activate a virtual environment
```bash
python -m venv .venv
source .venv/bin/activate
```

### 2) Install dependencies
Use whatever your repo is set up for (examples):

```bash
pip install -r requirements.txt
# or, if using a pyproject-based setup:
pip install -e .
```

### 3) Make sure `src/` is importable
If you see `ModuleNotFoundError: alps_briefing`, run:
```bash
export PYTHONPATH="$PWD/src:$PYTHONPATH"
```

---

## SLF bulletin endpoint

In `src/alps_briefing/services/avalanche_slf.py` you need a real endpoint (not the placeholder). A common public endpoint to try is:

```python
SLF_BULLETIN_URL = "https://aws.slf.ch/api/bulletin/caaml"
```

Tip: request JSON explicitly to avoid JSON decoding issues:
```python
headers = {
  "User-Agent": "alps-briefing-agent/1.0 (learning project)",
  "Accept": "application/json",
}
```

If you hit `Expecting value: line 1 column 1 (char 0)`, see **Troubleshooting** below.

---

## Run the app

```bash
streamlit run streamlit_app.py
```

Streamlit will print a local URL (usually `http://localhost:8501`).

---

## Quick smoke tests (before using the UI)

### Syntax check
```bash
python -m py_compile \
  src/alps_briefing/services/avalanche_slf.py \
  src/alps_briefing/services/avalanche_gear_qa.py \
  streamlit_app.py
```

### Test SLF fetch (prints response keys)
```bash
python - <<'PY'
from alps_briefing.services.avalanche_slf import fetch_slf_bulletin
p = fetch_slf_bulletin("en")
print("top-level keys:", list(p.keys()))
PY
```

### Test the Q&A function directly
```bash
python - <<'PY'
from alps_briefing.services.avalanche_gear_qa import answer_avalanche_gear_question
out = answer_avalanche_gear_question("Do I need avalanche gear in Andermatt tomorrow?")
print(out["answer"])
print("danger_level:", out["danger_level"])
print("region_id:", out["region_id"])
PY
```

---

## Test questions to ask in Streamlit

### “Happy path” (should work)
These assume the MVP mapping includes **Andermatt**:
- `Do I need avalanche gear in Andermatt tomorrow?`
- `Do I need avalanche gear in Andermatt today?`
- `Should I bring avalanche gear in Andermatt tomorrow?`
- `Is avalanche gear necessary in Andermatt tomorrow?`

### Error-handling tests (expected to show helpful errors)
- Missing location:
  - `Do I need avalanche gear tomorrow?`
- Missing mapping (unless you add it to `PLACE_TO_REGION_ID`):
  - `Do I need avalanche gear in Zermatt tomorrow?`
- Parser limitation (expects the word “in”):
  - `avalanche gear Andermatt tomorrow`

---

## Troubleshooting

### `Expecting value: line 1 column 1 (char 0)`
This usually means your code called `r.json()` but the response was **not JSON** (empty body, HTML, XML, etc.).

Run this to inspect the response:
```bash
python - <<'PY'
import requests
url="https://aws.slf.ch/api/bulletin/caaml"
r=requests.get(url, params={"lang":"en"}, headers={"Accept":"application/json"})
print("status:", r.status_code)
print("content-type:", r.headers.get("content-type"))
print("len:", len(r.text))
print("first 200 chars:", repr(r.text[:200]))
PY
```

Fixes often include:
- Add `Accept: application/json`
- Ensure the endpoint is correct/reachable from your network
- Improve error handling around `r.json()` to show `content-type` + a short body preview

### `ModuleNotFoundError: alps_briefing`
Make sure:
```bash
export PYTHONPATH="$PWD/src:$PYTHONPATH"
```

---

## Safety note
This project is an educational demo. Avalanche risk assessment is serious: always consult the official SLF bulletin and make conservative decisions.
```