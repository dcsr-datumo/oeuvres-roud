<?xml version="1.0" encoding="UTF-8"?>

<xsl:transform xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="2.0">

    <xsl:output method="html" encoding="utf-8" indent="yes"/>

    <xsl:template match="//text">
        <div>
            <xsl:apply-templates/>
        </div>
    </xsl:template>

    <xsl:template match="//placeName">
        <a>
            <xsl:attribute name="href">
                <xsl:value-of select="./@ref"></xsl:value-of>
            </xsl:attribute>
            <xsl:apply-templates/>
        </a>
    </xsl:template>

    

    <xsl:template match="//head">
        <em><xsl:apply-templates/></em>
    </xsl:template>

   
    

</xsl:transform>