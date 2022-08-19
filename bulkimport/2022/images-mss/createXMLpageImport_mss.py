###
### CREATE XML FOR BULK IMPORT OF SCANS
###


from xml.etree import ElementTree as ET
import csv
import os

### Open list of tiff to be imported
# test with 'list-tiff-mss_2import_test.txt'
listTifMss_file = open('list-tiff-mss_2import.txt', 'r', encoding="utf-8")

listTifMss = listTifMss_file.readlines()

for tif in listTifMss:

    # from CRLR_GR_MS6B110a/CRLR_GR_MS6B110a_1r_1.tif, remove first part and extension > CRLR_GR_MS6B110a_1r_1
    msContainingTif = tif.split('/')[0]
    tif = tif.split('/')[1].split('.')[0]
    

    print(tif)
    
    ### Building blocks
    msShelfmark = msContainingTif[8:] # MS6B110a
    msN = tif[10]  # 6
    msRestShelfmark = tif[11:].split('_')[0] # B110a
    
    
    msRest = tif[12:]  # 110a_1r_1.tif
    if (msRest.find('couv1') > 0):
        # example: G55a_couv1_1r_1.tif
        pageName = "première de couverture " + msRest.split('_')[2]
        pageSeqnum = msRest.split('_')[3]
    elif (msRest.find('couv4') > 0):
        # example: G55a_couv4_1r_255.tif
        pageName = "quatrième de couverture " + msRest.split('_')[2]
        pageSeqnum = msRest.split('_')[3]
    else:
        # example: B110a_1r_1.tif
        pageName = "f. " + msRest.split('_')[1]  # 1r
        pageSeqnum = msRest.split('_')[2]  # 1


    # csv downloaded from sparql query (query saved in graphdb). First column: iri, second column: shelfmark 
    # attention to delimiter for reading csv
    ### check shelfmark and store IRI in msTarget
    with open("iri-shelfmark.csv", 'r') as csv_iriShelfmark_correspondance:     
        iriShelfmark_correspondance = csv.reader(csv_iriShelfmark_correspondance, delimiter =',', doublequote=True)
        for row in iriShelfmark_correspondance:
            if (msShelfmark == row[1]):
                msTarget = row[0]

        ### Content for the XML
        pLabel = 'page_CRLR GR MS' + msN + ' ' + msRestShelfmark + '___' + pageName + '___' + pageSeqnum
        pId = tif + '.tif'
        pBitstream = '/mnt/scanlettMounted/GustaveRoud/E_Scan/Scans_complets/FondsArchive/' + msContainingTif + '/' + tif + '.tif'
        pName = pageName
        pSeqnum = pageSeqnum
        pMs = msTarget

    ### Write to XML
    if not os.path.exists('xml'):
        os.makedirs('xml')
    o = open('./xml/import'+tif+'.xml', 'w', encoding="utf-8")
    o.write('<?xml version="1.0" encoding="utf-8"?>'+'\n'+'<knora xmlns="https://dasch.swiss/schema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"'+'\n'+'    xsi:schemaLocation="https://dasch.swiss/schema https://raw.githubusercontent.com/dasch-swiss/dsp-tools/main/knora/dsplib/schemas/data.xsd"'+'\n'+'    shortcode="0112" default-ontology="roud-oeuvres">'+'\n'+'    '+'\n'+'    <permissions id="img-default">'+'\n'+'        <allow group="UnknownUser">V</allow>'+'\n'+'        <allow group="KnownUser">D</allow>'+'\n'+'        <allow group="ProjectAdmin">CR</allow>'+'\n'+'        <allow group="Creator">CR</allow>'+'\n'+'    </permissions>'+'\n')


    Resource = ET.Element('resource', attrib={'label':pLabel, 'restype':':Page', 'id':pId, 'permissions':'img-default'})

    Bitstream = ET.SubElement(Resource, 'bitstream', attrib={'permissions':'img-default'})   ## mimetype: png or tiff !!!
    Bitstream.text = pBitstream

    PageHasNameProp = ET.SubElement(Resource, 'text-prop', attrib={'name':':pageHasName'})
    PageHasName = ET.SubElement(PageHasNameProp, 'text', attrib={'permissions':'img-default', 'encoding':'utf8'})
    PageHasName.text = pName

    HasSeqnumProp = ET.SubElement(Resource, 'integer-prop', attrib={'name':':hasSeqnum'})
    HasSeqnum = ET.SubElement(HasSeqnumProp, 'integer', attrib={'permissions':'img-default'})
    HasSeqnum.text = pSeqnum

    PartOfMsProp = ET.SubElement(Resource, 'resptr-prop', attrib={'name':':pageIsPartOfManuscript'})
    PartOfMs = ET.SubElement(PartOfMsProp, 'resptr', attrib={'permissions':'img-default'})
    PartOfMs.text = pMs

    tree = ET.tostring(Resource, encoding="unicode")
    o.write('\n''\n'+ tree)


## WRITE END OF THE XML FILE
    o.write('\n'+'</knora>')
    o.close()
