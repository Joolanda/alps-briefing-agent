import re
from datetime import date, timedelta

from alps_briefing.services.geocoding import geocode
from alps_briefing.services.avalanche_slf import fetch_slf_bulletin


# MVP mapping (you can extend later)
# From your earlier JSON: "nördliches Urseren" had regionID "CH-2223" (fits Andermatt/Urseren)
PLACE_TO_REGION_ID = {
    "andermatt": "CH-2223",
}


def parse_place_and_day(question: str) -> tuple[str, date]:
    q = question.strip()

    # day (MVP: today/tomorrow only)
    q_lower = q.lower()
    day = date.today() + timedelta(days=1) if "tomorrow" in q_lower else date.today()

    # place: extract after "in ..."
    m = re.search(r"\bin\s+(.+?)(?:\s+tomorrow|\s+today|\?|$)", q, flags=re.IGNORECASE)
    if not m:
        raise ValueError('Could not find a location. Try: "Do I need avalanche gear in Andermatt tomorrow?"')

    place = m.group(1).strip(" ,.!?")
    return place, day


def pick_bulletin_for_region(slf_payload: dict, region_id: str) -> dict:
    bulletins = slf_payload.get("bulletins", [])
    for b in bulletins:
        regions = b.get("regions", [])
        if any(r.get("regionID") == region_id for r in regions):
            return b
    raise ValueError(f"No SLF bulletin found for regionID={region_id} (mapping may be wrong).")


def extract_max_danger_level(bulletin: dict) -> int | None:
    levels = []
    for dr in bulletin.get("dangerRatings", []):
        if not isinstance(dr, dict):
            continue

        # common patterns (try several keys)
        v = None
        if isinstance(dr.get("dangerLevel"), dict):
            v = dr["dangerLevel"].get("mainValue")
        elif dr.get("dangerLevel") is not None:
            v = dr.get("dangerLevel")

        if v is None:
            v = dr.get("mainValue") or dr.get("value") or dr.get("level")

        try:
            if v is not None:
                levels.append(int(v))
        except Exception:
            pass

    return max(levels) if levels else None


def render_gear_advice(place: str, danger_level: int | None) -> str:
    kit = "transceiver (PIEPS), probe, shovel"

    # Safety-first phrasing: conditional on off-piste/touring
    base = f"If you plan to go off-piste or ski touring near {place}: yes—bring {kit}."

    if danger_level is None:
        return base + " I couldn’t read the danger level from the bulletin output. Please check the official SLF bulletin."

    if danger_level >= 4:
        return base + f" The bulletin indicates danger level {danger_level}: avoid touring/off-piste and stick to secured terrain."
    if danger_level == 3:
        return base + " Danger level 3: be very conservative with terrain choices."
    if danger_level == 2:
        return base + " Danger level 2: be cautious and follow the bulletin guidance."
    return base + " Danger level 1: conditions may be more stable, but standard safety practices still apply."


def answer_avalanche_gear_question(question: str) -> dict:
    place, day = parse_place_and_day(question)

    # (Optional but useful for debug/future region mapping)
    loc = geocode(place)

    region_id = PLACE_TO_REGION_ID.get(place.lower().strip())
    if not region_id:
        raise ValueError(f"No region mapping for '{place}'. Add it to PLACE_TO_REGION_ID for the MVP.")

    slf = fetch_slf_bulletin(lang="en")
    bulletin = pick_bulletin_for_region(slf, region_id)

    danger_level = extract_max_danger_level(bulletin)
    answer = render_gear_advice(place, danger_level)

    return {
        "answer": answer + " (Educational demo — always rely on the official bulletin.)",
        "question": question,
        "place": place,
        "day_requested": day.isoformat(),
        "region_id": region_id,
        "danger_level": danger_level,
        "location": loc,
        "validTime": bulletin.get("validTime"),
        "nextUpdate": bulletin.get("nextUpdate"),
    }