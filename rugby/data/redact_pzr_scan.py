"""Mask contact blocks on encyclopedia scan; preserve original in private/."""
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
STATIC = ROOT / "static" / "rugby" / "img"
PRIVATE = ROOT / "private" / "scans"
SRC = STATIC / "pzr.png"
ORIG = PRIVATE / "pzr_original.png"


def main() -> None:
    PRIVATE.mkdir(parents=True, exist_ok=True)
    if SRC.exists() and not ORIG.exists():
        ORIG.write_bytes(SRC.read_bytes())
    elif not ORIG.exists():
        raise SystemExit(f"Missing {SRC}")
    im = Image.open(ORIG if ORIG.exists() else SRC).convert("RGB")
    w, h = im.size
    draw = ImageDraw.Draw(im)
    fill = (12, 12, 12)
    draw.rectangle([int(w * 0.52), int(h * 0.58), int(w * 0.98), int(h * 0.72)], fill=fill)
    draw.rectangle([int(w * 0.52), int(h * 0.38), int(w * 0.98), int(h * 0.44)], fill=fill)
    im.save(SRC, format="PNG", optimize=True)
    print("redacted", SRC)


if __name__ == "__main__":
    main()
