
###################
##
## BULK IMPORT
##
###################

DOWNLOAD
http://localhost:3333/v1/resources/xmlimportschemas/http%3A%2F%2Fwww.knora.org%2Fontology%2F0112%2Froud-oeuvres?email=root%40example.com&password=test

Download sembra funzionare anche con utente root, ma just in case funziona anche con il mio:
http://localhost:3333/v1/resources/xmlimportschemas/http%3A%2F%2Fwww.knora.org%2Fontology%2F0112%2Froud-oeuvres?email=elena.spadini%40unil.ch&password=k32V



UPLOAD
curl -X POST -d @importTest.xml http://root%40example.com:test@localhost:3333/v1/resources/xmlimport/http%3A%2F%2Frdfh.ch%2Fprojects%2F0112

curl -X POST -d @publishers.xml http://root%40example.com:test@localhost:3333/v1/resources/xmlimport/http%3A%2F%2Frdfh.ch%2Fprojects%2F0112





IMPORT PROCEDURES

- PUBLISHERS
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
	-> publishers_sorted_distinct_manuallychecked.csv
--- Create XML [import_publisher.ipynb] -> import_publisher.xml

