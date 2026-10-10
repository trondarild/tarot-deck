#!/usr/bin/env python3
"""Render code-drawn card art (tools/cardart) to JPEG at the paths deck.xsl expects.

Usage:
  python3 tools/svg_cards.py                      # every card that has a drawing
  python3 tools/svg_cards.py zen                  # one deck
  python3 tools/svg_cards.py zen:01,02 pessimistic:00

Writes assets/img/{deck}/majNN.jpg (minor cards: {id}.jpg) and the SVG source beside it.
Rendering uses headless Chrome through playwright-core: run `npm install` in tools/ once.
"""

import importlib
import json
import random
import subprocess
import sys
from pathlib import Path

from PIL import Image

TOOLS = Path(__file__).resolve().parent
ROOT = TOOLS.parent
sys.path.insert(0, str(TOOLS))

# Modules per deck; each defines CARDS = {card_id: draw(rng) -> svg string}
MODULES = {
    "zen": ["zen_way", "zen_transmission"]
           + [f"zen_minor_{s}" for s in ("earth", "water", "fire", "wind", "void")],
    "pessimistic": ["pess_awakening", "pess_world"]
                   + [f"pess_minor_{s}" for s in ("isolation", "anchoring", "distraction", "sublimation")],
}


def drawings(deck):
    cards = {}
    for name in MODULES[deck]:
        try:
            mod = importlib.import_module(f"cardart.{name}")
        except ModuleNotFoundError as e:
            if e.name == f"cardart.{name}":
                continue  # module not written yet
            raise
        cards.update(mod.CARDS)
    return cards


def parse(args):
    if not args:
        return {deck: None for deck in MODULES}
    jobs = {}
    for arg in args:
        deck, _, ids = arg.partition(":")
        if deck not in MODULES:
            sys.exit(f"unknown deck: {deck}")
        jobs[deck] = ids.split(",") if ids else None
    return jobs


def main(args):
    pairs = []
    for deck, ids in parse(args).items():
        cards = drawings(deck)
        for cid in ids or sorted(cards):
            if cid not in cards:
                sys.exit(f"no drawing for {deck}:{cid}")
            # Seed from deck and card so each card renders the same every time
            doc = cards[cid](random.Random(f"{deck}-{cid}"))
            out_dir = ROOT / "assets" / "img" / deck
            # Major cards are majNN; minor cards use their id, as in deck.xsl
            name = f"maj{cid}" if len(cid) == 2 else cid
            svg_path = out_dir / f"{name}.svg"
            svg_path.write_text(doc)
            pairs.append((str(svg_path), str(out_dir / f"{name}.png")))
    if not pairs:
        return
    subprocess.run(["node", str(TOOLS / "render_svg.js"), json.dumps(pairs)], cwd=TOOLS, check=True)
    for _, png in pairs:
        jpg = Path(png).with_suffix(".jpg")
        Image.open(png).convert("RGB").save(jpg, "JPEG", quality=90)
        Path(png).unlink()
        print("wrote", jpg.relative_to(ROOT))


if __name__ == "__main__":
    main(sys.argv[1:])
