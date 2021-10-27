<?xml version="1.0" encoding="UTF-8"?>

<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:tei="http://www.tei-c.org/ns/1.0"
    exclude-result-prefixes="xs tei" version="1.0">
    <xsl:output method="html" indent="yes" omit-xml-declaration="no" encoding="UTF-8"/>
    
    
    <!-- IN ALPHABETICA ORDER OF TEI ELEMENTS -->
    
    
    <xsl:template match="//add">
        <sup>
            <xsl:attribute name="class">
                <xsl:text>tei-add</xsl:text>
            </xsl:attribute>
            <xsl:apply-templates/>
        </sup>
    </xsl:template>
    
    
    <xsl:template match="//dateline">
        <p>
            <xsl:attribute name="class">
                <xsl:text>tei-dateline</xsl:text>
            </xsl:attribute>
            <xsl:attribute name="style">
                <xsl:text>text-align: right</xsl:text>
            </xsl:attribute>
            <xsl:apply-templates/>
        </p>
    </xsl:template>
    
    
    <xsl:template match="//div">
        <div>
            <xsl:attribute name="class">
                <xsl:text>tei-div</xsl:text>
            </xsl:attribute>
            <xsl:attribute name="style">
                <xsl:text>margin-bottom: 80px</xsl:text>
            </xsl:attribute>
            <xsl:apply-templates/>
        </div>
    </xsl:template>
    
    
    <xsl:template match="//ex">
        <span>
            <xsl:attribute name="class">
                <xsl:text>tei-ex</xsl:text>
            </xsl:attribute>
            <xsl:attribute name="style">
                <xsl:text>color: grey</xsl:text>
            </xsl:attribute>
            <xsl:text>[</xsl:text>
            <xsl:apply-templates/>
            <xsl:text>]</xsl:text>
        </span>
    </xsl:template>
    
    
    <xsl:template match="//foreign">
        <em>
            <xsl:attribute name="class">
                <xsl:text>tei-foreign</xsl:text>
            </xsl:attribute>
            <xsl:apply-templates/>
        </em>
    </xsl:template>
    
    
    <xsl:template match="//head[@type='main']">
        <!-- do not display -->
    </xsl:template>
    
    
    <xsl:template match="//head[@rend='p']">
        <p>
            <xsl:attribute name="class">
                <xsl:text>tei-head-rendP</xsl:text>
            </xsl:attribute>
            <xsl:apply-templates/>
        </p>
    </xsl:template>
    
    
    <xsl:template match="//head[@rend='h1']">
        <h1>
            <xsl:attribute name="class">
                <xsl:text>tei-head-rendH1</xsl:text>
            </xsl:attribute>
            <xsl:apply-templates/>
        </h1>
    </xsl:template>
    
    
    <xsl:template match="//head[@rend='h2']">
        <h2>
            <xsl:attribute name="class">
                <xsl:text>tei-head-rendH2</xsl:text>
            </xsl:attribute>
            <xsl:apply-templates/>
        </h2>
    </xsl:template>
    
    
    <xsl:template match="//hi[@rend='italic']">
        <em>
            <xsl:attribute name="class">
                <xsl:text>tei-hi-rendItalic</xsl:text>
            </xsl:attribute>
            <xsl:apply-templates/>
        </em>
    </xsl:template>   
    
    
    <xsl:template match="item">
        <li class="tei-item">
            <xsl:apply-templates/>
        </li>
    </xsl:template>
    
    
    <xsl:template match="//lb">
        <br/>
    </xsl:template>   
    
    
    <xsl:template match="list">
        <ul class="tei-list" style="list-style:none">
            <xsl:apply-templates/>
        </ul>
    </xsl:template>
    
    
    <xsl:template match="//note">
        <p>
            <xsl:attribute name="class">
                <xsl:text>tei-note</xsl:text>
            </xsl:attribute>
            <xsl:apply-templates/>
            <em> [Note de l'auteur]</em>
        </p>
    </xsl:template>    
    
    
    <xsl:template match="//p">
        <p>
            <xsl:attribute name="class">
                <xsl:text>tei-p</xsl:text>
            </xsl:attribute>
            <xsl:apply-templates/>
        </p>
    </xsl:template>  
    
    
    <xsl:template match="//persName">
        <a>
            <xsl:attribute name="href">
                <xsl:value-of select="./@ref"></xsl:value-of>
            </xsl:attribute>
            <xsl:attribute name="class">
                <xsl:text>resourceLink tei-persName</xsl:text>
            </xsl:attribute>
            <xsl:attribute name="target">
                <xsl:text>_blank</xsl:text>
            </xsl:attribute>
            <xsl:apply-templates/>
        </a>
    </xsl:template>
    
    
    <xsl:template match="//placeName">
        <a>
            <xsl:attribute name="href">
                <xsl:value-of select="./@ref"></xsl:value-of>
            </xsl:attribute>
            <xsl:attribute name="class">
                <xsl:text>resourceLink tei-placeName</xsl:text>
            </xsl:attribute>
            <xsl:attribute name="target">
                <xsl:text>_blank</xsl:text>
            </xsl:attribute>
            <xsl:apply-templates/>
        </a>
    </xsl:template>
    
    
    <xsl:template match="//quote">
        <a>
            <xsl:attribute name="class">
                <xsl:text>resourceLink tei-quote</xsl:text>
            </xsl:attribute>
            <xsl:attribute name="href">
                <xsl:value-of select="./@source"></xsl:value-of>
            </xsl:attribute>
            <xsl:attribute name="target">
                <xsl:text>_blank</xsl:text>
            </xsl:attribute>
            <xsl:apply-templates/>
        </a>
    </xsl:template> 
    
    
    <xsl:template match="//ref">
        <xsl:choose>
            <xsl:when test="substring-before(./@target,'___') = 'ms'">
                <a>
                    <xsl:attribute name="href">
                        <xsl:value-of select="substring-after(./@target,'___')"></xsl:value-of>
                    </xsl:attribute>
                    <xsl:attribute name="class">
                        <xsl:text>resourceLink tei-ref-ms</xsl:text>
                    </xsl:attribute>
                    <xsl:attribute name="target">
                        <xsl:text>_blank</xsl:text>
                    </xsl:attribute>
                    <xsl:apply-templates/>
                </a>
            </xsl:when>
            <xsl:when test="substring-before(./@target,'___') = 'pub'">
                <a>
                    <xsl:attribute name="href">
                        <xsl:value-of select="substring-after(./@target,'___')"></xsl:value-of>
                    </xsl:attribute>
                    <xsl:attribute name="class">
                        <xsl:text>resourceLink tei-ref-pub</xsl:text>
                    </xsl:attribute>
                    <xsl:attribute name="target">
                        <xsl:text>_blank</xsl:text>
                    </xsl:attribute>
                    <xsl:apply-templates/>
                </a>
            </xsl:when>
            <xsl:otherwise>
                <a>
                    <xsl:attribute name="href">
                        <xsl:value-of select="./@target"></xsl:value-of>
                    </xsl:attribute>
                    <xsl:attribute name="class">
                        <xsl:text>resourceLink tei-ref</xsl:text>
                    </xsl:attribute>
                    <xsl:attribute name="target">
                        <xsl:text>_blank</xsl:text>
                    </xsl:attribute>
                    <xsl:apply-templates/>
                </a>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    
    
    <xsl:template match="//seg">
        <a>
            <xsl:attribute name="id">
                <xsl:value-of select="./@n"></xsl:value-of>
            </xsl:attribute>
            <xsl:attribute name="href">
                <xsl:value-of select="./@corresp"></xsl:value-of>
            </xsl:attribute>
            <xsl:attribute name="class">
                <xsl:text>resourceLink tei-seg</xsl:text>
            </xsl:attribute>
            <xsl:attribute name="target">
                <xsl:text>_blank</xsl:text>
            </xsl:attribute>
            <xsl:apply-templates/>
        </a>
    </xsl:template>
    
    
    <xsl:template match="//space[@quantity='1']">
        <span class="tei-space-quantity1">&#8195;&#8195;</span>
    </xsl:template>
    
    <xsl:template match="//space[@quantity='2']">
        <span class="tei-space-quantity2">&#8195;&#8195;&#8195;&#8195;</span>
    </xsl:template> 
    
    <xsl:template match="//space[@quantity='3']">
        <span class="tei-space-quantity2">&#8195;&#8195;&#8195;&#8195;&#8195;&#8195;</span>
    </xsl:template> 
    
    <xsl:template match="//space[@quantity='4']">
        <span class="tei-space-quantity2">&#8195;&#8195;&#8195;&#8195;&#8195;&#8195;&#8195;&#8195;</span>
    </xsl:template> 
    
    
    <xsl:template match="//supplied">
        <span>
            <xsl:attribute name="class">
                <xsl:text>tei-supplied</xsl:text>
            </xsl:attribute>
            <xsl:attribute name="style">
                <xsl:text>color: grey</xsl:text>
            </xsl:attribute>
            <xsl:text>[</xsl:text>
            <xsl:apply-templates/>
            <xsl:text>]</xsl:text>
        </span>
    </xsl:template>
    
    
</xsl:stylesheet>