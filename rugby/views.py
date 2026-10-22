import json
import math

from django.shortcuts import render

from .data.accounts import ACCOUNTS
from .data.places import _clubs_payload, load_clubs, map_data_incomplete

# Keep in sync with rugby/data/build_map_svg.py
_LON_MIN, _LON_MAX = 5.0, 32.0
_LAT_MIN, _LAT_MAX = 44.0, 58.5
_MAP_W, _MAP_H, _MAP_PAD = 960, 720, 24
_POLAND = {"lonMin": 13.7, "lonMax": 24.5, "latMin": 48.7, "latMax": 55.05}
_POLAND_PAD = 1.36


def _merc(lat: float) -> float:
    rad = math.radians(max(min(lat, 85.0), -85.0))
    return math.log(math.tan(math.pi / 4 + rad / 2))


def _map_pos(lat: float, lng: float) -> tuple[float, float]:
    x = (lng - _LON_MIN) / (_LON_MAX - _LON_MIN) * (_MAP_W - 2 * _MAP_PAD) + _MAP_PAD
    y_top, y_bot = _merc(_LAT_MAX), _merc(_LAT_MIN)
    y = (y_top - _merc(lat)) / (y_top - y_bot) * (_MAP_H - 2 * _MAP_PAD) + _MAP_PAD
    return round(x / _MAP_W * 100, 3), round(y / _MAP_H * 100, 3)


def _competition(place: dict) -> tuple[str, str]:
    kind = place.get("kind")
    if kind == "ekstraliga":
        return "Ekstraliga", "Extraleague"
    if kind == "sevens":
        return "Polska Liga Rugby 7", "Polish Rugby 7s League"
    if kind == "both":
        return (
            "Ekstraliga i Polska Liga Rugby 7",
            "Extraleague and Polish Rugby 7s League",
        )
    return "", ""


def _map_projection_config() -> str:
    return json.dumps(
        {
            "lonMin": _LON_MIN,
            "lonMax": _LON_MAX,
            "latMin": _LAT_MIN,
            "latMax": _LAT_MAX,
            "mapW": _MAP_W,
            "mapH": _MAP_H,
            "mapPad": _MAP_PAD,
            "poland": _POLAND,
            "polandPad": _POLAND_PAD,
        }
    )


def post_list(request):
    raw_clubs = load_clubs()
    incomplete = map_data_incomplete((_clubs_payload().get("clubs") or []))
    places = []
    for place in raw_clubs:
        item = dict(place)
        item["map_x"], item["map_y"] = _map_pos(place["lat"], place["lng"])
        comp_pl, comp_en = _competition(place)
        item["comp_pl"] = comp_pl if place.get("kind") != "both" else ""
        item["comp_en"] = comp_en if place.get("kind") != "both" else ""
        seasons_pl = place.get("seasons_pl") or ""
        seasons_en = place.get("seasons_en") or ""
        item["seasons_pl"] = seasons_pl
        item["seasons_en"] = seasons_en
        places.append(item)
    return render(
        request,
        "rugby/post_list.html",
        {
            "accounts": ACCOUNTS,
            "places": places,
            "map_data_incomplete": incomplete,
            "map_projection_json": _map_projection_config(),
        },
    )
