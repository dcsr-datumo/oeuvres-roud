<?xml version="1.0" encoding="UTF-8"?>

<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:tei="http://www.tei-c.org/ns/1.0"
    exclude-result-prefixes="xs tei" version="1.0">
    <xsl:output method="html" indent="yes" omit-xml-declaration="no" encoding="UTF-8"/>
    
    
    <xsl:template match="//p">
        <p>
            <xsl:attribute name="class">
                <xsl:text>tei-p</xsl:text>
            </xsl:attribute>
            <xsl:apply-templates/>
        </p>
    </xsl:template>
    
    <xsl:template match="//quote">
        <a>
            <xsl:attribute name="class">
                <xsl:text>resourceLink tei-quote</xsl:text>
            </xsl:attribute>
            <xsl:attribute name="href">
                <xsl:value-of select="./@source"></xsl:value-of>
            </xsl:attribute>
            <xsl:apply-templates/>
        </a>
    </xsl:template>
    
    <xsl:template match="//placeName">
        <a>
            <xsl:attribute name="id">
                <xsl:value-of select="./@ref"></xsl:value-of>
            </xsl:attribute>
            <xsl:attribute name="href">
                <xsl:value-of select="./@ref"></xsl:value-of>
            </xsl:attribute>
            <xsl:attribute name="class">
                <xsl:text>resourceLink tei-placeName</xsl:text>
            </xsl:attribute>
            <xsl:apply-templates/>
        </a>
    </xsl:template>
    
    <xsl:template match="//persName">
        <a>
            <xsl:attribute name="href">
                <xsl:value-of select="./@ref"></xsl:value-of>
            </xsl:attribute>
            <xsl:attribute name="class">
                <xsl:text>resourceLink tei-persName</xsl:text>
            </xsl:attribute>
            <xsl:apply-templates/>
        </a>
    </xsl:template>
    
    <xsl:template match="//ref">
        <a>
            <xsl:attribute name="id">
                <xsl:text>id_</xsl:text>
                <xsl:value-of select="./@target/substring-after(.,'http://rdfh.ch/0112/')"></xsl:value-of>
            </xsl:attribute>
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
    
    
    <xsl:template match="//hi[@rend='italic']">
        <em>
            <xsl:attribute name="class">
                <xsl:text>tei-rend-italic</xsl:text>
            </xsl:attribute>
            <xsl:apply-templates/>
        </em>
    </xsl:template>   
    
    
    
</xsl:stylesheet>