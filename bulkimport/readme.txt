
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

curl -X POST -d @import_publisher.xml http://root%40example.com:test@localhost:3333/v1/resources/xmlimport/http%3A%2F%2Frdfh.ch%2Fprojects%2F0112
