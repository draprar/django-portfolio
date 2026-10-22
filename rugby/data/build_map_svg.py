#!/usr/bin/env python3
"""Natural Earth 50m → local atlas SVG (public domain).

Source: https://github.com/nvkelso/natural-earth-vector (50m geojson)
License: https://github.com/nvkelso/natural-earth-vector/blob/master/LICENSE.md
Fetched: 2026-10-20. Bbox, size and padding must match rugby/views.py map projection.
"""
from __future__ import annotations

import json
import math
import urllib.request
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "static" / "rugby" / "img" / "map-europe.svg"
LON_MIN, LON_MAX = 5.0, 32.0
LAT_MIN, LAT_MAX = 44.0, 58.5
W, H, PAD = 960, 720, 24

URLS = {
    "countries": "https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_50m_admin_0_countries.geojson",
    "coastline": "https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_50m_coastline.geojson",
    "rivers": "https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_50m_rivers_lake_centerlines.geojson",
    "lakes": "https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_50m_lakes.geojson",
}

INSIDE = 0
LEFT, RIGHT, BOTTOM, TOP = 1, 2, 4, 8


def fetch(key: str) -> dict:
    with urllib.request.urlopen(URLS[key], timeout=90) as resp:
        return json.loads(resp.read().decode())


def _merc(lat: float) -> float:
    rad = math.radians(max(min(lat, 85.0), -85.0))
    return math.log(math.tan(math.pi / 4 + rad / 2))


def project(lon: float, lat: float) -> tuple[float, float]:
    """Web Mercator. Keep in sync with rugby/views.py and rugby/static/rugby/js/map.js."""
    x = (lon - LON_MIN) / (LON_MAX - LON_MIN) * (W - 2 * PAD) + PAD
    y_top, y_bot = _merc(LAT_MAX), _merc(LAT_MIN)
    y = (y_top - _merc(lat)) / (y_top - y_bot) * (H - 2 * PAD) + PAD
    return x, y


def code(lon: float, lat: float) -> int:
    c = INSIDE
    if lon < LON_MIN:
        c |= LEFT
    elif lon > LON_MAX:
        c |= RIGHT
    if lat < LAT_MIN:
        c |= BOTTOM
    elif lat > LAT_MAX:
        c |= TOP
    return c


def clip_segment(a, b):
    lon1, lat1 = a
    lon2, lat2 = b
    c1, c2 = code(lon1, lat1), code(lon2, lat2)
    for _ in range(12):
        if not (c1 | c2):
            return (lon1, lat1), (lon2, lat2)
        if c1 & c2:
            return None
        c = c1 or c2
        if c & TOP:
            lon = lon1 + (lon2 - lon1) * (LAT_MAX - lat1) / (lat2 - lat1 or 1e-12)
            lat = LAT_MAX
        elif c & BOTTOM:
            lon = lon1 + (lon2 - lon1) * (LAT_MIN - lat1) / (lat2 - lat1 or 1e-12)
            lat = LAT_MIN
        elif c & RIGHT:
            lat = lat1 + (lat2 - lat1) * (LON_MAX - lon1) / (lon2 - lon1 or 1e-12)
            lon = LON_MAX
        else:
            lat = lat1 + (lat2 - lat1) * (LON_MIN - lon1) / (lon2 - lon1 or 1e-12)
            lon = LON_MIN
        if c == c1:
            lon1, lat1, c1 = lon, lat, code(lon, lat)
        else:
            lon2, lat2, c2 = lon, lat, code(lon, lat)
    return None


def clip_lines(coords: list) -> list[list]:
    runs: list[list] = []
    current: list = []

    def flush() -> None:
        if len(current) >= 2:
            runs.append(list(current))
        current.clear()

    for i in range(len(coords) - 1):
        seg = clip_segment(coords[i], coords[i + 1])
        if not seg:
            flush()
            continue
        if current and abs(current[-1][0] - seg[0][0]) + abs(current[-1][1] - seg[0][1]) > 1e-6:
            flush()
        if not current:
            current.append(seg[0])
        current.append(seg[1])
    flush()
    return runs


def clip_ring(ring: list) -> list:
    pts = [(lon, lat) for lon, lat, *_ in ring]

    def edge(points, inside, cross):
        if not points:
            return []
        out = []
        prev = points[-1]
        prev_in = inside(prev)
        for cur in points:
            cur_in = inside(cur)
            if cur_in:
                if not prev_in:
                    out.append(cross(prev, cur))
                out.append(cur)
            elif prev_in:
                out.append(cross(prev, cur))
            prev, prev_in = cur, cur_in
        return out

    def xv(a, b, lon):
        t = (lon - a[0]) / (b[0] - a[0] or 1e-12)
        return (lon, a[1] + t * (b[1] - a[1]))

    def xh(a, b, lat):
        t = (lat - a[1]) / (b[1] - a[1] or 1e-12)
        return (a[0] + t * (b[0] - a[0]), lat)

    pts = edge(pts, lambda p: p[0] >= LON_MIN, lambda a, b: xv(a, b, LON_MIN))
    pts = edge(pts, lambda p: p[0] <= LON_MAX, lambda a, b: xv(a, b, LON_MAX))
    pts = edge(pts, lambda p: p[1] >= LAT_MIN, lambda a, b: xh(a, b, LAT_MIN))
    pts = edge(pts, lambda p: p[1] <= LAT_MAX, lambda a, b: xh(a, b, LAT_MAX))
    return pts


def path_d(pts, close: bool) -> str:
    xy = [project(lon, lat) for lon, lat in pts]
    d = f"M {xy[0][0]:.1f} {xy[0][1]:.1f}"
    d += "".join(f" L {x:.1f} {y:.1f}" for x, y in xy[1:])
    return d + (" Z" if close else "")


def area(pts) -> float:
    s = 0.0
    for i, p in enumerate(pts):
        q = pts[(i + 1) % len(pts)]
        s += p[0] * q[1] - q[0] * p[1]
    return abs(s) / 2


def iter_polys(geom):
    t, c = geom.get("type"), geom.get("coordinates") or []
    if t == "Polygon":
        yield c
    elif t == "MultiPolygon":
        yield from c


def iter_lines(geom):
    t, c = geom.get("type"), geom.get("coordinates") or []
    if t == "LineString":
        yield c
    elif t == "MultiLineString":
        yield from c


def main() -> None:
    countries = fetch("countries")
    coast = fetch("coastline")
    rivers = fetch("rivers")
    try:
        lakes = fetch("lakes")
    except Exception:
        lakes = {"features": []}

    land, poland, water = [], [], []
    for feat in countries["features"]:
        iso = (feat.get("properties") or {}).get("ISO_A3")
        for poly in iter_polys(feat.get("geometry") or {}):
            if not poly:
                continue
            clipped = clip_ring(poly[0])
            if len(clipped) < 3 or area(clipped) < 0.05:
                continue
            d = path_d(clipped, True)
            land.append(d)
            if iso == "POL":
                poland.append(d)

    for feat in lakes["features"]:
        for poly in iter_polys(feat.get("geometry") or {}):
            if not poly:
                continue
            clipped = clip_ring(poly[0])
            if len(clipped) < 3 or area(clipped) < 0.008:
                continue
            water.append(path_d(clipped, True))

    coasts, river_paths = [], []
    for feat in coast["features"]:
        for line in iter_lines(feat.get("geometry") or {}):
            for run in clip_lines([(lon, lat) for lon, lat, *_ in line]):
                coasts.append(path_d(run, False))
    for feat in rivers["features"]:
        for line in iter_lines(feat.get("geometry") or {}):
            for run in clip_lines([(lon, lat) for lon, lat, *_ in line]):
                river_paths.append(path_d(run, False))

    graticule = []
    for lon in range(5, 35, 5):
        if LON_MIN < lon < LON_MAX:
            graticule.append(path_d([(lon, LAT_MIN), (lon, LAT_MAX)], False))
    for lat in range(45, 60, 5):
        if LAT_MIN < lat < LAT_MAX:
            graticule.append(path_d([(LON_MIN, lat), (LON_MAX, lat)], False))

    parts = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        "<!-- Natural Earth 50m, public domain. Built 2026-10-20 by rugby/data/build_map_svg.py -->",
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}">',
        '<rect width="100%" height="100%" fill="#101114"/>',
        '<g fill="none" stroke="#2a2c30" stroke-width="0.6" opacity="0.7">',
        * (f'<path d="{d}"/>' for d in graticule),
        "</g>",
        '<g fill="#1c1e22" stroke="#3a3d42" stroke-width="0.7" stroke-linejoin="round">',
        * (f'<path d="{d}"/>' for d in land),
        "</g>",
        '<g fill="#17140f" stroke="#c4922a" stroke-width="1.1" stroke-linejoin="round">',
        * (f'<path d="{d}"/>' for d in poland),
        "</g>",
        '<g fill="#1a2830" stroke="#2c4450" stroke-width="0.4">',
        * (f'<path d="{d}"/>' for d in water),
        "</g>",
        '<g fill="none" stroke="#8a939c" stroke-width="0.9" opacity="0.55">',
        * (f'<path d="{d}"/>' for d in coasts),
        "</g>",
        '<g fill="none" stroke="#3d5c68" stroke-width="0.7" opacity="0.8">',
        * (f'<path d="{d}"/>' for d in river_paths),
        "</g></svg>",
    ]
    OUT.write_text("\n".join(parts), encoding="utf-8")
    print(OUT, "land", len(land), "poland", len(poland), "bytes", OUT.stat().st_size)


if __name__ == "__main__":
    main()
