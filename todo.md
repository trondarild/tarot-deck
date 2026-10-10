# TODO
- General note: employ high-affordability subagents where possible
- [x] research a Zen Buddhism inspired deck - the Zen Buddhistic version of Major Arcane do not have to map to the European one, there can be more or less major cards to fit the Buddhistic philosophies and schemas
- [x] write the symbolism description for each card in zen-buddhism-symbolism.md
- [x] write descriptions for an image llm to generate the images of each major Arcana card in zen-buddhism-illustration-descriptions.md
- [x] research a pessimistic philosophy inspired deck - like the zen buddhism version the number of major cards do not have to map to the original version
- [x] write symbolism description for each card in pessmistic-symbolism.md
- [x] write image-llm descriptions for each pessimistic philosophy card in pessimistic-philosophy-illustration-description.md
- [x] add play or 'pull' functionality to the system; this should be implemented by having a 'shuffle' button, then a 'pull' button; cards are placed sequentially on the screen by default, and conform to the size of the window, wrapping to next line
- [x] add functionality for choosing the zen and pessimistic decks when playing
- [x] when clicking on a card so it shows the full image, show also the symbolism text, below the image 
- [x] add a symbolism document for the Rider-Waite-Smith tarot and show it with each card
- [x] write the minor cards for the zen deck
- [x] write the minor cards for the pessimistic deck

## Illustrations for the minor cards (131: Zen 75, pessimist 56)

Source for every card: the **Image** (pips) or **Figure** (ranks/courts) paragraph in `docs/*-minor-symbolism.md`.
Track A = image-model prompts (for mflux/Z-Image, see `docs/local-img-gen-path.md`); Track B = code-drawn art in `tools/cardart/`.

Decisions (defaults in brackets; change before the step that depends on them):
- [x] choose tracks [both, A first]
- [x] choose pip design: scenic / emblem / hybrid [hybrid: n suit emblems, arranged by number, plus a small vignette from the Image paragraph]
- [x] choose suit emblems [Zen: gorintō shapes — cube, sphere, pyramid, half-moon, jewel; pessimist: shutter, anchor, spinning top, burin]

Track A — prompts:
- [x] write `tools/prompts_from_symbolism.py` (Image/Figure paragraph + deck style suffix + suit cue → one prompt per card)
- [x] generate `docs/zen-minor-illustration-prompts.md` and `docs/pessimistic-minor-illustration-prompts.md`
- [x] generate batch files (card id, output path, prompt, seed) for local generation

Track B — code-drawn art:
- [x] add shared minor-card helpers to `tools/cardart/common.py`: suit emblems, emblem layouts for 1–10, vignette area
- [x] draw one sample suit (Zen Earth) and review it before scaling (approved with change: rank cards count the rank 1–5 in vermilion emblems on the dice-face pattern)
- [ ] Zen suits, one subagent each (`tools/cardart/zen_minor_<suit>.py`): Earth, Water, Fire, Wind, Void
- [ ] Zen rank cards: consistent figure type per rank across the five suits
- [ ] pessimist suits, one subagent each (`tools/cardart/pess_minor_<suit>.py`): Isolation, Anchoring, Distraction, Sublimation
- [ ] pessimist court cards: the same figure at four ages (Child, Youth, Adult, Elder) across the suits
- [ ] review contact sheets per suit (emblems, frames, colour, figure types) and fix
- [ ] commit and push suit by suit
