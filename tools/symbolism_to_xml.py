#!/usr/bin/env python3
"""Copy the per-card symbolism from docs/*-symbolism.md into the decks' English locale files.

Each "## <numeral> — <title>" section of a symbolism file becomes a <symbolism> element
on the card with the same position (0 -> "00", I -> "01", ...); a section headed by a card
title alone ("## Ace of Wands") goes to the card with that <title>. One <section label="...">
per "**Label.** text" paragraph. Markdown *italics* become <em>. Existing <symbolism>
elements are replaced, so the script can be rerun after editing the docs.

Usage: python3 tools/symbolism_to_xml.py
"""

import re
from pathlib import Path
from xml.sax.saxutils import escape, quoteattr

ROOT = Path(__file__).resolve().parent.parent
# Deck -> symbolism files; a deck may draw on several (Zen: major and minor cards)
SOURCES = {
    "zen": ["docs/zen-buddhism-symbolism.md", "docs/zen-buddhism-minor-symbolism.md"],
    "pessimistic": ["docs/pessimistic-symbolism.md", "docs/pessimistic-minor-symbolism.md"],
    "rws-tarot": ["docs/rws-tarot-symbolism.md"],
}

# Decks whose cards without a <description> get one from the first sentence of
# their "In a reading" section (the Zen and pessimist minor cards are written that way)
DERIVE_DESCRIPTION = {"zen", "pessimistic"}
ROMAN = ["0", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X",
         "XI", "XII", "XIII", "XIV", "XV", "XVI", "XVII", "XVIII", "XIX", "XX", "XXI"]


def inline(text):
    """Escape for XML, then turn *italics* into <em>."""
    return re.sub(r"\*([^*]+)\*", r"<em>\1</em>", escape(text))


def parse(md, titles):
    """Return {card_id: [(label, paragraph), ...]} from the card sections of a symbolism file.

    titles maps card titles to ids, for sections headed by a title alone.
    """
    cards = {}
    for block in re.split(r"(?m)^## ", md)[1:]:
        heading, _, body = block.partition("\n")
        numeral = heading.split(" — ")[0].strip()
        if numeral in ROMAN:
            cid = f"{ROMAN.index(numeral):02d}"
        elif heading.strip() in titles:
            cid = titles[heading.strip()]
        else:
            continue  # e.g. "Sources"
        sections = []
        for para in re.split(r"\n\s*\n", body.strip()):
            m = re.match(r"\*\*([^*]+?)\.\*\*\s+(.*)", para.strip(), re.S)
            if m:
                sections.append((m.group(1), " ".join(m.group(2).split())))
        cards[cid] = sections
    return cards


def first_sentence(text):
    m = re.match(r"(.+?[.!?])(\s|$)", text)
    return m.group(1) if m else text


def symbolism_xml(sections):
    lines = ["    <symbolism>"]
    for label, text in sections:
        lines.append(f"      <section label={quoteattr(label)}><p>{inline(text)}</p></section>")
    lines.append("    </symbolism>")
    return "\n".join(lines)


def main():
    for deck, srcs in SOURCES.items():
        path = ROOT / "data" / "decks" / deck / "locales" / "deck.en.xml"
        xml = path.read_text()
        titles = {t: cid for cid, t in re.findall(r'<card id="([\w-]+)">\s*<title>([^<]+)</title>', xml)}
        cards = {}
        for src in srcs:
            if (ROOT / src).exists():
                cards.update(parse((ROOT / src).read_text(), titles))
        done = 0

        def replace(m):
            nonlocal done
            cid, inner = m.group(1), m.group(2)
            inner = re.sub(r"\s*<symbolism>.*?</symbolism>", "", inner, flags=re.S).rstrip()
            if cid not in cards:
                return m.group(0)
            done += 1
            if deck in DERIVE_DESCRIPTION and "<description>" not in inner:
                reading = dict(cards[cid]).get("In a reading")
                if reading:
                    inner += f"<description><p>{inline(first_sentence(reading))}</p></description>"
            return f'<card id="{cid}">{inner}\n{symbolism_xml(cards[cid])}\n  </card>'

        xml = re.sub(r'<card id="([\w-]+)">(.*?)\s*</card>', replace, xml, flags=re.S)
        path.write_text(xml)
        print(f"{deck}: symbolism for {done} of {len(cards)} cards written to {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
