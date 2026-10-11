import re
from datetime import date

import pytest
from django.urls import reverse

from rugby.data.laws import LAWS
from rugby.data.poland import card_display

BANNED = re.compile(
    r"\b(PESEL|NIP|legitymacj|Biedronk|Wilanowsk)\b",
    re.IGNORECASE,
)
BANNED_GG = re.compile(r"\bGG\b")


@pytest.mark.django_db
def test_rugby_html_has_no_sensitive_archive_terms(client):
    response = client.get(reverse("post_list"))
    html = response.content.decode()
    assert not BANNED.search(html)
    assert not BANNED_GG.search(html)


@pytest.mark.django_db
def test_laws_have_source_and_checked_on():
    for law in LAWS:
        assert law["source_url"].startswith("https://")
        assert law["checked_on"]


@pytest.mark.django_db
def test_history_segment_count(client):
    response = client.get(reverse("post_list"))
    content = response.content.decode()
    assert content.count('class="rugby-history-item"') in (6, 7)


@pytest.mark.django_db
def test_poland_stable_card_shows_numbers(client):
    response = client.get(reverse("post_list"))
    content = response.content.decode()
    assert "36 (18 + 18)" in content
    assert "sprawdzone 2026-07-26" in content


def test_volatile_stale_card_hides_numbers():
    card = {
        "slug": "xv-men",
        "title": "Test",
        "competition": "X",
        "season": "s",
        "checked_on": "2020-01-01",
        "volatile": True,
        "position": "12.",
        "points": "99",
        "context_pl": "c",
        "source_url": "https://example.com",
    }
    shown = card_display(card, today=date(2026, 10, 11))
    assert shown["stale"] is True
    assert shown["show_numbers"] is False


@pytest.mark.django_db
def test_no_youtube_thumbnail_host(client):
    response = client.get(reverse("post_list"))
    assert "img.youtube.com" not in response.content.decode()


@pytest.mark.django_db
def test_learn_module_in_html_without_js(client):
    response = client.get(reverse("post_list"))
    content = response.content.decode()
    assert "data-variant=" in content
    assert "Mecz trwa 14 minut" in content
    assert "Gdzie jest przestrzeń?" not in content
    assert "rugby-scenario" not in content
    assert "pitch.js" in content
