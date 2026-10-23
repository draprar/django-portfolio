from pathlib import Path

import pytest

from wiciedzy import build_audyt_prompt as prompt


def test_audyt_prompt_header_mentions_catalog_size():
    assert "46" in prompt.HEADER
    assert "wiciędze" in prompt.HEADER


def test_audyt_prompt_main_writes_output(tmp_path, monkeypatch):
    root = tmp_path
    (root / "data").mkdir()
    styles = (
        "CORE = []\n"
        "RELATIONS: = [{'a': 1}]\n"
        "UMBRELLAS = []\n"
    )
    (root / "data" / "styles.py").write_text(styles, encoding="utf-8")
    (root / "teksty-audyt-eksport.md").write_text("# A\n", encoding="utf-8")
    (root / "katalog-opisy.md").write_text("# B\n", encoding="utf-8")
    (root / "quizopasowanie.md").write_text("# C\n", encoding="utf-8")

    monkeypatch.setattr(prompt, "ROOT", root)
    prompt.main()

    out = root / "prompt-audyt-chatgpt.md"
    assert out.is_file()
    text = out.read_text(encoding="utf-8-sig")
    assert "Sekcja D" in text
    assert "RELATIONS:" in text
    assert "# A" in text
    assert "# B" in text
    assert "# C" in text


def test_audyt_source_files_exist_in_repo():
    root = Path(prompt.ROOT)
    for name in ("teksty-audyt-eksport.md", "katalog-opisy.md", "quizopasowanie.md", "data/styles.py"):
        path = root / name
        if not path.exists():
            pytest.skip(f"optional audit source missing: {name}")
        assert path.stat().st_size > 0
