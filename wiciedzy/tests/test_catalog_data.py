import re
from io import StringIO
from pathlib import Path

import pytest
from django.core.management import call_command

from wiciedzy.content_validation import APPROVED_ACTIVE_SLUGS, collect_findings
from wiciedzy.data.styles import CORE, GOLDEN, RELATIONS
from wiciedzy.management.commands.export_wiciedzy_texts import _build_lines
from wiciedzy.models import Style


@pytest.mark.django_db
def test_catalog_matches_source(full_catalog):
    errors, _warnings, _infos = collect_findings()
    assert errors == []


@pytest.mark.django_db
def test_active_slug_count(full_catalog):
    assert Style.objects.filter(active=True).count() == len(APPROVED_ACTIVE_SLUGS) == 46


@pytest.mark.django_db
def test_relations_count(full_catalog):
    from wiciedzy.models import StyleRelation

    assert StyleRelation.objects.count() == len(RELATIONS)


@pytest.mark.django_db
def test_validate_command_exits_zero(full_catalog):
    out = StringIO()
    call_command("validate_wiciedzy_content", stdout=out)
    assert "ERROR:" not in out.getvalue()


def test_source_slug_shape():
    slugs = [row["slug"] for row in CORE + GOLDEN]
    assert len(slugs) == len(set(slugs))
    for slug in slugs:
        assert re.fullmatch(r"[a-z0-9-]+", slug)


@pytest.mark.django_db
def test_export_has_no_empty_en_lines(full_catalog):
    lines = _build_lines(pl_only=False, plain=False, include_seo=False)
    for index, line in enumerate(lines):
        if line == "**EN:**":
            assert lines[index - 1].startswith("**PL:**")
            pytest.fail(f"empty EN after {lines[index-1]}")


def test_export_utf8_sig_encoding():
    sample = Path(__file__).resolve().parents[1] / "teksty-eksport.md"
    if sample.is_file():
        assert sample.read_bytes()[:3] == b"\xef\xbb\xbf"


@pytest.mark.django_db
def test_export_includes_every_active_slug(full_catalog):
    lines = _build_lines(pl_only=False, plain=False, include_seo=False)
    text = "\n".join(lines)
    for slug in APPROVED_ACTIVE_SLUGS:
        assert f"### {slug} —" in text


@pytest.mark.django_db
def test_card_copy_regressions(full_catalog):
    kendo = Style.objects.get(slug="kendo")
    taiji = Style.objects.get(slug="taijiquan")
    iaido = Style.objects.get(slug="iaido")
    kyudo = Style.objects.get(slug="kyudo")
    lethwei = Style.objects.get(slug="lethwei")
    assert "scores on the shinai" not in kendo.practice_en.lower()
    assert "as in sanda" not in taiji.practice_en.lower()
    assert "sandowej wymiany na ciosy" in taiji.practice_pl.lower()
    assert "cut, the posture and the draw" not in iaido.practice_en.lower()
    assert "olimpijsk" not in kyudo.summary_pl.lower()
    assert "olympic archery" not in kyudo.summary_en.lower()
    assert "when the rules do not switch it off" not in lethwei.practice_en.lower()
    assert "gdy regulamin jej nie wyłączy" not in lethwei.practice_pl.lower()
