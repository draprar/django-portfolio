"""Offline helper: one English Tatoeba sentence that advertises a CC BY license."""

from __future__ import annotations

import json
import urllib.parse
import urllib.request
from pathlib import Path

USER_AGENT = "PoligonPortfolio/1.0 (study catalog; one-shot build)"
CACHE_PATH = Path(__file__).resolve().parent / "_tatoeba_cache.json"


def load_cache() -> dict[str, dict | None]:
    if not CACHE_PATH.exists():
        return {}
    return json.loads(CACHE_PATH.read_text(encoding="utf-8"))


def save_cache(cache: dict[str, dict | None]) -> None:
    CACHE_PATH.write_text(json.dumps(cache, ensure_ascii=False) + "\n", encoding="utf-8")


def fetch_sentence(term: str, cache: dict[str, dict | None] | None = None) -> dict | None:
    if cache is not None and term in cache:
        return cache[term]
    query = urllib.parse.urlencode({"from": "eng", "query": term, "trans_to": "pol"})
    url = f"https://tatoeba.org/eng/api_v0/search?{query}"
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"})
    with urllib.request.urlopen(request, timeout=25) as response:
        payload = json.load(response)
    for row in payload.get("results") or []:
        text = (row.get("text") or "").strip()
        license_name = (row.get("license") or "").lower()
        sentence_id = row.get("id")
        if not text or not sentence_id or "cc" not in license_name or "by" not in license_name:
            continue
        if len(text) > 180:
            continue
        found = {
            "text": text,
            "id": sentence_id,
            "url": f"https://tatoeba.org/en/sentences/show/{sentence_id}",
            "license": row.get("license") or "CC BY",
            "author": (row.get("user") or {}).get("username") or "Tatoeba user",
        }
        if cache is not None:
            cache[term] = found
            save_cache(cache)
        return found
    if cache is not None:
        cache[term] = None
        save_cache(cache)
    return None
