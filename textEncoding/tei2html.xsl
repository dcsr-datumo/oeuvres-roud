<?xml version="1.0" encoding="UTF-8"?>

<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:tei="http://www.tei-c.org/ns/1.0"
    exclude-result-prefixes="xs tei" version="1.0">
    <xsl:output method="html" indent="yes" omit-xml-declaration="no" encoding="UTF-8"/>
    
    
    
    <xsl:template match="//head"> 
        <h1>
            <span tei="head"><xsl:apply-templates/></span>
        </h1>
    </xsl:template>
    
    
    <xsl:template match="//p">
        <p>
            <span tei="p"><xsl:apply-templates/></span>
        </p>
    </xsl:template>

    <xsl:template match="//pb">
        <span tei="pb">
            <a>
                <xsl:attribute name="href">
                    <xsl:value-of select="./@n"></xsl:value-of>
                </xsl:attribute>
                <xsl:text>&#128459;</xsl:text>
            </a>
        </span>
    </xsl:template>

    
    <xsl:template match="//quote">
        <span tei="quote"><xsl:apply-templates/></span>
    </xsl:template>
    
    <xsl:template match="//placeName">
        <span tei="placeName">
            <a>
                <xsl:attribute name="href">
                    <xsl:value-of select="./@ref"></xsl:value-of>
                </xsl:attribute>
                <xsl:apply-templates/>
            </a>
        </span>
    </xsl:template>
    
    <xsl:template match="//persName">
        <span tei="persName">
            <a>
                <xsl:attribute name="href">
                    <xsl:value-of select="./@ref"></xsl:value-of>
                </xsl:attribute>
                <xsl:apply-templates/>
            </a>
        </span>
    </xsl:template>
    
    <xsl:template match="//ref">
        <span tei="ref">
            <a>
                <xsl:attribute name="href">
                    <xsl:value-of select="./@target"></xsl:value-of>
                </xsl:attribute>
                <xsl:apply-templates/>
            </a>
        </span>
    </xsl:template>
    
    <xsl:template match="//note">
        <div>
            <span tei="note">
                <em>Note de l'auteur : </em>
                <xsl:apply-templates/>
            </span>
        </div>
    </xsl:template>    
    
    
    <xsl:template match="//seg[@rend='italic']">
        <span tei="segItalic">
            <em><xsl:apply-templates/></em>
        </span>
    </xsl:template>
    
    
    
    
</xsl:stylesheet>