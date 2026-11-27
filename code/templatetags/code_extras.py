import re

from django import template
from django.utils.html import conditional_escape, format_html
from django.utils.safestring import mark_safe

register = template.Library()

ASIDE_PATTERN = re.compile(r"\[[^\]]*\]")


@register.filter
def aside_markup(value):
    text = str(value)
    parts = []
    last_end = 0

    for match in ASIDE_PATTERN.finditer(text):
        parts.append(conditional_escape(text[last_end:match.start()]))
        parts.append(format_html('<span class="aside">{}</span>', match.group()))
        last_end = match.end()

    parts.append(conditional_escape(text[last_end:]))
    return mark_safe("".join(str(part) for part in parts))
