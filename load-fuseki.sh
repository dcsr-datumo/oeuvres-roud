#USER
USERPWD=${1:-admin:test}
#ARGHOST=http://db-sipipv.unil.ch:3030
ARGHOST=${2:-http://localhost:3030}
ARGREPO=knora-test


ARGTTL=roud-admin.ttl
ARGGRAPH=http://www.knora.org/data/admin
curl -u $USERPWD  -H "Content-Type:text/turtle; charset=utf-8" --data-binary @${ARGTTL} -X POST ${ARGHOST}/${ARGREPO}\?graph\="${ARGGRAPH}"

ARGTTL=roud-permissions.ttl
ARGGRAPH=http://www.knora.org/data/permissions
curl -u $USERPWD  -H "Content-Type:text/turtle; charset=utf-8" --data-binary @${ARGTTL} -X POST ${ARGHOST}/${ARGREPO}\?graph\="${ARGGRAPH}"

ARGTTL=roud-onto.ttl
ARGGRAPH=http://www.knora.org/ontology/0112/roud-oeuvres
curl -u $USERPWD  -H "Content-Type:text/turtle; charset=utf-8" --data-binary @${ARGTTL} -X POST ${ARGHOST}/${ARGREPO}\?graph\="${ARGGRAPH}"

ARGTTL=roud-standoff.ttl
ARGGRAPH=http://www.knora.org/ontology/0112/roud-oeuvres
curl -u $USERPWD  -H "Content-Type:text/turtle; charset=utf-8" --data-binary @${ARGTTL} -X POST ${ARGHOST}/${ARGREPO}\?graph\="${ARGGRAPH}"

ARGTTL=roud-data-lists.ttl
ARGGRAPH=http://www.knora.org/data/0112/roud-oeuvres
curl -u $USERPWD  -H "Content-Type:text/turtle; charset=utf-8" --data-binary @${ARGTTL} -X POST ${ARGHOST}/${ARGREPO}\?graph\="${ARGGRAPH}"

#ARGTTL=roud-data/roud-data-local_20200929.ttl
#ARGGRAPH=http://www.knora.org/data/0112/roud-oeuvres
#curl -u $USERPWD  -H "Content-Type:text/turtle; charset=utf-8" --data-binary @${ARGTTL} -X POST ${ARGHOST}/${ARGREPO}\?graph\="${ARGGRAPH}"
