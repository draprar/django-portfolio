"""Offline helper: one Wikipedia summary, CC BY-SA, or nothing."""

from __future__ import annotations

import json
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

USER_AGENT = "PoligonPortfolio/1.0 (study catalog; one-shot build)"
MAX_CHARS = 500
HOSTS = {"en": "en.wikipedia.org", "simple": "simple.wikipedia.org"}
CACHE_PATH = Path(__file__).resolve().parent / "_wikipedia_cache.json"


def load_cache() -> dict[str, dict | None]:
    if not CACHE_PATH.exists():
        return {}
    loaded = json.loads(CACHE_PATH.read_text(encoding="utf-8"))
    if not isinstance(loaded, dict):
        return {}
    return loaded


def save_cache(cache: dict[str, dict | None]) -> None:
    CACHE_PATH.write_text(json.dumps(cache, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def fetch_summary(title: str, wiki: str = "en", cache: dict[str, dict | None] | None = None) -> dict | None:
    host = HOSTS.get(wiki, HOSTS["en"])
    key = f"{wiki}:{title}"
    if cache is not None and key in cache:
        return cache[key] or None
    slug = urllib.parse.quote(title.replace(" ", "_"))
    url = f"https://{host}/api/rest_v1/page/summary/{slug}"
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"})
    payload = None
    for attempt in range(5):
        try:
            with urllib.request.urlopen(request, timeout=25) as response:
                payload = json.load(response)
            break
        except urllib.error.HTTPError as exc:
            if exc.code == 429:
                time.sleep(4 + attempt * 3)
                continue
            if exc.code == 404:
                if cache is not None:
                    cache[key] = None
                    save_cache(cache)
                return None
            time.sleep(2 + attempt)
        except Exception:
            time.sleep(2 + attempt)
    if payload is None:
        return None
    extract = (payload.get("extract") or "").strip()
    page = (payload.get("content_urls") or {}).get("desktop", {}).get("page") or ""
    if len(extract) < 40 or not page:
        if cache is not None:
            cache[key] = None
            save_cache(cache)
        return None
    if len(extract) > MAX_CHARS:
        extract = extract[:MAX_CHARS].rsplit(" ", 1)[0].rstrip(" ,;") + "…"
    row = {
        "extract": extract,
        "url": page,
        "license": "CC BY-SA 4.0",
        "title": payload.get("title") or title,
        "wiki": wiki,
    }
    if cache is not None:
        cache[key] = row
        save_cache(cache)
    return row
