
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

curl -X POST -d @periodicals.xml http://root%40example.com:test@localhost:3333/v1/resources/xmlimport/http%3A%2F%2Frdfh.ch%2Fprojects%2F0112

curl -X POST -d @importExamplePeriodical.xml http://root%40example.com:test@localhost:3333/v1/resources/xmlimport/http%3A%2F%2Frdfh.ch%2Fprojects%2F0112





IMPORT PROCEDURES



-----------------------> Problemi durante IMPORT <-----------------------

- invalid text : attenzione che non vuole elementi vuoti. Check elementi vuoti: //*[not(text())]
- lexical error : no "" in label
------------------------------------->  <--------------------------------




TO IMPORT PUBLICATIONS, I NEED:
- publishers
- periodicals



PUBLISHERS -> publishers_backup
--- Extract column 8 and 9 from BiblioDB, corresponding to Class Publishers and properties publisherHasName and publisherHasLocation [copy-paste, create a dedicated csv]
--- Delete empty lines [import.ipynb]
--- Sort and deduplicate [import.ipynb] -> import_data/publishers_sorted_distinct.csv
--- Clean manually from false distinct and changed in biblioDB: 
	'J. R. Geigy' > 'J.R. Geigy'
	L'Aire ("Cooperative Rencontre"), Lausanne > L'Aire, Vevey
	L'Âge d'homme >	L'Âge d'Homme
	toutes graphies > La Guilde du Livre, Lausanne
	Zoé. Genève
	Horizons de France, "Champs" > Horizons de France
	Pierre Seghers, coll. Poètes d'aujourd'hui, no 173 > Pierre Seghers
	-> publishers_sorted_distinct_manuallychecked.csv (THIS IS THE GOOD SOURCE FOR TRANSFORMATION IN XML!)
--- Create XML [import.ipynb] -> publishers.xml




PUBLICATIONS 
In biblioDB.ods
--- doppio autore separato da virgola, non da ET
--- find and replace all ’ -> '
--- dividere tra le classi: book, book section, periodicalArticle, disk
		https://docs.google.com/spreadsheets/d/1xgVFlQ7-lmf9U6Sx7G9yPNpOAumEd79N2nabi3R6BDI/edit#gid=96888708



PERIODICALS
--- Clean biblioDB (the copy in googleDoc), check periodicals e issues and volumes numbers (comma distinguishes issue and volume, - means that more issues or volumes are taken)
--- extract colonna periodical in nuovo csv -> periodicals.csv
--- deduplicate [import.ipynb] -> delete manually first column (it has numbers that are not important for us) -> periodicals_distinct.csv
--- Create XML [import.ipynb] -> periodicals.xml




--- s.i.a. ? s.n.a. ?




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


