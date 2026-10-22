"""One-off: build rugby/data/club-history.json from legacy PLACES in places_legacy.py snapshot."""
from __future__ import annotations

import json
import re
from pathlib import Path

# Legacy list copied from pre-v11 places.py (run once).
from rugby.data import places_legacy  # noqa: E402

PZR = "https://polskie.rugby"
OUT = Path(__file__).resolve().parent / "club-history.json"


def split_urls(url: str | None) -> tuple[str, str]:
    if not url or url.strip() == f"{PZR}/kluby":
        return "", ""
    raw = url.strip()
    if PZR in raw and "/kluby/" in raw:
        return "", raw
    if PZR in raw:
        return "", ""
    return raw, ""


def seasons_from_legacy(place: dict) -> list[dict]:
    kind = place.get("kind")
    if kind == "historic":
        return []
    tier = (place.get("tier_pl") or "").lower()
    seasons: list[dict] = []

    def add(league: str, season: str, status: str = "brak_zrodla", source_url: str = "") -> None:
        seasons.append(
            {
                "league": league,
                "season": season,
                "status": status,
                "source_url": source_url,
            }
        )

    if kind == "ekstraliga" or kind == "both":
        if "2019" in tier:
            add("ekstraliga", "2019")
        if "2020/21" in tier or "2020/2021" in tier:
            add("ekstraliga", "2020/21")
        if "2021/22" in tier:
            add("ekstraliga", "2021/22")
        if "2022/23" in tier:
            add("ekstraliga", "2022/23")
        if "2024/25" in tier:
            add("ekstraliga", "2024/25")
        if not any(s["league"] == "ekstraliga" for s in seasons):
            add("ekstraliga", "2022/23")
    if kind == "sevens" or kind == "both" or "plr7" in tier or "liga rugby 7" in tier:
        if "2022/23" in tier or kind == "sevens":
            add("sevens", "2022/23")
        if "2023/24" in tier:
            add("sevens", "2023/24")
        if "2024/25" in tier:
            add("sevens", "2024/25")
    if kind == "ekstraliga" and "juvenia" in tier.lower() and "2023/24" in tier:
        add("sevens", "2023/24")
    return seasons


def main() -> None:
    clubs = []
    for place in places_legacy.PLACES:
        club_url, pzr_url = split_urls(place.get("url"))
        entry = {
            "club_id": place["id"],
            "display_name_pl": place["label_pl"],
            "display_name_en": place["label_en"],
            "city_pl": place["city_pl"],
            "city_en": place["city_en"],
            "lat": place["lat"],
            "lng": place["lng"],
            "label_pos": place.get("label_pos", "e"),
            "club_url": club_url,
            "pzr_profile_url": pzr_url,
            "aliases": [],
            "historic": place.get("kind") == "historic",
            "internal_href": place.get("internal_href", "") or "",
            "seasons": seasons_from_legacy(place),
        }
        clubs.append(entry)
    payload = {
        "window": "2016-10-21 to 2026-10-21",
        "clubs": clubs,
    }
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {len(clubs)} clubs to {OUT}")


if __name__ == "__main__":
    main()
