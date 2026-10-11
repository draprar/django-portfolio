"""Load editorial data for the public rugby page."""

from rugby.data.history import SEGMENTS
from rugby.data.laws import DISCLAIMER, LAWS
from rugby.data.poland import CARDS, LINKS, SCENE_NOTE, card_display
from rugby.data.timeline import CLOSING_QUOTE, HOW_IT_WAS, TIMELINE

MEDIA_ITEMS = [
    {
        "slug": "poster-1",
        "title": "Pierwszy plakat",
        "author": "Jakub Turek",
        "static": "rugby/img/1_poster.png",
        "timeline_slugs": ["2008"],
    },
    {
        "slug": "poster-2",
        "title": "Drugi plakat",
        "author": "Jakub Turek",
        "static": "rugby/img/2_poster.jpg",
        "timeline_slugs": ["2008"],
    },
    {
        "slug": "gg",
        "title": "Artykuł (Gazeta Giżycka)",
        "author": "Paweł Mieczkowski",
        "static": "rugby/img/gg.png",
        "timeline_slugs": ["2008"],
    },
    {
        "slug": "go",
        "title": "Artykuł (Gazeta Olsztyńska)",
        "author": "Sebastian Woźniak",
        "static": "rugby/img/go.png",
        "timeline_slugs": ["2008"],
    },
    {
        "slug": "pzr",
        "title": "Encyklopedia Polskiego Rugby",
        "author": "Maciej Powała-Niedźwiedzki & Jacek Wierzbicki",
        "static": "rugby/img/pzr.png",
        "timeline_slugs": ["2008"],
    },
    {
        "slug": "film",
        "title": "Film",
        "author": "Michał Walerowicz",
        "youtube_id": "TBdK3AkhQKE",
        "static": "rugby/img/logo.jpg",
        "timeline_slugs": ["2008"],
    },
]


def page_context() -> dict:
    return {
        "laws": LAWS,
        "law_disclaimer": DISCLAIMER,
        "history_segments": [s for s in SEGMENTS if s["status"] == "verified"],
        "timeline": TIMELINE,
        "how_it_was": HOW_IT_WAS,
        "closing_quote": CLOSING_QUOTE,
        "poland_cards": [card_display(c) for c in CARDS],
        "poland_links": LINKS,
        "poland_note": SCENE_NOTE,
        "media_items": MEDIA_ITEMS,
    }
