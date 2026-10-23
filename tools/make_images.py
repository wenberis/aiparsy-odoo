"""Icon and cover for apps.odoo.com from the AiParsy brand icon and a screenshot of a filled bill.

Usage: python tools/make_images.py <brand-icon-512.png> <filled-bill-screenshot.png>
"""

import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).resolve().parent.parent / "aiparsy_connector" / "static" / "description"
NAVY = (28, 37, 71)
CYAN = (95, 208, 224)
LIGHT = (252, 251, 248)
FONTS = "C:/Windows/Fonts/"


def font(name, size):
    return ImageFont.truetype(FONTS + name, size)


def icon(brand):
    Image.open(brand).convert("RGBA").resize((140, 140), Image.LANCZOS).save(OUT / "icon.png")


def cover(brand, screenshot):
    width, height = 1120, 560
    image = Image.new("RGB", (width, height), NAVY)
    draw = ImageDraw.Draw(image)
    logo = Image.open(brand).convert("RGBA").resize((72, 72), Image.LANCZOS)
    image.paste(logo, (56, 56), logo)
    draw.text((144, 66), "AiParsy for Odoo", font=font("segoeuib.ttf", 40), fill=LIGHT)
    lines = ["Vendor bills from scans", "for Ukrainian accounting"]
    for i, line in enumerate(lines):
        draw.text((56, 170 + i * 52), line, font=font("segoeuib.ttf", 34), fill=LIGHT)
    points = ["Waybills, acts, invoices", "Vendor found by ЄДРПОУ", "Lines and VAT 20/14/7/0 %"]
    for i, point in enumerate(points):
        y = 310 + i * 44
        draw.rounded_rectangle((56, y + 10, 70, y + 24), radius=4, fill=CYAN)
        draw.text((84, y), point, font=font("segoeui.ttf", 26), fill=LIGHT)
    shot = Image.open(screenshot).convert("RGB").crop((0, 46, 1440, 860))
    shot.thumbnail((560, 440), Image.LANCZOS)
    x, y = width - shot.width - 40, (height - shot.height) // 2
    draw.rounded_rectangle((x - 6, y - 6, x + shot.width + 6, y + shot.height + 6), radius=10, fill=LIGHT)
    image.paste(shot, (x, y))
    image.save(OUT / "banner.png")


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    icon(sys.argv[1])
    cover(sys.argv[1], sys.argv[2])
