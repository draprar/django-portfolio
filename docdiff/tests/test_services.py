import zipfile

from docdiff.services import exceeds_uncompressed_limit, uncompressed_size_bytes


def test_uncompressed_size_txt(tmp_path):
    path = tmp_path / "note.txt"
    path.write_bytes(b"hello")
    assert uncompressed_size_bytes(path) == 5


def test_uncompressed_size_zip_container(tmp_path):
    path = tmp_path / "doc.docx"
    with zipfile.ZipFile(path, "w") as archive:
        archive.writestr("word/document.xml", "x" * 2048)
    assert uncompressed_size_bytes(path) == 2048


def test_exceeds_uncompressed_limit(tmp_path, settings):
    settings.DOCDIFF_MAX_UNCOMPRESSED_MB = 0
    path = tmp_path / "note.txt"
    path.write_bytes(b"too-big")
    assert exceeds_uncompressed_limit(path) is True


def test_within_uncompressed_limit(tmp_path, settings):
    settings.DOCDIFF_MAX_UNCOMPRESSED_MB = 50
    path = tmp_path / "note.txt"
    path.write_bytes(b"ok")
    assert exceeds_uncompressed_limit(path) is False
