# Roud TEI standoff Mapping

**Resources:**
- *How to create a standoff mapping and test with bulk import* [tutorial](https://github.com/LaDHUL/KnoraBulkStandoffImport)


## Import the mapping in Knora

1. Load the standoff onto `roudMapping.ttl` into db. Can use [load-standoff-onto.expect](load-standoff-onto.expect): 
```bash
./load-standoff-onto.expect http://localhost:7200
```

2. Import the XSLT if haven't done it yet (see above)
```bash
# create env and install deps (first time only)
python3 -m venv env
source env/bin/activate
pip3 install -r requirements.txt
# or just enter in env and launch script
python importXSL.py
```
It will give us back the IRI of the uploaded XSL. Add it to the XML mapping, at the beginning of the file in the tag `<defaultXSLTransformation>`.


3. Restart Knora
```bash
make stack-restart-api
```

4. Load the XML mapping. It will give us back the IRI of the mapping, composed by the IRI of the project and the value of the `:mappingHasName` property.
```bash
curl -u root@example.com:test -X POST -F json=@roudMapping.json -F xml=@roudMapping.xml http://localhost:3333/v2/mapping
```

**Attention**. The db cannot store two different mappings with the same name, need to change the value of the `:mappingHasName` property each time. Each time a new mapping has to be imported in Knora, it is safer to delete all the project assets (ontologies and data) and restart from scratch, to avoid duplicates in the onto.
