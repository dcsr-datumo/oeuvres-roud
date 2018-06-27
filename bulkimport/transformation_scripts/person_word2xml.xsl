<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    xmlns:p0112-roud-oeuvres="http://api.knora.org/ontology/0112/roud-oeuvres/xml-import/v1#"
    xmlns:knoraXmlImport="http://api.knora.org/ontology/knoraXmlImport/v1#"
    exclude-result-prefixes="xs"
    version="2.0">
    <xsl:output encoding="UTF-8" indent="yes" method="xml"></xsl:output>
    
    <xsl:template match="/">
        
        <!-- insert root element -->
        <knoraXmlImport:resources xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
            xsi:schemaLocation="http://api.knora.org/ontology/knoraXmlImport/v1# ../p0112-roud-oeuvres-xml-schemas/p0112-roud-oeuvres.xsd"
            xmlns="http://api.knora.org/ontology/0112/roud-oeuvres/xml-import/v1#"
            xmlns:knoraXmlImport="http://api.knora.org/ontology/knoraXmlImport/v1#"
            xmlns:p0112-roud-oeuvres="http://api.knora.org/ontology/0112/roud-oeuvres/xml-import/v1#">
            
            <!-- iterate for each person -->
            <xsl:for-each select="//person">
                
                <!-- create element person, with attribute id and children (directly or with xsl:element) -->
                <xsl:element name="p0112-roud-oeuvres:Person">  
                    <xsl:attribute name="id">
                        <xsl:value-of select="substring-after(./h//span, ' ')"/>
                        <xsl:text>_</xsl:text>
                        <xsl:value-of select="substring-before(./h//span, ' ')"/>
                    </xsl:attribute>
                    
                    <knoraXmlImport:label>
                        <xsl:text>pers_</xsl:text>
                        <xsl:value-of select="substring-after(./h//span, ' ')"/>
                        <xsl:text> </xsl:text>
                        <xsl:value-of select="substring-before(./h//span, ' ')"/>
                    </knoraXmlImport:label>
                    
                    <xsl:if test="./starts-with(p[1]//span[1], '1')">
                        <p0112-roud-oeuvres:hasBirthDate knoraType="date_value">
                            <xsl:text>GREGORIAN:</xsl:text>
                            <xsl:value-of select="./p[1]//span[1]/substring-before(., '-')"/>
                        </p0112-roud-oeuvres:hasBirthDate>
                        
                        <p0112-roud-oeuvres:hasDeathDate knoraType="date_value">
                            <xsl:text>GREGORIAN:</xsl:text>
                            <xsl:value-of select="./p[1]//span[1]/substring-after(substring-before(., '.'), '-')"/>
                        </p0112-roud-oeuvres:hasDeathDate>
                    </xsl:if>
                    
                    <p0112-roud-oeuvres:hasFamilyName knoraType="richtext_value">
                        <xsl:value-of select="substring-after(./h//span, ' ')"/>
                    </p0112-roud-oeuvres:hasFamilyName>
                    
                    <p0112-roud-oeuvres:hasGivenName knoraType="richtext_value">
                        <xsl:value-of select="substring-before(./h//span, ' ')"/>
                    </p0112-roud-oeuvres:hasGivenName>
                    
                    <xsl:if test="./p//span">
                        
                        <xsl:choose>
                            <xsl:when test="./starts-with(p[1]//span[1], '1')">
                                <p0112-roud-oeuvres:personHasNotice knoraType="richtext_value">
                                    <xsl:value-of select="./p[1]//span[1]/substring-after(., '. ')"/>
                                    <xsl:value-of select="./p//span[position()>1]"/>
                                </p0112-roud-oeuvres:personHasNotice>
                            </xsl:when>
                            <xsl:otherwise>
                                <p0112-roud-oeuvres:personHasNotice knoraType="richtext_value">
                                    <xsl:value-of select="./p//span"/>
                                </p0112-roud-oeuvres:personHasNotice>
                            </xsl:otherwise>
                        </xsl:choose>
                    </xsl:if>
                    
                </xsl:element>
                
                
            </xsl:for-each>
            
        </knoraXmlImport:resources>
        
    </xsl:template>
    
    
    <!-- 
    <xsl:for-each select="//w:t">
            blabla
            <xsl:value-of select="."/>
            blabla
        </xsl:for-each>
    -->
    
    
        
    
    
</xsl:stylesheet>