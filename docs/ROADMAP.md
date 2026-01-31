# Tarot Project Roadmap

## Project Vision

Transform the current card gallery into a comprehensive digital reference for the Rider-Waite-Smith Tarot deck, honoring the work of Arthur Edward Waite and Pamela Colman Smith. The site will serve as both an educational resource and a demonstration of XML/XSLT technologies applied to structured content management.

## XML Technologies as Learning Platform

This project is fundamentally a learning exercise in XML technologies, treating the tarot deck data as a real-world use case for exploring the full power of XML, XPath, XSLT, and related standards.

### Core XML Technologies

#### XPath: Query Language for XML

XPath serves as the primary query mechanism for navigating and selecting data from the XML database. The project will demonstrate:

- Axis navigation (child, parent, ancestor, descendant, following-sibling)
- Predicate filtering with complex conditions
- Node tests and type checking
- XPath functions (string manipulation, numeric operations, boolean logic)
- Context-aware queries using current node position
- Advanced patterns like `//card[@id=$cid]/description/p[1]`
- Performance optimization through efficient path expressions

Current implementation examples:

```xpath
$db_structure/arcana[@type='major']/card
$db_metadata/card[@id=$cid]
$db_deck/card[@id=$cid]/description
```

Future advanced queries:

```xpath
// Find all cards with specific keywords
//card[contains(description, 'wisdom')]

// Complex filtering with multiple conditions
//card[@id and metadata/element='fire' and number > 10]

// Relationship queries
//card[following-sibling::card[1]/@suit = @suit]
```

#### XSLT: Transformation and Presentation Engine

XSLT transforms the raw XML data into HTML, implementing the business logic for card rendering, navigation, and layout. The project explores:

- Template matching and modes for different page types
- Named templates for reusable components
- Variables and parameters for data passing
- Conditional processing with xsl:choose, xsl:if
- Iteration with xsl:for-each and xsl:apply-templates
- Sorting and grouping operations
- Key-based lookups for performance
- Output methods (HTML5, XML, text)
- XSLT functions and extension functions

Planned XSLT patterns:

- Template modes for card rendering (thumbnail, full, print)
- Recursive templates for breadcrumb generation
- Grouping by suit using Muenchian method or xsl:for-each-group
- Dynamic URL generation based on card properties
- Conditional inclusion of reversed meanings
- Cross-reference generation between related cards

#### XQuery: Advanced Data Querying

While XSLT handles transformation, XQuery could be explored for complex analytical queries:

- Statistical analysis of card symbolism
- Full-text search with scoring
- FLWOR expressions (For, Let, Where, Order by, Return)
- Joining multiple XML documents
- Aggregation functions (count, sum, avg)
- User-defined functions for custom logic

Potential XQuery applications:

```xquery
(: Find cards by keyword with relevance scoring :)
for $card in //card
let $score := count($card/description//text()[contains(., 'love')])
where $score > 0
order by $score descending
return $card

(: Generate card relationship graph :)
for $card in //card[@type='major']
return element relationship {
  attribute from { $card/@id },
  for $related in //card[description[contains(., $card/title)]]
  return element to { $related/@id }
}
```

#### XML DTD: Document Structure Validation

Document Type Definitions ensure data consistency and provide documentation of the XML schema. The project will implement:

- Element declarations defining allowed structure
- Attribute lists with type constraints
- Entity definitions for reusable content
- Notation declarations for external resources
- Parameter entities for modular DTD design

Planned DTD structure:

```dtd
<!ELEMENT deck (metadata, structure, locales)>
<!ELEMENT card (title, description, keywords?, related*)>
<!ATTLIST card
  id ID #REQUIRED
  type (major|minor) #REQUIRED
  suit (wands|cups|swords|pentacles) #IMPLIED
  number CDATA #IMPLIED>
<!ELEMENT description (p+)>
<!ELEMENT keywords (keyword+)>
```

Benefits of DTD validation:

- Catch data entry errors early
- Document expected structure for contributors
- Enable IDE autocompletion and validation
- Ensure consistency across translation files
- Provide formal contract for data format

#### XML Schema (XSD): Advanced Validation

As an alternative or complement to DTD, XML Schema provides:

- Strong data typing (integers, dates, enumerations)
- Complex type definitions
- Inheritance and extension mechanisms
- Namespace support
- More expressive constraints

Example schema definitions:

```xsd
<xs:simpleType name="cardIdType">
  <xs:restriction base="xs:string">
    <xs:pattern value="[0-9]{2}|[wcsp][0-9]{2}"/>
  </xs:restriction>
</xs:simpleType>

<xs:complexType name="cardType">
  <xs:sequence>
    <xs:element name="title" type="xs:string"/>
    <xs:element name="description" type="descriptionType"/>
  </xs:sequence>
  <xs:attribute name="id" type="cardIdType" use="required"/>
</xs:complexType>
```

### XML Database Concepts

The project treats XML files as a relational database, demonstrating:

#### Table Structure

- `structure.xml` - Primary key table (card IDs, hierarchy)
- `metadata.xml` - Attribute table (numbers, symbols, elements)
- `deck.{lang}.xml` - Localized content tables
- `ui.xml` - Interface strings table

#### JOIN Operations

XSLT performs JOIN operations using XPath predicates:

```xslt
<!-- Inner join between structure and metadata -->
<xsl:variable name="meta" select="$db_metadata/card[@id=$cid]"/>

<!-- Left join with locale data -->
<xsl:variable name="loc" select="$db_deck/card[@id=$cid]"/>
```

#### Indexes and Keys

XSLT keys provide indexed lookups:

```xslt
<xsl:key name="card-by-id" match="card" use="@id"/>
<xsl:key name="card-by-suit" match="card" use="@suit"/>

<!-- Fast lookup using key -->
<xsl:variable name="card" select="key('card-by-id', $cardId)"/>
```

#### Aggregation and Grouping

```xslt
<!-- Count cards by suit -->
<xsl:for-each select="//card[generate-id() =
                      generate-id(key('card-by-suit', @suit)[1])]">
  <suit name="{@suit}" count="{count(key('card-by-suit', @suit))}"/>
</xsl:for-each>
```

### Learning Objectives

Through this project, developers will gain practical experience with:

- Writing complex XPath expressions for data navigation
- Designing modular XSLT templates with proper separation of concerns
- Implementing the template pattern in XSLT
- Understanding XSLT processing model and context nodes
- Using XSLT keys for performance optimization
- Validating XML documents with DTD and Schema
- Structuring XML data for queryability
- Implementing database-like operations in pure XML
- Debugging XSLT transformations
- Optimizing XPath queries for performance
- Understanding the trade-offs between XQuery and XSLT
- Working with XML namespaces
- Generating multiple output formats from single source

### Advanced XML Techniques to Explore

#### Dynamic Content Generation

- Generating sitemaps from card data
- Creating RSS/Atom feeds for card of the day
- Producing JSON-LD structured data for SEO
- Exporting card data to CSV or other formats

#### Parameterized Transformations

- Passing runtime parameters to XSLT (language, theme, layout mode)
- Conditional compilation based on build flags
- Environment-specific configuration

#### XSLT Extensions

- Custom functions for complex calculations
- Integration with external data sources
- Date/time manipulation for card of the day
- Random number generation for card selection

#### Performance Optimization

- Lazy evaluation strategies
- Streaming transformations for large datasets
- Caching intermediate results
- Minimizing document() function calls

#### Modular XSLT Design

- Importing and including stylesheets
- Template libraries for reusable components
- Override patterns for customization
- Stylesheet parameters for configuration

## Current State

The project currently implements:

- Basic card gallery with Major and Minor Arcana
- Bilingual support (English and Ukrainian)
- Native browser XSLT transformation
- XML-based data architecture treating files as database tables
- Minimal JavaScript for navigation and UI interactions only
- Universal Card Deck Schema (Multi-deck architecture)
- DTD-validated data structures
- Generic XSLT rendering engine (`deck.xsl`)

## Planned Features

### Content Structure

#### Home Page

- Introduction to the Rider-Waite-Smith Tarot deck
- Historical context about A.E. Waite and Pamela Colman Smith
- Featured cover image from the deck
- Navigation to Major Arcana, Minor Arcana, and search functionality
- Brief explanation of the deck's significance in tarot history

#### Major Arcana Section

- Dedicated page listing all 22 Major Arcana cards
- Grid layout with card thumbnails
- Quick reference to card meanings
- Link to individual card pages

#### Minor Arcana Section

- Dedicated page organized by suit (Wands, Cups, Swords, Pentacles)
- Suit-specific introductions
- Card thumbnails grouped by suit
- Links to individual card pages

#### Individual Card Pages

- Full card image with multiple size variants
- Complete card description from Waite's Pictorial Key
- Card symbolism and interpretation
- Divinatory meanings (upright and reversed)
- Related cards and cross-references
- Permanent URL structure for deep linking

#### Card of the Day

- Daily featured card with full details
- Persistent URL for sharing specific daily cards
- Archive of previous cards of the day
- Rotation algorithm based on date

#### Search and Browse

- Full-text search across all card descriptions
- Filter by arcana type, suit, or keywords
- Advanced search with multiple criteria
- Search results with card previews

### Technical Enhancements

#### Semantic HTML

- Proper use of HTML5 semantic elements (article, section, nav, aside)
- Microdata or JSON-LD structured data for search engines
- ARIA labels and roles for screen readers
- Logical heading hierarchy

#### Accessibility

- Comprehensive alt text for all card images describing symbolism
- Keyboard navigation support
- Screen reader optimization
- High contrast mode support
- Focus indicators for interactive elements
- Skip navigation links

#### Image Optimization

- Multiple image variants:
  - Thumbnail (150x250px) for gallery views
  - Medium (300x500px) for section pages
  - Large (600x1000px) for individual card pages
  - Full resolution for detailed study
- Responsive images using srcset and sizes attributes
- WebP format with JPEG fallback
- Lazy loading for performance
- Proper aspect ratio preservation

#### URL Structure

- Clean, semantic URLs:
  - `/` - Home page
  - `/major-arcana` - Major Arcana section
  - `/minor-arcana` - Minor Arcana section
  - `/cards/{card-id}` - Individual card pages
  - `/card-of-the-day` - Daily card feature
  - `/card-of-the-day/{date}` - Archived daily cards
  - `/search?q={query}` - Search results

#### Enhanced XSLT

- Template modes for different page types
- Reusable components for card rendering
- Breadcrumb navigation generation
- Sitemap generation
- RSS feed for card of the day

### Data Enhancements

#### Extended Card Data

- Import full descriptions from PictorialKey.xml
- Add reversed meanings
- Include keywords and themes
- Cross-reference related cards
- Add historical notes and variations

#### Universal Schema & Multi-Deck Support

- [x] Implement Universal Card Deck Schema (v1.0)
- [x] Migrate RWS Tarot to modular structure
- [ ] Complete full card metadata and locales for `standard-playing` deck
- [ ] Complete full card metadata and locales for `lenormand` deck
- [ ] Implement client-side deck switcher using XSLT parameters
- [ ] Support custom user-defined decks via local XML loading

#### Multilingual Expansion

- Framework for adding additional languages
- Separate translation files for:
  - UI strings (ui.xml)
  - Card content (deck.{lang}.xml)
  - Static content (content.{lang}.xml)
- Language-specific URL paths

### User Experience

#### Navigation

- Persistent header with main navigation
- Breadcrumb trails
- Previous/Next card navigation on individual pages
- Quick jump menu for card selection
- Mobile-responsive hamburger menu

#### Visual Design

- Maintain Nord color palette
- Enhance typography hierarchy
- Improve card hover states
- Add subtle animations for transitions
- Responsive grid layouts
- Print-friendly stylesheets

#### Interactive Features

- Card comparison tool
- Reading spread layouts
- Bookmark favorite cards
- Share card links on social media
- Print individual cards or collections

## Implementation Phases

### Phase 1: Content Foundation

- Restructure home page with deck introduction
- Create separate Major and Minor Arcana section pages
- Import full card descriptions from PictorialKey.xml
- Implement individual card page template

### Phase 2: Technical Infrastructure

- Develop URL routing system
- Generate semantic HTML structure
- Implement image optimization pipeline
- Add comprehensive accessibility features
- Create alt text for all card images

### Phase 3: Enhanced Features

- Build search functionality
- Implement card of the day feature
- Add navigation enhancements
- Create breadcrumb system
- Develop card comparison tools

### Phase 4: Multilingual Support

- Extend localization framework
- Translate extended content
- Implement language-specific URLs
- Add language switcher improvements

### Phase 5: Polish and Optimization

- Performance optimization
- Cross-browser testing
- Accessibility audit
- SEO optimization
- Documentation updates

## Technical Constraints

- Maintain pure XML/XSLT approach for data transformation
- Keep JavaScript minimal (navigation, UI interactions only)
- Ensure compatibility with native browser XSLT processors
- Preserve educational value for learning XPath and XSLT
- Maintain clean separation between content, presentation, and behavior

## Success Criteria

- All 78 cards have individual pages with complete information
- Site is fully accessible (WCAG 2.1 AA compliance)
- Search functionality returns relevant results
- Page load times under 2 seconds
- Mobile-responsive design works on all screen sizes
- Multilingual support for at least 3 languages
- Clean, bookmarkable URLs for all content
- Semantic HTML validates without errors
