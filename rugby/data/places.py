"""
Map club data for /rugby/. Canonical source: club-history.json in this directory.
"""

from __future__ import annotations

import json
from pathlib import Path

PZR = "https://polskie.rugby"
_DATA_PATH = Path(__file__).resolve().parent / "club-history.json"


def _load_raw() -> dict:
    with _DATA_PATH.open(encoding="utf-8") as fh:
        return json.load(fh)


def _kind_from_seasons(seasons: list[dict], historic: bool) -> str:
    if historic:
        return "historic"
    leagues = {s.get("league") for s in seasons}
    has_xv = "ekstraliga" in leagues
    has_sevens = "sevens" in leagues
    if has_xv and has_sevens:
        return "both"
    if has_sevens:
        return "sevens"
    if has_xv:
        return "ekstraliga"
    return "ekstraliga"


def _format_seasons(seasons: list[dict]) -> str:
    confirmed = [
        s["season"]
        for s in seasons
        if s.get("status") in ("potwierdzony", "w_toku") and s.get("season")
    ]
    if not confirmed:
        return ""
    confirmed = sorted(set(confirmed), key=lambda x: x.replace("/", ""))
    if len(confirmed) == 1:
        return confirmed[0]
    return f"{confirmed[0]}–{confirmed[-1]}"


def _primary_source_url(seasons: list[dict]) -> str:
    for season in seasons:
        if season.get("status") in ("potwierdzony", "w_toku") and (season.get("source_url") or "").strip():
            return season["source_url"].strip()
    return ""


def map_data_incomplete(clubs: list[dict]) -> bool:
    for club in clubs:
        if club.get("historic"):
            continue
        for season in club.get("seasons") or []:
            if season.get("status") != "potwierdzony":
                return True
    return False


def load_clubs() -> list[dict]:
    payload = _load_raw()
    out: list[dict] = []
    for club in payload.get("clubs") or []:
        seasons = club.get("seasons") or []
        historic = bool(club.get("historic"))
        kind = _kind_from_seasons(seasons, historic)
        seasons_text = _format_seasons(seasons)
        item = {
            "id": club["club_id"],
            "kind": kind,
            "city_pl": club["city_pl"],
            "city_en": club["city_en"],
            "label_pl": club["display_name_pl"],
            "label_en": club["display_name_en"],
            "lat": club["lat"],
            "lng": club["lng"],
            "label_pos": club.get("label_pos", "e"),
            "club_url": (club.get("club_url") or "").strip(),
            "pzr_profile_url": (club.get("pzr_profile_url") or "").strip(),
            "source_url": _primary_source_url(seasons),
            "seasons_pl": seasons_text,
            "seasons_en": seasons_text,
            "internal_href": (club.get("internal_href") or "").strip(),
            "seasons": seasons,
        }
        if historic:
            item["seasons_pl"] = "Inicjatywa historyczna · 2008–2010"
            item["seasons_en"] = "Historical initiative · 2008–2010"
        out.append(item)
    return out


# Back-compat for imports/tests
def _clubs_payload() -> dict:
    return _load_raw()


PLACES = load_clubs()
