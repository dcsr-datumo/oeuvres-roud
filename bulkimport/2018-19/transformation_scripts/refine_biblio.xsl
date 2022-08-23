<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:knoraXmlImport="http://api.knora.org/ontology/knoraXmlImport/v1#"
    xmlns:p0112-roud-oeuvres="http://api.knora.org/ontology/0112/roud-oeuvres/xml-import/v1#"
    exclude-result-prefixes="xs"
    version="2.0" >
    <xsl:output encoding="UTF-8" method="xml"></xsl:output>
    
    
    <!--  copy all  -->
    <xsl:template match="@* | node()">
        <xsl:copy>
            <xsl:apply-templates select="@* | node()"/>
        </xsl:copy>
    </xsl:template>
    
    
    <!--  disambiguate when Periodical and Publisher have the same name -->
    <xsl:template match="//p0112-roud-oeuvres:Periodical/@id[.='Rencontre']">
        <xsl:attribute name="id">period_Rencontre</xsl:attribute>
    </xsl:template>    
    <xsl:template match="//p0112-roud-oeuvres:Periodical/@target[.='Rencontre']">
        <xsl:attribute name="target">period_Rencontre</xsl:attribute>
    </xsl:template>
    <xsl:template match="//p0112-roud-oeuvres:Publisher/@id[.='Rencontre']">
        <xsl:attribute name="id">edi_Rencontre</xsl:attribute>
    </xsl:template>    
    <xsl:template match="//p0112-roud-oeuvres:Publisher/@target[.='Rencontre']">
        <xsl:attribute name="target">edi_Rencontre</xsl:attribute>
    </xsl:template>
    
    
    <xsl:template match="//p0112-roud-oeuvres:Periodical/@id[.='Pour_l_Art']">
        <xsl:attribute name="id">period_Pour_l_Art</xsl:attribute>
    </xsl:template>    
    <xsl:template match="//p0112-roud-oeuvres:Periodical/@target[.='Pour_l_Art']">
        <xsl:attribute name="target">period_Pour_l_Art</xsl:attribute>
    </xsl:template>
    <xsl:template match="//p0112-roud-oeuvres:Publisher/@id[.='Pour_l_Art']">
        <xsl:attribute name="id">edi_Pour_l_Art</xsl:attribute>
    </xsl:template>    
    <xsl:template match="//p0112-roud-oeuvres:Publisher/@target[.='Pour_l_Art']">
        <xsl:attribute name="target">edi_Pour_l_Art</xsl:attribute>
    </xsl:template>
    
    
    <xsl:template match="//p0112-roud-oeuvres:Periodical/@id[.='La_Guilde_du_Livre']">
        <xsl:attribute name="id">period_La_Guilde_du_Livre</xsl:attribute>
    </xsl:template>    
    <xsl:template match="//p0112-roud-oeuvres:Periodical/@target[.='La_Guilde_du_Livre']">
        <xsl:attribute name="target">period_La_Guilde_du_Livre</xsl:attribute>
    </xsl:template>
    <xsl:template match="//p0112-roud-oeuvres:Publisher/@id[.='La_Guilde_du_Livre']">
        <xsl:attribute name="id">edi_La_Guilde_du_Livre</xsl:attribute>
    </xsl:template>    
    <xsl:template match="//p0112-roud-oeuvres:Publisher/@target[.='La_Guilde_du_Livre']">
        <xsl:attribute name="target">edi_La_Guilde_du_Livre</xsl:attribute>
    </xsl:template>
    
    
    
    
    
    
    
    
    
    
</xsl:stylesheet>