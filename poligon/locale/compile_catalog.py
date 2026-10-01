"""Write django.mo from django.po. Used when GNU gettext is not installed."""

from __future__ import annotations

import ast
import json
import struct
from pathlib import Path


def parse_po(text: str) -> list[tuple[str, str]]:
    pairs: list[tuple[str, str]] = []
    msgid: str | None = None
    msgstr: str | None = None
    bucket: str | None = None
    for raw in text.splitlines():
        line = raw.strip()
        if line.startswith("msgid "):
            if msgid is not None and msgstr is not None:
                pairs.append((msgid, msgstr))
            msgid = ast.literal_eval(line[len("msgid ") :])
            msgstr = None
            bucket = "id"
        elif line.startswith("msgstr "):
            msgstr = ast.literal_eval(line[len("msgstr ") :])
            bucket = "str"
        elif line.startswith('"') and bucket == "id" and msgid is not None:
            msgid += ast.literal_eval(line)
        elif line.startswith('"') and bucket == "str" and msgstr is not None:
            msgstr += ast.literal_eval(line)
    if msgid is not None and msgstr is not None:
        pairs.append((msgid, msgstr))
    return pairs


def write_mo(pairs: list[tuple[str, str]], path: Path) -> None:
    pairs = sorted(pairs, key=lambda item: item[0].encode())
    ids = [item[0].encode() + b"\0" for item in pairs]
    strs = [item[1].encode() + b"\0" for item in pairs]
    count = len(pairs)
    key_table = 7 * 4
    value_table = key_table + count * 8
    offset = value_table + count * 8
    key_meta: list[tuple[int, int]] = []
    for blob in ids:
        key_meta.append((len(blob) - 1, offset))
        offset += len(blob)
    value_meta: list[tuple[int, int]] = []
    for blob in strs:
        value_meta.append((len(blob) - 1, offset))
        offset += len(blob)
    chunks = [struct.pack("<Iiiiiii", 0x950412DE, 0, count, key_table, value_table, 0, key_table)]
    chunks.extend(struct.pack("<II", length, off) for length, off in key_meta)
    chunks.extend(struct.pack("<II", length, off) for length, off in value_meta)
    chunks.extend(ids)
    chunks.extend(strs)
    path.write_bytes(b"".join(chunks))


def main() -> None:
    locale = Path(__file__).resolve().parent
    english = locale / "en" / "LC_MESSAGES"
    pairs = parse_po((english / "django.po").read_text(encoding="utf-8"))
    write_mo(pairs, english / "django.mo")
    polish = locale / "pl" / "LC_MESSAGES"
    polish.mkdir(parents=True, exist_ok=True)
    header = next(msgstr for msgid, msgstr in pairs if msgid == "")
    header = header.replace("Language: en", "Language: pl")
    identity = [(msgid, msgid if msgid else header) for msgid, _msgstr in pairs]
    write_mo(identity, polish / "django.mo")
    lines = [
        'msgid ""',
        'msgstr ""',
        '"Content-Type: text/plain; charset=UTF-8\\n"',
        '"Language: pl\\n"',
        "",
    ]
    for msgid, _msgstr in pairs:
        if not msgid:
            continue
        lines.append(f"msgid {json.dumps(msgid, ensure_ascii=False)}")
        lines.append(f"msgstr {json.dumps(msgid, ensure_ascii=False)}")
        lines.append("")
    (polish / "django.po").write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {len(pairs)} strings")


if __name__ == "__main__":
    main()
