"""Links that keep a borrowed sentence attached to its license."""

from __future__ import annotations

import re

from django import template

register = template.Library()

LICENSE_HREFS = {
    "CC BY-SA 4.0": "https://creativecommons.org/licenses/by-sa/4.0/",
    "CC BY 2.0 FR": "https://creativecommons.org/licenses/by/2.0/fr/",
    "CC BY 2.0": "https://creativecommons.org/licenses/by/2.0/",
}
TATOEBA_ID = re.compile(r"Tatoeb\w* #(\d+)")


@register.filter
def license_href(license_name: str) -> str:
    return LICENSE_HREFS.get((license_name or "").strip(), "")


@register.filter
def tatoeba_sentence_url(text: str) -> str:
    match = TATOEBA_ID.search(text or "")
    if match is None:
        return ""
    return f"https://tatoeba.org/en/sentences/show/{match.group(1)}"
