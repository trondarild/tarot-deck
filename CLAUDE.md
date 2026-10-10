# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A multilingual card-deck reference built from XML, DTDs and a single XSLT 1.0 stylesheet, with no build step. The project is a learning platform for XPath, XSLT and XML-as-database; the XML files play the role of database tables. Treat that framing as a design constraint: queries and joins belong in XSLT/XPath, and JavaScript stays limited to UI behaviour.

## Commands

There is no build, lint or test tooling. Serve the repository root and open an entry point in a browser:

```bash
npx http-server . -p 8080     # then http://localhost:8080/index.xml or /index-uk.xml
```

The site must be served over HTTP. Native browser XSLT (triggered by `<?xml-stylesheet?>`) cannot `document()`-load the data files from `file://`.

Validate data against the DTDs (the `<!DOCTYPE ... SYSTEM ...>` in each file points at `data/schemas/`); no output means valid:

```bash
xmllint --noout --valid data/decks.xml data/decks/*/structure.xml data/decks/*/metadata.xml data/decks/*/locales/*.xml
```

`xsltproc` is also available for checking the stylesheet from the command line. Markdown is linted with `.markdownlint.yaml` (MD013 off); `.editorconfig` requires 2-space indent, LF, final newline.

## Architecture

Rendering is entirely client-side. `index.xml` / `index-uk.xml` are tiny `<page lang="...">` documents whose only job is to carry the language and the `xml-stylesheet` link to `styles/deck.xsl`. The stylesheet then pulls everything else in with `document()`:

```text
data/decks.xml                          registry: one <deck> per deck, with hrefs to the files below
data/decks/{id}/structure.xml           card hierarchy: nested <group type= value=> containing <card id= order=>
data/decks/{id}/metadata.xml            per-card attributes, namespaced by deck type (<core>, <tarot>, <playing>, <oracle>)
data/decks/{id}/locales/deck.{lang}.xml per-language <title> and <description><p>
data/locales/ui.xml                     interface strings, one <strings lang=> per language, shared by all decks
data/schemas/*.dtd                      one DTD per file kind
```

Cards are joined across files by `@id`: `structure.xml` supplies the ordering and grouping, and `deck.xsl` looks up `$db_metadata/card[@id=$cid]` and `$db_locale/card[@id=$cid]` for each card. `deck.xsl` renders the hierarchy recursively (`group` in `mode="recursive"`), so a deck can nest groups to any depth.

Things that span files and are easy to miss:

- **Adding or changing a deck** touches `decks.xml` (registry entry, `cardCount`, `images/@basePath`), the deck's three data files, and possibly `deck.xsl`. `deck/@type` is restricted by `decks.dtd` to `tarot|playing-cards|oracle`, and the stylesheet branches on it for image naming and header fields.
- **Image filenames are derived in `deck.xsl`**, not stored in data. For tarot, card id `00`–`21` maps to `maj{id}.jpg`, and `w|c|s|p{nn}` maps to `wands|cups|swords|pents{nn}.jpg`; other deck types use `{id}.jpg`. Only the RWS images exist under `assets/img/big/`; the `playing/` and `lenormand/` base paths in the registry have no images yet.
- **Metadata and locale fields are optional per card.** The stylesheet uses `xsl:if`/`xsl:choose` to tolerate missing `hebrew`, `astrology`, `description`, and falls back to the card id when a title is absent.
- **Adding a language** needs `deck.{lang}.xml` for each deck, a `<strings lang=>` block in `ui.xml`, a new `index-{lang}.xml`, and a registry `<locale>` entry. The language switcher in `deck.xsl` and `setLanguage()` in `scripts/helper.js` hard-code `en`/`uk`, so both need editing.
- **Active deck is hard-coded.** `$activeDeckId` in `deck.xsl` is the literal `'rws-tarot'`. `setDeck()` in `helper.js` writes a `?deck=` query parameter that the stylesheet does not read, because XSLT 1.0 in the browser cannot see URL parameters. Multi-deck selection is unfinished (see `docs/ROADMAP.md`).
- **Card detail modal and the play area** (shuffle/pull, `#play` in `deck.xsl`) are built by `scripts/helper.js` from the rendered DOM (`.tarot-card` elements under `#deck-main` and their CSS classes), so renaming a class in `deck.xsl` breaks both. Button labels for the play area come from `<play>` in `ui.xml`.

## Docs

- `README.md` still describes the earlier single-deck layout (`tarot.xsl`, `data/structure.xml`, `data/locales/deck.*.xml`). `docs/SCHEMA.md` and the files under `data/` reflect the current layout.
- `docs/SCHEMA.md` is the file-format specification; `docs/ROADMAP.md` lists planned XPath/XSLT/XQuery/XSD exercises.
- `archive/PictorialKey.xml` is the original source text and is not loaded by the site.
- Known data issue: `data/decks/rws-tarot/metadata.xml` card `03` has a Cyrillic `д` as its Hebrew letter, and card `06` has the sign text ` Gemini ` instead of a symbol.
