#!/usr/bin/env python3
"""Generate placeholder card images for decks that have no artwork yet.

Reads the deck registry (data/decks.xml) and writes one JPEG per card at the
path deck.xsl expects. Existing files are never overwritten, so real artwork
can replace placeholders one card at a time.

Usage: python3 tools/make_placeholders.py [deck-id ...]   (default: all decks)
Requires Pillow. Fonts are the macOS system fonts listed below.
"""

import sys
import textwrap
import xml.etree.ElementTree as ET
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
SIZE = (340, 578)  # 1:1.7, the aspect ratio of .card-image in main.css

SERIF = "/System/Library/Fonts/Supplemental/Georgia.ttf"
CJK = "/System/Library/Fonts/Supplemental/Songti.ttc"
CJK_INDEX = 2  # Songti TC Bold: has the traditional characters (來, 無, 鄽)

# Pessimist deck: dominant wash per card, from docs/pessimistic-philosophy-illustration-description.md
WASH = {"bone": "#D8C59A", "slate": "#5E6B78", "caput": "#5A2E2E", "verdigris": "#6F8C7A"}
PESSIMIST_WASH = {
    "00": "bone", "02": "bone", "05": "bone", "13": "bone",
    "03": "slate", "07": "slate", "08": "slate", "15": "slate",
    "04": "caput", "06": "caput", "09": "caput", "12": "caput",
    "01": "verdigris", "10": "verdigris", "11": "verdigris", "14": "verdigris",
}


def image_name(deck_type, cid):
    """Mirror the image naming in deck.xsl."""
    if deck_type == "tarot":
        if len(cid) == 2:
            return f"maj{cid}"
        for prefix, suit in (("w", "wands"), ("c", "cups"), ("s", "swords"), ("p", "pents")):
            if len(cid) == 3 and cid.startswith(prefix):  # RWS minors: w01 ... p14
                return f"{suit}{cid[1:]}"
    return cid


def font(path, size, index=0):
    return ImageFont.truetype(path, size, index=index)


def centred(draw, y, text, fnt, fill):
    w = draw.textlength(text, font=fnt)
    draw.text(((SIZE[0] - w) / 2, y), text, font=fnt, fill=fill)


def title_lines(draw, y, title, fnt, fill, width=22, leading=30):
    for line in textwrap.wrap(title, width):
        centred(draw, y, line, fnt, fill)
        y += leading


def zen(card):
    img = Image.new("RGB", SIZE, "#F3EBDD")
    d = ImageDraw.Draw(img)
    ink = "#2B2B2B"
    # Ensō: a thick, slightly open circle
    box = (45, 120, 295, 370)
    d.arc(box, start=-60, end=270, fill=ink, width=14)
    if card["glyph"]:
        size = {1: 72, 2: 64, 3: 48, 4: 44}.get(len(card["glyph"]), 34)
        g = font(CJK, size, CJK_INDEX)
        w = d.textlength(card["glyph"], font=g)
        d.text(((SIZE[0] - w) / 2, 245 - size * 0.7), card["glyph"], font=g, fill=ink)
    centred(d, 40, card["number"], font(SERIF, 34), ink)
    title_lines(d, 410, card["title"], font(SERIF, 22), ink)
    d.rectangle((282, 528, 306, 552), fill="#B5452F")  # vermilion seal
    return img


def pessimist(card):
    img = Image.new("RGB", SIZE, "#F4F0E6")
    d = ImageDraw.Draw(img)
    ink = "#2A2622"
    # Thin the wash toward the paper colour, as a watercolour tint would be
    wash = Image.blend(Image.new("RGB", (1, 1), "#F4F0E6"),
                       Image.new("RGB", (1, 1), WASH[PESSIMIST_WASH.get(card["id"], "slate")]), 0.45).getpixel((0, 0))
    # Plate mark, with the card's dominant wash inside it
    d.rectangle((24, 24, SIZE[0] - 24, SIZE[1] - 24), outline="#B9B2A4", width=3)
    d.rectangle((40, 110, SIZE[0] - 40, 380), fill=wash)
    centred(d, 44, card["number"], font(SERIF, 34), ink)
    title_lines(d, 410, card["title"], font(SERIF, 22), ink)
    return img


def generic(card):
    img = Image.new("RGB", SIZE, "#D8DEE9")
    d = ImageDraw.Draw(img)
    ink = "#2E3440"
    d.rectangle((12, 12, SIZE[0] - 12, SIZE[1] - 12), outline=ink, width=3)
    centred(d, 200, card["number"], font(SERIF, 48), ink)
    title_lines(d, 300, card["title"], font(SERIF, 22), ink)
    centred(d, SIZE[1] - 60, card["deck_name"], font(SERIF, 16), ink)
    return img


STYLES = {"zen": zen, "pessimistic": pessimist}


def cards_of(deck):
    structure = ET.parse(DATA / deck.find("structure").get("href")).getroot()
    metadata = ET.parse(DATA / deck.find("metadata").get("href")).getroot()
    locale_el = deck.find("locales/locale[@lang='en']")
    locale = ET.parse(DATA / locale_el.get("href")).getroot() if locale_el is not None else None

    for card in structure.iter("card"):
        cid = card.get("id")
        meta = metadata.find(f"card[@id='{cid}']")
        loc = locale.find(f"card[@id='{cid}']") if locale is not None else None
        glyph = meta.find("custom/attribute[@name='glyph']") if meta is not None else None
        yield {
            "id": cid,
            "number": meta.findtext("core/displayNumber", cid) if meta is not None else cid,
            "title": loc.findtext("title", cid) if loc is not None else cid,
            "glyph": glyph.get("value") if glyph is not None else None,
            "deck_name": deck.findtext("name"),
        }


def main(selected):
    registry = ET.parse(DATA / "decks.xml").getroot()
    for deck in registry.findall("deck"):
        deck_id = deck.get("id")
        if selected and deck_id not in selected:
            continue
        out_dir = ROOT / deck.find("images").get("basePath")
        out_dir.mkdir(parents=True, exist_ok=True)
        draw = STYLES.get(deck_id, generic)
        made = 0
        for card in cards_of(deck):
            path = out_dir / f"{image_name(deck.get('type'), card['id'])}.jpg"
            if path.exists():
                continue
            draw(card).save(path, "JPEG", quality=85)
            made += 1
        print(f"{deck_id}: {made} placeholders written to {out_dir.relative_to(ROOT)}")


if __name__ == "__main__":
    main(set(sys.argv[1:]))
