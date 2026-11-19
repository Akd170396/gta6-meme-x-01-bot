#!/usr/bin/env python3
"""Render the GTA 6 meme: AI illustration + crisp caption text.

The base illustration (media-generation-gta6-meme-chucky-base-*.png) was made
with an image generator and carries no text on purpose. This script adds the
caption bands and the bus-stop sign text with PIL so every letter is spelled
right and stays readable when the picture is shrunk to 480x480.
"""

import glob
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

REPO = Path(__file__).resolve().parent
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

TOP_TEXT = "13 YEARS WAITING FOR GTA 6"
BOTTOM_LINES = ["MEANWHILE MY AI AGENT EARNS", "REAL MONEY ON MAKE.FUN"]
SIGN_TEXT = "VICE CITY"

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
MAGENTA = (233, 30, 156)


def fit_font(draw, text, max_width, start_size):
    """Largest bold font size whose rendered text fits max_width."""
    size = start_size
    while size > 10:
        font = ImageFont.truetype(FONT_BOLD, size)
        if draw.textlength(text, font=font) <= max_width:
            return font
        size -= 4
    return ImageFont.truetype(FONT_BOLD, 10)


def centered(draw, text, font, cx, cy, fill):
    box = draw.textbbox((0, 0), text, font=font)
    w = box[2] - box[0]
    h = box[3] - box[1]
    draw.text((cx - w / 2 - box[0], cy - h / 2 - box[1]), text, font=font, fill=fill)


def main():
    base_path = sorted(glob.glob(str(REPO / "media-generation-gta6-meme-chucky-base-*.png")))[0]
    img = Image.open(base_path).convert("RGB")
    width, height = img.size
    draw = ImageDraw.Draw(img)

    # Top caption band.
    top_band = int(height * 0.12)
    draw.rectangle([0, 0, width, top_band], fill=BLACK)
    top_font = fit_font(draw, TOP_TEXT, int(width * 0.94), 140)
    centered(draw, TOP_TEXT, top_font, width / 2, top_band / 2, WHITE)

    # Bottom caption band, two lines; MAKE.FUN picked out in magenta.
    bottom_band = int(height * 0.17)
    y0 = height - bottom_band
    draw.rectangle([0, y0, width, height], fill=BLACK)
    longest = max(BOTTOM_LINES, key=len)
    bottom_font = fit_font(draw, longest, int(width * 0.94), 120)
    line_h = bottom_band / len(BOTTOM_LINES)
    for i, line in enumerate(BOTTOM_LINES):
        cy = y0 + line_h * (i + 0.5)
        if line.endswith("MAKE.FUN"):
            head = line[: -len("MAKE.FUN")]
            total_w = draw.textlength(line, font=bottom_font)
            x = width / 2 - total_w / 2
            box = draw.textbbox((0, 0), line, font=bottom_font)
            ty = cy - (box[3] - box[1]) / 2 - box[1]
            draw.text((x, ty), head, font=bottom_font, fill=WHITE)
            draw.text(
                (x + draw.textlength(head, font=bottom_font), ty),
                "MAKE.FUN",
                font=bottom_font,
                fill=MAGENTA,
            )
        else:
            centered(draw, line, bottom_font, width / 2, cy, WHITE)

    # Bus-stop sign text: the chucky illustration's blank sign is the tall
    # rounded rectangle on the left, so stack the words upright on it.
    sign_font = fit_font(draw, "VICE", 165, 64)
    centered(draw, "VICE", sign_font, 133, 368, (10, 40, 40))
    centered(draw, "CITY", sign_font, 133, 438, (10, 40, 40))

    out = REPO / "meme.png"
    img.save(out, "PNG")
    print(f"wrote {out} ({width}x{height})")


if __name__ == "__main__":
    main()
