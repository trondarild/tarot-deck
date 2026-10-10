<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

    <!--
      Pure XSLT Query Engine for Universal Card Deck Schema
      Supports multiple deck types and recursive hierarchy.
      Every deck in the registry is rendered; the default is visible and
      helper.js switches between them (XSLT 1.0 in the browser cannot read URL parameters).
    -->

    <xsl:output method="html" indent="yes" encoding="UTF-8"/>

    <xsl:variable name="lang" select="/page/@lang"/>
    <xsl:variable name="defaultDeckId" select="'rws-tarot'"/>

    <!-- Database Connection -->
    <xsl:variable name="baseDir">../data/</xsl:variable>
    <xsl:variable name="db_decks" select="document(concat($baseDir, 'decks.xml'))/decks"/>
    <!-- Decks marked status="draft" in the registry are not shown -->
    <xsl:variable name="shown_decks" select="$db_decks/deck[not(@status='draft')]"/>
    <xsl:variable name="defaultDeck" select="$shown_decks[@id=$defaultDeckId]"/>
    <xsl:variable name="db_ui" select="document(concat($baseDir, 'locales/ui.xml'))/ui/strings[@lang=$lang]"/>

    <xsl:template match="/">
        <html lang="{$lang}">
            <head>
                <meta charset="UTF-8"/>
                <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
                <title><xsl:value-of select="$defaultDeck/name"/> - <xsl:value-of select="$db_ui/title"/></title>
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
                                <a href="#play"><xsl:value-of select="$db_ui/play/title"/></a>
                                <xsl:for-each select="$shown_decks">
                                    <xsl:variable name="deckId" select="@id"/>
                                    <div class="deck-nav" data-deck="{$deckId}">
                                        <xsl:if test="$deckId != $defaultDeckId">
                                            <xsl:attribute name="hidden">hidden</xsl:attribute>
                                        </xsl:if>
                                        <xsl:for-each select="document(concat($baseDir, structure/@href))/structure/group">
                                            <a href="#{$deckId}-{@type}-{@value}"><xsl:value-of select="@label"/></a>
                                        </xsl:for-each>
                                    </div>
                                </xsl:for-each>
                            </div>
                            <div class="lang-switcher">
                                <button onclick="setLanguage('en')">EN</button>
                                <button onclick="setLanguage('uk')">UK</button>
                            </div>
                        </nav>

                        <div class="deck-switcher">
                            <xsl:for-each select="$shown_decks">
                                <button type="button" data-deck="{@id}">
                                    <xsl:if test="@id=$defaultDeckId">
                                        <xsl:attribute name="class">active</xsl:attribute>
                                    </xsl:if>
                                    <xsl:value-of select="name"/>
                                </button>
                            </xsl:for-each>
                        </div>
                    </header>

                    <section id="play" class="play-area">
                        <div class="section-header">
                            <h2><xsl:value-of select="$db_ui/play/title"/></h2>
                        </div>
                        <div class="play-controls">
                            <button id="shuffle-btn" type="button"><xsl:value-of select="$db_ui/play/shuffle"/></button>
                            <button id="pull-btn" type="button" disabled="disabled"><xsl:value-of select="$db_ui/play/pull"/></button>
                            <span id="pile-count" class="pile-count" data-label="{$db_ui/play/remaining}"></span>
                        </div>
                        <div id="spread" class="spread" data-layout="sequence"></div>
                    </section>

                    <main id="deck-main">
                        <xsl:apply-templates select="$shown_decks"/>
                    </main>

                    <footer>
                        <p><xsl:value-of select="$db_ui/footer"/></p>
                    </footer>
                </div>
                <script src="scripts/helper.js" type="text/javascript"><xsl:text> </xsl:text></script>
            </body>
        </html>
    </xsl:template>

    <!-- One deck: load its tables and render its hierarchy -->
    <xsl:template match="deck">
        <!-- Fall back to English when the deck has no locale for the page language -->
        <xsl:variable name="localeHref">
            <xsl:choose>
                <xsl:when test="locales/locale[@lang=$lang]"><xsl:value-of select="locales/locale[@lang=$lang]/@href"/></xsl:when>
                <xsl:otherwise><xsl:value-of select="locales/locale[@lang='en']/@href"/></xsl:otherwise>
            </xsl:choose>
        </xsl:variable>

        <div class="deck" id="deck-{@id}" data-deck="{@id}">
            <xsl:if test="@id != $defaultDeckId">
                <xsl:attribute name="hidden">hidden</xsl:attribute>
            </xsl:if>
            <xsl:apply-templates select="document(concat($baseDir, structure/@href))/structure/group" mode="recursive">
                <xsl:with-param name="deck" select="."/>
                <xsl:with-param name="metadata" select="document(concat($baseDir, metadata/@href))/metadata"/>
                <xsl:with-param name="locale" select="document(concat($baseDir, $localeHref))/locale"/>
            </xsl:apply-templates>
        </div>
    </xsl:template>

    <xsl:template match="group" mode="recursive">
        <xsl:param name="deck"/>
        <xsl:param name="metadata"/>
        <xsl:param name="locale"/>

        <section id="{$deck/@id}-{@type}-{@value}" class="card-group">
            <div class="section-header">
                <h2><xsl:value-of select="@label"/></h2>
            </div>

            <xsl:choose>
                <xsl:when test="group">
                    <div class="nested-groups">
                        <xsl:apply-templates select="group" mode="recursive">
                            <xsl:with-param name="deck" select="$deck"/>
                            <xsl:with-param name="metadata" select="$metadata"/>
                            <xsl:with-param name="locale" select="$locale"/>
                        </xsl:apply-templates>
                    </div>
                </xsl:when>
                <xsl:otherwise>
                    <div class="card-grid">
                        <xsl:apply-templates select="card">
                            <xsl:with-param name="deck" select="$deck"/>
                            <xsl:with-param name="metadata" select="$metadata"/>
                            <xsl:with-param name="locale" select="$locale"/>
                        </xsl:apply-templates>
                    </div>
                </xsl:otherwise>
            </xsl:choose>
        </section>
    </xsl:template>

    <xsl:template match="card">
        <xsl:param name="deck"/>
        <xsl:param name="metadata"/>
        <xsl:param name="locale"/>

        <xsl:variable name="cid" select="@id"/>
        <xsl:variable name="meta" select="$metadata/card[@id=$cid]"/>
        <xsl:variable name="loc" select="$locale/card[@id=$cid]"/>
        <xsl:variable name="deckType" select="$deck/@type"/>

        <div class="tarot-card" id="card-{$deck/@id}-{$cid}">
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
                <!-- Decks without artwork yet: hide the broken image and keep the placeholder background -->
                <img src="{$deck/images/@basePath}{$imgName}.jpg" alt="{$loc/title}" loading="lazy" onerror="this.classList.add('missing')"/>
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
                            <xsl:when test="$meta/custom/attribute[@name='glyph']"><span class="sign-symbol glyph"><xsl:value-of select="$meta/custom/attribute[@name='glyph']/@value"/></span></xsl:when>
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
