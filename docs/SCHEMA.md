# Universal Card Deck Schema Specification

Version 1.0

## Overview

A universal XML schema for representing card decks using a generic hierarchy model.

## Core Concepts

- **Generic Hierarchy**: Flexible grouping ([structure.dtd](../data/schemas/structure.dtd))
- **Separation of Concerns**: Data modularity ([decks.xml](../data/decks.xml))

## File Specifications

### 1. Deck Registry

Catalogs available decks.

- **Location:** [data/decks.xml](../data/decks.xml)
- **DTD:** [decks.dtd](../data/schemas/decks.dtd)

### 2. Card Structure

Defines hierarchy (groups/cards).

- **Location:** `data/decks/{id}/structure.xml`
- **DTD:** [structure.dtd](../data/schemas/structure.dtd)

### 3. Card Metadata

Attributes like astrology or suits.

- **Location:** `data/decks/{id}/metadata.xml`
- **DTD:** [metadata.dtd](../data/schemas/metadata.dtd)

### 4. Localized Content

Translated titles and descriptions.

- **Location:** `data/decks/{id}/locales/deck.{lang}.xml`
- **DTD:** [locale.dtd](../data/schemas/locale.dtd)

## Implementation (Aggregated)

Generic rendering logic is implemented in [deck.xsl](../styles/deck.xsl).

### Directory Structure

```text
data/
├── decks.xml
├── decks/
│   ├── rws-tarot/
│   ├── standard-playing/
│   └── lenormand/
└── schemas/
    ├── decks.dtd
    ├── structure.dtd
    ├── metadata.dtd
    └── locale.dtd
```

## Implementation Checklist

- [x] Create schemas and registry
- [x] Migrate RWS tarot
- [x] Implement generic [deck.xsl](../styles/deck.xsl)
- [x] Add Playing Cards and Lenormand (MVP)
- [x] Validate all XML via DTDs

## Future Extensions

- Marseille/Thoth Tarot support
- XSD schemas for strong typing
- XQuery for analytical queries

## References

- [XML/XPath/XSLT Specs](https://www.w3.org/TR/)
