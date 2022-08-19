###
### CREATE XML FOR BULK IMPORT OF SCANS
###



from xml.etree import ElementTree as ET
import csv
import os

### Open list of tiff to be imported
listTifPubs_file = open('list-tiff-pubs-books_2import.txt', 'r', encoding="utf-8")

listTifPubs = listTifPubs_file.readlines()

for scan in listTifPubs:

    # remove dir and extension
    book = scan.split('/')[0]
    tif = scan.split('/')[1].split('.')[0]
    print(tif)
    correspondingPubLabel = scan.split('/')[0] 
    pageSeqnum = tif.split('_')[-1]

    # PAGE NAME
    # There was a problem with books, because they have been scanned as if they were mss
    # using folios instead of pages, which does not correspond to anything for books.
    # To solve this, adding rules to calculate the page from the sequence number.
    if (book == "CRLR_GR_ED1_REQUIEM_1967" or book == "CRLR_GR_ED3_JORAT_1949" or
        book == "CRLR_GR_ED4_FEUILLETS_1929" or book == "CRLR_GR_ED5_ADIEU_1944" or book == "CRLR_GR_ED9_CAMPAGNE_1972" ):
        pageName = "p. " + str(int(pageSeqnum)-2)
    elif (book == "CRLR_GR_ED7_ECRITS1_1950"):  # the two volumes were reunited under one publication
        pageName = "vol. I p. " + str(int(pageSeqnum)-2)
    elif (book == "CRLR_GR_ED6_ADIEU_1927"):
        pageName = "p. " + pageSeqnum
    elif (book == "CRLR_GR_ED8_ECRITS2_1950"):
        pageName = "vol. II p. " + pageSeqnum
    elif (book == "CRLR_GR_ED12_SOLITUDE_1945"):
        pageName = "p. " + str(int(pageSeqnum)+2)
    elif (book == "CRLR_GR_ED2_ESSAI_1932"):
        pageName = "p. " + str(int(pageSeqnum)-6)
    elif (book == "CRLR_GR_ED10_MOISSONNEUR_1941"):
        if int(pageSeqnum) > 35:
            pageName = "p. " + str(int(pageSeqnum)+2)
        else:
            pageName = "p. " + pageSeqnum
    elif (book == "CRLR_GR_ED11_CAVALIER_1958"):
        if int(pageSeqnum) < 23:
            pageName = "p. " + str(int(pageSeqnum)-2)
        elif int(pageSeqnum) < 58:
            pageName = "p. " + str(int(pageSeqnum)-4)
        elif int(pageSeqnum) < 60:
            pageName = "p. " + str(int(pageSeqnum)-5)
        else:
            pageName = "p. " + str(int(pageSeqnum)-6)
    elif (book == "CRLR_GR_ED13_TRAITE_1932"):
        if int(pageSeqnum) <= 68:
            pageName = "p. " + str(int(pageSeqnum)-4)
        elif int(pageSeqnum) <= 70:
            pageName = "p. " + str(int(pageSeqnum)-5)
        else:
            pageName = "p. " + str(int(pageSeqnum)-6)

    
    ### Building blocks
    pLabel = tif
    pId = tif + '.tif'
    pBitstream = '/mnt/scanlettMounted/GustaveRoud/E_Scan/Scans_complets/Publications/OuvragesNumerises/' + book + '/' + tif + '.tif'
    pName = pageName
    pSeqnum = pageSeqnum


    # csv downloaded from sparql query (query saved in graphdb). First column: iri, second column: label 
    # attention to delimiter for reading csv
    ### check label and store IRI in correspondingPubIri
    with open("iri-label-books.csv", 'r') as csv_iriLabel_correspondance:     
        iriLabel_correspondance = csv.reader(csv_iriLabel_correspondance, delimiter =',', doublequote=True)
        for row in iriLabel_correspondance:
            if (correspondingPubLabel == row[1]):
                correspondingPubIri = row[0]
        pPub = correspondingPubIri
    
    ### Write to XML
    if not os.path.exists('xml-books'):
        os.makedirs('xml-books')
    o = open('./xml-books/import'+tif+'.xml', 'w', encoding="utf-8")
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
