from rugby.data import build_map_svg as svg
from rugby.views import _competition, _map_pos


def test_project_keeps_points_inside_canvas():
    x, y = svg.project(21.0, 52.2)  # roughly Warsaw
    assert 0 <= x <= svg.W
    assert 0 <= y <= svg.H


def test_code_flags_outside_bbox():
    assert svg.code(0.0, 50.0) & svg.LEFT
    assert svg.code(40.0, 50.0) & svg.RIGHT
    assert svg.code(20.0, 40.0) & svg.BOTTOM
    assert svg.code(20.0, 60.0) & svg.TOP
    assert svg.code(20.0, 50.0) == svg.INSIDE


def test_clip_segment_inside_and_outside():
    assert svg.clip_segment((10.0, 50.0), (20.0, 52.0)) is not None
    assert svg.clip_segment((-10.0, 30.0), (-5.0, 35.0)) is None


def test_views_map_pos_and_competition_labels():
    x, y = _map_pos(52.2297, 21.0122)
    assert 0 <= x <= 100
    assert 0 <= y <= 100
    assert _competition({"kind": "ekstraliga"}) == ("Ekstraliga", "Extraleague")
    assert _competition({"kind": "sevens"})[0].startswith("Polska Liga")
    assert _competition({"kind": "both"})[0].startswith("Ekstraliga")
    assert _competition({"kind": "historic"}) == ("", "")
