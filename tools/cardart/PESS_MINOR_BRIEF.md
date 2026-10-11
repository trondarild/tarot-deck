# Brief: one pessimist minor suit, in the approved Isolation style

You are drawing one suit of the pessimist deck's minor series as code (SVG built in Python), in /Users/trond/Projects/tarot-deck. The Isolation suit is finished and approved by the user. It is your model in every respect except colour.

## Read first
- `tools/cardart/pess_minor_isolation.py` in full. It contains:
  - the Plate engine;
  - the age figures `child()`, `youth()`, `adult()` and `elder()`;
  - the helpers `fade`, `cast`, `mass`, `sky`, `window`, `floor_band` and `floor_shadow`;
  - the `CONTRAST` setting;
  - the `suit_colour(colour)` decorator.
- `tools/cardart/common.py`, the "minor cards" section:
  - `pess_pip_open(suit, n)` and `pess_pip_close()`, which draw the emblem frieze above `PESS_VIGNETTE`;
  - `pess_court_open(suit, age)` and `pess_court_close()`, with age 1 = Child … 4 = Elder;
  - the `WASH` palette.
- Your suit's entries in `docs/pessimistic-minor-symbolism.md`. Each card's Image paragraph (pips) or Figure paragraph (court cards) gives the scene.
- The approved cards `assets/img/pessimistic/is01.jpg` … `is14.jpg`, viewed with the Read tool. Match their line, hatching, contrast, dark masses and graded skies.

## Colour: each suit must be distinguishable
- Isolation is slate. Your suit uses its own colour from `WASH` in the same roles slate plays in Isolation: shadow washes, tints, sky gradients, night windows and the dark underlays.
- Wrap every card function in `@suit_colour(WASH["<your colour>"])` so the shared helpers draw in your colour. After rendering, check each card's SVG: slate (`#5E6B78`) should not appear except where you deliberately want a cool accent.
- Where a helper or `head()` hard-codes slate, pass your colour explicitly.
- The suit colour should dominate each card visibly, so that at thumbnail size a reader can tell your suit from Isolation without counting emblems. Keep the contrast and the dark masses: the darks become a deep version of your colour mixed with ink.
- You may use at most one other colour, small.

## Structure
- Create `tools/cardart/pess_minor_<suit>.py` with a module docstring, one drawing function per card, and a `CARDS` dict mapping your ids to them. Pips are 01–10 and court cards are 11–14.
- Import the engine, helpers and age figures from `.pess_minor_isolation`; do not copy them. New helpers go in your module.
- Pips: `pess_pip_open("<suit>", n)`, then a scene inside `PESS_VIGNETTE` from the Image paragraph, then `pess_pip_close()`. The frieze count is the card's number. Draw nothing near the frieze that looks like your emblem.
- Court cards: `pess_court_open("<suit>", age)`, then a scene from the Figure paragraph using the matching age helper as the main figure, then `pess_court_close()`.

## Rules
- No text or letters.
- No gore, and no depiction or suggestion of suicide or self-harm.
- Use only the rng passed in.
- SVG ids must be unique per card and must not reuse "inside", "scroll", "img", "fade" or "fadeMask".
- Figures must be readable, stand on the ground line, and have clear joints. Keep everything inside the image area.

## Process
1. After each card, render it with `python3 tools/svg_cards.py pessimistic:<id>` and view the JPEG with the Read tool. Fix problems, up to about three passes per card.
2. Once at least, put one of your cards side by side with `is06.jpg` to confirm the colours are distinct and the style matches.
3. Edit only your own module and render only your own cards. Do not touch `pess_minor_isolation.py`, `common.py`, `tools/svg_cards.py`, any doc, any other image, or `assets/img/pessimistic/maj00-pessimistic.png`. Do not commit.
4. When done, report the cards finished, any new helpers, and anything that falls short.
