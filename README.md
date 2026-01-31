# Tarot Pictorial Key

![The Rider-Waite Tarot Deck](img/cover.jpg)

A multilingual tarot card reference built with pure XML/XSLT technologies.

## 🎯 Project Goals

This project serves as a learning platform for:

- **XPath** — querying XML data structures
- **XSLT** — transforming XML into HTML
- **XQuery concepts** — treating XML files as a database

## 📁 Project Structure

```text
tarot/
├── index.xml           # English entry point
├── index-uk.xml        # Ukrainian entry point
├── data/               # XML Database
│   ├── structure.xml   # Card hierarchy (Major/Minor Arcana)
│   ├── metadata.xml    # Card metadata (numbers, symbols, suits)
│   └── locales/        # Translations
│       ├── deck.en.xml # English card translations
│       ├── deck.uk.xml # Ukrainian card translations
│       └── ui.xml      # UI strings (all languages)
├── styles/
│   ├── tarot.xsl       # Main XSLT stylesheet (data queries)
│   └── main.css        # Nord theme styling
├── scripts/
│   └── helper.js       # Minimal JS (only URL routing & UI)
└── assets/
    └── img/big/        # Rider-Waite card images
```

## 🗄️ Database Architecture

The project treats XML files as database tables:

- **structure.xml** — Primary key table (card IDs, arcana types)
- **metadata.xml** — Metadata table (card numbers, Hebrew letters, astrological signs)
- **deck.{lang}.xml** — Localization tables (card titles & descriptions)
- **ui.xml** — UI strings table (interface translations)

XSLT performs **JOIN operations** using XPath:

```xsl
<xsl:variable name="meta" select="$db_metadata/card[@id=$cid]"/>
<xsl:variable name="loc" select="$db_deck/card[@id=$cid]"/>
```

## 🌍 Adding New Languages

1. Create `data/locales/deck.{lang}.xml` (copy from `deck.en.xml`)
2. Add UI strings to `data/locales/ui.xml`:

   ```xml
   <strings lang="{lang}">
     <title>...</title>
     <nav><major>...</major><minor>...</minor></nav>
     <footer>...</footer>
   </strings>
   ```

3. Create `index-{lang}.xml` entry point:

   ```xml
   <?xml version="1.0" encoding="UTF-8"?>
   <?xml-stylesheet type="text/xsl" href="styles/tarot.xsl"?>
   <page lang="{lang}">
       <content>...</content>
   </page>
   ```

4. Update language switcher buttons in `tarot.xsl`

## 🚀 Running Locally

```bash
npx http-server . -p 8080
```

Then open:

- English: `http://localhost:8080/index.xml`
- Ukrainian: `http://localhost:8080/index-uk.xml`

## 🎨 Design

- **Color Palette**: Nord theme
- **Typography**: Outfit (headings), Inter (body)
- **Layout**: Responsive CSS Grid
- **Aesthetic**: Minimalist, clean, focused on content

## 📝 Technical Notes

### Why Native XSLT?

Modern browsers (Firefox, Chrome) block `document()` calls in JavaScript-initiated XSLT transformations due to CORS policy. This project uses **native browser XSLT processing** triggered by `<?xml-stylesheet?>` processing instructions, avoiding CORS issues entirely.

### JavaScript Role

JavaScript is minimal and handles only:

- Language switching (URL redirection)
- Card click handlers (modal display)
- Modal window management

All data queries and transformations are performed in **pure XSLT**.

## 📚 Learning Resources

- [XPath Tutorial](https://www.w3schools.com/xml/xpath_intro.asp)
- [XSLT Reference](https://developer.mozilla.org/en-US/docs/Web/XSLT)
- [XML as Database](https://www.xml.com/pub/a/2001/10/31/databases.html)

## 📄 License

Educational project. Card images from the public domain Rider-Waite deck.

---

## Built with ❤️ for learning XML technologies
