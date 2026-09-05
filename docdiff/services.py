import zipfile
from pathlib import Path

from django.conf import settings

OOXML_EXTENSIONS = {".docx", ".xlsx"}


def max_uncompressed_bytes() -> int:
    return int(getattr(settings, "DOCDIFF_MAX_UNCOMPRESSED_MB", 50)) * 1024 * 1024


def uncompressed_size_bytes(path: Path) -> int:
    """Return uncompressed payload size. OOXML files are ZIP containers."""
    path = Path(path)
    if path.suffix.lower() in OOXML_EXTENSIONS:
        with zipfile.ZipFile(path) as archive:
            return sum(info.file_size for info in archive.infolist())
    return path.stat().st_size


def exceeds_uncompressed_limit(path: Path) -> bool:
    return uncompressed_size_bytes(path) > max_uncompressed_bytes()
