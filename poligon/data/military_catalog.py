"""Rules for keeping only military-relevant Poligon catalog items."""

from __future__ import annotations

import re

HANDCRAFTED = re.compile(r"^(listen|read|speak|write)-\d+")

CIVILIAN_CATEGORIES = {
    "workplace",
    "routine workplace",
    "travel",
    "town",
    "place",
    "school",
    "home",
    "health",
    "work",
    "food",
}

WIKI_DROP_TITLES = {
    "Weather",
    "Breakfast",
    "Public transport",
    "Public_transport",
}

# Civilian filler words from generated level packs and l2-x slugs.
CIVILIAN_TERMS = {
    "apple",
    "breakfast",
    "budget",
    "clinic",
    "doctor",
    "garden",
    "harbor",
    "hotel",
    "island",
    "library",
    "market",
    "museum",
    "office",
    "passport",
    "price",
    "salary",
    "shop",
    "station",
    "teacher",
    "ticket",
    "train",
    "vaccine",
}

# Level-1 travel/shopping words we no longer ship.
LEVEL_1_DROP = {
    "ticket",
    "station",
    "breakfast",
    "doctor",
    "hotel",
    "train",
    "shop",
    "price",
}

CATEGORY_FIXES = {
    "routine workplace": ("training", "szkolenie"),
    "workplace": ("operations", "działania"),
    "work": ("operations", "działania"),
    "food": ("logistics", "logistyka"),
}


def fix_categories(item: dict) -> dict:
    cat_en = item.get("category_en", "")
    if cat_en in CATEGORY_FIXES:
        cat_en, cat_pl = CATEGORY_FIXES[cat_en]
        item["category_en"] = cat_en
        item["category_pl"] = cat_pl
    return item


def keep_exercise(item: dict) -> bool:
    slug = item["slug"]
    if HANDCRAFTED.match(slug):
        return True
    if "-x" in slug or slug.startswith("l2-"):
        return False
    if "wiki" in slug:
        title = item.get("title_en", "")
        if any(drop in title for drop in WIKI_DROP_TITLES):
            return False
    if item.get("category_en", "") in CIVILIAN_CATEGORIES:
        return False
    return True


def keep_vocabulary(item: dict, *, source: str) -> bool:
    if source.endswith("original.json"):
        return True
    term = item.get("term", "").lower()
    if term in CIVILIAN_TERMS:
        return False
    if source.endswith("level-1.json") and term in LEVEL_1_DROP:
        return False
    if item.get("category_en", "") in CIVILIAN_CATEGORIES:
        return False
    return True
