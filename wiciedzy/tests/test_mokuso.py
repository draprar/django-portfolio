from __future__ import annotations

import re
from pathlib import Path

import pytest
from django.urls import reverse

APP_ROOT = Path(__file__).resolve().parents[1]
WIKI = "https://en.wikipedia.org/wiki/The_Relaxation_Response"
HARVARD = (
    "https://www.health.harvard.edu/blog/"
    "a-once-and-future-meditator-tries-the-relaxation-response-for-stress-201110143598"
)
FORBIDDEN = ("test", "quiz", "match", "fit", "recommend", "archetyp")
HEALTH = (
    r"ciśnieni",
    r"kortyzol",
    r"zapaln",
    r"terapi",
    r"depresj",
    r"lęk",
    r"blood pressure",
    r"cortisol",
    r"inflammation",
    r"therap",
    r"depress",
    r"anxiety",
    r"udowodnion",
    r"proven",
)


def _word_hit(text: str, word: str) -> bool:
    pattern = rf"(?<![\w]){re.escape(word)}(?![\w])"
    return re.search(pattern, text, re.IGNORECASE) is not None


def _main(html: str) -> str:
    match = re.search(r'id="wiciedzy-main"[^>]*>(.*)</main>', html, re.DOTALL | re.IGNORECASE)
    return match.group(1) if match else html


def _copy_blob(main: str) -> str:
    parts = [main]
    for attr in ("data-pl", "data-en", "aria-label"):
        parts.extend(re.findall(rf'{attr}="([^"]*)"', main, re.IGNORECASE))
    visible = re.sub(r"<script[^>]*>.*?</script>", " ", main, flags=re.DOTALL | re.IGNORECASE)
    visible = re.sub(r"<[^>]+>", " ", visible)
    parts.append(visible)
    return " ".join(parts)


@pytest.mark.django_db
def test_mokuso_page_renders_in_base(client):
    response = client.get(reverse("wiciedzy:mokuso"))
    html = response.content.decode()

    assert response.status_code == 200
    assert 'id="wiciedzy-main"' in html
    assert "wiciedzy-stage" in html
    assert "core/js/lang.js" in html
    assert "mokuso.css" in html
    assert "mokuso.js" in html
    assert "<h1" in html
    assert 'data-pl="mokuso"' in html
    assert "noindex" not in html


@pytest.mark.django_db
def test_mokuso_copy_has_both_languages_and_durations(client):
    html = client.get(reverse("wiciedzy:mokuso")).content.decode()
    main = _main(html)

    assert 'data-pl="Chwila ciszy. Przed treningiem, w ciągu dnia, kiedy tam ci leży."' in main
    assert 'data-en="A quiet moment. Before training, during the day, whenever you feel like it."' in main
    assert "w ciągu dnia" in main
    assert "during the day" in main
    assert "Metoda pochodzi z instrukcji Herberta Bensona" in main
    assert "The method comes from the instructions of Herbert Benson" in main
    assert "1975" in main
    assert "Bierz albo nie" not in main
    assert "Take it or leave it" not in main
    assert "Praktyka inspirowana" not in main
    assert "A practice inspired" not in main

    steps = re.findall(r'<ol class="mokuso-steps">(.*?)</ol>', main, re.DOTALL)
    assert len(steps) == 1
    step_items = re.findall(r"<li\b", steps[0])
    assert len(step_items) == 4
    assert "połóż" in steps[0]
    assert "mięśnie" in steps[0]
    assert "lie down" in steps[0]
    assert "muscles" in steps[0]
    assert "nie na głos" not in steps[0]
    assert "krótkie" in steps[0]
    assert "not out loud" not in steps[0]
    assert "short" in steps[0]
    assert "na luzie" in steps[0]
    assert "powtarzaj" in steps[0]
    assert "Ease back" in steps[0]

    assert 'data-pl="jak „one”, ale możesz wybrać swoje"' in main
    assert 'data-en="or pick your own"' in main
    assert "ŁAN to angielskie" not in main
    assert "original instructions" not in main.lower()
    assert 'data-pl="ŁAN"' in main
    assert 'data-en="ONE"' in main
    for label in ("5 min", "10 min", "20 min"):
        assert f'data-pl="{label}"' in main
        assert f'data-en="{label}"' in main
    assert 'data-pl="Start"' in main
    assert 'data-en="Start"' in main
    assert 'data-pl="Stop"' in main
    assert 'data-en="Stop"' in main
    assert "nie ma gwarancji" in main
    assert "there are no guarantees" in main
    assert "ciszy i bezruchu" not in main
    assert "being still and quiet" not in main
    assert re.search(r'name="mokuso-minutes" value="5" checked', main)
    assert not re.search(r'<input[^>]*type="(?:text|search)"', main, re.IGNORECASE)


@pytest.mark.django_db
def test_mokuso_forbidden_copy(client):
    html = client.get(reverse("wiciedzy:mokuso")).content.decode()
    blob = _copy_blob(_main(html))

    for word in FORBIDDEN:
        assert not _word_hit(blob, word), word
    for pattern in HEALTH:
        assert re.search(pattern, blob, re.IGNORECASE) is None, pattern
    assert "Zen Jaskiniowca" not in blob
    assert re.search(r"jaskiniow", blob, re.IGNORECASE) is None
    assert re.search(r"(?<![A-Za-z])LAM(?![A-Za-z])", blob) is None
    assert "to nic" not in blob.lower()
    assert not _word_hit(blob, "dojo")
    assert re.search(r"\bbuddyj", blob, re.IGNORECASE) is None
    assert re.search(r"\bbuddh", blob, re.IGNORECASE) is None


@pytest.mark.django_db
def test_mokuso_footer_sources(client):
    html = client.get(reverse("wiciedzy:mokuso")).content.decode()
    block = re.search(r'class="mokuso-foot"(.*?)</footer>', html, re.DOTALL)
    assert block
    foot = block.group(1)
    hrefs = re.findall(r'href="(https?://[^"]+)"', foot)
    assert hrefs == [WIKI, HARVARD]
    assert 'data-pl="Źródła:"' not in foot
    assert 'data-en="Sources:"' not in foot
    assert 'target="_blank"' in foot
    assert 'rel="noopener"' in foot
    assert "Praktyka inspirowana" not in foot


def test_mokuso_assets_have_no_copy():
    js = (APP_ROOT / "static" / "wiciedzy" / "js" / "mokuso.js").read_text(encoding="utf-8")
    css = (APP_ROOT / "static" / "wiciedzy" / "css" / "mokuso.css").read_text(encoding="utf-8")
    for source in (js, css):
        assert "Zen Jaskiniowca" not in source
        assert re.search(r"jaskiniow", source, re.IGNORECASE) is None
        assert re.search(r"(?<![A-Za-z])LAM(?![A-Za-z])", source) is None
        assert "to nic" not in source.lower()
        assert re.search(r"(?<![\w])ŁAN(?![\w])", source) is None
        assert re.search(r"(?<![\w])ONE(?![\w])", source) is None
        assert "Ukłon" not in source


@pytest.mark.django_db
def test_home_links_mokuso_and_sitemap_lists_it(client):
    home = client.get(reverse("wiciedzy:home")).content.decode()
    listed = client.get(reverse("wiciedzy:list")).content.decode()
    sitemap = client.get(reverse("wiciedzy:sitemap"))
    path = reverse("wiciedzy:mokuso")

    assert path in home
    assert 'data-pl="wbijaj się wyciszyć"' in home
    assert 'data-en="come in and quiet down"' in home
    assert "wiciedzy-home-quiet-desc" not in home
    assert "A kto to przyszedł?" not in home
    assert "wiciedzy-home-mokuso" not in home
    assert path not in listed
    assert sitemap.status_code == 200
    assert path in sitemap.content.decode()
