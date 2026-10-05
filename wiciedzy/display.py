"""Turn a 0–5 training profile into words. Not a ranking of strength."""

from __future__ import annotations

from wiciedzy.dimensions import DIFF_COPY, DIMENSION_GROUPS, DIMENSION_LABELS, HEADLINE_AXES, level_words
from wiciedzy.models import Style, TrainingProfile

GROUP_LABELS = {
    "uderzenia": ("Uderzenia", "Striking"),
    "chwyt": ("Chwyt", "Grappling"),
    "bron": ("Broń", "Weapons"),
    "trening": ("Trening", "Training"),
}


def profile_groups(profile: TrainingProfile | None) -> list[dict]:
    if profile is None:
        return []
    groups: list[dict] = []
    for key, names in DIMENSION_GROUPS:
        label_pl, label_en = GROUP_LABELS[key]
        rows = []
        for name in names:
            word_pl, word_en = level_words(int(getattr(profile, name)))
            row_pl, row_en = DIMENSION_LABELS[name]
            rows.append({"pl": row_pl, "en": row_en, "word_pl": word_pl, "word_en": word_en})
        groups.append({"pl": label_pl, "en": label_en, "rows": rows})
    return groups


def paired_groups(left: list[dict], right: list[dict]) -> list[dict]:
    pairs: list[dict] = []
    for group_left, group_right in zip(left, right, strict=False):
        rows = []
        for row_left, row_right in zip(group_left["rows"], group_right["rows"], strict=False):
            rows.append(
                {
                    "pl": row_left["pl"],
                    "en": row_left["en"],
                    "left_pl": row_left["word_pl"],
                    "left_en": row_left["word_en"],
                    "right_pl": row_right["word_pl"],
                    "right_en": row_right["word_en"],
                }
            )
        pairs.append({"pl": group_left["pl"], "en": group_left["en"], "rows": rows})
    return pairs


def description_is_thin(style: Style) -> bool:
    """True when a discovery-only page is standing in for a second real source."""
    sources = list(style.sources.all())
    useful = [source for source in sources if source.quality != "discovery_only"]
    return any(source.quality == "discovery_only" for source in sources) and len(useful) < 2


def load_profile(style: Style) -> TrainingProfile | None:
    try:
        return style.profile
    except TrainingProfile.DoesNotExist:
        return None


COMPETITION_WORDS = {
    "sport": ("Zawody", "Competition"),
    "traditional": ("Praktyka tradycyjna", "Traditional practice"),
    "both": ("Zawody i tradycja", "Competition and tradition"),
    "none": ("Bez zawodów", "No competition"),
    "historical": ("Rekonstrukcja", "Reconstruction"),
}

WEAPON_WORDS = {
    "none": ("Bez broni", "No weapon"),
    "optional": ("Broń opcjonalna", "Optional weapon"),
    "primary": ("Broń główna", "Weapon first"),
    "training": ("Broń treningowa", "Training weapon"),
}


def _axis_row(profile: TrainingProfile, name: str) -> dict:
    word_pl, word_en = level_words(int(getattr(profile, name)))
    label_pl, label_en = DIMENSION_LABELS[name]
    return {"pl": label_pl, "en": label_en, "word_pl": word_pl, "word_en": word_en, "name": name}


def split_profile(profile: TrainingProfile | None) -> tuple[list[dict], list[dict]]:
    if profile is None:
        return [], []
    headline = [_axis_row(profile, name) for name in HEADLINE_AXES]
    hidden = {name for name in HEADLINE_AXES}
    rest: list[dict] = []
    for key, names in DIMENSION_GROUPS:
        rows = [_axis_row(profile, name) for name in names if name not in hidden]
        if not rows:
            continue
        label_pl, label_en = GROUP_LABELS[key]
        rest.append({"pl": label_pl, "en": label_en, "rows": rows})
    return headline, rest


def character_label(profile: TrainingProfile | None) -> tuple[str, str] | None:
    if profile is None:
        return None
    best_key = ""
    best_mean = -1.0
    for key, names in DIMENSION_GROUPS:
        if key == "trening":
            continue
        mean = sum(int(getattr(profile, name)) for name in names) / len(names)
        if mean > best_mean:
            best_mean = mean
            best_key = key
    if not best_key:
        return None
    return GROUP_LABELS[best_key]


def quick_profile(style: Style, profile: TrainingProfile | None) -> dict:
    types = list(style.style_types.all())
    character = character_label(profile)
    contact = None
    solo = None
    partner = None
    if profile is not None:
        contact = level_words(int(profile.contact_level))
        solo = level_words(int(profile.solo_training))
        partner = level_words(int(profile.partner_training))
    competition = COMPETITION_WORDS.get(style.competition_status, ("", ""))
    weapon = WEAPON_WORDS.get(style.weapon_status, ("", ""))
    return {
        "types": types,
        "character": character,
        "contact": contact,
        "competition": competition,
        "weapon": weapon,
        "solo": solo,
        "partner": partner,
    }


def key_differences(left: Style, right: Style, left_profile: TrainingProfile | None, right_profile: TrainingProfile | None) -> list[dict]:
    if left_profile is None or right_profile is None:
        return []
    gaps: list[tuple[int, str]] = []
    for name in DIFF_COPY:
        left_score = int(getattr(left_profile, name))
        right_score = int(getattr(right_profile, name))
        if level_words(left_score)[0] == level_words(right_score)[0]:
            continue
        gaps.append((abs(left_score - right_score), name))
    gaps.sort(key=lambda item: (-item[0], item[1]))
    lines: list[dict] = []
    for _gap, name in gaps[:3]:
        left_score = int(getattr(left_profile, name))
        right_score = int(getattr(right_profile, name))
        if left_score >= right_score:
            higher_pl, higher_en = left.name_pl, left.name_en
            lower_pl, lower_en = right.name_pl, right.name_en
        else:
            higher_pl, higher_en = right.name_pl, right.name_en
            lower_pl, lower_en = left.name_pl, left.name_en
        template_pl, template_en = DIFF_COPY[name]
        lines.append(
            {
                "pl": template_pl.format(higher=higher_pl, lower=lower_pl),
                "en": template_en.format(higher=higher_en, lower=lower_en),
            }
        )
    return lines
