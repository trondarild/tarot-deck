<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

    <!--
      Pure XSLT Query Engine for Tarot XML Database
      Restructured localization: deck.{lang}.xml + ui.xml
    -->

    <xsl:output method="html" indent="yes" encoding="UTF-8"/>

    <!-- Read language from source XML document -->
    <xsl:variable name="lang" select="/page/@lang"/>

    <!-- Database Connection (relative to stylesheet location: /styles/) -->
    <xsl:variable name="baseDir">../data/</xsl:variable>

    <!-- Database Tables -->
    <xsl:variable name="db_structure" select="document(concat($baseDir, 'structure.xml'))/structure"/>
    <xsl:variable name="db_metadata" select="document(concat($baseDir, 'metadata.xml'))/metadata"/>
    <xsl:variable name="db_deck" select="document(concat($baseDir, 'locales/deck.', $lang, '.xml'))/locale"/>
    <xsl:variable name="db_ui" select="document(concat($baseDir, 'locales/ui.xml'))/ui/strings[@lang=$lang]"/>

    <xsl:template match="/">
        <html lang="{$lang}">
            <head>
                <meta charset="UTF-8"/>
                <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
                <title><xsl:value-of select="$db_ui/title"/></title>
                <link rel="stylesheet" href="styles/main.css"/>
                <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;600&amp;family=Inter:wght@400;600&amp;display=swap" rel="stylesheet"/>
            </head>
            <body>
                <xsl:call-template name="render-deck"/>
                <script src="scripts/helper.js" type="text/javascript"><xsl:text> </xsl:text></script>
            </body>
        </html>
    </xsl:template>

    <xsl:template name="render-deck">
        <div class="deck-container">
            <header>
                <h1><xsl:value-of select="$db_ui/title"/></h1>
                <nav>
                    <div class="nav-links">
                        <a href="#major"><xsl:value-of select="$db_ui/nav/major"/></a>
                        <a href="#minor"><xsl:value-of select="$db_ui/nav/minor"/></a>
                    </div>
                    <div class="lang-switcher">
                        <button onclick="setLanguage('en')">EN</button>
                        <button onclick="setLanguage('uk')">UK</button>
                    </div>
                </nav>
            </header>

            <main id="tarot-main">
                <!-- XPath Query: SELECT * FROM structure WHERE type='major' -->
                <section id="major">
                    <div class="section-header">
                        <h2><xsl:value-of select="$db_ui/nav/major"/></h2>
                    </div>
                    <div class="card-grid">
                        <xsl:choose>
                            <xsl:when test="$db_structure/arcana[@type='major']/card">
                                <xsl:apply-templates select="$db_structure/arcana[@type='major']/card">
                                    <xsl:with-param name="arcanaType">major</xsl:with-param>
                                </xsl:apply-templates>
                            </xsl:when>
                            <xsl:otherwise>
                                <div class="error-msg" style="grid-column: 1/-1; background: #bf616a; color: white; padding: 2rem; border-radius: 8px;">
                                    <h3>Database Query Failed</h3>
                                    <p>Could not execute XPath query on structure.xml</p>
                                </div>
                            </xsl:otherwise>
                        </xsl:choose>
                    </div>
                </section>

                <!-- XPath Query: SELECT * FROM structure WHERE type='minor' JOIN suits -->
                <section id="minor">
                    <div class="section-header">
                        <h2><xsl:value-of select="$db_ui/nav/minor"/></h2>
                    </div>
                    <xsl:for-each select="$db_structure/arcana[@type='minor']/suit">
                        <div class="suit-section">
                            <div class="suit-header">
                                <h3><xsl:value-of select="@type"/></h3>
                            </div>
                            <div class="card-grid">
                                <xsl:apply-templates select="card">
                                    <xsl:with-param name="arcanaType">minor</xsl:with-param>
                                </xsl:apply-templates>
                            </div>
                        </div>
                    </xsl:for-each>
                </section>
            </main>

            <footer>
                <p><xsl:value-of select="$db_ui/footer"/></p>
            </footer>
        </div>
    </xsl:template>

    <!-- Card Template: Performs JOIN between structure, metadata, and deck locale tables -->
    <xsl:template match="card">
        <xsl:param name="arcanaType"/>
        <xsl:variable name="cid" select="@id"/>

        <!-- XPath JOIN: metadata WHERE id = $cid -->
        <xsl:variable name="meta" select="$db_metadata/card[@id=$cid]"/>

        <!-- XPath JOIN: deck locale WHERE id = $cid AND lang = $lang -->
        <xsl:variable name="loc" select="$db_deck/card[@id=$cid]"/>

        <!-- Image name mapping logic -->
        <xsl:variable name="imgName">
            <xsl:choose>
                <xsl:when test="string-length($cid) = 2">maj<xsl:value-of select="$cid"/></xsl:when>
                <xsl:when test="starts-with($cid, 'w')">wands<xsl:value-of select="substring($cid, 2)"/></xsl:when>
                <xsl:when test="starts-with($cid, 'c')">cups<xsl:value-of select="substring($cid, 2)"/></xsl:when>
                <xsl:when test="starts-with($cid, 's')">swords<xsl:value-of select="substring($cid, 2)"/></xsl:when>
                <xsl:when test="starts-with($cid, 'p')">pents<xsl:value-of select="substring($cid, 2)"/></xsl:when>
                <xsl:otherwise><xsl:value-of select="$cid"/></xsl:otherwise>
            </xsl:choose>
        </xsl:variable>

        <div class="tarot-card" id="card-{$cid}">
            <div class="card-image">
                <img src="assets/img/big/{$imgName}.jpg" alt="{$loc/title}" loading="lazy"/>
            </div>
            <div class="card-content">
                <div class="card-header-grid">
                    <div class="id-cluster">
                        <span class="card-number"><xsl:value-of select="$meta/number"/></span>
                        <xsl:if test="$meta/hebrew">
                            <span class="meta-separator">|</span>
                            <span class="hebrew"><xsl:value-of select="$meta/hebrew"/></span>
                        </xsl:if>
                    </div>
                    <div class="category-cluster">
                        <span class="tag tag-mini"><xsl:value-of select="$meta/arcana"/></span>
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
                            <xsl:when test="$meta/sign"><span class="sign-symbol"><xsl:value-of select="$meta/sign"/></span></xsl:when>
                            <xsl:when test="$meta/suit"><span class="tag tag-mini-suit"><xsl:value-of select="$meta/suit"/></span></xsl:when>
                        </xsl:choose>
                    </div>
                </div>

                <!-- Show description ONLY for Major Arcana -->
                <xsl:if test="$arcanaType = 'major'">
                    <p class="card-description">
                        <xsl:choose>
                            <xsl:when test="$loc/description/p[1]"><xsl:value-of select="$loc/description/p[1]"/></xsl:when>
                            <xsl:otherwise><xsl:value-of select="$loc/description"/></xsl:otherwise>
                        </xsl:choose>
                    </p>
                </xsl:if>
            </div>
        </div>
    </xsl:template>

</xsl:stylesheet>
