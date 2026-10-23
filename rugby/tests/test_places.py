from rugby.data.places import (
    _format_seasons,
    _kind_from_seasons,
    _primary_source_url,
    load_clubs,
    map_data_incomplete,
)


def test_kind_from_seasons_variants():
    assert _kind_from_seasons([], historic=True) == "historic"
    assert _kind_from_seasons([{"league": "ekstraliga"}], historic=False) == "ekstraliga"
    assert _kind_from_seasons([{"league": "sevens"}], historic=False) == "sevens"
    assert (
        _kind_from_seasons(
            [{"league": "ekstraliga"}, {"league": "sevens"}],
            historic=False,
        )
        == "both"
    )


def test_format_seasons_range_and_empty():
    assert _format_seasons([]) == ""
    assert _format_seasons([{"season": "2024/2025", "status": "potwierdzony"}]) == "2024/2025"
    assert (
        _format_seasons(
            [
                {"season": "2022/2023", "status": "potwierdzony"},
                {"season": "2024/2025", "status": "w_toku"},
            ]
        )
        == "2022/2023–2024/2025"
    )


def test_primary_source_url_prefers_confirmed():
    seasons = [
        {"status": "draft", "source_url": "https://example.com/draft"},
        {"status": "potwierdzony", "source_url": " https://example.com/ok "},
    ]
    assert _primary_source_url(seasons) == "https://example.com/ok"


def test_load_clubs_from_canonical_json():
    clubs = load_clubs()
    assert len(clubs) >= 1
    first = clubs[0]
    assert {"id", "kind", "lat", "lng", "label_pl", "label_en"} <= first.keys()


def test_map_data_incomplete_detects_unconfirmed():
    assert map_data_incomplete([{"historic": False, "seasons": [{"status": "w_toku"}]}]) is True
    assert map_data_incomplete([{"historic": True, "seasons": [{"status": "w_toku"}]}]) is False
    assert map_data_incomplete([{"historic": False, "seasons": [{"status": "potwierdzony"}]}]) is False


def test_places_legacy_list_is_populated():
    from rugby.data.places_legacy import PLACES

    assert isinstance(PLACES, list)
    assert len(PLACES) > 10
    assert all("lat" in p and "lng" in p for p in PLACES)
