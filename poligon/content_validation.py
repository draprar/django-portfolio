"""Checks for the exercise catalog on disk.

The JSON files are the source of truth. ``active`` in the database is only the
technical flag seed sets for ``publication_status=published``.
"""

from __future__ import annotations

import json
import re
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path

from poligon.framework import (
    COVERAGE_GATES,
    EXERCISE_TYPES,
    LEVEL_PROFILES,
    PUBLICATION_STATUSES,
    SKILLS,
    competency_for,
    level_profile,
)
from poligon.levels import LEVELS

DATA_ROOT = Path(__file__).resolve().parent / "data"
MANIFEST_PATH = DATA_ROOT / "manifest.json"

HTML_MARKUP = re.compile(r"<[a-zA-Z/!]")
PLACEHOLDER = re.compile(r"\b(TODO|TBD|FIXME|lorem|xxxx)\b|\[\.\.\.\]", re.IGNORECASE)
CHOICE_TYPES = frozenset({"mcq", "listening", "true_false"})


@dataclass
class ContentReport:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    counts: dict[int, dict[str, int]] = field(default_factory=dict)
    strict_counts: dict[int, dict[str, int]] = field(default_factory=dict)

    def text(self) -> str:
        lines: list[str] = []
        for level in LEVELS:
            lines.append(f"LEVEL {level}")
            row = self.counts.get(level, {})
            for skill, label in (("L", "Listening"), ("S", "Speaking"), ("R", "Reading"), ("W", "Writing")):
                lines.append(f"  {label:<10} {row.get(skill, 0)}")
        lines.append("Coverage:")
        for level in LEVELS:
            lines.append(f"L{level} {self.coverage(level)}%")
        lines.append("Gates (published, including legacy):")
        for gate in COVERAGE_GATES:
            met = sum(1 for level in LEVELS for skill in SKILLS if self.counts.get(level, {}).get(skill, 0) >= gate)
            lines.append(f"  cells at {gate}: {met}/20")
        lines.append("Gates (published, not legacy):")
        for gate in COVERAGE_GATES:
            met = sum(
                1 for level in LEVELS for skill in SKILLS if self.strict_counts.get(level, {}).get(skill, 0) >= gate
            )
            lines.append(f"  reviewed cells at {gate}: {met}/20")
        lines.append(f"errors: {len(self.errors)}")
        lines.append(f"warnings: {len(self.warnings)}")
        lines.extend(f"ERROR {item}" for item in self.errors)
        lines.extend(f"WARN {item}" for item in self.warnings)
        return "\n".join(lines)

    def coverage(self, level: int) -> int:
        row = self.counts.get(level, {})
        filled = sum(1 for skill in SKILLS if row.get(skill, 0) > 0)
        return round(100 * filled / len(SKILLS))


def load_exercises() -> list[dict]:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    rows: list[dict] = []
    for relative in manifest["exercises"]:
        payload = json.loads((DATA_ROOT / relative).read_text(encoding="utf-8"))
        for item in payload:
            item["_file"] = relative
            rows.append(item)
    return rows


def validate_catalog(*, strict: bool = False) -> ContentReport:
    report = ContentReport()
    rows = load_exercises()
    seen: dict[str, str] = {}
    prompts: dict[str, str] = {}
    report.counts = {level: {skill: 0 for skill in SKILLS} for level in LEVELS}
    report.strict_counts = {level: {skill: 0 for skill in SKILLS} for level in LEVELS}
    for item in rows:
        _validate_one(item, seen, prompts, report, strict=strict)
    _validate_placement_bank(report)
    return report


def _validate_placement_bank(report: ContentReport) -> None:
    path = DATA_ROOT / "placement" / "v1.json"
    if not path.exists():
        report.errors.append("placement bank is missing")
        return
    rows = json.loads(path.read_text(encoding="utf-8"))
    if len(rows) != 15:
        report.errors.append(f"placement bank has {len(rows)} items, expected 15")
    per_level: dict[int, int] = dict.fromkeys(LEVELS, 0)
    for item in rows:
        if item.get("catalog_role") != "placement":
            report.errors.append(f"{item.get('slug')}: placement item is not marked placement")
        level = item.get("level")
        if level in per_level:
            per_level[level] += 1
        if item.get("publication_status") != "published":
            report.errors.append(f"{item.get('slug')}: placement item is not published")
    for level, count in per_level.items():
        if count != 3:
            report.errors.append(f"placement level {level} has {count} items, expected 3")


def _validate_one(
    item: dict,
    seen: dict[str, str],
    prompts: dict[str, str],
    report: ContentReport,
    *,
    strict: bool,
) -> None:
    slug = str(item.get("slug") or "").strip()
    where = item.get("_file", "?")
    if not slug:
        report.errors.append(f"{where}: missing slug")
        return
    if slug in seen:
        report.errors.append(f"{slug}: duplicate slug (also in {seen[slug]})")
    seen[slug] = where

    skill = item.get("skill")
    level = item.get("level")
    if level not in LEVEL_PROFILES:
        report.errors.append(f"{slug}: unknown level {level!r}")
    if skill not in SKILLS:
        report.errors.append(f"{slug}: unknown skill {skill!r}")
    exercise_type = item.get("exercise_type")
    if exercise_type not in EXERCISE_TYPES:
        report.errors.append(f"{slug}: unknown exercise type {exercise_type!r}")
    if "publication_status" not in item:
        report.errors.append(f"{slug}: missing publication status")
        status = "draft"
    else:
        raw_status = item["publication_status"]
        status = raw_status if isinstance(raw_status, str) else ""
    if status not in PUBLICATION_STATUSES:
        report.errors.append(f"{slug}: unknown publication status {status!r}")
    if not str(item.get("prompt_en") or "").strip():
        report.errors.append(f"{slug}: missing English prompt")
    if not str(item.get("title_en") or "").strip():
        report.errors.append(f"{slug}: missing English title")

    options = item.get("options") or []
    if exercise_type in CHOICE_TYPES:
        _validate_options(slug, options, report)
    if exercise_type == "true_false":
        texts = {str(option.get("text_en") or "").strip().lower() for option in options}
        if texts != {"true", "false"}:
            report.errors.append(f"{slug}: a true/false item must offer True and False")

    published = False
    if status == "published" and isinstance(level, int) and isinstance(skill, str) and skill in SKILLS:
        published = True
        report.counts[level][skill] += 1
        if item.get("quality_status") != "legacy":
            report.strict_counts[level][skill] += 1

    legacy = item.get("quality_status") == "legacy"
    if published and (strict or not legacy):
        _validate_published(slug, item, report, as_error=strict or not legacy)
    elif published and legacy and not strict:
        _validate_published(slug, item, report, as_error=False)

    _language_notes(slug, item, report, as_error=published and (strict or not legacy))
    prompt = str(item.get("prompt_en") or "").strip()
    if published and prompt:
        previous = prompts.get(prompt)
        if previous:
            _note(report, f"{slug}: same English prompt as {previous}", as_error=strict or not legacy)
        else:
            prompts[prompt] = slug


def _validate_options(slug: str, options: list, report: ContentReport) -> None:
    if not 2 <= len(options) <= 6:
        report.errors.append(f"{slug}: expected 2–6 options, found {len(options)}")
        return
    correct = [option for option in options if option.get("is_correct")]
    if len(correct) != 1:
        report.errors.append(f"{slug}: expected exactly one correct option, found {len(correct)}")
    texts = [str(option.get("text_en") or "").strip() for option in options]
    if any(not text for text in texts):
        report.errors.append(f"{slug}: an option is missing English text")
    if len(texts) != len(set(texts)):
        report.errors.append(f"{slug}: two options have the same English text")
    if len(correct) == 1 and all(texts):
        right = str(correct[0].get("text_en") or "").strip()
        others = [text for text in texts if text != right]
        if others and len(right) > max(len(text) for text in others) + 20:
            report.warnings.append(f"{slug}: the correct option is much longer than the others")


def _validate_published(slug: str, item: dict, report: ContentReport, *, as_error: bool) -> None:
    level = item.get("level")
    skill = item.get("skill")
    profile = level_profile(level) if isinstance(level, int) else None
    if not str(item.get("learning_objective") or "").strip():
        _note(report, f"{slug}: published exercise has no learning objective", as_error=as_error)
    if not str(item.get("explanation_en") or "").strip() or not str(item.get("explanation_pl") or "").strip():
        _note(report, f"{slug}: published exercise has no bilingual explanation", as_error=as_error)
    scenario = str(item.get("scenario") or "").strip()
    if profile is not None and scenario not in profile.scenarios:
        _note(report, f"{slug}: scenario {scenario or '(empty)'} is not allowed at level {level}", as_error=as_error)
    if profile is not None and isinstance(level, int) and isinstance(skill, str):
        expected = competency_for(level, skill)
    else:
        expected = None
    if expected is not None and item.get("competency") != expected.id:
        _note(
            report,
            f"{slug}: competency {item.get('competency') or '(empty)'} does not match {expected.id}",
            as_error=as_error,
        )
    if not str(item.get("review_status") or "").strip() or not str(item.get("reviewed_by") or "").strip():
        _note(report, f"{slug}: published exercise has no review status or reviewer", as_error=as_error)
    if item.get("source_type") == "external" and not (
        str(item.get("source_url") or "").strip() and str(item.get("source_license") or "").strip()
    ):
        _note(report, f"{slug}: external item is missing a source URL or license", as_error=as_error)


def _language_notes(slug: str, item: dict, report: ContentReport, *, as_error: bool) -> None:
    fields = (
        "prompt_en",
        "prompt_pl",
        "content_en",
        "content_pl",
        "explanation_en",
        "explanation_pl",
        "title_en",
        "title_pl",
    )
    for name in fields:
        text = str(item.get(name) or "")
        if HTML_MARKUP.search(text):
            report.errors.append(f"{slug}: HTML in {name}")
        if PLACEHOLDER.search(text):
            _note(report, f"{slug}: placeholder in {name}", as_error=as_error)
    prompt_pl = str(item.get("prompt_pl") or "").strip()
    prompt_en = str(item.get("prompt_en") or "").strip()
    if not prompt_pl:
        _note(report, f"{slug}: missing Polish prompt", as_error=as_error)
    elif prompt_pl == prompt_en and len(prompt_en) > 12:
        _note(report, f"{slug}: Polish prompt repeats the English prompt", as_error=False)
    for text in (prompt_en, str(item.get("content_en") or "")):
        for sentence in re.split(r"[.!?]+", text):
            if len(sentence.split()) > 40:
                _note(report, f"{slug}: a sentence is longer than 40 words", as_error=False)
                return


def _note(report: ContentReport, message: str, *, as_error: bool) -> None:
    if as_error:
        report.errors.append(message)
    else:
        report.warnings.append(message)


def published_counts() -> Counter[tuple[int, str]]:
    counts: Counter[tuple[int, str]] = Counter()
    for item in load_exercises():
        if item.get("publication_status") == "published":
            level = item.get("level")
            skill = item.get("skill")
            if isinstance(level, int) and isinstance(skill, str):
                counts[(level, skill)] += 1
    return counts
