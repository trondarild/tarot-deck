#!/usr/bin/env python3
"""Copy the per-card symbolism from docs/*-symbolism.md into the decks' English locale files.

Each "## <numeral> — <title>" section of a symbolism file becomes a <symbolism> element
on the card with the same position (0 -> "00", I -> "01", ...), one <section label="...">
per "**Label.** text" paragraph. Markdown *italics* become <em>. Existing <symbolism>
elements are replaced, so the script can be rerun after editing the docs.

Usage: python3 tools/symbolism_to_xml.py
"""

import re
from pathlib import Path
from xml.sax.saxutils import escape, quoteattr

ROOT = Path(__file__).resolve().parent.parent
SOURCES = {
    "zen": "docs/zen-buddhism-symbolism.md",
    "pessimistic": "docs/pessimistic-symbolism.md",
}
ROMAN = ["0", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X",
         "XI", "XII", "XIII", "XIV", "XV", "XVI", "XVII", "XVIII", "XIX", "XX", "XXI"]


def inline(text):
    """Escape for XML, then turn *italics* into <em>."""
    return re.sub(r"\*([^*]+)\*", r"<em>\1</em>", escape(text))


def parse(md):
    """Return {card_id: [(label, paragraph), ...]} from the card sections of a symbolism file."""
    cards = {}
    for block in re.split(r"(?m)^## ", md)[1:]:
        heading, _, body = block.partition("\n")
        numeral = heading.split(" — ")[0].strip()
        if numeral not in ROMAN:
            continue  # e.g. "Sources"
        sections = []
        for para in re.split(r"\n\s*\n", body.strip()):
            m = re.match(r"\*\*([^*]+?)\.\*\*\s+(.*)", para.strip(), re.S)
            if m:
                sections.append((m.group(1), " ".join(m.group(2).split())))
        cards[f"{ROMAN.index(numeral):02d}"] = sections
    return cards


def symbolism_xml(sections):
    lines = ["    <symbolism>"]
    for label, text in sections:
        lines.append(f"      <section label={quoteattr(label)}><p>{inline(text)}</p></section>")
    lines.append("    </symbolism>")
    return "\n".join(lines)


def main():
    for deck, src in SOURCES.items():
        cards = parse((ROOT / src).read_text())
        path = ROOT / "data" / "decks" / deck / "locales" / "deck.en.xml"
        xml = path.read_text()
        done = 0

        def replace(m):
            nonlocal done
            cid, inner = m.group(1), m.group(2)
            inner = re.sub(r"\s*<symbolism>.*?</symbolism>", "", inner, flags=re.S).rstrip()
            if cid not in cards:
                return m.group(0)
            done += 1
            return f'<card id="{cid}">{inner}\n{symbolism_xml(cards[cid])}\n  </card>'

        xml = re.sub(r'<card id="(\d+)">(.*?)\s*</card>', replace, xml, flags=re.S)
        path.write_text(xml)
        print(f"{deck}: symbolism for {done} of {len(cards)} cards written to {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
