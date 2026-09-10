"""Looping terminal GIF for the /wybierz/ kodzillin' tile."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).resolve().parents[1] / "static" / "rozdroze" / "img" / "code-bg.gif"
W, H = 560, 360
BG = (7, 11, 18)
GOLD = (212, 165, 53)
GREEN = (158, 214, 132)
CYAN = (120, 190, 210)
DIM = (90, 98, 110)
TEXT = (226, 226, 214)
PROMPT = ">>>"


def font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    for name in ("consola.ttf", "CONSOLA.TTF", "cour.ttf", "lucon.ttf"):
        try:
            return ImageFont.truetype(f"C:/Windows/Fonts/{name}", size)
        except OSError:
            continue
    return ImageFont.load_default()


BODY = font(20)
HEAD = font(16)
LINE_H = 26
PAD_X = 28
PAD_Y = 22


def draw_scanlines(im: Image.Image) -> Image.Image:
    overlay = Image.new("RGB", im.size, BG)
    d = ImageDraw.Draw(overlay)
    for y in range(0, H, 3):
        d.line((0, y, W, y), fill=(4, 6, 10))
    return Image.blend(im.convert("RGB"), overlay, 0.18)


def paint(lines: list[tuple[str, tuple[int, int, int]]], cursor: bool) -> Image.Image:
    im = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(im)
    y = PAD_Y
    d.text((PAD_X, y), "walery@code:~$ python", font=HEAD, fill=DIM)
    y += LINE_H + 6
    for text, color in lines:
        d.text((PAD_X, y), text, font=BODY, fill=color)
        y += LINE_H
    if cursor:
        bbox = d.textbbox((PAD_X, y - LINE_H), lines[-1][0] if lines else "", font=BODY)
        cx = bbox[2] + 4 if lines else PAD_X
        cy = y - LINE_H if lines else y
        d.rectangle((cx, cy + 4, cx + 10, cy + LINE_H - 6), fill=GOLD)
    return draw_scanlines(im)


def typewrite(frames: list, base: list[tuple[str, tuple[int, int, int]]], prefix: str, typed: str, color):
    shown = ""
    for ch in typed:
        shown += ch
        frames.append(paint(base + [(prefix + shown, color)], cursor=True))
        frames.append(paint(base + [(prefix + shown, color)], cursor=True))


def main() -> None:
    frames: list[Image.Image] = []
    hist: list[tuple[str, tuple[int, int, int]]] = []

    typewrite(frames, hist, f"{PROMPT} ", "who?", GOLD)
    hist.append((f"{PROMPT} who?", GOLD))
    hist.append(('"kodzillin\'"', GREEN))
    frames.append(paint(hist, cursor=False))
    frames.extend([paint(hist, cursor=False)] * 6)

    typewrite(frames, hist, f"{PROMPT} ", "what?", GOLD)
    hist.append((f"{PROMPT} what?", GOLD))
    hist.append(("[", TEXT))
    frames.append(paint(hist, cursor=False))
    for item in ('  "web",', '  "code",', '  "power bi",', '  "machine learning"'):
        hist.append((item, GREEN))
        frames.extend([paint(hist, cursor=False)] * 4)
    hist.append(("]", TEXT))
    frames.extend([paint(hist, cursor=False)] * 6)

    typewrite(frames, hist, f"{PROMPT} ", "uuu", GOLD)
    hist.append((f"{PROMPT} uuu", GOLD))
    hist.append(('"nom"', GREEN))
    hold = paint(hist, cursor=True)
    frames.extend([hold] * 10)
    blink_off = paint(hist, cursor=False)
    frames.extend([blink_off, hold, blink_off, hold, hold, hold])

    OUT.parent.mkdir(parents=True, exist_ok=True)
    frames[0].save(
        OUT,
        save_all=True,
        append_images=frames[1:],
        duration=90,
        loop=0,
        optimize=True,
    )
    print(f"wrote {OUT} frames={len(frames)} bytes={OUT.stat().st_size}")


if __name__ == "__main__":
    main()
