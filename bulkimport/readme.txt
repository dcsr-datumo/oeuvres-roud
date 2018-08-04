


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

curl -X POST -d @BIBLIOGRAPHY_refined.xml http://root%40example.com:test@localhost:3333/v1/resources/xmlimport/http%3A%2F%2Frdfh.ch%2Fprojects%2F0112

curl -X POST -d @importExampleFiche.xml http://root%40example.com:test@localhost:3333/v1/resources/xmlimport/http%3A%2F%2Frdfh.ch%2Fprojects%2F0112




###################
##
## IMPORT PROCEDURES
##
###################


-----------------------> Chidere a colleghi <-----------------------

- volete resp ?
- Le regarde et la voix CRLR GR MS 12/K. "Le document manque". Deleted perché creava problemi. Giusto ... ?
Fiche 103 --- commentaire interne truncated ... sorry ...
------------------------------------->  <--------------------------------


-----------------------> Problemi durante IMPORT <-----------------------

- invalid text : attention, it does not want empty element. Check empty elements: //*[not(text())]
- lexical error : no "", ?, and other characters in label
- when importing something with @target, the targeted resources need to be present as well :)
- when there is a problem, limit the processing to few rows and see where exactly the problem is
------------------------------------->  <--------------------------------



-----------------------> BIBLIO - TO BE DONE MANUALLY IN FINAL XML !!! così poi l'import è completo <-----------------------

- check publication with photos, form BiblioDB (there are few, and in the ontology should be a link, but we don't have the photo yet)
- pubblicato dove ? 631	Photographie	Roud Gustave	[Bûcherons], [paysans à table], [Moisonneur], [Paysage]				93			1967-04-22(23)	p. 27, 30, 31
- check, se non sono già tra gli articoli inserirli a mano:
	- 634	Traduction	Holderlin Friedrich, Brentano Clemens	Le Romantisme allemand			Dirigé par Béguin Albert		Marseille	Les Cahiers du Sud	1949	p. 393-405	Hölderlin: "Souvenir", "Temps de la moisson", "Âges de la vie", "Moitié de la vie", "Diotima de l'au-delà (fragment)", "L'Hivers", "Le Printemps", "Quatrain". Brentano: "Je suis une maison...", "Au coeur d'une douleur profonde...", "Échos d'une musique de Beethoven", "Myrte, bien aimé, murmure...", "Chant du cygne". Les versions des poèmes de Hölderlin diffèrent de celles de 1937.	Fait + photocopié			Non
	- 663	Traduction	Hölderlin Friedrich, Brentano Clemens	Le Romantisme allemand			Dirigé par Béguin Albert	194, no. spécial	Marseille	Les Cahiers du Sud	1937-05(-06)	p. 361-371	Hölderlin: "Souvenir", "Temps de la moisson", "Âges de la vie", "Moitié de la vie", Diotima de l'au-delà (fragment)", "L'Hiver", "Le Printemps", "Quatrain") Poèmes de Clémens Brentano ("Je sais une maison", Au coeur d'une douleur profonde…", "Echos d'une musique de Beethoven", "Myrte bien-aimé murmure…", "Chant du cygne")	Fait + photocopié			Non
	- Traduction	Leisinger Hermann	Les peintures étrusques de Tarquinia				10		La Guilde du Livre	1953			Fait		Oui	Non (mais dans boîte La Guilde du Livre)
	- articolo di traduzione con 10 autori ...
- libri (books.csv) con più di due autori, add gli autori dal terzo in poi
- INPUT_data/check.csv
- sections recueils

------------------------------------->  <--------------------------------


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
		https://docs.google.com/spreadsheets/d/1xgVFlQ7-lmf9U6Sx7G9yPNpOAumEd79N2nabi3R6BDI/edit?usp=sharing


PERIODICALS
--- Clean biblioDB (the copy in googleDoc), check periodicals e issues and volumes numbers (comma distinguishes issue and volume, - means that more issues or volumes are taken)
--- extract colonna periodical in nuovo csv -> periodicals.csv
--- deduplicate [import.ipynb] -> delete manually first column (it has numbers that are not important for us) -> periodicals_distinct.csv
--- create XML [import.ipynb] -> periodicals.xml


AUTHORS
--- extract column Creator (for all kinds of publication) -> author.csv
--- deduplicate [import.ipynb] > check manually delete entry with more than one author (create another row or delete if the second author already exists), delete first column (it has number that are not important for us) -> authors_distinct.csv
--- create csv with column for name and column for surname [import.ipynb] -> authors_distinct_surname_name.csv
--- check manually
--- create XML [import.ipynb] -> authors.xml


ARTICLES
--- extract spreadsheet from googledoc -> articles.csv
--- create XML [import.ipynb] -> authors.xml
attention:  row[5] photo not included because there are no photo yet
    		row[8] and row[9] place and publisher not included
    		row[14] website interest not included
    		PublicationIsDigitized = row[15] not included, because there is no scan made with the new rules


BOOKS
--- import.ipynb


BOOKSECTIONS
--- import.ipynb


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
	BIBLIOGRAPHY.xml > refine_biblio.xsl > BIBLIOGRAPHY_refined.xml
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%




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




FICHES 
--- prepare importExampleFiche.xml
--- export fiches from mysql 
		- select table 'fiche_texte'
		- go to tab Export
		- Custom, CSV: 	columns separated with $
						columns enclosed with §
						columns escaped with 
						lines terminated with AUTO
						replace NULL with 
						[check] remove carriage return/line feed characters within columns
		The same parameters should be in the csv.reader function in the python import file
						f = open('../INPUT_data/fiche_texte.csv')
						csv_f = csv.reader(f, delimiter='$', quotechar="§")   

--- corrected in DB (fiches fonds-roud/unil.ch). Done
		- [Biblio xxx] with pages inside squared brackets > pages reference moved outside (fiche 114)
		- mismatched tags (one case only: <i>some text<i/> in hasPublicComment, fiche 243). This is caused by the HTML editor used in Remplir fiche in fonds-roud.unil.ch
		- fields with richtext that does not have <p> paragraphs, because have been created before the new editor > add <p>
		- dates, a lot of dates (missing parts, not well formatted, not in the right column)
		- 


		row14 = date ---> datereadable and datecomputable
		Inside manuscriptHasDateEstablishedReadable are gathered columns of the DB: datationlist_id, datation, datationcomment 
		Date facciamole per ultime, perché dovremo cambiare cose direttamente nel csv





RECOMPILE authors (added Heine, Lavater-Sloman, D'Annunzio, Michelangelo, Coccioli, )