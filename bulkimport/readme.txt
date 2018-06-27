
###################
##
## BULK IMPORT
##
###################

DOWNLOAD (in browser)
http://localhost:3333/v1/resources/xmlimportschemas/http%3A%2F%2Fwww.knora.org%2Fontology%2F0112%2Froud-oeuvres?email=root%40example.com&password=test

Download sembra funzionare anche con utente root, ma just in case funziona anche con il mio:
http://localhost:3333/v1/resources/xmlimportschemas/http%3A%2F%2Fwww.knora.org%2Fontology%2F0112%2Froud-oeuvres?email=elena.spadini%40unil.ch&password=k32V



UPLOAD (in terminal)
curl -X POST -d @importTest.xml http://root%40example.com:test@localhost:3333/v1/resources/xmlimport/http%3A%2F%2Frdfh.ch%2Fprojects%2F0112

curl -X POST -d @publishers.xml http://root%40example.com:test@localhost:3333/v1/resources/xmlimport/http%3A%2F%2Frdfh.ch%2Fprojects%2F0112

curl -X POST -d @persons.xml http://root%40example.com:test@localhost:3333/v1/resources/xmlimport/http%3A%2F%2Frdfh.ch%2Fprojects%2F0112





IMPORT PROCEDURES


Problemi durante IMPORT
- invalid text : attenzione che non vuole elementi vuoti. Check elementi vuoti: //*[not(text())]



TO IMPORT PUBLICATION, I NEED:
- persons (author, translator)
- publishers
- periodical


- PUBLISHERS -> publishers_backup
--- Extract column 8 and 9 from BiblioDB, corresponding to Class Publishers and properties publisherHasName and publisherHasLocation [copy-paste, create a dedicated csv]
--- Delete empty lines [import_publisher.ipynb]
--- Sort and deduplicate [import_publisher.ipynb] -> import_data/publishers_sorted_distinct.csv
--- Clean manually from false distinct and changed in biblioDB: 
	'J. R. Geigy' > 'J.R. Geigy'
	L'Aire ("Cooperative Rencontre"), Lausanne > L'Aire, Vevey
	L'Âge d'homme >	L'Âge d'Homme
	toutes graphies > La Guilde du Livre, Lausanne
	Zoé. Genève
	Horizons de France, "Champs" > Horizons de France
	Pierre Seghers, coll. Poètes d'aujourd'hui, no 173 > Pierre Seghers
	-> publishers_sorted_distinct_manuallychecked.csv (THIS IS THE GOOD SOURCE FOR TRANSFORMATION IN XML!)
--- Create XML [import_publisher.ipynb] -> publisher.xml



PERSONS -> persons_backup
--- Save Chronologie_Gens_Revues_Lieux.docx as ODT, because the xml below is easier
--- Consider only the person and save only the xml content of the odt file -> Gens.xml
--- Delete all the odt blabla and namespaces and left only structures, plus add element <person> around each h (was text:a) including p, with find and replace. -> Gens.xml
--- cambiato a mano: Affolter (aggiunto famille così ha un giveName), Franz. W. Beidler (cambiato in Franz Wilhelm Beidler) -> Gens.xml
--- Transform using   person_word2xml.xslt -> persons.xml
--- Corrected by hand in the xml output (it's faster) 
			name (two names): Ramuz, Leon Nicolas, Marcel Perretten, Robert Jean Dominique
			birthDate (take from notice): Ferrini, Ramseyer André
			delete hasNotice because empty: Chessex, ramuz 
			added by hand: Gustave Roud !  
					<p0112-roud-oeuvres:Person id="Roud_Gustave">
				      <knoraXmlImport:label>pers_Roud Gustave</knoraXmlImport:label>
				      <p0112-roud-oeuvres:hasFamilyName knoraType="richtext_value">Roud</p0112-roud-oeuvres:hasFamilyName>
				      <p0112-roud-oeuvres:hasGivenName knoraType="richtext_value">Gustave</p0112-roud-oeuvres:hasGivenName>
				   </p0112-roud-oeuvres:Person>



