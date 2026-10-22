"""One-off helper: fetch PZR season pages and list /kluby/ slugs. Not imported at runtime."""
from __future__ import annotations

import re
import urllib.request

URLS = {
    "ekstra_2223": "https://polskie.rugby/sezon/1/ekstraliga-rugby-20222023",
    "ekstra_2324": "https://polskie.rugby/sezon/9/ekstraliga-rugby-20232024",
    "ekstra_2425": "https://polskie.rugby/sezon/23/ekstraliga-rugby-20242025",
    "ekstra_2526": "https://polskie.rugby/sezon/32/ekstraliga-rugby-20252026",
    "ekstra_2627": "https://polskie.rugby/sezon/39/ekstraliga-rugby-20262027",
    "plr7_2223": "https://polskie.rugby/sezon/5/polska-liga-rugby-7-20222023",
    "plr7_2324": "https://polskie.rugby/sezon/12/polska-liga-rugby-7-20232024",
    "plr7_2425": "https://polskie.rugby/sezon/27/polska-liga-rugby-7-20242025",
}


def fetch(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (compatible; AFC-Rugby-audit/1.0)"})
    with urllib.request.urlopen(req, timeout=45) as resp:
        return resp.read().decode("utf-8", "replace")


def club_slugs(html: str) -> list[str]:
    slugs = re.findall(r"/kluby/\d+/([a-z0-9\-]+)", html, flags=re.I)
    return sorted(set(slugs))


def short_names(html: str) -> list[str]:
    names = re.findall(
        r'<span class="make-short-name[^"]*">\s*([^<]+?)\s*</span>',
        html,
        flags=re.I,
    )
    out: list[str] = []
    seen: set[str] = set()
    for raw in names:
        name = re.sub(r"\s+", " ", raw).strip()
        if not name or name in seen:
            continue
        seen.add(name)
        out.append(name)
    return out


def main() -> None:
    needles = ["Ogniwo", "Juvenia", "Budowlani", "Lechia", "Skra", "Orkan", "Bia", "Barbarians"]
    for key, url in URLS.items():
        try:
            html = fetch(url)
            slugs = club_slugs(html)
            names = short_names(html)
            hits = [n for n in needles if n.lower() in html.lower()]
            print(f"=== {key} ({len(slugs)} slugs, {len(names)} short names, hits {hits}) ===")
            for s in names:
                print(" ", s)
        except Exception as exc:
            print(f"=== {key} FAILED: {exc} ===")


if __name__ == "__main__":
    main()
