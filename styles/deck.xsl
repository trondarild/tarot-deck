<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

    <!--
      Pure XSLT Query Engine for Universal Card Deck Schema
      Supports multiple deck types and recursive hierarchy
    -->

    <xsl:output method="html" indent="yes" encoding="UTF-8"/>

    <!-- URL Parameters (mocked in simple XSLT 1.0) -->
    <xsl:variable name="lang" select="/page/@lang"/>
    <xsl:variable name="activeDeckId" select="'rws-tarot'"/> <!-- Default for now -->

    <!-- Database Connection -->
    <xsl:variable name="baseDir">../data/</xsl:variable>
    <xsl:variable name="db_decks" select="document(concat($baseDir, 'decks.xml'))/decks"/>
    <xsl:variable name="activeDeck" select="$db_decks/deck[@id=$activeDeckId]"/>

    <!-- Load active deck resources -->
    <xsl:variable name="db_structure" select="document(concat($baseDir, $activeDeck/structure/@href))/structure"/>
    <xsl:variable name="db_metadata" select="document(concat($baseDir, $activeDeck/metadata/@href))/metadata"/>
    <xsl:variable name="db_locale" select="document(concat($baseDir, $activeDeck/locales/locale[@lang=$lang]/@href))/locale"/>
    <xsl:variable name="db_ui" select="document(concat($baseDir, 'locales/ui.xml'))/ui/strings[@lang=$lang]"/>

    <xsl:template match="/">
        <html lang="{$lang}">
            <head>
                <meta charset="UTF-8"/>
                <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
                <title><xsl:value-of select="$activeDeck/name"/> - <xsl:value-of select="$db_ui/title"/></title>
                <link rel="stylesheet" href="styles/main.css"/>
                <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;600&amp;family=Inter:wght@400;600&amp;display=swap" rel="stylesheet"/>
                <style>
                    /* Inline styles for new components to be moved to main.css eventually */
                    .deck-switcher { margin: 1rem 0; display: flex; gap: 0.5rem; }
                    .deck-switcher button { padding: 0.5rem 1rem; cursor: pointer; border-radius: 4px; border: 1px solid #ccc; background: white; }
                    .deck-switcher button.active { background: #eee; font-weight: bold; }
                    .meta-field { font-size: 0.8rem; opacity: 0.8; }
                </style>
            </head>
            <body>
                <div class="deck-container">
                    <header>
                        <h1><xsl:value-of select="$db_ui/title"/></h1>
                        <nav>
                            <div class="nav-links">
                                <xsl:for-each select="$db_structure/group">
                                    <a href="#{@type}-{@value}"><xsl:value-of select="@label"/></a>
                                </xsl:for-each>
                            </div>
                            <div class="lang-switcher">
                                <button onclick="setLanguage('en')">EN</button>
                                <button onclick="setLanguage('uk')">UK</button>
                            </div>
                        </nav>

                        <div class="deck-switcher">
                            <xsl:for-each select="$db_decks/deck">
                                <button onclick="setDeck('{@id}')">
                                    <xsl:if test="@id=$activeDeckId">
                                        <xsl:attribute name="class">active</xsl:attribute>
                                    </xsl:if>
                                    <xsl:value-of select="name"/>
                                </button>
                            </xsl:for-each>
                        </div>
                    </header>

                    <main id="deck-main">
                        <xsl:apply-templates select="$db_structure/group" mode="recursive"/>
                    </main>

                    <footer>
                        <p><xsl:value-of select="$db_ui/footer"/></p>
                    </footer>
                </div>
                <script src="scripts/helper.js" type="text/javascript"><xsl:text> </xsl:text></script>
            </body>
        </html>
    </xsl:template>

    <xsl:template match="group" mode="recursive">
        <section id="{@type}-{@value}" class="card-group">
            <div class="section-header">
                <h2><xsl:value-of select="@label"/></h2>
            </div>

            <xsl:choose>
                <xsl:when test="group">
                    <div class="nested-groups">
                        <xsl:apply-templates select="group" mode="recursive"/>
                    </div>
                </xsl:when>
                <xsl:otherwise>
                    <div class="card-grid">
                        <xsl:apply-templates select="card"/>
                    </div>
                </xsl:otherwise>
            </xsl:choose>
        </section>
    </xsl:template>

    <xsl:template match="card">
        <xsl:variable name="cid" select="@id"/>
        <xsl:variable name="meta" select="$db_metadata/card[@id=$cid]"/>
        <xsl:variable name="loc" select="$db_locale/card[@id=$cid]"/>
        <xsl:variable name="deckType" select="$activeDeck/@type"/>

        <div class="tarot-card" id="card-{$cid}">
            <div class="card-image">
                <xsl:variable name="imgName">
                    <xsl:choose>
                        <xsl:when test="$deckType = 'tarot'">
                            <xsl:choose>
                                <xsl:when test="string-length($cid) = 2">maj<xsl:value-of select="$cid"/></xsl:when>
                                <xsl:when test="starts-with($cid, 'w')">wands<xsl:value-of select="substring($cid, 2)"/></xsl:when>
                                <xsl:when test="starts-with($cid, 'c')">cups<xsl:value-of select="substring($cid, 2)"/></xsl:when>
                                <xsl:when test="starts-with($cid, 's')">swords<xsl:value-of select="substring($cid, 2)"/></xsl:when>
                                <xsl:when test="starts-with($cid, 'p')">pents<xsl:value-of select="substring($cid, 2)"/></xsl:when>
                                <xsl:otherwise><xsl:value-of select="$cid"/></xsl:otherwise>
                            </xsl:choose>
                        </xsl:when>
                        <xsl:otherwise><xsl:value-of select="$cid"/></xsl:otherwise>
                    </xsl:choose>
                </xsl:variable>
                <img src="{$activeDeck/images/@basePath}{$imgName}.jpg" alt="{$loc/title}" loading="lazy"/>
            </div>
            <div class="card-content">
                <div class="card-header-grid">
                    <div class="id-cluster">
                        <span class="card-number"><xsl:value-of select="$meta/core/displayNumber"/></span>
                        <xsl:if test="$meta/tarot/hebrew">
                            <span class="meta-separator">|</span>
                            <span class="hebrew"><xsl:value-of select="$meta/tarot/hebrew"/></span>
                        </xsl:if>
                    </div>
                    <div class="category-cluster">
                        <span class="tag tag-mini">
                            <xsl:choose>
                                <xsl:when test="$deckType = 'tarot'"><xsl:value-of select="$meta/tarot/arcana"/></xsl:when>
                                <xsl:when test="$deckType = 'playing-cards'">Playing</xsl:when>
                                <xsl:otherwise><xsl:value-of select="$deckType"/></xsl:otherwise>
                            </xsl:choose>
                        </span>
                    </div>
                    <div class="title-cluster">
                        <h3 class="card-title">
                            <xsl:choose>
                                <xsl:when test="$loc/title"><xsl:value-of select="$loc/title"/></xsl:when>
                                <xsl:otherwise><xsl:value-of select="$cid"/></xsl:otherwise>
                            </xsl:choose>
                        </h3>
                    </div>
                    <div class="symbol-cluster">
                        <xsl:choose>
                            <xsl:when test="$meta/tarot/astrology/sign"><span class="sign-symbol"><xsl:value-of select="$meta/tarot/astrology/sign"/></span></xsl:when>
                            <xsl:when test="$meta/playing/suit"><span class="tag tag-mini-suit"><xsl:value-of select="$meta/playing/suit"/></span></xsl:when>
                            <xsl:when test="$meta/oracle/symbol"><span class="sign-symbol"><xsl:value-of select="$meta/oracle/symbol"/></span></xsl:when>
                        </xsl:choose>
                    </div>
                </div>

                <xsl:if test="$loc/description/p[1]">
                    <p class="card-description">
                        <xsl:value-of select="$loc/description/p[1]"/>
                    </p>
                </xsl:if>

                <!-- Expanded metadata for different types -->
                <div class="card-footer-meta">
                   <xsl:if test="$meta/playing">
                       <span class="meta-field">Rank: <xsl:value-of select="$meta/playing/rank"/></span>
                   </xsl:if>
                   <xsl:if test="$meta/tarot/astrology/element">
                       <span class="meta-field">Element: <xsl:value-of select="$meta/tarot/astrology/element"/></span>
                   </xsl:if>
                </div>
            </div>
        </div>
    </xsl:template>

</xsl:stylesheet>
