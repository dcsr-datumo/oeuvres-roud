

TO DO
==========

## FIND TEXTS
- Bisogno della notice per fare la codifica di Adieu 
- Prendere notes 1919 et Adieu, nuove versoni !!!

## IN ENCODING
- come mettere multiple languages in xml:lang dell'header ?
- parte genetica, la mettiamo da qualche parte o rimane in DB ? Se la mettiamo in TEI, potrebbe stare in <\creation> in <\profileDesc> (anche se non è specificato), in <\derivation> (DA CONTROLLARE), in <\edition> (forse questa è la più adatta), 
- come fare link a DB
- vd. se serve esempio di header abbastanza completo alla fine del capitolo sull'Header
- encodingDesc è l'unica parte comune a tutti! Come renderla disponibile? O la mettiamo in un file a parte, oppure la mettiamo in un TeiCorpus ... capire come è meglio anche per l'implementazione in DB




DECISO e risorse utili
===========
- Should automatically extract how to cite from the header.
- lista di persone e di luoghi non servono, perché sono già nel DB

- Doc di Gilles
https://github.com/LaDHUL/KnoraBulkStandoffImport

- With a mapping, a default XSL transformation may be provided to transform the XML to HTML before sending it back to the client. This is useful when the client is a web-browser expecting HTML (instead of XML).
https://docs.knora.org/paradox/03-apis/api-v1/xml-to-standoff-mapping.html

- TEI/XML: Converting Standoff to TEI/XML
https://github.com/dhlab-basel/Knora/blob/e189861d7219cf78f520fdc84037616094c45d35/docs/src/paradox/03-apis/api-v2/tei-xml.md

- Header transformation
https://github.com/dhlab-basel/Knora/blob/a568257c6897ffb75285a36c86f8176bfd7d1958/webapi/_test_data/test_route/texts/beol/header.xsl

=============================== cose varie =================================

Vd. DOC GILLES !!!

Validating a Mapping and sending it to Knora
https://docs.knora.org/paradox/03-apis/api-v2/xml-to-standoff-mapping.html

1. Create testMapping.xml and validate using mappingXMLToStandoff.xsd

2. Create standoff.ttl

3. Upload standoff.ttl using load-standoff-onto.expect

4. HTTP POST http://localhost:3333/v2/mapping (ogni volta bisogna specificare un nome diverso nel json)
curl -u root@example.com:test -X POST -F json=@sendMapping.json -F xml=@testMapping.xml http://localhost:3333/v2/mapping

5. request in Postman to post newResource (vd. body!!)
https://docs.knora.org/paradox/03-apis/api-v2/editing-resources.html

6. Check la risorsa, in browser: 
http://0.0.0.0:3333/v2/resources/URL della risorsa
http://0.0.0.0:3333/v2/resources/http%3A%2F%2Frdfh.ch%2F0112%2FVply6mleRkeZ7JZQsYsNVw



import XSL
use importXSL.py (in oeuvres-roud)
generate new iri
take this iri and put it into the xml mapping




xml che si mette nel doc da mandare con Postman non va copia-incolla. Scriverlo direttamente.


resources.html use the standard mapping only


get resource v1 gives back source
get resrouce v2 gives back textValueAsHtml




=================== TOBIAS =======================


per header decidere cosa fare


mapping solo per il body
relazione diretta tra l'elemento e l'attributo e un'entità standoff


tei > create bulkimport
see article Tobias (parla di export, ma serve import)

---> create issue in Knora, assign Tobias, create not only html
XML or HTML
c'è una cosa che ti da standoff

salsah1, parla con Loic et Marion

https://docs.knora.org/paradox/03-apis/api-v2/tei-xml.html



