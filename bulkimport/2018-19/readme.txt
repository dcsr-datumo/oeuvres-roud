


#######################
## 
## BULK IMPORT COMMANDS
##
#######################


DOWNLOAD the schemas for the XML files (in browser)
	http://localhost:3333/v1/resources/xmlimportschemas/http%3A%2F%2Fwww.knora.org%2Fontology%2F0112%2Froud-oeuvres?email=root%40example.com&password=test

	http://knora.unil.ch/v1/resources/xmlimportschemas/http%3A%2F%2Fwww.knora.org%2Fontology%2F0112%2Froud-oeuvres?email=root%40example.com&password=test


UPLOAD the XML file (in terminal)
	curl -X POST -d @importTest.xml http://root%40example.com:test@localhost:3333/v1/resources/xmlimport/http%3A%2F%2Frdfh.ch%2Fprojects%2F0112

	curl -X POST -d @backup_images_all_tif_1_copy.xml http://root%40example.com:test@localhost:3333/v1/resources/xmlimport/http%3A%2F%2Frdfh.ch%2Fprojects%2F0112

	curl -X POST -d @backup_images_all_tif_1.xml http://root%40example.com:test@knora.unil.ch/v1/resources/xmlimport/http%3A%2F%2Frdfh.ch%2Fprojects%2F0112








###################
##
## IMPORT PROCEDURES
##
###################



-----------------------> problems during IMPORT <-----------------------

- invalid text : attention, it does not want empty element. Check empty elements: //*[not(text())]
- lexical error : no "", ?, and other characters in label
- when importing something with @target, the targeted resources need to be present as well :)
- when there is a problem, limit the processing to half of the rows and see where exactly the problem is (painful debugging)
------------------------------------->  <--------------------------------



Note:
All mentions of 'import.ipynb' refers to the python scripts (jupyter notebook) in folder transformation_scripts
_____________________________________________________________________________________________________________



PUBLISHERS
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


PERSONS -> persons_backup
--- Save Chronologie_Gens_Revues_Lieux.docx as ODT, because the xml below is easier
--- Consider only the person and save only the xml content of the odt file -> Gens.xml
--- Delete all the odt blabla and namespaces and left only structures, plus add element <person> around each h (was text:a) including p, with find and replace. -> Gens.xml
--- cambiato a mano: Affolter (aggiunto famille così ha un giveName), Franz. W. Beidler (cambiato in Franz Wilhelm Beidler) -> Gens.xml
--- Transform using   person_word2xml.xslt -> persons.xml
--- Corrected by hand in the xml output (it's faster)  --- NO PROBLEM THAT IT IS INDENTED ---
			- add "pers_" to id, otherwise has the same of some authors (find and replace)
			- name (two names): Ramuz, Leon Nicolas, Marcel Perretten, Robert Jean Dominique
			- birthDate (take from notice): Ferrini, Ramseyer André
			- delete hasNotice because empty: Chessex, ramuz 
			- added by hand: Gustave Roud !  
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
--- import.ipynb
--- in the xml output, manually
	- delete "fiches problematiques" (easier to add them manually afterwards than to try to understand why they cause problems. They are liste in OUTPUT/fiches_problematiques.xml)
	- replace <text> with <text xmlns="">
	- replace <p class="p1"> with <p>
	- replace <p class="p2"> with <p>
	- replace     knoraType="richtext_value"><text xmlns="">    with     knoraType="richtext_value" mapping_id="http://rdfh.ch/standoff/mappings/StandardMapping"><text xmlns="">    (because commented out in the import, stupid!)  
	- replace <i>  with   <em>   and   </i>   with   </em>  (<i> not present in StandardMapping, oh yes)



PAGES (SCANS)
--- connect à /mnt/
--- import.ipynb 
		this is an import with link to existing resources, so need the iri (of manuscripts, in this case, because the images are part of a manuscript). The iris are downloaded, together with the shelfmark for finding the correspondance, from graphdb (sparql query saved) in a csv. This csv is needed for the import to work
--- for importing the xml with curl
	147 images yes, 189 no, 170 yes
	Also, this image does not work
		<p0112-roud-oeuvres:Page xmlns:knoraXmlImport="http://api.knora.org/ontology/knoraXmlImport/v1#" xmlns:p0112-roud-oeuvres="http://api.knora.org/ontology/0112/roud-oeuvres/xml-import/v1#" id="CRLR_GR_MS2C14a_1r_1.png"><knoraXmlImport:label>page_CRLR GR MS 2 C/14a___f. 1r___1</knoraXmlImport:label><knoraXmlImport:file mimetype="image/png" path="/mnt/scanlettMounted/GustaveRoud/E_Scan/Scans_import/FondsArchive/CRLR_GR_MS2C14a/CRLR_GR_MS2C14a_1r_1.png" /><p0112-roud-oeuvres:hasSeqnum knoraType="int_value">1</p0112-roud-oeuvres:hasSeqnum><p0112-roud-oeuvres:pageHasName knoraType="richtext_value">f. 1r</p0112-roud-oeuvres:pageHasName><p0112-roud-oeuvres:pageIsPartOfManuscript><p0112-roud-oeuvres:Manuscript knoraType="link_value" linkType="iri" target="http://rdfh.ch/0112/roud-oeuvres/vG0O91nzRWuwx7r3fAaiXw" /></p0112-roud-oeuvres:pageIsPartOfManuscript></p0112-roud-oeuvres:Page>
	deleted in backup_images_all.xml !!!!!!!!!!!!
--- per importare i tiff: in backup_images_all
		replace '.png' with '.tif'
		replace 'image/png' with 'image/tiff'
		replace 'E_Scan/Scans_import/FondsArchive' with 'E_Scan/Scans_complets/FondsArchive'






%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%         TO BUILD ALL.xml        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
- BIBLIOGRAPHY.xml (authors_publishers_periodicals_articles_books_booksections) > refine_biblio.xsl > BIBLIOGRAPHY_refined.xml
- add PERSONS and FICHES
----> ALL !!
ATTENTION: 'ALL___BIBLIOGRAPHYrefined__FICHES__PERSONS.xml' has a number of fake publications added in order to to make it work	
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%







