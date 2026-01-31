# Universal Card Deck Schema Specification

Version 1.0

## Overview

This specification defines a universal XML schema for representing card decks of various types. The schema uses a generic hierarchy approach that allows different deck types to define their own organizational structures while maintaining a consistent query interface.

## Supported Deck Types

This specification covers three deck types for MVP:

- **rws-tarot** - Rider-Waite-Smith Tarot (78 cards, Major/Minor Arcana structure)
- **standard-playing** - Standard Playing Cards (52 cards, 4 suits)
- **lenormand** - Lenormand Oracle (36 cards, flat numbered structure)

## Core Concepts

### Generic Hierarchy Model

The schema uses a flexible grouping mechanism where:

- Decks define their own hierarchy levels (arcana, suit, theme, etc.)
- Groups can contain cards or nested groups
- Each group has a type and value for categorization
- Cards are referenced by unique IDs within their deck

### Separation of Concerns

Data is separated into distinct files:

- **decks.xml** - Deck registry and metadata
- **structure.xml** - Card hierarchy and organization
- **metadata.xml** - Card attributes and properties
- **deck.{lang}.xml** - Localized content (titles, descriptions)

## File Specifications

### Deck Registry (decks.xml)

Catalogs all available decks and their resources.

**Location:** `/data/decks.xml`

**DTD:**

```dtd
<!ELEMENT decks (deck+)>

<!ELEMENT deck (name, description?, created?, cardCount, structure, metadata, locales, images?)>
<!ATTLIST deck
  id ID #REQUIRED
  type (tarot|playing-cards|oracle) #REQUIRED
  version CDATA #IMPLIED>

<!ELEMENT name (#PCDATA)>
<!ELEMENT description (#PCDATA)>
<!ELEMENT created (#PCDATA)>
<!ELEMENT cardCount (#PCDATA)>

<!ELEMENT structure EMPTY>
<!ATTLIST structure href CDATA #REQUIRED>

<!ELEMENT metadata EMPTY>
<!ATTLIST metadata href CDATA #REQUIRED>

<!ELEMENT locales (locale+)>
<!ELEMENT locale EMPTY>
<!ATTLIST locale
  lang CDATA #REQUIRED
  href CDATA #REQUIRED>

<!ELEMENT images EMPTY>
<!ATTLIST images basePath CDATA #REQUIRED>
```

**Example:**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE decks SYSTEM "schemas/decks.dtd">
<decks>
  <deck id="rws-tarot" type="tarot" version="1.0">
    <name>Rider-Waite-Smith Tarot</name>
    <description>Classic tarot deck by A.E. Waite and Pamela Colman Smith</description>
    <created>1909</created>
    <cardCount>78</cardCount>
    <structure href="decks/rws-tarot/structure.xml"/>
    <metadata href="decks/rws-tarot/metadata.xml"/>
    <locales>
      <locale lang="en" href="decks/rws-tarot/locales/deck.en.xml"/>
      <locale lang="uk" href="decks/rws-tarot/locales/deck.uk.xml"/>
    </locales>
    <images basePath="decks/rws-tarot/images/"/>
  </deck>

  <deck id="standard-playing" type="playing-cards" version="1.0">
    <name>Standard Playing Cards</name>
    <description>52-card French-suited deck</description>
    <cardCount>52</cardCount>
    <structure href="decks/standard-playing/structure.xml"/>
    <metadata href="decks/standard-playing/metadata.xml"/>
    <locales>
      <locale lang="en" href="decks/standard-playing/locales/deck.en.xml"/>
    </locales>
    <images basePath="decks/standard-playing/images/"/>
  </deck>

  <deck id="lenormand" type="oracle" version="1.0">
    <name>Lenormand Oracle</name>
    <description>36-card fortune-telling deck</description>
    <cardCount>36</cardCount>
    <structure href="decks/lenormand/structure.xml"/>
    <metadata href="decks/lenormand/metadata.xml"/>
    <locales>
      <locale lang="en" href="decks/lenormand/locales/deck.en.xml"/>
    </locales>
    <images basePath="decks/lenormand/images/"/>
  </deck>
</decks>
```

### Card Structure (structure.xml)

Defines the hierarchical organization of cards within a deck.

**Location:** `/data/decks/{deck-id}/structure.xml`

**DTD:**

```dtd
<!ELEMENT structure (hierarchy?, group+)>
<!ATTLIST structure deck CDATA #REQUIRED>

<!ELEMENT hierarchy (level+)>
<!ELEMENT level EMPTY>
<!ATTLIST level
  name CDATA #REQUIRED
  label CDATA #REQUIRED
  optional (true|false) "false">

<!ELEMENT group ((card | group)*)>
<!ATTLIST group
  type CDATA #REQUIRED
  value CDATA #REQUIRED
  label CDATA #IMPLIED
  count CDATA #IMPLIED>

<!ELEMENT card EMPTY>
<!ATTLIST card
  id ID #REQUIRED
  order CDATA #IMPLIED>
```

#### Example: RWS Tarot

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE structure SYSTEM "../../schemas/structure.dtd">
<structure deck="rws-tarot">
  <hierarchy>
    <level name="arcana" label="Arcana Type"/>
    <level name="suit" label="Suit" optional="true"/>
  </hierarchy>

  <group type="arcana" value="major" label="Major Arcana" count="22">
    <card id="00" order="1"/>
    <card id="01" order="2"/>
    <card id="02" order="3"/>
    <!-- ... all 22 Major Arcana cards -->
  </group>

  <group type="arcana" value="minor" label="Minor Arcana" count="56">
    <group type="suit" value="wands" label="Wands" count="14">
      <card id="w01" order="1"/>
      <card id="w02" order="2"/>
      <!-- ... all 14 Wands cards -->
    </group>

    <group type="suit" value="cups" label="Cups" count="14">
      <card id="c01" order="1"/>
      <!-- ... -->
    </group>

    <group type="suit" value="swords" label="Swords" count="14">
      <card id="s01" order="1"/>
      <!-- ... -->
    </group>

    <group type="suit" value="pentacles" label="Pentacles" count="14">
      <card id="p01" order="1"/>
      <!-- ... -->
    </group>
  </group>
</structure>
```

#### Example: Standard Playing Cards

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE structure SYSTEM "../../schemas/structure.dtd">
<structure deck="standard-playing">
  <hierarchy>
    <level name="suit" label="Suit"/>
  </hierarchy>

  <group type="suit" value="hearts" label="Hearts" count="13">
    <card id="h01" order="1"/>
    <card id="h02" order="2"/>
    <!-- ... all 13 Hearts -->
  </group>

  <group type="suit" value="diamonds" label="Diamonds" count="13">
    <card id="d01" order="1"/>
    <!-- ... -->
  </group>

  <group type="suit" value="clubs" label="Clubs" count="13">
    <card id="c01" order="1"/>
    <!-- ... -->
  </group>

  <group type="suit" value="spades" label="Spades" count="13">
    <card id="s01" order="1"/>
    <!-- ... -->
  </group>
</structure>
```

#### Example: Lenormand Oracle

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE structure SYSTEM "../../schemas/structure.dtd">
<structure deck="lenormand">
  <!-- No hierarchy - flat structure -->

  <group type="deck" value="main" label="Lenormand Cards" count="36">
    <card id="01" order="1"/>
    <card id="02" order="2"/>
    <card id="03" order="3"/>
    <!-- ... all 36 cards -->
  </group>
</structure>
```

### Card Metadata (metadata.xml)

Contains card attributes and properties.

**Location:** `/data/decks/{deck-id}/metadata.xml`

**DTD:**

```dtd
<!ELEMENT metadata (card+)>
<!ATTLIST metadata deck CDATA #REQUIRED>

<!ELEMENT card (core, tarot?, playing?, oracle?, custom?)>
<!ATTLIST card id CDATA #REQUIRED>

<!ELEMENT core (displayNumber, sortOrder)>
<!ELEMENT displayNumber (#PCDATA)>
<!ELEMENT sortOrder (#PCDATA)>

<!ELEMENT tarot (arcana, hebrew?, astrology?, kabbalah?)>
<!ELEMENT arcana (#PCDATA)>
<!ELEMENT hebrew (#PCDATA)>
<!ELEMENT astrology (sign?, element?)>
<!ELEMENT sign (#PCDATA)>
<!ELEMENT element (#PCDATA)>
<!ELEMENT kabbalah (path?, sephiroth?)>
<!ELEMENT path (#PCDATA)>
<!ELEMENT sephiroth EMPTY>
<!ATTLIST sephiroth
  from CDATA #IMPLIED
  to CDATA #IMPLIED>

<!ELEMENT playing (suit, rank, value?, faceCard?)>
<!ELEMENT suit (#PCDATA)>
<!ELEMENT rank (#PCDATA)>
<!ELEMENT value (#PCDATA)>
<!ELEMENT faceCard (#PCDATA)>

<!ELEMENT oracle (number, symbol?)>
<!ELEMENT number (#PCDATA)>
<!ELEMENT symbol (#PCDATA)>

<!ELEMENT custom (attribute*)>
<!ELEMENT attribute EMPTY>
<!ATTLIST attribute
  name CDATA #REQUIRED
  value CDATA #REQUIRED>
```

#### Example: RWS Tarot Card

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE metadata SYSTEM "../../schemas/metadata.dtd">
<metadata deck="rws-tarot">
  <card id="00">
    <core>
      <displayNumber>0</displayNumber>
      <sortOrder>1</sortOrder>
    </core>
    <tarot>
      <arcana>major</arcana>
      <hebrew>א</hebrew>
      <astrology>
        <sign>🜁</sign>
        <element>air</element>
      </astrology>
    </tarot>
  </card>

  <card id="w01">
    <core>
      <displayNumber>Ace</displayNumber>
      <sortOrder>23</sortOrder>
    </core>
    <tarot>
      <arcana>minor</arcana>
      <astrology>
        <element>fire</element>
      </astrology>
    </tarot>
  </card>
  <!-- ... -->
</metadata>
```

#### Example: Playing Card

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE metadata SYSTEM "../../schemas/metadata.dtd">
<metadata deck="standard-playing">
  <card id="h01">
    <core>
      <displayNumber>A</displayNumber>
      <sortOrder>1</sortOrder>
    </core>
    <playing>
      <suit>hearts</suit>
      <rank>ace</rank>
      <value>1</value>
      <faceCard>false</faceCard>
    </playing>
  </card>

  <card id="h13">
    <core>
      <displayNumber>K</displayNumber>
      <sortOrder>13</sortOrder>
    </core>
    <playing>
      <suit>hearts</suit>
      <rank>king</rank>
      <value>10</value>
      <faceCard>true</faceCard>
    </playing>
  </card>
  <!-- ... -->
</metadata>
```

#### Example: Lenormand Card

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE metadata SYSTEM "../../schemas/metadata.dtd">
<metadata deck="lenormand">
  <card id="01">
    <core>
      <displayNumber>1</displayNumber>
      <sortOrder>1</sortOrder>
    </core>
    <oracle>
      <number>1</number>
      <symbol>🚴</symbol>
    </oracle>
  </card>
  <!-- ... -->
</metadata>
```

### Localized Content (deck.{lang}.xml)

Contains translated card titles and descriptions.

**Location:** `/data/decks/{deck-id}/locales/deck.{lang}.xml`

**DTD:**

```dtd
<!ELEMENT locale (card+)>
<!ATTLIST locale
  lang CDATA #REQUIRED
  deck CDATA #REQUIRED>

<!ELEMENT card (title, description?, keywords?, divinatory?)>
<!ATTLIST card id CDATA #REQUIRED>

<!ELEMENT title (#PCDATA)>
<!ELEMENT description (p+)>
<!ELEMENT p (#PCDATA)>
<!ELEMENT keywords (keyword+)>
<!ELEMENT keyword (#PCDATA)>
<!ELEMENT divinatory (upright?, reversed?)>
<!ELEMENT upright (#PCDATA)>
<!ELEMENT reversed (#PCDATA)>
```

#### Example: Tarot Card (English)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE locale SYSTEM "../../../schemas/locale.dtd">
<locale lang="en" deck="rws-tarot">
  <card id="00">
    <title>The Fool</title>
    <description>
      <p>Beginnings, innocence, potential.</p>
    </description>
    <keywords>
      <keyword>innocence</keyword>
      <keyword>new beginnings</keyword>
      <keyword>free spirit</keyword>
    </keywords>
    <divinatory>
      <upright>New beginnings, optimism, trust in life</upright>
      <reversed>Recklessness, taken advantage of, inconsideration</reversed>
    </divinatory>
  </card>
  <!-- ... -->
</locale>
```

#### Example: Playing Card (English)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE locale SYSTEM "../../../schemas/locale.dtd">
<locale lang="en" deck="standard-playing">
  <card id="h01">
    <title>Ace of Hearts</title>
    <description>
      <p>The highest card in the hearts suit.</p>
    </description>
  </card>
  <!-- ... -->
</locale>
```

#### Example: Lenormand Card (English)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE locale SYSTEM="../../../schemas/locale.dtd">
<locale lang="en" deck="lenormand">
  <card id="01">
    <title>Rider</title>
    <description>
      <p>News, messages, movement, speed.</p>
    </description>
    <keywords>
      <keyword>news</keyword>
      <keyword>messages</keyword>
      <keyword>arrival</keyword>
    </keywords>
  </card>
  <!-- ... -->
</locale>
```

## XPath Query Patterns

### Common Queries

**Get all cards in a deck:**

```xpath
//structure[@deck='rws-tarot']//card
```

**Get cards by group type:**

```xpath
//structure[@deck='rws-tarot']/group[@type='arcana'][@value='major']/card
```

**Get nested groups (e.g., suits within minor arcana):**

```xpath
//structure[@deck='rws-tarot']/group[@type='arcana'][@value='minor']/group[@type='suit']
```

**Get card metadata:**

```xpath
//metadata[@deck='rws-tarot']/card[@id='00']
```

**Get localized card content:**

```xpath
//locale[@lang='en'][@deck='rws-tarot']/card[@id='00']
```

**JOIN operation (structure + metadata):**

```xslt
<xsl:variable name="cid" select="@id"/>
<xsl:variable name="meta" select="$db_metadata/card[@id=$cid]"/>
<xsl:variable name="loc" select="$db_locale/card[@id=$cid]"/>
```

### Deck-Specific Queries

**Tarot: Get all Major Arcana cards:**

```xpath
//structure[@deck='rws-tarot']/group[@type='arcana'][@value='major']/card
```

**Playing Cards: Get all Hearts:**

```xpath
//structure[@deck='standard-playing']/group[@type='suit'][@value='hearts']/card
```

**Lenormand: Get all cards (flat structure):**

```xpath
//structure[@deck='lenormand']/group[@type='deck']/card
```

## XSLT Template Patterns

### Generic Deck Rendering

```xslt
<!-- Render any deck structure recursively -->
<xsl:template name="render-deck">
  <xsl:param name="deckId"/>

  <xsl:variable name="structure" select="document(concat('decks/', $deckId, '/structure.xml'))"/>

  <div class="deck-container">
    <xsl:apply-templates select="$structure/structure/group" mode="recursive"/>
  </div>
</xsl:template>

<xsl:template match="group" mode="recursive">
  <section id="{@type}-{@value}" class="card-group">
    <h2><xsl:value-of select="@label"/></h2>

    <xsl:choose>
      <xsl:when test="group">
        <!-- Nested groups -->
        <xsl:apply-templates select="group" mode="recursive"/>
      </xsl:when>
      <xsl:otherwise>
        <!-- Cards -->
        <div class="card-grid">
          <xsl:apply-templates select="card"/>
        </div>
      </xsl:otherwise>
    </xsl:choose>
  </section>
</xsl:template>
```

### Deck-Type Specific Rendering

```xslt
<!-- Dispatch based on deck type -->
<xsl:template name="render-by-type">
  <xsl:param name="deckType"/>

  <xsl:choose>
    <xsl:when test="$deckType = 'tarot'">
      <xsl:call-template name="render-tarot"/>
    </xsl:when>
    <xsl:when test="$deckType = 'playing-cards'">
      <xsl:call-template name="render-playing-cards"/>
    </xsl:when>
    <xsl:when test="$deckType = 'oracle'">
      <xsl:call-template name="render-oracle"/>
    </xsl:when>
  </xsl:choose>
</xsl:template>
```

## Directory Structure

```text
data/
├── decks.xml                           # Deck registry
├── decks/
│   ├── rws-tarot/
│   │   ├── structure.xml
│   │   ├── metadata.xml
│   │   ├── locales/
│   │   │   ├── deck.en.xml
│   │   │   └── deck.uk.xml
│   │   └── images/
│   │       ├── thumbnails/
│   │       ├── medium/
│   │       └── large/
│   ├── standard-playing/
│   │   ├── structure.xml
│   │   ├── metadata.xml
│   │   ├── locales/
│   │   │   └── deck.en.xml
│   │   └── images/
│   └── lenormand/
│       ├── structure.xml
│       ├── metadata.xml
│       ├── locales/
│       │   └── deck.en.xml
│       └── images/
└── schemas/
    ├── decks.dtd
    ├── structure.dtd
    ├── metadata.dtd
    └── locale.dtd
```

## Migration from Current Schema

### Current RWS Tarot Structure

The existing RWS tarot implementation uses:

- `/data/structure.xml` - Card hierarchy
- `/data/metadata.xml` - Card attributes
- `/data/locales/deck.en.xml` - English content
- `/data/locales/deck.uk.xml` - Ukrainian content

### Migration Steps

1. Create `/data/decks.xml` registry
2. Move existing files to `/data/decks/rws-tarot/`
3. Update structure.xml to add `deck` attribute and hierarchy definition
4. Update XSLT to query from new locations
5. Test backward compatibility
6. Add DTD validation

### Backward Compatibility

XSLT can detect schema version and adapt:

```xslt
<xsl:variable name="schemaVersion">
  <xsl:choose>
    <xsl:when test="document('data/decks.xml')">2.0</xsl:when>
    <xsl:otherwise>1.0</xsl:otherwise>
  </xsl:choose>
</xsl:variable>
```

## Validation

### DTD Validation

Add DOCTYPE declarations to all XML files:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE decks SYSTEM "schemas/decks.dtd">
<decks>
  <!-- ... -->
</decks>
```

### Command-Line Validation

```bash
xmllint --valid --noout data/decks.xml
xmllint --valid --noout data/decks/rws-tarot/structure.xml
```

## Implementation Checklist

- [ ] Create `/data/schemas/` directory
- [ ] Write DTD files (decks.dtd, structure.dtd, metadata.dtd, locale.dtd)
- [ ] Create `/data/decks.xml` registry
- [ ] Migrate RWS tarot to new structure
- [ ] Update XSLT to support generic hierarchy
- [ ] Test with RWS tarot
- [ ] Add standard playing cards deck
- [ ] Add Lenormand oracle deck
- [ ] Validate all XML files against DTDs
- [ ] Update documentation

## Future Extensions

### Additional Deck Types

- Marseille Tarot
- Thoth Tarot
- Oracle of the Mermaids
- Custom user decks

### Schema Enhancements

- XSD schemas for stronger typing
- Namespace support for extensions
- Relationship definitions between cards
- Spread definitions
- Reading history

### Query Enhancements

- XQuery for complex analytics
- Full-text search indexing
- Card relationship graphs
- Statistical analysis

## References

- XML 1.0 Specification: <https://www.w3.org/TR/xml/>
- XPath 1.0 Specification: <https://www.w3.org/TR/xpath-10/>
- XSLT 1.0 Specification: <https://www.w3.org/TR/xslt-10/>
- DTD Tutorial: <https://www.w3schools.com/xml/xml_dtd.asp>
