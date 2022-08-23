###
### CREATE XML FOR BULK IMPORT OF SCANS
###



from xml.etree import ElementTree as ET
import csv
import os

### Open list of tiff to be imported
listTifPubs_file = open('list-tiff-pubs-articles_2import.txt', 'r', encoding="utf-8")

listTifPubs = listTifPubs_file.readlines()

for scan in listTifPubs:

    # remove dir and extension
    article = scan.split('/')[0]
    tif = scan.split('/')[1].split('.tif')[0]
    print(tif)
    correspondingPubLabel = scan.split('/')[0]
    print(correspondingPubLabel)
    pageSeqnum = tif.split('_')[-1]
    pageName = tif.split('_')[-2].strip('p')
    
    ### Building blocks
    pLabel = tif
    pId = tif.replace(' ', '').replace("'", "").replace("’","").replace("[","").replace("]","").replace(",","").replace("…","").replace("(","").replace(")","").replace("-","").replace("–", "") + '.tif'
    pBitstream = '/mnt/scanlettMounted/GustaveRoud/E_Scan/Scans_complets/Publications/' + article + '/' + tif + '.tif'
    pName = 'p. ' + pageName
    pSeqnum = pageSeqnum


    # csv downloaded from sparql query (query saved in graphdb). First column: iri, second column: label 
    # attention to delimiter for reading csv
    ### check label and store IRI in correspondingPubIri
    with open("iri-label-articles.csv", 'r') as csv_iriLabel_correspondance:     
        iriLabel_correspondance = csv.reader(csv_iriLabel_correspondance, delimiter =',', doublequote=True)
        correspondingPubIri = ""
        for row in iriLabel_correspondance:
            if (correspondingPubLabel == row[1]):
                correspondingPubIri = row[0]
        pPub = correspondingPubIri
    if (pPub == ""):
        print("MISSING LINK" + '\n')
    else:
        print(pPub + '\n')
    
    ### Write to XML
    if not os.path.exists('xml-articles'):
        os.makedirs('xml-articles')
    o = open('./xml-articles/import'+tif+'.xml', 'w', encoding="utf-8")
    o.write('<?xml version="1.0" encoding="utf-8"?>'+'\n'+'<knora xmlns="https://dasch.swiss/schema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"'+'\n'+'    xsi:schemaLocation="https://dasch.swiss/schema https://raw.githubusercontent.com/dasch-swiss/dsp-tools/main/knora/dsplib/schemas/data.xsd"'+'\n'+'    shortcode="0112" default-ontology="roud-oeuvres">'+'\n'+'    '+'\n'+'    <permissions id="img-default">'+'\n'+'        <allow group="UnknownUser">V</allow>'+'\n'+'        <allow group="KnownUser">D</allow>'+'\n'+'        <allow group="ProjectAdmin">CR</allow>'+'\n'+'        <allow group="Creator">CR</allow>'+'\n'+'    </permissions>'+'\n')


    Resource = ET.Element('resource', attrib={'label':pLabel, 'restype':':Page', 'id':pId, 'permissions':'img-default'})

    Bitstream = ET.SubElement(Resource, 'bitstream', attrib={'permissions':'img-default'})
    Bitstream.text = pBitstream

    PageHasNameProp = ET.SubElement(Resource, 'text-prop', attrib={'name':':pageHasName'})
    PageHasName = ET.SubElement(PageHasNameProp, 'text', attrib={'permissions':'img-default', 'encoding':'utf8'})
    PageHasName.text = pName

    HasSeqnumProp = ET.SubElement(Resource, 'integer-prop', attrib={'name':':hasSeqnum'})
    HasSeqnum = ET.SubElement(HasSeqnumProp, 'integer', attrib={'permissions':'img-default'})
    HasSeqnum.text = pSeqnum

    PartOfPubProp = ET.SubElement(Resource, 'resptr-prop', attrib={'name':':pageIsPartOfPublication'})
    PartOfPub = ET.SubElement(PartOfPubProp, 'resptr', attrib={'permissions':'img-default'})
    PartOfPub.text = pPub

    tree = ET.tostring(Resource, encoding="unicode")
    o.write('\n''\n'+ tree)


## WRITE END OF THE XML FILE
    o.write('\n'+'</knora>')
    o.close()
