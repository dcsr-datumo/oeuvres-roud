
# coding: utf-8

# In[ ]:


###
### SORT ACCORDING TO COLUMN
###

import sys, csv ,operator
data = csv.reader(open('../INPUT_data/publishers.csv'))
sortedlist = sorted(data, key=operator.itemgetter(1))    # 1 specifies according to first column we want to sort
#now write the sorted result into new CSV file
with open("../INPUT_data/publishers_sorted.csv", "w") as f:
  fileWriter = csv.writer(f, delimiter=',')
  for row in sortedlist:
      fileWriter.writerow(row)




# In[ ]:


###
### DEDUPLICATE DATA PUBLISHERS
### Check manually at the end
###

import sys, csv ,operator
reader=csv.reader(open('../INPUT_data/publishers_sorted.csv', 'r'), delimiter=',')
writer=csv.writer(open('../INPUT_data/publishers_sorted_distinct.csv', 'w'), delimiter=',')
entries = set()

for row in reader:
   key = (row[0], row[1]) # instead of just the last name

   if key not in entries:
      writer.writerow(row)
      entries.add(key)





# In[ ]:


###
### DEDUPLICATE DATA PERIODICALS  (using Pandas)
### Check manually at the end
###


import pandas as pd
file_name = "../INPUT_data/periodicals.csv"
file_name_output = "../INPUT_data/periodicals_distinct.csv"

df = pd.read_csv(file_name, sep="\t or ,")

# Notes:
# - the `subset=None` means that every column is used 
#    to determine if two rows are different; to change that specify
#    the columns as an array
# - the `inplace=True` means that the data structure is changed and
#   the duplicate rows are gone  
df.drop_duplicates(subset=None, inplace=True)

# Write the results to a different file
df.to_csv(file_name_output)





# In[ ]:


###
### DEDUPLICATE DATA AUTHORS  (using Pandas)
### Check manually at the end
###


import pandas as pd

file_name = "../INPUT_data/authors.csv"
file_name_output = "../INPUT_data/authors_distinct.csv"

df = pd.read_csv(file_name, sep="\t or ,")

# Notes:
# - the `subset=None` means that every column is used 
#    to determine if two rows are different; to change that specify
#    the columns as an array
# - the `inplace=True` means that the data structure is changed and
#   the duplicate rows are gone  
df.drop_duplicates(subset=None, inplace=True)

# Write the results to a different file
df.to_csv(file_name_output)


# In[ ]:


###
### AUTHORS distinguish name and surname
###

import csv

f = open('../INPUT_data/authors_distinct.csv')
o = open('../INPUT_data/authors_distinct_surname_name2.csv', 'w')

csv_f = csv.reader(f)   
data = []

for row in csv_f: 
   data.append(row)
f.close()

writer = csv.writer(o, quoting=csv.QUOTE_ALL)
for row in data[1:]:
    author = row[0]
    surname = author.partition(' ')[2] 
    name = author.partition(' ')[0]
    new_author = [surname, name]
    writer.writerow([new_author])

o.close()


# In[ ]:


###
### READ THE CSV (just to check)
###

import csv

f = open('../INPUT_data/publishers_sorted_distinct_manuallychecked.csv')
csv_f = csv.reader(f)   
data = []

for row in csv_f: 
   data.append(row)
f.close()

## TEST COSA C'È NELLE LINEE SPECIFICATE
## print(data[1:3])

for row in data[1:]:
    
    if (row[0] == ''):
        print('hello')


# In[ ]:


###
### CREATE XML FROM CSV (PUBLISHERS)
###





from xml.etree import ElementTree as ET
import csv

f = open('../INPUT_data/publishers_sorted_distinct_manuallychecked.csv')
o = open('../OUTPUT_xml/publishers.xml', 'w')

csv_f = csv.reader(f)   
data = []

for row in csv_f: 
   data.append(row)
f.close()

## TEST COSA C'È NELLE LINEE SPECIFICATE
## print(data[1:3])

## WRITE DECLARATIONS AND BEGINNING OF THE XML FILE -adding more line breaks for readibility '+'\n'+' ???-
o.write('<?xml version="1.0" encoding="UTF-8"?>'+'\n'+'<knoraXmlImport:resources xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://api.knora.org/ontology/knoraXmlImport/v1# ../p0112-roud-oeuvres-xml-schemas/p0112-roud-oeuvres.xsd" xmlns="http://api.knora.org/ontology/0112/roud-oeuvres/xml-import/v1#" xmlns:knoraXmlImport="http://api.knora.org/ontology/knoraXmlImport/v1#" xmlns:p0112-roud-oeuvres="http://api.knora.org/ontology/0112/roud-oeuvres/xml-import/v1#">'+'\n')


## WRITE ITEMS TO FILE
for row in data[0:]:
    
    publisherLocation = row[0] 
    publisherName = row[1]
    word_list = row[1].replace("'", ' ') ## replace accent with space
    word_list = word_list.replace(",", '').split()  ## replace comma with nothing and split words
    words = '_'.join(word_list)     
    
    ## registering namespace
    NS_ROUD = "http://api.knora.org/ontology/0112/roud-oeuvres/xml-import/v1#" 
    NS_KNORAIMPORT = "http://api.knora.org/ontology/knoraXmlImport/v1#"
    ET.register_namespace("p0112-roud-oeuvres", NS_ROUD)
    ET.register_namespace("knoraXmlImport", NS_KNORAIMPORT)

    ## define elements with ns
    PublisherNS = ET.QName(NS_ROUD, "Publisher")
    labelNS = ET.QName(NS_KNORAIMPORT, "label")
    publisherHasLocationNS = ET.QName(NS_ROUD, "publisherHasLocation")
    publisherHasNameNS = ET.QName(NS_ROUD, "publisherHasName")

    ## create elements (as previously defined with ns)
    Publisher = ET.Element(PublisherNS, attrib={'id':words}) 
    label = ET.SubElement(Publisher, labelNS)
    label.text = "edi_"+publisherName
    
    ## if row is empty, don't create element, otherwise the import will fail (of course only for properties that are not mandatory)
    if (row[0] == ''):
        print()
    else:
        publisherHasLocation = ET.SubElement(Publisher, publisherHasLocationNS, attrib={'knoraType':'richtext_value'})
        publisherHasLocation.text = publisherLocation ## use variable defined with location of the publisher corresponding to first row
    
    publisherHasName = ET.SubElement(Publisher, publisherHasNameNS, attrib={'knoraType':'richtext_value'})
    publisherHasName.text = publisherName  ## use variable defined with name of the publisher corresponding to second row
    
    tree = ET.tostring(Publisher, encoding="unicode")
    o.write('\n''\n'+ tree)

## WRITE END OF THE XML FILE
with o:  ## this is to append the text, if just write o.write does not work here (why??)
    o.write('\n'+'</knoraXmlImport:resources>')

o.close


# In[ ]:


###
### CREATE XML FROM CSV (PERIODICALS)
###





from xml.etree import ElementTree as ET
import csv, re

f = open('../INPUT_data/periodicals_distinct.csv')
o = open('../OUTPUT_xml/periodicals.xml', 'w')

csv_f = csv.reader(f)   
data = []

for row in csv_f: 
   data.append(row)
f.close()

## TEST COSA C'È NELLE LINEE SPECIFICATE
## print(data[1:3])

## WRITE DECLARATIONS AND BEGINNING OF THE XML FILE -adding more line breaks for readibility '+'\n'+' ???-
o.write('<?xml version="1.0" encoding="UTF-8"?>'+'\n'+'<knoraXmlImport:resources xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://api.knora.org/ontology/knoraXmlImport/v1# ../p0112-roud-oeuvres-xml-schemas/p0112-roud-oeuvres.xsd" xmlns="http://api.knora.org/ontology/0112/roud-oeuvres/xml-import/v1#" xmlns:knoraXmlImport="http://api.knora.org/ontology/knoraXmlImport/v1#" xmlns:p0112-roud-oeuvres="http://api.knora.org/ontology/0112/roud-oeuvres/xml-import/v1#">'+'\n')


## WRITE ITEMS TO FILE
for row in data[0:]:
    
    periodicalTitle = row[0] 
    labelPeriodicalTitle = row[0].replace('"', '')  ## in label " not accepted
    word_list = re.split(', |\(|/', labelPeriodicalTitle) ## split at comma, parenthesis or slash and take the first part (take the first part is below), using labelPeriodicalTitle where quotes have been already deleted
    word_list = word_list[0].replace("'", ' ').replace(",", '').split()  ## replace accent with space and replace comma with nothing and split words
    words = '_'.join(word_list) 
    
    ## registering namespace
    NS_ROUD = "http://api.knora.org/ontology/0112/roud-oeuvres/xml-import/v1#" 
    NS_KNORAIMPORT = "http://api.knora.org/ontology/knoraXmlImport/v1#"
    ET.register_namespace("p0112-roud-oeuvres", NS_ROUD)
    ET.register_namespace("knoraXmlImport", NS_KNORAIMPORT)

    ## define elements with ns
    PeriodicalNS = ET.QName(NS_ROUD, "Periodical")
    labelNS = ET.QName(NS_KNORAIMPORT, "label")
    periodicalHasTitleNS = ET.QName(NS_ROUD, "periodicalHasTitle")

    ## create elements (as previously defined with ns)
    Periodical = ET.Element(PeriodicalNS, attrib={'id':words}) 
    label = ET.SubElement(Periodical, labelNS)
    label.text = "period_"+labelPeriodicalTitle
    periodicalHasTitle = ET.SubElement(Periodical, periodicalHasTitleNS, attrib={'knoraType':'richtext_value'})
    periodicalHasTitle.text = periodicalTitle  ## use variable defined with name of the publisher corresponding to second row
    
    tree = ET.tostring(Periodical, encoding="unicode")
    o.write('\n''\n'+ tree)

## WRITE END OF THE XML FILE
with o:  ## this is to append the text, if just write o.write does not work here (why??)
    o.write('\n'+'</knoraXmlImport:resources>')

o.close


# In[ ]:


###
### CREATE XML FROM CSV (AUTHORS)
###





from xml.etree import ElementTree as ET
import csv, re

f = open('../INPUT_data/authors_distinct_surname_name.csv')
o = open('../OUTPUT_xml/authors.xml', 'w')

csv_f = csv.reader(f)   
data = []

for row in csv_f: 
   data.append(row)
f.close()

## TEST COSA C'È NELLE LINEE SPECIFICATE
## print(data[1:3])

## WRITE DECLARATIONS AND BEGINNING OF THE XML FILE -adding more line breaks for readibility '+'\n'+' ???-
o.write('<?xml version="1.0" encoding="UTF-8"?>'+'\n'+'<knoraXmlImport:resources xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://api.knora.org/ontology/knoraXmlImport/v1# ../p0112-roud-oeuvres-xml-schemas/p0112-roud-oeuvres.xsd" xmlns="http://api.knora.org/ontology/0112/roud-oeuvres/xml-import/v1#" xmlns:knoraXmlImport="http://api.knora.org/ontology/knoraXmlImport/v1#" xmlns:p0112-roud-oeuvres="http://api.knora.org/ontology/0112/roud-oeuvres/xml-import/v1#">'+'\n')


## WRITE ITEMS TO FILE
for row in data[0:]:
    
    surname = row[1]
    name = row[0]
    #### for building id
    if len(surname.split()) > 1:  ## if long name and surname
        surnameid = '_'.join(re.split(' ', surname))
    else:
        surnameid = surname
    if len(name.split()) > 1:
        nameid = '_'.join(re.split(' ', name))
    else:
        nameid = name
    if (row[0] == ''):  ## if author has only surname
        authorid = (surnameid).replace("'", '').replace("(", '').replace(")", '')
    else:
        authorid = (surnameid+'_'+nameid).replace("'", '').replace("(", '').replace(")", '') 
   

    
    ## registering namespace
    NS_ROUD = "http://api.knora.org/ontology/0112/roud-oeuvres/xml-import/v1#" 
    NS_KNORAIMPORT = "http://api.knora.org/ontology/knoraXmlImport/v1#"
    ET.register_namespace("p0112-roud-oeuvres", NS_ROUD)
    ET.register_namespace("knoraXmlImport", NS_KNORAIMPORT)

    ## define elements with ns
    AuthorNS = ET.QName(NS_ROUD, "Author")  
    labelNS = ET.QName(NS_KNORAIMPORT, "label")
    AuthorHasFamilyNameNS = ET.QName(NS_ROUD, "authorHasFamilyName")
    AuthorHasGivenNameNS = ET.QName(NS_ROUD, "authorHasGivenName")

    ## create elements (as previously defined with ns)
    
    
    
    Author = ET.Element(AuthorNS, attrib={'id':authorid}) 
    label = ET.SubElement(Author, labelNS)
    if (row[0] == ''):  ## if author has surname and name
        label.text = "aut_"+surname
        authorHasFamilyName = ET.SubElement(Author, AuthorHasFamilyNameNS, attrib={'knoraType':'richtext_value'})
        authorHasFamilyName.text = surname  ## 
    else:
        label.text = "aut_"+surname+" "+name
        authorHasFamilyName = ET.SubElement(Author, AuthorHasFamilyNameNS, attrib={'knoraType':'richtext_value'})
        authorHasFamilyName.text = surname  ## 
        authorHasGivenName = ET.SubElement(Author, AuthorHasGivenNameNS, attrib={'knoraType':'richtext_value'})
        authorHasGivenName.text = name  ## 
    
    tree = ET.tostring(Author, encoding="unicode")
    o.write('\n''\n'+ tree)

## WRITE END OF THE XML FILE
with o:  ## this is to append the text, if just write o.write does not work here (why??)
    o.write('\n'+'</knoraXmlImport:resources>')

o.close


# In[ ]:


###
### CREATE XML FROM CSV (ARTICLES)
###



from xml.etree import ElementTree as ET
import csv, re

f = open('../INPUT_data/articles.csv')
o = open('../OUTPUT_xml/articles.xml', 'w')

csv_f = csv.reader(f)   
data = []

for row in csv_f: 
   data.append(row)
f.close()


###################################
## WRITE DECLARATIONS AND BEGINNING OF THE XML FILE -adding more line breaks for readibility '+'\n'+' ???-
###################################
o.write('<?xml version="1.0" encoding="UTF-8"?>'+'\n'+'<knoraXmlImport:resources xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://api.knora.org/ontology/knoraXmlImport/v1# ../p0112-roud-oeuvres-xml-schemas/p0112-roud-oeuvres.xsd" xmlns="http://api.knora.org/ontology/0112/roud-oeuvres/xml-import/v1#" xmlns:knoraXmlImport="http://api.knora.org/ontology/knoraXmlImport/v1#" xmlns:p0112-roud-oeuvres="http://api.knora.org/ontology/0112/roud-oeuvres/xml-import/v1#">'+'\n')



biblio_number_new = 1000  ## starting point for counting biblioid that should be added because are not in the original
    

###################################
## PREPARE CONTENT OF ELEMENTS AND ATTRIBUTES
###################################
for row in data[0:]:
    
    
    
    
    ## -----------------------> @id
    biblio_number_new += 1    
    if (row[0] != ''):
        Publicationid = 'biblio_'+row[0] ## @id
    else:
        Publicationid = 'biblio_'+str(biblio_number_new)   ## increasing number, just to give it an id. Starts from 1000
    
      
        
        
    
    ## -----------------------> hasPublicationType
    if ('Œuvre poétique' in row[1]):
        HasPublicationType = 'http://rdfh.ch/lists/0112/roud-oeuvres-flatlist-hasPublicationType-oeuvrePoetique'
    if ('Périodique' in row[1]):
        HasPublicationType = 'http://rdfh.ch/lists/0112/roud-oeuvres-flatlist-hasPublicationType-propos'
    ##if ('À propos de Roud' in row[1]):
      ##  HasPublicationType = 'http://rdfh.ch/lists/0112/roud-oeuvres-flatlist-hasPublicationType-journal'
    if ('Traduction' in row[1]):
        HasPublicationType = 'http://rdfh.ch/lists/0112/roud-oeuvres-flatlist-hasPublicationType-traduction'
    if ('Photographie' in row[1]):
        HasPublicationType = 'http://rdfh.ch/lists/0112/roud-oeuvres-flatlist-hasPublicationType-photo'
    if ('Correspondance' in row[1]):
        HasPublicationType = 'http://rdfh.ch/lists/0112/roud-oeuvres-flatlist-hasPublicationType-correspondance'
    if ('À propos de Roud' in row[1]):
        HasPublicationType = 'http://rdfh.ch/lists/0112/roud-oeuvres-flatlist-hasPublicationType-surRoud'
    
    
    ## -----------------------> publicationHasTitle
    PublicationHasTitle = row[3]  
    
    
    ## -----------------------> isPublishedInPeriodical
    periodicalTitle = row[4].replace('"', '')  ## all this copied from transformation to periodical above
    word_list = re.split(', |\(|/', periodicalTitle) 
    word_list = word_list[0].replace("'", ' ').replace(",", '').split()  
    PeriodicalTarget = '_'.join(word_list) 
    
    
    ## -----------------------> publicationHasTitle
    HasCollaborators = row[6]  
    
    
    ## -----------------------> IsInPeriodicalIssue
    IsInPeriodicalIssueVolume = row[7]
    if (',' in row[7]):
        IsInPeriodicalIssue_split = re.split(', ',row[7])
        IsInPeriodicalIssue = IsInPeriodicalIssue_split[0]
        IsInPeriodicalVolume = IsInPeriodicalIssue_split[1].replace('-', ' et ')
    else:
        IsInPeriodicalVolumeOnly = row[7].replace('-', ' et ')
    
    
    ## -----------------------> publicationHasDate   
    Date = row[10]
    pattern = re.compile("\d\d\d\d-\d\d\d\d")
    if ('(' in Date):
        Datedmy_split = re.split('-', Date)  ## split in day, month, year
        Date1y = Datedmy_split[0]
        Date1m = Datedmy_split[1]
        Date12_split = re.split('\(', Date)  ## split in date1 and date2
        Date1 = Date12_split[0]
        Date2 = Date12_split[1].replace('(', '').replace(')', '')
        if len(Date1) > 7:             ## period includes year and month and days
            if len(Date2) > 3:         ## period includes year and month and days (month and days are different)
                PeriodMD = 'GREGORIAN:'+Date1+' CE:'+Date1y+Date2+' CE'  
            else:                      ## period includes year and month and days (only days are different)     
                PeriodD = 'GREGORIAN:'+Date1+' CE:'+Date1y+'-'+Date1m+Date2+' CE'  
        else:                          ## period includes year and month
            PeriodM = 'GREGORIAN:'+Date1+' CE:'+Date1y+Date2+' CE'
    else:
        if (pattern.match(Date)):
            DateY_split = re.split('-', Date)
            DateY1 = DateY_split[0]
            DateY2 = DateY_split[1]
            PeriodY = 'GREGORIAN:'+DateY1+' CE:'+DateY2+' CE'
        else:
            PublicationHasDate = 'GREGORIAN:'+Date+' CE'
    
    
    ## -----------------------> periodicalArticleIsInPages
    PeriodicalArticleIsInPages = row[11]  
    
    
    ## -----------------------> publicationHasInternalComment
    PublicationHasInternalComment = row[12]
    
    
    ## -----------------------> PublicationIsTranscribed
    PublicationIsTranscribed = row[13]
    
    
    ## -----------------------> PublicationIsTranscribed
    OriginalIsInCrlrArchive = row[16]
  
    
    ## -----------------------> publicationHasAuthor
    ArticleAuthor = row[2]
    if (',' in ArticleAuthor):
        ArticleAuthor_split = re.split(', ', ArticleAuthor)
        if (' ' in ArticleAuthor_split[0]):
            ArticlesSurname = ArticleAuthor_split[0].partition(' ')[0]
            ArticlesName = ArticleAuthor_split[0].partition(' ')[2]
            ArticlesSurnameSecond = ArticleAuthor_split[1].partition(' ')[0]
            ArticlesNameSecond = ArticleAuthor_split[1].partition(' ')[2]
            with open("../INPUT_data/authors_with_id.csv", 'r') as authors_with_id:   
                csv_authors = csv.reader(authors_with_id)
                ## AuthorTarget = [row[2] for row in csv_authors if ArticlesSurname in row[0]]  this creates list, while I want item
                for row in csv_authors:
                    if (ArticlesSurname == row[0] and ArticlesName == row[1]):
                        AuthorTarget = row[2]
                    if (ArticlesSurnameSecond == row[0] and ArticlesNameSecond == row[1]):
                        AuthorTargetSecond = row[2]
        else:
            ArticlesSurname = ArticleAuthor_split[0]
            ArticlesSurnameSecond = ArticleAuthor_split[1].partition(' ')[0]
            ArticlesNameSecond = ArticleAuthor_split[1].partition(' ')[2]
            with open("../INPUT_data/authors_with_id.csv", 'r') as authors_with_id:   
                csv_authors = csv.reader(authors_with_id)
                ## AuthorTarget = [row[2] for row in csv_authors if ArticlesSurname in row[0]]  this creates list, while I want item
                for row in csv_authors:
                    if (ArticlesSurname == row[0]):
                        AuthorTarget = row[2]
                    if (ArticlesSurnameSecond == row[0] and ArticlesNameSecond == row[1]):
                        AuthorTargetSecond = row[2]
    else:
        if (' ' in ArticleAuthor):
            ArticlesSurname = ArticleAuthor.partition(' ')[0]
            ArticlesName = ArticleAuthor.partition(' ')[2]
            with open("../INPUT_data/authors_with_id.csv", 'r') as authors_with_id:   
                csv_authors = csv.reader(authors_with_id)
                ## AuthorTarget = [row[2] for row in csv_authors if ArticlesSurname in row[0]]  this creates list, while I want item
                for row in csv_authors:
                    if (ArticlesSurname == row[0] and ArticlesName == row[1]):
                        AuthorTargetSingle = row[2]
        else:
            ArticlesSurname = ArticleAuthor
            with open("../INPUT_data/authors_with_id.csv", 'r') as authors_with_id:   
                csv_authors = csv.reader(authors_with_id)
                ## AuthorTarget = [row[2] for row in csv_authors if ArticlesSurname in row[0]]  this creates list, while I want item
                for row in csv_authors:
                    if (ArticlesSurname == row[0]):
                        AuthorTargetSingle = row[2]  
        
    
    
    ## -----------------------> label
    if (ArticleAuthor != '' and PublicationHasTitle != '' and PeriodicalTarget != '' and Date != ''):
        PeriodicalArticleLabelComplete = "pub_"+ArticleAuthor+' ___ '+PublicationHasTitle+' ___ '+PeriodicalTarget+' ___ '+Date
    else:
        if (ArticleAuthor != '' and PublicationHasTitle != '' and PeriodicalTarget != ''):
            PeriodicalArticleLabelComplete = "pub_"+ArticleAuthor+' ___ '+PublicationHasTitle+' ___ '+PeriodicalTarget
        else:
            if (ArticleAuthor != '' and PublicationHasTitle != '' and Date != ''):
                PeriodicalArticleLabelComplete = "pub_"+ArticleAuthor+' ___ '+PublicationHasTitle+' ___ '+Date
            else:
                if (ArticleAuthor != '' and PeriodicalTarget != '' and Date != ''):
                    PeriodicalArticleLabelComplete = "pub_"+ArticleAuthor+' ___ '+PeriodicalTarget+' ___ '+Date
                else:
                    if (PublicationHasTitle != '' and PeriodicalTarget != '' and Date != ''):
                        PeriodicalArticleLabelComplete = "pub_"+PublicationHasTitle+' ___ '+PeriodicalTarget+' ___ '+Date

    PeriodicalArticleLabel = re.sub(r"\(([^\)]+)\)", "", PeriodicalArticleLabelComplete)
    
    
    
                
                
    
    ###################################
    #### REGISTERING NAMESPACES
    ###################################
    NS_ROUD = "http://api.knora.org/ontology/0112/roud-oeuvres/xml-import/v1#" 
    NS_KNORAIMPORT = "http://api.knora.org/ontology/knoraXmlImport/v1#"
    ET.register_namespace("p0112-roud-oeuvres", NS_ROUD)
    ET.register_namespace("knoraXmlImport", NS_KNORAIMPORT)

    
    ###################################
    ## DEFINE ELEMENTS WITH NS
    ###################################
    PeriodicalArticleNS = ET.QName(NS_ROUD, "PeriodicalArticle")
    labelNS = ET.QName(NS_KNORAIMPORT, "label")
    hasPublicationTypeNS = ET.QName(NS_ROUD, "hasPublicationType")
    publicationHasAuthorNS = ET.QName(NS_ROUD, "publicationHasAuthor")
    AuthorNS = ET.QName(NS_ROUD, "Author")
    publicationHasTitleNS = ET.QName(NS_ROUD, "publicationHasTitle")
    isPublishedInPeriodicalNS = ET.QName(NS_ROUD, "isPublishedInPeriodical")
    PeriodicalNS = ET.QName(NS_ROUD, "Periodical")
    hasCollaboratorsNS = ET.QName(NS_ROUD, "hasCollaborators")
    isInPeriodicalIssueNS = ET.QName(NS_ROUD, "isInPeriodicalIssue")
    isInPeriodicalVolumeNS = ET.QName(NS_ROUD, "isInPeriodicalVolume")
    publicationHasDateNS = ET.QName(NS_ROUD, "publicationHasDate")
    periodicalArticleIsInPagesNS = ET.QName(NS_ROUD, "periodicalArticleIsInPages")
    publicationHasInternalCommentNS = ET.QName(NS_ROUD, "publicationHasInternalComment")
    publicationIsTranscribedNS = ET.QName(NS_ROUD, "publicationIsTranscribed")
    originalIsInCrlrArchiveNS = ET.QName(NS_ROUD, "originalIsInCrlrArchive")
    
    
    ###################################
    ## CREATE ELEMENTS AND ATTRIBUTES (AS PREVIOUSLY DEFINED WITH NS) AND ASSIGN THEM CONTENT
    ###################################
    PeriodicalArticle = ET.Element(PeriodicalArticleNS, attrib={'id':Publicationid}) 
    
    label = ET.SubElement(PeriodicalArticle, labelNS)
    label.text = PeriodicalArticleLabel
    
    
    ## -----------------------------> hasCollaborators
    if (HasCollaborators != ''):
        hasCollaborators = ET.SubElement(PeriodicalArticle, hasCollaboratorsNS, attrib={'knoraType':'richtext_value'})
        hasCollaborators.text = HasCollaborators
    
    
    ## -----------------------------> hasPublicationType
    hasPublicationType = ET.SubElement(PeriodicalArticle, hasPublicationTypeNS, attrib={'knoraType':'hlist_value'})
    hasPublicationType.text = HasPublicationType  ## use variable defined with name of the publisher corresponding to second row
    
    
    ## -----------------------------> isInPeriodicalVolume  and  isInPeriodicalIssue
    if (IsInPeriodicalIssueVolume != '' and IsInPeriodicalVolumeOnly == ''):
        isInPeriodicalIssue = ET.SubElement(PeriodicalArticle, isInPeriodicalIssueNS, attrib={'knoraType':'richtext_value'})
        isInPeriodicalIssue.text = IsInPeriodicalIssue
        isInPeriodicalVolume = ET.SubElement(PeriodicalArticle, isInPeriodicalVolumeNS, attrib={'knoraType':'richtext_value'})
        isInPeriodicalVolume.text = IsInPeriodicalVolume
    else:   
        if (IsInPeriodicalIssueVolume != ''):
            isInPeriodicalVolume = ET.SubElement(PeriodicalArticle, isInPeriodicalVolumeNS, attrib={'knoraType':'richtext_value'})
            isInPeriodicalVolume.text = IsInPeriodicalVolumeOnly
    
    
    ## -----------------------------> isPublishedInPeriodical
    isPublishedInPeriodical = ET.SubElement(PeriodicalArticle, isPublishedInPeriodicalNS)
    Periodical = ET.SubElement(isPublishedInPeriodical, PeriodicalNS, attrib={'knoraType':'link_value', 'linkType':'ref', 'target':PeriodicalTarget})
    
    
    ## -----------------------------> OriginalIsInCrlrArchive
    if (OriginalIsInCrlrArchive != ''):
        originalIsInCrlrArchive = ET.SubElement(PeriodicalArticle, originalIsInCrlrArchiveNS, attrib={'knoraType':'richtext_value'})
        originalIsInCrlrArchive.text = OriginalIsInCrlrArchive
        
    
    ## -----------------------------> periodicalArticleIsInPages
    if (PeriodicalArticleIsInPages != ''):
        periodicalArticleIsInPages = ET.SubElement(PeriodicalArticle, periodicalArticleIsInPagesNS, attrib={'knoraType':'richtext_value'})
        periodicalArticleIsInPages.text = PeriodicalArticleIsInPages
        
    
    
    ## -----------------------------> publicationHasAuthor
    if (ArticleAuthor != ''):
        if (',') in ArticleAuthor:
            publicationHasAuthor = ET.SubElement(PeriodicalArticle, publicationHasAuthorNS)
            Author = ET.SubElement(publicationHasAuthor, AuthorNS, attrib={'knoraType':'link_value', 'linkType':'ref', 'target':AuthorTarget})
            publicationHasAuthor = ET.SubElement(PeriodicalArticle, publicationHasAuthorNS)
            Author = ET.SubElement(publicationHasAuthor, AuthorNS, attrib={'knoraType':'link_value', 'linkType':'ref', 'target':AuthorTargetSecond})
        else:
            publicationHasAuthor = ET.SubElement(PeriodicalArticle, publicationHasAuthorNS)
            Author = ET.SubElement(publicationHasAuthor, AuthorNS, attrib={'knoraType':'link_value', 'linkType':'ref', 'target':AuthorTargetSingle})
    
    
    
    ## -----------------------------> publicationHasDate
    if (Date != ''):
        publicationHasDate = ET.SubElement(PeriodicalArticle, publicationHasDateNS, attrib={'knoraType':'date_value'})
    
    if ('(' in Date):
        if len(Date1) > 7:
            if len(Date2) > 3:   
                publicationHasDate.text = PeriodMD
            else:
                publicationHasDate.text = PeriodD
        else:
            publicationHasDate.text = PeriodM
    else:
        if (pattern.match(Date)):
            publicationHasDate.text = PeriodY
        else:
            if (Date != ''):
                publicationHasDate.text = PublicationHasDate
    
    
    ## -----------------------------> publicationHasInternalComment
    if (PublicationHasInternalComment != ''):
        publicationHasInternalComment = ET.SubElement(PeriodicalArticle, publicationHasInternalCommentNS, attrib={'knoraType':'richtext_value'})
        publicationHasInternalComment.text = PublicationHasInternalComment
        
    
    ## -----------------------------> publicationHasTitle
    publicationHasTitle = ET.SubElement(PeriodicalArticle, publicationHasTitleNS, attrib={'knoraType':'richtext_value'})
    publicationHasTitle.text = PublicationHasTitle
    
    
     ## -----------------------------> publicationIsTranscribed
    if (PublicationIsTranscribed != ''):
        publicationIsTranscribed = ET.SubElement(PeriodicalArticle, publicationIsTranscribedNS, attrib={'knoraType':'richtext_value'})
        publicationIsTranscribed.text = PublicationIsTranscribed
        
        
    
    
    tree = ET.tostring(PeriodicalArticle, encoding="unicode")
    o.write('\n''\n'+ tree)

## WRITE END OF THE XML FILE
with o:  ## this is to append the text, if just write o.write does not work here (why??)
    o.write('\n'+'</knoraXmlImport:resources>')

o.close


# In[ ]:


###
### CREATE XML FROM CSV (BOOKS)
###



from xml.etree import ElementTree as ET
import csv, re

f = open('../INPUT_data/books.csv')
o = open('../OUTPUT_xml/books.xml', 'w')

csv_f = csv.reader(f)   
data = []

for row in csv_f: 
   data.append(row)
f.close()


## SI [0] id, [1] type, [2] author, [3] title, [6] collaborateurs, [8] placepub, [9] namepub, 
## SI [10] date, [11] pages, [12] comm interne, [13] Retranscrit, [15] digitized, [16] dans fonds CRLR  ##
## NO [4] title_pub, [5] illustré par, [7] numéro, [14] website interest  ##



###################################
## WRITE DECLARATIONS AND BEGINNING OF THE XML FILE -adding more line breaks for readibility '+'\n'+' ???-
###################################
o.write('<?xml version="1.0" encoding="UTF-8"?>'+'\n'+'<knoraXmlImport:resources xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://api.knora.org/ontology/knoraXmlImport/v1# ../p0112-roud-oeuvres-xml-schemas/p0112-roud-oeuvres.xsd" xmlns="http://api.knora.org/ontology/0112/roud-oeuvres/xml-import/v1#" xmlns:knoraXmlImport="http://api.knora.org/ontology/knoraXmlImport/v1#" xmlns:p0112-roud-oeuvres="http://api.knora.org/ontology/0112/roud-oeuvres/xml-import/v1#">'+'\n')



biblio_number_new = 2000  ## starting point for counting biblioid that should be added because are not in the original
    

###################################
## PREPARE CONTENT OF ELEMENTS AND ATTRIBUTES
###################################
for row in data[0:]:
    
    
    
    
    ## -----------------------> @id
    biblio_number_new += 1    
    if (row[0] != ''):
        Publicationid = 'biblio_'+row[0] ## @id
    else:
        Publicationid = 'biblio_'+str(biblio_number_new)   ## increasing number, just to give it an id. Starts from 1000
    
      
        
        
    
    ## -----------------------> hasPublicationType
    if ('Œuvre poétique' in row[1]):
        HasPublicationType = 'http://rdfh.ch/lists/0112/roud-oeuvres-flatlist-hasPublicationType-oeuvrePoetique'
    if ('Périodique' in row[1]):
        HasPublicationType = 'http://rdfh.ch/lists/0112/roud-oeuvres-flatlist-hasPublicationType-propos'
    ##if ('À propos de Roud' in row[1]):
      ##  HasPublicationType = 'http://rdfh.ch/lists/0112/roud-oeuvres-flatlist-hasPublicationType-journal'
    if ('Traduction' in row[1]):
        HasPublicationType = 'http://rdfh.ch/lists/0112/roud-oeuvres-flatlist-hasPublicationType-traduction'
    if ('Photographie' in row[1]):
        HasPublicationType = 'http://rdfh.ch/lists/0112/roud-oeuvres-flatlist-hasPublicationType-photo'
    if ('Correspondance' in row[1]):
        HasPublicationType = 'http://rdfh.ch/lists/0112/roud-oeuvres-flatlist-hasPublicationType-correspondance'
    if ('À propos de Roud' in row[1]):
        HasPublicationType = 'http://rdfh.ch/lists/0112/roud-oeuvres-flatlist-hasPublicationType-surRoud'
    
    
    ## -----------------------> publicationHasTitle
    PublicationHasTitle = row[3]  
    
    
    ## -----------------------> publicationHasCollaborators
    HasCollaborators = row[6]  
    
    
    ## -----------------------> hasPublisher (PublisherTarget)
    publisherName = row[9]
    word_list = publisherName.replace("'", ' ') ## replace accent with space
    word_list = word_list.replace(",", '').split()  ## replace comma with nothing and split words
    PublisherTarget = '_'.join(word_list)
    
    
    ## -----------------------> publicationHasDate   
    Date = row[10]
    pattern = re.compile("\d\d\d\d-\d\d\d\d")
    if ('(' in Date):
        Datedmy_split = re.split('-', Date)  ## split in day, month, year
        Date1y = Datedmy_split[0]
        Date1m = Datedmy_split[1]
        Date12_split = re.split('\(', Date)  ## split in date1 and date2
        Date1 = Date12_split[0]
        Date2 = Date12_split[1].replace('(', '').replace(')', '')
        if len(Date1) > 7:             ## period includes year and month and days
            if len(Date2) > 3:         ## period includes year and month and days (month and days are different)
                PeriodMD = 'GREGORIAN:'+Date1+' CE:'+Date1y+Date2+' CE'  
            else:                      ## period includes year and month and days (only days are different)     
                PeriodD = 'GREGORIAN:'+Date1+' CE:'+Date1y+'-'+Date1m+Date2+' CE'  
        else:                          ## period includes year and month
            PeriodM = 'GREGORIAN:'+Date1+' CE:'+Date1y+Date2+' CE'
    else:
        if (pattern.match(Date)):
            DateY_split = re.split('-', Date)
            DateY1 = DateY_split[0]
            DateY2 = DateY_split[1]
            PeriodY = 'GREGORIAN:'+DateY1+' CE:'+DateY2+' CE'
        else:
            PublicationHasDate = 'GREGORIAN:'+Date+' CE'
    
    
    ## -----------------------> bookHasSpecificPages
    BookHasSpecificPages = row[11]  
    
    
    ## -----------------------> publicationHasInternalComment
    PublicationHasInternalComment = row[12]
    
    
    ## -----------------------> PublicationIsTranscribed
    PublicationIsTranscribed = row[13]
    
    
    ## -----------------------> PublicationIsTranscribed
    OriginalIsInCrlrArchive = row[16]
  
    
    ## -----------------------> publicationHasAuthor
    ArticleAuthor = row[2]
    if (',' in ArticleAuthor):
        ArticleAuthor_split = re.split(', ', ArticleAuthor)
        if (' ' in ArticleAuthor_split[0]):
            ArticlesSurname = ArticleAuthor_split[0].partition(' ')[0]
            ArticlesName = ArticleAuthor_split[0].partition(' ')[2]
            ArticlesSurnameSecond = ArticleAuthor_split[1].partition(' ')[0]
            ArticlesNameSecond = ArticleAuthor_split[1].partition(' ')[2]
            with open("../INPUT_data/authors_with_id.csv", 'r') as authors_with_id:   
                csv_authors = csv.reader(authors_with_id)
                ## AuthorTarget = [row[2] for row in csv_authors if ArticlesSurname in row[0]]  this creates list, while I want item
                for row in csv_authors:
                    if (ArticlesSurname == row[0] and ArticlesName == row[1]):
                        AuthorTarget = row[2]
                    if (ArticlesSurnameSecond == row[0] and ArticlesNameSecond == row[1]):
                        AuthorTargetSecond = row[2]
        else:
            ArticlesSurname = ArticleAuthor_split[0]
            ArticlesSurnameSecond = ArticleAuthor_split[1].partition(' ')[0]
            ArticlesNameSecond = ArticleAuthor_split[1].partition(' ')[2]
            with open("../INPUT_data/authors_with_id.csv", 'r') as authors_with_id:   
                csv_authors = csv.reader(authors_with_id)
                ## AuthorTarget = [row[2] for row in csv_authors if ArticlesSurname in row[0]]  this creates list, while I want item
                for row in csv_authors:
                    if (ArticlesSurname == row[0]):
                        AuthorTarget = row[2]
                    if (ArticlesSurnameSecond == row[0] and ArticlesNameSecond == row[1]):
                        AuthorTargetSecond = row[2]
    else:
        if (' ' in ArticleAuthor):
            ArticlesSurname = ArticleAuthor.partition(' ')[0]
            ArticlesName = ArticleAuthor.partition(' ')[2]
            with open("../INPUT_data/authors_with_id.csv", 'r') as authors_with_id:   
                csv_authors = csv.reader(authors_with_id)
                ## AuthorTarget = [row[2] for row in csv_authors if ArticlesSurname in row[0]]  this creates list, while I want item
                for row in csv_authors:
                    if (ArticlesSurname == row[0] and ArticlesName == row[1]):
                        AuthorTargetSingle = row[2]
        else:
            ArticlesSurname = ArticleAuthor
            with open("../INPUT_data/authors_with_id.csv", 'r') as authors_with_id:   
                csv_authors = csv.reader(authors_with_id)
                ## AuthorTarget = [row[2] for row in csv_authors if ArticlesSurname in row[0]]  this creates list, while I want item
                for row in csv_authors:
                    if (ArticlesSurname == row[0]):
                        AuthorTargetSingle = row[2]  
                        
                    
    ## -----------------------> label
    if (ArticleAuthor != '' and PublicationHasTitle != '' and Date != ''):
        BookLabelComplete = "pub_"+ArticleAuthor+' ___ '+PublicationHasTitle+' ___ '+Date
    else:
        if (ArticleAuthor != '' and PublicationHasTitle != ''):
            BookLabelComplete = "pub_"+ArticleAuthor+' ___ '+PublicationHasTitle
        else:
            if (ArticleAuthor != '' and Date != ''):
                BookLabelComplete = "pub_"+ArticleAuthor+Date
            else:
                if (PublicationHasTitle != '' and Date != ''):
                    BookLabelComplete = "pub_"+PublicationHasTitle+' ___ '+Date

    BookLabel = re.sub(r"\(([^\)]+)\)", "", BookLabelComplete)

    
                
                
    
    ###################################
    #### REGISTERING NAMESPACES
    ###################################
    NS_ROUD = "http://api.knora.org/ontology/0112/roud-oeuvres/xml-import/v1#" 
    NS_KNORAIMPORT = "http://api.knora.org/ontology/knoraXmlImport/v1#"
    ET.register_namespace("p0112-roud-oeuvres", NS_ROUD)
    ET.register_namespace("knoraXmlImport", NS_KNORAIMPORT)

    
    ###################################
    ## DEFINE ELEMENTS WITH NS
    ###################################
    BookNS = ET.QName(NS_ROUD, "Book")
    labelNS = ET.QName(NS_KNORAIMPORT, "label")
    bookHasSpecificPagesNS = ET.QName(NS_ROUD, "bookHasSpecificPages")
    hasPublicationTypeNS = ET.QName(NS_ROUD, "hasPublicationType")
    hasPublisherNS = ET.QName(NS_ROUD, "hasPublisher")
    PublisherNS = ET.QName(NS_ROUD, "Publisher")
    publicationHasAuthorNS = ET.QName(NS_ROUD, "publicationHasAuthor")
    AuthorNS = ET.QName(NS_ROUD, "Author")
    publicationHasTitleNS = ET.QName(NS_ROUD, "publicationHasTitle")
    hasCollaboratorsNS = ET.QName(NS_ROUD, "hasCollaborators")
    publicationHasDateNS = ET.QName(NS_ROUD, "publicationHasDate")
    publicationHasInternalCommentNS = ET.QName(NS_ROUD, "publicationHasInternalComment")
    publicationIsTranscribedNS = ET.QName(NS_ROUD, "publicationIsTranscribed")
    originalIsInCrlrArchiveNS = ET.QName(NS_ROUD, "originalIsInCrlrArchive")
    
    
    ###################################
    ## CREATE ELEMENTS AND ATTRIBUTES (AS PREVIOUSLY DEFINED WITH NS) AND ASSIGN THEM CONTENT
    ###################################
    
    Book = ET.Element(BookNS, attrib={'id':Publicationid}) 
    
    label = ET.SubElement(Book, labelNS)
    label.text = BookLabel
    
    ## -----------------------------> bookHasSpecificPages
    if (BookHasSpecificPages!= ''):
        bookHasSpecificPages = ET.SubElement(Book, bookHasSpecificPagesNS, attrib={'knoraType':'richtext_value'})
        bookHasSpecificPages.text = BookHasSpecificPages
    
    
    ## -----------------------------> hasCollaborators
    if (HasCollaborators != ''):
        hasCollaborators = ET.SubElement(Book, hasCollaboratorsNS, attrib={'knoraType':'richtext_value'})
        hasCollaborators.text = HasCollaborators
    
    
    ## -----------------------------> hasPublicationType
    hasPublicationType = ET.SubElement(Book, hasPublicationTypeNS, attrib={'knoraType':'hlist_value'})
    hasPublicationType.text = HasPublicationType  ## use variable defined with name of the publisher corresponding to second row
    
    
    ## -----------------------------> hasPublisher
    if (publisherName != ''):
        hasPublisher = ET.SubElement(Book, hasPublisherNS)
        Publisher = ET.SubElement(hasPublisher, PublisherNS, attrib={'knoraType':'link_value', 'linkType':'ref', 'target':PublisherTarget})
    
    
    
    ## -----------------------------> OriginalIsInCrlrArchive
    if (OriginalIsInCrlrArchive != ''):
        originalIsInCrlrArchive = ET.SubElement(Book, originalIsInCrlrArchiveNS, attrib={'knoraType':'richtext_value'})
        originalIsInCrlrArchive.text = OriginalIsInCrlrArchive
        
    
    ## -----------------------------> publicationHasAuthor
    if (',') in ArticleAuthor:
        publicationHasAuthor = ET.SubElement(Book, publicationHasAuthorNS)
        Author = ET.SubElement(publicationHasAuthor, AuthorNS, attrib={'knoraType':'link_value', 'linkType':'ref', 'target':AuthorTarget})
        publicationHasAuthor = ET.SubElement(Book, publicationHasAuthorNS)
        Author = ET.SubElement(publicationHasAuthor, AuthorNS, attrib={'knoraType':'link_value', 'linkType':'ref', 'target':AuthorTargetSecond})
    else:
        publicationHasAuthor = ET.SubElement(Book, publicationHasAuthorNS)
        Author = ET.SubElement(publicationHasAuthor, AuthorNS, attrib={'knoraType':'link_value', 'linkType':'ref', 'target':AuthorTargetSingle})
    
    
    
    ## -----------------------------> publicationHasDate
    if (Date != ''):
        publicationHasDate = ET.SubElement(Book, publicationHasDateNS, attrib={'knoraType':'date_value'})
    
    if ('(' in Date):
        if len(Date1) > 7:
            if len(Date2) > 3:   
                publicationHasDate.text = PeriodMD
            else:
                publicationHasDate.text = PeriodD
        else:
            publicationHasDate.text = PeriodM
    else:
        if (pattern.match(Date)):
            publicationHasDate.text = PeriodY
        else:
            if (Date != ''):
                publicationHasDate.text = PublicationHasDate
    
    
    ## -----------------------------> publicationHasInternalComment
    if (PublicationHasInternalComment != ''):
        publicationHasInternalComment = ET.SubElement(Book, publicationHasInternalCommentNS, attrib={'knoraType':'richtext_value'})
        publicationHasInternalComment.text = PublicationHasInternalComment
        
    
    ## -----------------------------> publicationHasTitle
    publicationHasTitle = ET.SubElement(Book, publicationHasTitleNS, attrib={'knoraType':'richtext_value'})
    publicationHasTitle.text = PublicationHasTitle
    
    
     ## -----------------------------> publicationIsTranscribed
    if (PublicationIsTranscribed != ''):
        publicationIsTranscribed = ET.SubElement(Book, publicationIsTranscribedNS, attrib={'knoraType':'richtext_value'})
        publicationIsTranscribed.text = PublicationIsTranscribed
        
        
    
    
    tree = ET.tostring(Book, encoding="unicode")
    o.write('\n''\n'+ tree)

## WRITE END OF THE XML FILE
with o:  ## this is to append the text, if just write o.write does not work here (why??)
    o.write('\n'+'</knoraXmlImport:resources>')

o.close


# In[ ]:


###
### CREATE XML FROM CSV (BOOK SECTION)
###



from xml.etree import ElementTree as ET
import csv, re

f = open('../INPUT_data/booksections.csv')
o = open('../OUTPUT_xml/booksections.xml', 'w')

csv_f = csv.reader(f)   
data = []

for row in csv_f: 
   data.append(row)
f.close()


## SI [0] id, [1] type, [2] author, [3] title, [4] title_pub, [6] collaborateurs, [7] volume, [8] placepub, [9] namepub, 
## SI [10] date, [11] pages, [12] comm interne, [13] Retranscrit, [15] digitized, [16] dans fonds CRLR  ##
## NO [5] illustré par, [14] website interest  ##



###################################
## WRITE DECLARATIONS AND BEGINNING OF THE XML FILE -adding more line breaks for readibility '+'\n'+' ???-
###################################
o.write('<?xml version="1.0" encoding="UTF-8"?>'+'\n'+'<knoraXmlImport:resources xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://api.knora.org/ontology/knoraXmlImport/v1# ../p0112-roud-oeuvres-xml-schemas/p0112-roud-oeuvres.xsd" xmlns="http://api.knora.org/ontology/0112/roud-oeuvres/xml-import/v1#" xmlns:knoraXmlImport="http://api.knora.org/ontology/knoraXmlImport/v1#" xmlns:p0112-roud-oeuvres="http://api.knora.org/ontology/0112/roud-oeuvres/xml-import/v1#">'+'\n')



biblio_number_new = 3000  ## starting point for counting biblioid that should be added because are not in the original
    

###################################
## PREPARE CONTENT OF ELEMENTS AND ATTRIBUTES
###################################
for row in data[0:]:
    
    
    
    
    ## -----------------------> @id
    biblio_number_new += 1    
    if (row[0] != ''):
        Publicationid = 'biblio_'+row[0] ## @id
    else:
        Publicationid = 'biblio_'+str(biblio_number_new)   ## increasing number, just to give it an id. Starts from 1000
    
      
        
        
    
    ## -----------------------> hasPublicationType
    if ('Œuvre poétique' in row[1]):
        HasPublicationType = 'http://rdfh.ch/lists/0112/roud-oeuvres-flatlist-hasPublicationType-oeuvrePoetique'
    if ('Périodique' in row[1]):
        HasPublicationType = 'http://rdfh.ch/lists/0112/roud-oeuvres-flatlist-hasPublicationType-propos'
    ##if ('À propos de Roud' in row[1]):
      ##  HasPublicationType = 'http://rdfh.ch/lists/0112/roud-oeuvres-flatlist-hasPublicationType-journal'
    if ('Traduction' in row[1]):
        HasPublicationType = 'http://rdfh.ch/lists/0112/roud-oeuvres-flatlist-hasPublicationType-traduction'
    if ('Photographie' in row[1]):
        HasPublicationType = 'http://rdfh.ch/lists/0112/roud-oeuvres-flatlist-hasPublicationType-photo'
    if ('Correspondance' in row[1]):
        HasPublicationType = 'http://rdfh.ch/lists/0112/roud-oeuvres-flatlist-hasPublicationType-correspondance'
    if ('À propos de Roud' in row[1]):
        HasPublicationType = 'http://rdfh.ch/lists/0112/roud-oeuvres-flatlist-hasPublicationType-surRoud'
    
    
    ## -----------------------> publicationHasTitle
    PublicationHasTitle = row[3]  
    
    
    ## -----------------------> bookSectionIsPartOf
    BookSectionIsPartOf = row[4]  
    
    
    ## -----------------------> publicationHasCollaborators
    HasCollaborators = row[6]  
    
    ## -----------------------> isInBookVolume
    IsInBookVolume = row[7]  
    
    
    ## -----------------------> hasPublisher (PublisherTarget)
    publisherName = row[9]
    word_list = publisherName.replace("'", ' ') ## replace accent with space
    word_list = word_list.replace(",", '').split()  ## replace comma with nothing and split words
    PublisherTarget = '_'.join(word_list)
    
    
    ## -----------------------> publicationHasDate   
    Date = row[10]
    pattern = re.compile("\d\d\d\d-\d\d\d\d")
    if ('(' in Date):
        Datedmy_split = re.split('-', Date)  ## split in day, month, year
        Date1y = Datedmy_split[0]
        Date1m = Datedmy_split[1]
        Date12_split = re.split('\(', Date)  ## split in date1 and date2
        Date1 = Date12_split[0]
        Date2 = Date12_split[1].replace('(', '').replace(')', '')
        if len(Date1) > 7:             ## period includes year and month and days
            if len(Date2) > 3:         ## period includes year and month and days (month and days are different)
                PeriodMD = 'GREGORIAN:'+Date1+' CE:'+Date1y+Date2+' CE'  
            else:                      ## period includes year and month and days (only days are different)     
                PeriodD = 'GREGORIAN:'+Date1+' CE:'+Date1y+'-'+Date1m+Date2+' CE'  
        else:                          ## period includes year and month
            PeriodM = 'GREGORIAN:'+Date1+' CE:'+Date1y+Date2+' CE'
    else:
        if (pattern.match(Date)):
            DateY_split = re.split('-', Date)
            DateY1 = DateY_split[0]
            DateY2 = DateY_split[1]
            PeriodY = 'GREGORIAN:'+DateY1+' CE:'+DateY2+' CE'
        else:
            PublicationHasDate = 'GREGORIAN:'+Date+' CE'
    
    
    ## -----------------------> bookSectionIsInPages
    BookSectionIsInPages = row[11]  
    
    
    ## -----------------------> publicationHasInternalComment
    PublicationHasInternalComment = row[12]
    
    
    ## -----------------------> PublicationIsTranscribed
    PublicationIsTranscribed = row[13]
    
    
    ## -----------------------> PublicationIsTranscribed
    OriginalIsInCrlrArchive = row[16]
  
    
    ## -----------------------> publicationHasAuthor
    ArticleAuthor = row[2]
    if (',' in ArticleAuthor):
        ArticleAuthor_split = re.split(', ', ArticleAuthor)
        if (' ' in ArticleAuthor_split[0]):
            ArticlesSurname = ArticleAuthor_split[0].partition(' ')[0]
            ArticlesName = ArticleAuthor_split[0].partition(' ')[2]
            ArticlesSurnameSecond = ArticleAuthor_split[1].partition(' ')[0]
            ArticlesNameSecond = ArticleAuthor_split[1].partition(' ')[2]
            with open("../INPUT_data/authors_with_id.csv", 'r') as authors_with_id:   
                csv_authors = csv.reader(authors_with_id)
                ## AuthorTarget = [row[2] for row in csv_authors if ArticlesSurname in row[0]]  this creates list, while I want item
                for row in csv_authors:
                    if (ArticlesSurname == row[0] and ArticlesName == row[1]):
                        AuthorTarget = row[2]
                    if (ArticlesSurnameSecond == row[0] and ArticlesNameSecond == row[1]):
                        AuthorTargetSecond = row[2]
        else:
            ArticlesSurname = ArticleAuthor_split[0]
            ArticlesSurnameSecond = ArticleAuthor_split[1].partition(' ')[0]
            ArticlesNameSecond = ArticleAuthor_split[1].partition(' ')[2]
            with open("../INPUT_data/authors_with_id.csv", 'r') as authors_with_id:   
                csv_authors = csv.reader(authors_with_id)
                ## AuthorTarget = [row[2] for row in csv_authors if ArticlesSurname in row[0]]  this creates list, while I want item
                for row in csv_authors:
                    if (ArticlesSurname == row[0]):
                        AuthorTarget = row[2]
                    if (ArticlesSurnameSecond == row[0] and ArticlesNameSecond == row[1]):
                        AuthorTargetSecond = row[2]
    else:
        if (' ' in ArticleAuthor):
            ArticlesSurname = ArticleAuthor.partition(' ')[0]
            ArticlesName = ArticleAuthor.partition(' ')[2]
            with open("../INPUT_data/authors_with_id.csv", 'r') as authors_with_id:   
                csv_authors = csv.reader(authors_with_id)
                ## AuthorTarget = [row[2] for row in csv_authors if ArticlesSurname in row[0]]  this creates list, while I want item
                for row in csv_authors:
                    if (ArticlesSurname == row[0] and ArticlesName == row[1]):
                        AuthorTargetSingle = row[2]
        else:
            ArticlesSurname = ArticleAuthor
            with open("../INPUT_data/authors_with_id.csv", 'r') as authors_with_id:   
                csv_authors = csv.reader(authors_with_id)
                ## AuthorTarget = [row[2] for row in csv_authors if ArticlesSurname in row[0]]  this creates list, while I want item
                for row in csv_authors:
                    if (ArticlesSurname == row[0]):
                        AuthorTargetSingle = row[2]  
                        
                    
    ## -----------------------> label
    if (ArticleAuthor != '' and PublicationHasTitle != '' and BookSectionIsPartOf != '' and Date != ''):
        BookSectionLabelComplete = "pub_"+ArticleAuthor+' ___ '+PublicationHasTitle+' ___ '+BookSectionIsPartOf+' ___ '+Date
    else:
        if (ArticleAuthor != '' and PublicationHasTitle != '' and PeriodicalTarget != ''):
            BookSectionLabelComplete = "pub_"+ArticleAuthor+' ___ '+PublicationHasTitle+' ___ '+BookSectionIsPartOf
        else:
            if (ArticleAuthor != '' and PublicationHasTitle != '' and Date != ''):
                BookSectionLabelComplete = "pub_"+ArticleAuthor+' ___ '+PublicationHasTitle+' ___ '+Date
            else:
                if (ArticleAuthor != '' and PeriodicalTarget != '' and Date != ''):
                    BookSectionLabelComplete = "pub_"+ArticleAuthor+' ___ '+BookSectionIsPartOf+' ___ '+Date
                else:
                    if (PublicationHasTitle != '' and PeriodicalTarget != '' and Date != ''):
                        BookSectionLabelComplete = "pub_"+PublicationHasTitle+' ___ '+BookSectionIsPartOf+' ___ '+Date

    BookSectionLabel = re.sub(r"\(([^\)]+)\)", "", BookSectionLabelComplete)

    
                
                
    
    ###################################
    #### REGISTERING NAMESPACES
    ###################################
    NS_ROUD = "http://api.knora.org/ontology/0112/roud-oeuvres/xml-import/v1#" 
    NS_KNORAIMPORT = "http://api.knora.org/ontology/knoraXmlImport/v1#"
    ET.register_namespace("p0112-roud-oeuvres", NS_ROUD)
    ET.register_namespace("knoraXmlImport", NS_KNORAIMPORT)

    
    ###################################
    ## DEFINE ELEMENTS WITH NS
    ###################################
    BookSectionNS = ET.QName(NS_ROUD, "BookSection")
    labelNS = ET.QName(NS_KNORAIMPORT, "label")
    bookSectionIsInPagesNS = ET.QName(NS_ROUD, "bookSectionIsInPages")
    bookSectionIsPartOfNS = ET.QName(NS_ROUD, "bookSectionIsPartOf")
    hasPublicationTypeNS = ET.QName(NS_ROUD, "hasPublicationType")
    isInBookVolumeNS = ET.QName(NS_ROUD, "isInBookVolume")
    bookSectionHasPublisherNS = ET.QName(NS_ROUD, "bookSectionHasPublisher")
    PublisherNS = ET.QName(NS_ROUD, "Publisher")
    publicationHasAuthorNS = ET.QName(NS_ROUD, "publicationHasAuthor")
    AuthorNS = ET.QName(NS_ROUD, "Author")
    publicationHasTitleNS = ET.QName(NS_ROUD, "publicationHasTitle")
    hasCollaboratorsNS = ET.QName(NS_ROUD, "hasCollaborators")
    publicationHasDateNS = ET.QName(NS_ROUD, "publicationHasDate")
    publicationHasInternalCommentNS = ET.QName(NS_ROUD, "publicationHasInternalComment")
    publicationIsTranscribedNS = ET.QName(NS_ROUD, "publicationIsTranscribed")
    originalIsInCrlrArchiveNS = ET.QName(NS_ROUD, "originalIsInCrlrArchive")
    
    
    ###################################
    ## CREATE ELEMENTS AND ATTRIBUTES (AS PREVIOUSLY DEFINED WITH NS) AND ASSIGN THEM CONTENT
    ###################################
    
    BookSection = ET.Element(BookSectionNS, attrib={'id':Publicationid}) 
    
    label = ET.SubElement(BookSection, labelNS)
    label.text = BookSectionLabel
    
    ## -----------------------------> bookSectionHasPublisher
    if (publisherName != ''):
        bookSectionHasPublisher = ET.SubElement(BookSection, bookSectionHasPublisherNS)
        Publisher = ET.SubElement(bookSectionHasPublisher, PublisherNS, attrib={'knoraType':'link_value', 'linkType':'ref', 'target':PublisherTarget})
    
    
    ## -----------------------------> bookSectionIsInPages
    if (BookSectionIsInPages!= ''):
        bookSectionIsInPages = ET.SubElement(BookSection, bookSectionIsInPagesNS, attrib={'knoraType':'richtext_value'})
        bookSectionIsInPages.text = BookSectionIsInPages
        
    
        
    ## -----------------------------> BookSectionIsPartOf
    if (BookSectionIsPartOf!= ''):
        bookSectionIsPartOf = ET.SubElement(BookSection, bookSectionIsPartOfNS, attrib={'knoraType':'richtext_value'})
        bookSectionIsPartOf.text = BookSectionIsPartOf
    
    
    ## -----------------------------> hasCollaborators
    if (HasCollaborators != ''):
        hasCollaborators = ET.SubElement(BookSection, hasCollaboratorsNS, attrib={'knoraType':'richtext_value'})
        hasCollaborators.text = HasCollaborators
    
    
    ## -----------------------------> hasPublicationType
    hasPublicationType = ET.SubElement(BookSection, hasPublicationTypeNS, attrib={'knoraType':'hlist_value'})
    hasPublicationType.text = HasPublicationType  ## use variable defined with name of the publisher corresponding to second row
    
    
    ## -----------------------------> isInBookVolume
    if (IsInBookVolume != ''):
        isInBookVolume = ET.SubElement(BookSection, isInBookVolumeNS, attrib={'knoraType':'richtext_value'})
        isInBookVolume.text = IsInBookVolume
    
    
    ## -----------------------------> OriginalIsInCrlrArchive
    if (OriginalIsInCrlrArchive != ''):
        originalIsInCrlrArchive = ET.SubElement(BookSection, originalIsInCrlrArchiveNS, attrib={'knoraType':'richtext_value'})
        originalIsInCrlrArchive.text = OriginalIsInCrlrArchive
        
    
    ## -----------------------------> publicationHasAuthor
    if (',') in ArticleAuthor:
        publicationHasAuthor = ET.SubElement(BookSection, publicationHasAuthorNS)
        Author = ET.SubElement(publicationHasAuthor, AuthorNS, attrib={'knoraType':'link_value', 'linkType':'ref', 'target':AuthorTarget})
        publicationHasAuthor = ET.SubElement(BookSection, publicationHasAuthorNS)
        Author = ET.SubElement(publicationHasAuthor, AuthorNS, attrib={'knoraType':'link_value', 'linkType':'ref', 'target':AuthorTargetSecond})
    else:
        publicationHasAuthor = ET.SubElement(BookSection, publicationHasAuthorNS)
        Author = ET.SubElement(publicationHasAuthor, AuthorNS, attrib={'knoraType':'link_value', 'linkType':'ref', 'target':AuthorTargetSingle})
    
    
    
    ## -----------------------------> publicationHasDate
    if (Date != ''):
        publicationHasDate = ET.SubElement(BookSection, publicationHasDateNS, attrib={'knoraType':'date_value'})
    
    if ('(' in Date):
        if len(Date1) > 7:
            if len(Date2) > 3:   
                publicationHasDate.text = PeriodMD
            else:
                publicationHasDate.text = PeriodD
        else:
            publicationHasDate.text = PeriodM
    else:
        if (pattern.match(Date)):
            publicationHasDate.text = PeriodY
        else:
            if (Date != ''):
                publicationHasDate.text = PublicationHasDate
    
    
    ## -----------------------------> publicationHasInternalComment
    if (PublicationHasInternalComment != ''):
        publicationHasInternalComment = ET.SubElement(BookSection, publicationHasInternalCommentNS, attrib={'knoraType':'richtext_value'})
        publicationHasInternalComment.text = PublicationHasInternalComment
        
    
    ## -----------------------------> publicationHasTitle
    publicationHasTitle = ET.SubElement(BookSection, publicationHasTitleNS, attrib={'knoraType':'richtext_value'})
    publicationHasTitle.text = PublicationHasTitle
    
    
     ## -----------------------------> publicationIsTranscribed
    if (PublicationIsTranscribed != ''):
        publicationIsTranscribed = ET.SubElement(BookSection, publicationIsTranscribedNS, attrib={'knoraType':'richtext_value'})
        publicationIsTranscribed.text = PublicationIsTranscribed
        
        
    
    
    tree = ET.tostring(BookSection, encoding="unicode")
    o.write('\n''\n'+ tree)

## WRITE END OF THE XML FILE
with o:  ## this is to append the text, if just write o.write does not work here (why??)
    o.write('\n'+'</knoraXmlImport:resources>')

o.close


# In[ ]:


###
### BROWSE AN XML DOCUMENT (TO BE USED BELOW FOR CREATING FICHES AND REFERRING TO THE BIBLIOGRAPHY)
###

from xml.etree import ElementTree as ET


tree_bibliodata = ET.parse('../INPUT_data/bibliography_id_correspondance.xml')
root = tree_bibliodata.getroot()
for publication in root:
    publication_id = publication.get('id')
    print(publication_id)
    namespaces = {'p0112-roud-oeuvres': 'http://api.knora.org/ontology/0112/roud-oeuvres/xml-import/v1#'} 
    ### TITLE
    publicationHasTitle = publication.findall('./p0112-roud-oeuvres:publicationHasTitle', namespaces)[0].text
    #if len(publicationHasTitle.split()) > 10:  ### it title is too long, take only first 10 words
         # do something
    if (publication.tag == "{http://api.knora.org/ontology/0112/roud-oeuvres/xml-import/v1#}PeriodicalArticle" or publication.tag == "{http://api.knora.org/ontology/0112/roud-oeuvres/xml-import/v1#}BookSection"):
        title = "« "+publicationHasTitle+" »"
    else:
        title = "<i>"+publicationHasTitle+"</i>"
    ### AUTHOR    
    publicationHasAuthor = publication.find('./p0112-roud-oeuvres:publicationHasAuthor', namespaces)
    ### DATE
    publicationHasDate = publication.find('./p0112-roud-oeuvres:publicationHasDate', namespaces)
    ### BIBLIO = AUTHOR + TITLE + DATE
    if (publicationHasAuthor is None):
        if (publicationHasDate is None):
            biblio = title
        else:
            date = publication.findall('./p0112-roud-oeuvres:publicationHasDate', namespaces)[0].text.split("GREGORIAN:")[1].split("-")[0].split(" CE")[0]
            biblio = title+", "+date
    else:
        author = publication.findall('./p0112-roud-oeuvres:publicationHasAuthor', namespaces)[0].findall('./p0112-roud-oeuvres:Author', namespaces)[0].get('target').split("_")[0]
        if (publicationHasDate is None):
            biblio = author+", "+title
        else:
            date = publication.findall('./p0112-roud-oeuvres:publicationHasDate', namespaces)[0].text.split("GREGORIAN:")[1].split("-")[0].split(" CE")[0]
            biblio = author+", "+title+", "+date
    print(biblio)


# In[ ]:


test = '<p>Version interm&eacute;diaire entre [Biblio 207] et [Biblio 282].</p><p>Dat&eacute; &agrave; la main: Novembre 35-novembre 41. novembre 49.</p><p>Repris dans [Biblio 517].</p>'
findBiblioNumber = re.compile(r'\[Biblio (\d+)\]')
for biblioOccur in re.finditer(findBiblioNumber, test):
    biblioNumber = biblioOccur.group(1)
    print(biblioNumber)


# In[ ]:


###
### CREATE XML FROM CSV (FICHES)
###



from xml.etree import ElementTree as ET
import csv, re
from datetime import datetime

f = open('../INPUT_data/fiches.csv')   ## should not be manipulated, because when changing the content of certain cells go to the next cell and the entire row is erroneous
o = open('../OUTPUT_xml/fiches.xml', 'w')

csv_f = csv.reader(f, delimiter='$', quotechar="§")   
data = []

for row in csv_f: 
   data.append(row)
f.close()

#print(data[10:11])


## [0] id, [1] titre, [2] archive_id, [3] oldcote, [4] cote, [5] ensemble_id, [6] type_id, [7] annotation, [8] support_id, 
## [9] support_info, [10] instrument_id, [11] color_id, [12] other_tool, [13] statut_id, [14] dates, [15] datation, 
## [16] datationlist_id, [17] datationcomment, [18] publie, [19] biblio_id, [20] auteurtraduit_id, [21]alreadydigitized, 
## [22] numerise_info, [23] commentaire, [24] photocopy, [25] resp_id


###################################
## WRITE DECLARATIONS AND BEGINNING OF THE XML FILE -adding more line breaks for readibility '+'\n'+' ???-
###################################
o.write('<?xml version="1.0" encoding="UTF-8"?>'+'\n'+'<knoraXmlImport:resources xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://api.knora.org/ontology/knoraXmlImport/v1# ../p0112-roud-oeuvres-xml-schemas/p0112-roud-oeuvres.xsd" xmlns="http://api.knora.org/ontology/0112/roud-oeuvres/xml-import/v1#" xmlns:knoraXmlImport="http://api.knora.org/ontology/knoraXmlImport/v1#" xmlns:p0112-roud-oeuvres="http://api.knora.org/ontology/0112/roud-oeuvres/xml-import/v1#">'+'\n')


    
###################################
#### REGISTERING NAMESPACES
###################################
NS_ROUD = "http://api.knora.org/ontology/0112/roud-oeuvres/xml-import/v1#" 
NS_KNORAIMPORT = "http://api.knora.org/ontology/knoraXmlImport/v1#"
ET.register_namespace("p0112-roud-oeuvres", NS_ROUD)
ET.register_namespace("knoraXmlImport", NS_KNORAIMPORT)


###################################
## DEFINE ELEMENTS WITH NS
###################################
ManuscriptNS = ET.QName(NS_ROUD, "Manuscript")
labelNS = ET.QName(NS_KNORAIMPORT, "label")
hasAnnotationNS = ET.QName(NS_ROUD, "hasAnnotation")
hasDocumentTypeNS = ET.QName(NS_ROUD, "hasDocumentType")
hasGeneticStageNS = ET.QName(NS_ROUD, "hasGeneticStage")
hasOtherWritingToolNS = ET.QName(NS_ROUD, "hasOtherWritingTool")
hasPublicCommentNS = ET.QName(NS_ROUD, "hasPublicComment")
hasSupportInfoNS = ET.QName(NS_ROUD, "hasSupportInfo")
hasSupportTypeNS = ET.QName(NS_ROUD, "hasSupportType")
hasTranslatedAuthorNS = ET.QName(NS_ROUD, "hasTranslatedAuthor")
AuthorNS = ET.QName(NS_ROUD, "Author")
hasWritingColorNS = ET.QName(NS_ROUD, "hasWritingColor")
hasWritingToolNS = ET.QName(NS_ROUD, "hasWritingTool")
isPhotocopyNS = ET.QName(NS_ROUD, "isPhotocopy")
manuscriptHasDateReadableNS = ET.QName(NS_ROUD, "manuscriptHasDateReadable")
manuscriptHasDateComputableNS = ET.QName(NS_ROUD, "manuscriptHasDateComputable")
manuscriptHasDateEstablishedComputableNS = ET.QName(NS_ROUD, "manuscriptHasDateEstablishedComputable")
manuscriptHasDateEstablishedListNS = ET.QName(NS_ROUD, "manuscriptHasDateEstablishedList")
manuscriptHasDateEstablishedReadableNS = ET.QName(NS_ROUD, "manuscriptHasDateEstablishedReadable")
manuscriptHasEditorialSetNS = ET.QName(NS_ROUD, "manuscriptHasEditorialSet")
manuscriptHasInternalCommentNS = ET.QName(NS_ROUD, "manuscriptHasInternalComment")
manuscriptHasOldShelfmarkNS = ET.QName(NS_ROUD, "manuscriptHasOldShelfmark")
manuscriptHasPublishedReferenceNS = ET.QName(NS_ROUD, "manuscriptHasPublishedReference")
PublicationNS = ET.QName(NS_ROUD, "Publication")
manuscriptHasShelfmarkNS = ET.QName(NS_ROUD, "manuscriptHasShelfmark")
manuscriptHasTitleNS = ET.QName(NS_ROUD, "manuscriptHasTitle")
manuscriptIsDigitizedNS = ET.QName(NS_ROUD, "manuscriptIsDigitized")
manuscriptIsInArchiveNS = ET.QName(NS_ROUD, "manuscriptIsInArchive")





###################################
## PREPARE CONTENT OF ELEMENTS AND ATTRIBUTES
###################################


## to avoid undefined entities when parsing the XML present is certain cells of the CSV
## "https://dev.w3.org/html5/html-author/charref"
entities_declaration = '''  <!DOCTYPE HTML PUBLIC "-//W3C//ENTITIES //EN//HTML" 
                            "https://www.w3.org/TR/html4/sgml/entities.html"
                            [   <!ENTITY agrave 'à'>
                                <!ENTITY egrave 'è'>
                                <!ENTITY igrave 'ì'>
                                <!ENTITY ograve 'ò'>
                                <!ENTITY ugrave 'ù'>
                                <!ENTITY Agrave 'À'>
                                <!ENTITY Egrave 'È'>
                                <!ENTITY Igrave 'Ì'>
                                <!ENTITY Ograve 'Ò'>
                                <!ENTITY Ugrave 'Ù'>
                                <!ENTITY eacute 'é'>
                                <!ENTITY Eacute 'É'>
                                <!ENTITY acirc 'â'>
                                <!ENTITY ecirc 'ê'>
                                <!ENTITY icirc 'î'>
                                <!ENTITY ocirc 'ô'>
                                <!ENTITY ucirc 'û'>
                                <!ENTITY Acirc 'Â'>
                                <!ENTITY Ecirc 'Ê'>
                                <!ENTITY Icirc 'Î'>
                                <!ENTITY Ocirc 'Ô'>
                                <!ENTITY Ucirc 'Û'>
                                <!ENTITY auml 'ä'>
                                <!ENTITY euml 'ë'>
                                <!ENTITY iuml 'ï'>
                                <!ENTITY ouml 'ö'>
                                <!ENTITY uuml 'ü'>
                                <!ENTITY yuml 'ÿ'>
                                <!ENTITY Auml 'Ä'>
                                <!ENTITY Euml 'Ë'>
                                <!ENTITY Iuml 'Ï'>
                                <!ENTITY Ouml 'Ö'>
                                <!ENTITY Uuml 'Ü'>
                                <!ENTITY ccedil 'ç'>
                                <!ENTITY Ccedil 'Ç'>
                                <!ENTITY oelig 'œ'>
                                <!ENTITY OElig 'Œ'>
                                <!ENTITY szlig '&#223;'>
                                
                                <!ENTITY rsquo "'">  <!-- as if it was &apos; --> 
                                <!ENTITY lsquo "'">  <!-- as if it was &apos; -->
                                
                                <!ENTITY laquo '«'>
                                <!ENTITY raquo '»'>
                                <!ENTITY hellip '…'>
                                <!ENTITY nbsp ' '>
                                <!ENTITY ndash '&#8211;'>
                                <!ENTITY deg '&#176;'>
                                
                                <!ENTITY Alpha '&#913;'>
                                <!ENTITY Delta '&#916;'>
                                <!ENTITY Tau '&#932;'>
                                <!ENTITY Epsilon '&#917;'>
                                <!ENTITY alpha '&#945;'>
                                <!ENTITY beta '&#946;'>
                                <!ENTITY pi '&#928;'>
                                <!ENTITY omicron '&#959;'>
                                <!ENTITY lambda '&#955;'>
                                <!ENTITY nu '&#957;'>
                                <!ENTITY gamma '&#947;'>
                                <!ENTITY upsilon '&#965;'>
                                <!ENTITY iota '&#953;'>
                                <!ENTITY tau '&#964;'>
                                <!ENTITY omega '&#969;'>
                                <!ENTITY epsilon '&#949;'>
                                <!ENTITY mu '&#956;'>
                                <!ENTITY sigmaf '&#962;'>
                                <!ENTITY eta '&#951;'>
                                <!ENTITY chi '&#967;'>
                                <!ENTITY rho '&#961;'>
                                <!ENTITY kappa '&#954;'> ]>  '''


for row in data[0:]:
    
    
    ## -----------------------> @id 
    ficheid = 'fiche'+row[0] 
    
    
    ## -----------------------> hasAnnotation
    if (row[7] == 'oui'):
        hasAnnotation_content = 'true'
    else:
        hasAnnotation_content = 'false'    
    
    
    ## -----------------------> hasDocumentType
    documentType = row[6]
    if (documentType == '1'):
        hasDocumentType_content = 'http://rdfh.ch/lists/0112/roud-oeuvres-flatlist-hasDocumentType-manuscript'
    if (documentType == '2'):
        hasDocumentType_content = 'http://rdfh.ch/lists/0112/roud-oeuvres-flatlist-hasDocumentType-dactylo'
    if (documentType == '3'):
        hasDocumentType_content = 'http://rdfh.ch/lists/0112/roud-oeuvres-flatlist-hasDocumentType-imprime'
    
    
    ## -----------------------> hasGeneticStage
    geneticStage = row[13]
    if (geneticStage == '1'):
        hasGeneticStage_content = 'http://rdfh.ch/lists/0112/roud-oeuvres-flatlist-hasGeneticStage-note'
    if (geneticStage == '2'):
        hasGeneticStage_content = 'http://rdfh.ch/lists/0112/roud-oeuvres-flatlist-hasGeneticStage-plan'
    if (geneticStage == '3'):
        hasGeneticStage_content = 'http://rdfh.ch/lists/0112/roud-oeuvres-flatlist-hasGeneticStage-brouillon'
    if (geneticStage == '4'):
        hasGeneticStage_content = 'http://rdfh.ch/lists/0112/roud-oeuvres-flatlist-hasGeneticStage-miseAuNet'
    if (geneticStage == '5'):
        hasGeneticStage_content = 'http://rdfh.ch/lists/0112/roud-oeuvres-flatlist-hasGeneticStage-manuscritDefinitif'
    if (geneticStage == '6'):
        hasGeneticStage_content = 'http://rdfh.ch/lists/0112/roud-oeuvres-flatlist-hasGeneticStage-epreuvesCorriges'
    if (geneticStage == '7'):
        hasGeneticStage_content = 'http://rdfh.ch/lists/0112/roud-oeuvres-flatlist-hasGeneticStage-originalCorrige'
    if (geneticStage == '8'):
        hasGeneticStage_content = 'http://rdfh.ch/lists/0112/roud-oeuvres-flatlist-hasGeneticStage-verifier'
    if (geneticStage == '10'):
        hasGeneticStage_content = 'http://rdfh.ch/lists/0112/roud-oeuvres-flatlist-hasGeneticStage-liste'
    if (geneticStage == '12'):
        hasGeneticStage_content = ''
     
    
    ## -----------------------> hasOtherWritingTool
    otherWritingTool = row[12]
    if (otherWritingTool != ''):
        ## attach <text> to the xml in the cell, so it has a wrapping element and the function 'fromstring' works
        hasOtherWritingTool_content = '<text xmlns="">'+otherWritingTool+'</text>'
        
        
    ## -----------------------> hasPublicComment
    publicComment = row[23]
    if (publicComment != ''):
        if ("[Biblio" in publicComment):
            # add link
            refbiblio = re.compile(r'\[(Biblio (\d+))\]')
            publicComment_link = re.sub(refbiblio, r'<a class="salsah-link" href="'+"ref:"+r'\1">[\1]</a>', publicComment)
            publicComment_linkref = re.sub('ref:Biblio ','ref:biblio_',publicComment_link)
            
            # isolate biblio_id in the comment 
            for biblio_number in re.finditer(refbiblio,publicComment_linkref):
                biblio_number = biblio_number.group(2)
                biblio_id = 'biblio_'+biblio_number
                
                # find corresponding biblio_id in bibliography xml file and build correspoding bibliographic reference
                tree_bibliodata = ET.parse('../INPUT_data/bibliography_id_correspondance.xml')
                root = tree_bibliodata.getroot()
                for publication in root:
                    publication_id = publication.attrib['id']
                    if (biblio_id == publication_id):
                        namespaces = {'p0112-roud-oeuvres': 'http://api.knora.org/ontology/0112/roud-oeuvres/xml-import/v1#'} 
                        # TITLE
                        ref_publicationHasTitle = publication.findall('./p0112-roud-oeuvres:publicationHasTitle', namespaces)[0].text
                        #if len(publicationHasTitle.split()) > 10:  ### it title is too long, take only first 10 words
                             # do something
                        if (publication.tag == "{http://api.knora.org/ontology/0112/roud-oeuvres/xml-import/v1#}PeriodicalArticle" or publication.tag == "{http://api.knora.org/ontology/0112/roud-oeuvres/xml-import/v1#}BookSection"):
                            ref_title = "« "+ref_publicationHasTitle+" »"
                        else:
                            ref_title = "<i>"+ref_publicationHasTitle+"</i>"
                        # AUTHOR    
                        ref_publicationHasAuthor = publication.find('./p0112-roud-oeuvres:publicationHasAuthor', namespaces)
                        # DATE
                        ref_publicationHasDate = publication.find('./p0112-roud-oeuvres:publicationHasDate', namespaces)
                        # BIBLIO = AUTHOR + TITLE + DATE
                        if (ref_publicationHasAuthor is None):
                            if (ref_publicationHasDate is None):
                                ref_biblioInPublicComment = ref_title
                            else:
                                ref_date = publication.findall('./p0112-roud-oeuvres:publicationHasDate', namespaces)[0].text.split("GREGORIAN:")[1].split("-")[0].split(" CE")[0]
                                biblioInPublicComment = ref_title+", "+ref_date
                        else:
                            ref_author = publication.findall('./p0112-roud-oeuvres:publicationHasAuthor', namespaces)[0].findall('./p0112-roud-oeuvres:Author', namespaces)[0].get('target').split("_")[0]
                            if (ref_publicationHasDate is None):
                                biblioInPublicComment = ref_author+", "+ref_title
                            else:
                                ref_date = publication.findall('./p0112-roud-oeuvres:publicationHasDate', namespaces)[0].text.split("GREGORIAN:")[1].split("-")[0].split(" CE")[0]
                                biblioInPublicComment = ref_author+", "+ref_title+", "+ref_date
                # replace [Biblio number] with bibliographic reference
                biblioToBeReplaced = '\[Biblio '+biblio_number+'\]'
                publicComment_linkref = re.sub(biblioToBeReplaced,biblioInPublicComment,publicComment_linkref)
            
            hasPublicComment_content = '<text xmlns="">'+publicComment_linkref+'</text>'
        else:
            hasPublicComment_content = '<text xmlns="">'+publicComment+'</text>'
        
    ## -----------------------> hasSupportInfo
    supportInfo = row[9]
    if (supportInfo != ''):
        hasSupportInfo_content = '<text xmlns="">'+supportInfo+'</text>'
        
    ## -----------------------> hasSupportType
    supportType = row[8]
    if (supportType == '1'):
        hasSupportType_content = 'http://rdfh.ch/lists/0112/roud-oeuvres-flatlist-hasSupportType-feuillet'
    if (supportType == '2'):
        hasSupportType_content = 'http://rdfh.ch/lists/0112/roud-oeuvres-flatlist-hasSupportType-agenda'
    if (supportType == '3'):
        hasSupportType_content = 'http://rdfh.ch/lists/0112/roud-oeuvres-flatlist-hasSupportType-carnet'
    if (supportType == '4'):
        hasSupportType_content = 'http://rdfh.ch/lists/0112/roud-oeuvres-flatlist-hasSupportType-cahier'
    if (supportType == '5'):
        hasSupportType_content = 'http://rdfh.ch/lists/0112/roud-oeuvres-flatlist-hasSupportType-enveloppe'
    if (supportType == '6'):
        hasSupportType_content = 'http://rdfh.ch/lists/0112/roud-oeuvres-flatlist-hasSupportType-divers'
    if (supportType == '7'):
        hasSupportType_content = 'http://rdfh.ch/lists/0112/roud-oeuvres-flatlist-hasSupportType-imprimesReliesParRoud'
    if (supportType == '8'):
        hasSupportType_content = 'http://rdfh.ch/lists/0112/roud-oeuvres-flatlist-hasSupportType-blocNotes'
    if (supportType == '9'):
        hasSupportType_content = 'http://rdfh.ch/lists/0112/roud-oeuvres-flatlist-hasSupportType-imprime'
        
    
    ## -----------------------> hasTranslatedAuthor
    translatedAuthor = row[20]
    if (translatedAuthor == '1'):
        hasTranslatedAuthor_content = ''
    if (translatedAuthor == '2'):
        hasTranslatedAuthor_content = 'Hölderlin_Friedrich'
    if (translatedAuthor == '3'):
        hasTranslatedAuthor_content = 'Rilke_Rainer_Maria'
    if (translatedAuthor == '4'):
        hasTranslatedAuthor_content = 'Novalis'
    if (translatedAuthor == '5'):
        hasTranslatedAuthor_content = 'Trakl_Georg'
    if (translatedAuthor == '6'):
        hasTranslatedAuthor_content = 'Gudmundsson_Kristmann'
    if (translatedAuthor == '7'):
        hasTranslatedAuthor_content = 'Brentano_Clemens'
    if (translatedAuthor == '8'):
        hasTranslatedAuthor_content = 'Heym_Georg'
    if (translatedAuthor == '9'):
        hasTranslatedAuthor_content = 'Goethe_Johann_Wolfgang_von'
    if (translatedAuthor == '10'):
        hasTranslatedAuthor_content = 'Eichendorff_Joseph_von'
    if (translatedAuthor == '11'):
        hasTranslatedAuthor_content = 'Platen_August_von'
    if (translatedAuthor == '12'):
        hasTranslatedAuthor_content = 'Heine_Heinrich'
    if (translatedAuthor == '13'):
        hasTranslatedAuthor_content = 'Nietzsche_Friedrich'
    if (translatedAuthor == '14'):
        hasTranslatedAuthor_content = 'Hesse_Hermann'
    if (translatedAuthor == '15'):
        hasTranslatedAuthor_content = 'Werfel_Franz'
    if (translatedAuthor == '16'):
        hasTranslatedAuthor_content = 'Bergengruen_Werner'
    if (translatedAuthor == '17'):
        hasTranslatedAuthor_content = 'Dürer_Albrecht'
    if (translatedAuthor == '18'):
        hasTranslatedAuthor_content = 'Müller_Wilhelm'
    if (translatedAuthor == '19'):
        hasTranslatedAuthor_content = 'Lavater-Sloman_Mary'
    if (translatedAuthor == '20'):
        hasTranslatedAuthor_content = 'Leisinger_Hermann'
    if (translatedAuthor == '21'):
        hasTranslatedAuthor_content = 'DAnnunzio_Gabriele'
    if (translatedAuthor == '22'):
        hasTranslatedAuthor_content = 'Montale_Eugenio'
    if (translatedAuthor == '23'):
        hasTranslatedAuthor_content = 'Barilli_Bruno'
    if (translatedAuthor == '24'):
        hasTranslatedAuthor_content = 'Cardarelli_Vincenzo'
    if (translatedAuthor == '25'):
        hasTranslatedAuthor_content = 'Buonarroti_Michelangelo'
    if (translatedAuthor == '26'):
        hasTranslatedAuthor_content = 'Coccioli_Carlo'
    if (translatedAuthor == '28'):
        hasTranslatedAuthor_content = 'Lejeune_Robert'
    if (translatedAuthor == '29'):
        hasTranslatedAuthor_content = 'Gotthelf_Jeremias'
    if (translatedAuthor == '30'):
        hasTranslatedAuthor_content = 'Kleist_Heinrich_von'
    if (translatedAuthor == '31'):
        hasTranslatedAuthor_content = 'Oeschger_Johannes'
        
        
    
    ## -----------------------> hasWritingColor
    writingColor = row[11]
    if (writingColor == '1'):
        hasWritingColor_content = 'http://rdfh.ch/lists/0112/roud-oeuvres-flatlist-hasWritingColor-black'
    if (writingColor == '2'):
        hasWritingColor_content = 'http://rdfh.ch/lists/0112/roud-oeuvres-flatlist-hasWritingColor-red'
    if (writingColor == '3'):
        hasWritingColor_content = 'http://rdfh.ch/lists/0112/roud-oeuvres-flatlist-hasWritingColor-blue'
    if (writingColor == '4'):
        hasWritingColor_content = 'http://rdfh.ch/lists/0112/roud-oeuvres-flatlist-hasWritingColor-rose'
    if (writingColor == '5'):
        hasWritingColor_content = 'http://rdfh.ch/lists/0112/roud-oeuvres-flatlist-hasWritingColor-violet'
    if (writingColor == '6'):
        hasWritingColor_content = 'http://rdfh.ch/lists/0112/roud-oeuvres-flatlist-hasWritingColor-gray'
    if (writingColor == '7'):
        hasWritingColor_content = ''
    
    
    ## -----------------------> hasWritingTool
    writingTool = row[10]
    if (writingTool == '1'):
        hasWritingTool_content = 'http://rdfh.ch/lists/0112/roud-oeuvres-flatlist-hasWritingTool-pencil'
    if (writingTool == '2'):
        hasWritingTool_content = 'http://rdfh.ch/lists/0112/roud-oeuvres-flatlist-hasWritingTool-typingMachine'
    if (writingTool == '3'):
        hasWritingTool_content = 'http://rdfh.ch/lists/0112/roud-oeuvres-flatlist-hasWritingTool-quill'
    if (writingTool == '4'):
        hasWritingTool_content = 'http://rdfh.ch/lists/0112/roud-oeuvres-flatlist-hasWritingTool-ballpointPen'
    if (writingTool == '5'):
        hasWritingTool_content = 'http://rdfh.ch/lists/0112/roud-oeuvres-flatlist-hasWritingTool-feltTip'
    if (writingTool == '6'):
        hasWritingTool_content = 'http://rdfh.ch/lists/0112/roud-oeuvres-flatlist-hasWritingTool-other'
    if (writingTool == '7'):
        hasWritingTool_content = 'http://rdfh.ch/lists/0112/roud-oeuvres-flatlist-hasWritingTool-toBeDetermined'
    if (writingTool == '8'):
        hasWritingTool_content = ''
    
    
    ## -----------------------> isPhotocopy
    if (row[24] == 'oui'):
        isPhotocopy_content = 'true'
    else:
        isPhotocopy_content = 'false'    
        
        
    ## -----------------------> manuscriptHasDateComputable   
    date = row[14]
    if (date != '' and not date.startswith('0000#')): 
        if ('–' in date):   # it is a period
            date12_split = re.split(' – ', date)  ## split in date1 and date2
            date1 = date12_split[0]
            date2 = date12_split[1]
            manuscriptHasDateComputable_content = 'GREGORIAN:'+date1+' CE:'+date2+' CE'
        else:   # no period
            manuscriptHasDateComputable_content = 'GREGORIAN:'+date+' CE'

            
    ## -----------------------> manuscriptHasDateReadable
    if (date != '' and not date.startswith('0000#')): 
        if ('–' in date):   # it is a period
            date1_len = len(date1)
            if (date1_len > 7):
                date1_object = datetime.strptime(date1, '%Y-%m-%d')
                date1_string = date1_object.strftime('<%A, >%-d %B %Y')
            if (date1_len > 5 and date1_len < 8):
                date1_object = datetime.strptime(date1, '%Y-%m')
                date1_string = date1_object.strftime('%B %Y')
            if (date1_len < 5):
                date1_object = datetime.strptime(date1, '%Y')
                date1_string = date1_object.strftime('%Y')
            date2_len = len(date2)
            if (date2_len > 7):
                date2_object = datetime.strptime(date2, '%Y-%m-%d')
                date2_string = date2_object.strftime('<%A, >%-d %B %Y')
            if (date2_len > 5 and date2_len < 8):
                date2_object = datetime.strptime(date2, '%Y-%m')
                date2_string = date2_object.strftime('%B %Y')
            if (date2_len < 5):
                date2_object = datetime.strptime(date2, '%Y')
                date2_string = date2_object.strftime('%Y')
            date_string = date1_string +' - '+date2_string
        else:
            date_len = len(date)
            if (date_len > 7):
                date_object = datetime.strptime(date, '%Y-%m-%d')
                date_string = date_object.strftime('<%A, >%-d %B %Y')
            if (date_len > 5 and date_len < 8):
                date_object = datetime.strptime(date, '%Y-%m')
                date_string = date_object.strftime('%B %Y')
            if (date_len < 5):
                date_object = datetime.strptime(date, '%Y')
                date_string = date_object.strftime('%Y')
        def multipleReplace(text, wordDict):
            for key in wordDict:
                text = text.replace(key, wordDict[key])
            return text
        en_fr_months_days = {'January':'janvier', 'February':'février', 'March':'mars', 'April':'avril', 'May':'mai', 
                             'June':'juin', 'July':'juillet', 'August':'août', 'September':'septembre', 
                             'October':'octobre', 'November':'novembre', 'December':'décembre', 
                             'Monday':'lundi', 'Tuesday':'mardi', 'Wednesday':'mercredi', 'Thursday':'jeudi', 
                             'Friday':'vendredi', 'Saturday':'samedi', 'Sunday':'dimanche', '<':'&#12296;', '>':'&#12297;'}
        date_string_fr = multipleReplace(date_string, en_fr_months_days)
        manuscriptHasDateReadable_content = '<text xmlns="">'+date_string_fr+'</text>'
        # do not delete text, because it is build to work like this
    if (date.startswith('0000#')):   #### certain dates have been marked like this to indicate that they do not have the year therefore cannot be transformed into computable dates
        uncomplete_date = date.split('0000#',1)[1]
        manuscriptHasDateReadable_content = '<text xmlns="">'+uncomplete_date+'</text>'   
        
    ## -----------------------> manuscriptHasDateEstablishedComputable   
    datation = row[15]
    if (datation != ''): 
        if ('–' in datation):   # it is a period
            datation12_split = re.split(' – ', datation) 
            datation1 = datation12_split[0]
            datation2 = datation12_split[1]
            manuscriptHasDateEstablishedComputable_content = 'GREGORIAN:'+datation1+' CE:'+datation2+' CE'
        else:   # no period
            manuscriptHasDateEstablishedComputable_content = 'GREGORIAN:'+datation+' CE'
    
    
    ## -----------------------> manuscriptHasDateEstablishedList
    dateEstablishedList = row[16]
    if (dateEstablishedList != '1'):
        if (dateEstablishedList == '2'):
            manuscriptHasDateEstablishedList_content = 'http://rdfh.ch/lists/0112/roud-oeuvres-flatlist-dateEstablishedList-circa'
        if (dateEstablishedList == '3'):
            manuscriptHasDateEstablishedList_content = 'http://rdfh.ch/lists/0112/roud-oeuvres-flatlist-dateEstablishedList-before'
        if (dateEstablishedList == '4'):
            manuscriptHasDateEstablishedList_content = 'http://rdfh.ch/lists/0112/roud-oeuvres-flatlist-dateEstablishedList-after'
  
            
    ## -----------------------> manuscriptHasDateEstablishedReadable  
    datation = row[15]
    datation_list = row[16]
    datation_comment = row[17]  
    #### include biblio in datation comment
    if ("[Biblio" in datation_comment):
        refbiblioin = re.compile(r'\[(Biblio (\d+))\]')
        datation_comment_link = re.sub(refbiblioin, r'<a class="salsah-link" href="'+"ref:"+r'\1">[\1]</a>', datation_comment)
        datation_comment_linkref = re.sub('ref:Biblio ','ref:biblio_',datation_comment_link)
        datation_comment = datation_comment_linkref
    #### make datation readable (copy code above)
    if (datation != ''): 
        if ('–' in datation):   # it is a period
            datation1_len = len(datation1)
            if (datation1_len > 7):
                datation1_object = datetime.strptime(datation1, '%Y-%m-%d')
                datation1_string = datation1_object.strftime('<%A, >%-d %B %Y')
            if (datation1_len > 5 and datation1_len < 8):
                datation1_object = datetime.strptime(datation1, '%Y-%m')
                datation1_string = datation1_object.strftime('%B %Y')
            if (datation1_len < 5):
                datation1_object = datetime.strptime(datation1, '%Y')
                datation1_string = datation1_object.strftime('%Y')
            datation2_len = len(datation2)
            if (datation2_len > 7):
                datation2_object = datetime.strptime(datation2, '%Y-%m-%d')
                datation2_string = datation2_object.strftime('<%A, >%-d %B %Y')
            if (datation2_len > 5 and datation2_len < 8):
                datation2_object = datetime.strptime(datation2, '%Y-%m')
                datation2_string = datation2_object.strftime('%B %Y')
            if (datation2_len < 5):
                datation2_object = datetime.strptime(datation2, '%Y')
                datation2_string = datation2_object.strftime('%Y')
            datation_string = datation1_string +' - '+datation2_string
        else:
            datation_len = len(datation)
            if (datation_len > 7):
                datation_object = datetime.strptime(datation, '%Y-%m-%d')
                datation_string = datation_object.strftime('<%A, >%-d %B %Y')
            if (datation_len > 5 and datation_len < 8):
                datation_object = datetime.strptime(datation, '%Y-%m')
                datation_string = datation_object.strftime('%B %Y')
            if (datation_len < 5):
                datation_object = datetime.strptime(datation, '%Y')
                datation_string = datation_object.strftime('%Y')
        def multipleReplace(text, wordDict):
            for key in wordDict:
                text = text.replace(key, wordDict[key])
            return text
        en_fr_months_days = {'January':'janvier', 'February':'février', 'March':'mars', 'April':'avril', 'May':'mai', 
                             'June':'juin', 'July':'juillet', 'August':'août', 'September':'septembre', 
                             'October':'octobre', 'November':'novembre', 'December':'décembre', 
                             'Monday':'lundi', 'Tuesday':'mardi', 'Wednesday':'mercredi', 'Thursday':'jeudi', 
                             'Friday':'vendredi', 'Saturday':'samedi', 'Sunday':'dimanche', '<':'&#12296;', '>':'&#12297;'}
        datation_string_fr = multipleReplace(datation_string, en_fr_months_days)  ### datation in readable format
    if (datation != '' and datation_comment != ''):    
        manuscriptHasDateEstablishedReadable_content = '<text xmlns="">'+datation_string_fr+'. '+datation_comment+'</text>'
    if (datation != '' and datation_comment == ''): 
        manuscriptHasDateEstablishedReadable_content = '<text xmlns="">'+datation_string_fr+'</text>'
    if (datation == '' and datation_comment != ''): 
        manuscriptHasDateEstablishedReadable_content = '<text xmlns="">'+datation_comment+'</text>'
    
    
    
    ## -----------------------> manuscriptHasEditorialSet
    editorialSet = row[5]
    if (editorialSet == '1'):
        manuscriptHasEditorialSet_content = 'http://rdfh.ch/lists/0112/roud-oeuvres-flatlist-hasEditorialSet-oeuvrePoetique'
    if (editorialSet == '2'):
        manuscriptHasEditorialSet_content = 'http://rdfh.ch/lists/0112/roud-oeuvres-flatlist-hasEditorialSet-journal'
    if (editorialSet == '3'):
        manuscriptHasEditorialSet_content = 'http://rdfh.ch/lists/0112/roud-oeuvres-flatlist-hasEditorialSet-propos'
    if (editorialSet == '4'):
        manuscriptHasEditorialSet_content = 'http://rdfh.ch/lists/0112/roud-oeuvres-flatlist-hasEditorialSet-traduction'
    if (editorialSet == '5'):
        manuscriptHasEditorialSet_content = 'http://rdfh.ch/lists/0112/roud-oeuvres-flatlist-hasEditorialSet-aDeterminer'
    
    
    ## -----------------------> manuscriptHasInternalComment
    internalComment = row[22]
    if (internalComment != ''):
        if ("[Biblio" in internalComment):
            # add link
            refbiblio = re.compile(r'\[(Biblio (\d+))\]')
            internalComment_link = re.sub(refbiblio, r'<a class="salsah-link" href="'+"ref:"+r'\1">[\1]</a>', internalComment)
            internalComment_linkref = re.sub('ref:Biblio ','ref:biblio_',internalComment_link)
            
            # isolate biblio_id in the comment 
            for biblio_number in re.finditer(refbiblio,internalComment_linkref):
                biblio_number = biblio_number.group(2)
                biblio_id = 'biblio_'+biblio_number
                
                # find corresponding biblio_id in bibliography xml file and build correspoding bibliographic reference
                tree_bibliodata = ET.parse('../INPUT_data/bibliography_id_correspondance.xml')
                root = tree_bibliodata.getroot()
                for publication in root:
                    publication_id = publication.attrib['id']
                    if (biblio_id == publication_id):
                        namespaces = {'p0112-roud-oeuvres': 'http://api.knora.org/ontology/0112/roud-oeuvres/xml-import/v1#'} 
                        # TITLE
                        ref_publicationHasTitle = publication.findall('./p0112-roud-oeuvres:publicationHasTitle', namespaces)[0].text
                        #if len(publicationHasTitle.split()) > 10:  ### it title is too long, take only first 10 words
                             # do something
                        if (publication.tag == "{http://api.knora.org/ontology/0112/roud-oeuvres/xml-import/v1#}PeriodicalArticle" or publication.tag == "{http://api.knora.org/ontology/0112/roud-oeuvres/xml-import/v1#}BookSection"):
                            ref_title = "« "+ref_publicationHasTitle+" »"
                        else:
                            ref_title = "<i>"+ref_publicationHasTitle+"</i>"
                        # AUTHOR    
                        ref_publicationHasAuthor = publication.find('./p0112-roud-oeuvres:publicationHasAuthor', namespaces)
                        # DATE
                        ref_publicationHasDate = publication.find('./p0112-roud-oeuvres:publicationHasDate', namespaces)
                        # BIBLIO = AUTHOR + TITLE + DATE
                        if (ref_publicationHasAuthor is None):
                            if (ref_publicationHasDate is None):
                                biblioInInternalComment = ref_title
                            else:
                                ref_date = publication.findall('./p0112-roud-oeuvres:publicationHasDate', namespaces)[0].text.split("GREGORIAN:")[1].split("-")[0].split(" CE")[0]
                                biblioInInternalComment = ref_title+", "+ref_date
                        else:
                            ref_author = publication.findall('./p0112-roud-oeuvres:publicationHasAuthor', namespaces)[0].findall('./p0112-roud-oeuvres:Author', namespaces)[0].get('target').split("_")[0]
                            if (ref_publicationHasDate is None):
                                biblioInInternalComment = ref_author+", "+ref_title
                            else:
                                ref_date = publication.findall('./p0112-roud-oeuvres:publicationHasDate', namespaces)[0].text.split("GREGORIAN:")[1].split("-")[0].split(" CE")[0]
                                biblioInInternalComment = ref_author+", "+ref_title+", "+ref_date
                # replace [Biblio number] with bibliographic reference
                biblioToBeReplaced = '\[Biblio '+biblio_number+'\]'
                internalComment_linkref = re.sub(biblioToBeReplaced,biblioInInternalComment,internalComment_linkref)
            
            manuscriptHasInternalComment_content = '<text xmlns="">'+internalComment_linkref+'</text>'
        else:
            manuscriptHasInternalComment_content = '<text xmlns="">'+internalComment+'</text>'
            
            
    ## -----------------------> manuscriptHasOldShelfmark
    oldShelfmark = row[3]
    if (oldShelfmark != ''):
        manuscriptHasOldShelfmark_content = '<text xmlns="">'+oldShelfmark+'</text>'
    
    
    ## -----------------------> manuscriptHasPublishedReference
    publishedRef = row[19]
    if (publishedRef != ''):
        publishedRef_content = 'biblio_'+publishedRef
        

    ## -----------------------> manuscriptHasShelfmark
    shelfmark = row[4]
    if (shelfmark != ''):
        manuscriptHasShelfmark_content = '<text xmlns="">'+shelfmark+'</text>'
        
        
    ## -----------------------> manuscriptHasTitle
    title = row[1]
    if (title != ''):
        title = re.sub('<','&#12296;', title)
        title = re.sub('>', '&#12297;', title)
        title = re.sub('&','&amp;', title)
        manuscriptHasTitle_content = '<text xmlns="">'+title+'</text>'
        
        
    ## -----------------------> manuscriptIsDigitized
    if (row[21] == 'oui'):
        manuscriptIsDigitized_content = 'true'
    else:
        manuscriptIsDigitized_content = 'false'  
        
        
    ## -----------------------> manuscriptIsInArchive
    archive = row[2]
    if (archive == '1'):
        manuscriptIsInArchive_content = 'http://rdfh.ch/lists/0112/roud-oeuvres-flatlist-isInArchive-CRLRGR'
        manuscriptIsInArchive4label = "CRLR GR"
    if (archive == '2'):
        manuscriptIsInArchive_content = 'http://rdfh.ch/lists/0112/roud-oeuvres-flatlist-isInArchive-CRLRMermod'
        manuscriptIsInArchive4label = "CRLR Mermod"
    if (archive == '3'):
        manuscriptIsInArchive_content = 'http://rdfh.ch/lists/0112/roud-oeuvres-flatlist-isInArchive-BCUSimond'
        manuscriptIsInArchive4label = "BCU Simond"
    if (archive == '4'):
        manuscriptIsInArchive_content = 'http://rdfh.ch/lists/0112/roud-oeuvres-flatlist-isInArchive-BCUChevalley'
        manuscriptIsInArchive4label = "BCU Chevalley"
    if (archive == '5'):
        manuscriptIsInArchive_content = 'http://rdfh.ch/lists/0112/roud-oeuvres-flatlist-isInArchive-BCUGuildeDuLivre'
        manuscriptIsInArchive4label = "BCU Guilde du livre"
    if (archive == '6'):
        manuscriptIsInArchive_content = 'http://rdfh.ch/lists/0112/roud-oeuvres-flatlist-isInArchive-BCUHutterPerrier'
        manuscriptIsInArchive4label = "BCU Perrier"
    if (archive == '7'):
        manuscriptIsInArchive_content = 'http://rdfh.ch/lists/0112/roud-oeuvres-flatlist-isInArchive-BiblioChauxDeFonds'
        manuscriptIsInArchive4label = "Biblio Chaux-de-fonds"
    if (archive == '8'):
        manuscriptIsInArchive_content = 'http://rdfh.ch/lists/0112/roud-oeuvres-flatlist-isInArchive-CollectionPrivee'
        manuscriptIsInArchive4label = "Collection privée"
    if (archive == '9'):
        manuscriptIsInArchive_content = 'http://rdfh.ch/lists/0112/roud-oeuvres-flatlist-isInArchive-CRLRColomb'
        manuscriptIsInArchive4label = "CRLR Colomb"
    if (archive == '10'):
        manuscriptIsInArchive_content = 'http://rdfh.ch/lists/0112/roud-oeuvres-flatlist-isInArchive-CRLRStevenPaulRobert'
        manuscriptIsInArchive4label = "CRLR Steven PR"
    
    
    ficheLabel = "fiche"+'_'+manuscriptIsInArchive4label+' '+shelfmark+' ___ '+title
    
    
   

    
    
    ###################################
    ## CREATE ELEMENTS AND ATTRIBUTES (AS PREVIOUSLY DEFINED WITH NS) AND ASSIGN THEM CONTENT
    ###################################
    
    
    Manuscript = ET.Element(ManuscriptNS, attrib={'id':ficheid}) 
    
    label = ET.SubElement(Manuscript, labelNS)
    label.text = ficheLabel
    
    
    ## -----------------------------> hasAnnotation
    hasAnnotation = ET.SubElement(Manuscript, hasAnnotationNS, attrib={'knoraType':'boolean_value'})
    hasAnnotation.text = hasAnnotation_content
    
    
    ## -----------------------------> hasDocumentType
    hasDocumentType = ET.SubElement(Manuscript, hasDocumentTypeNS, attrib={'knoraType':'hlist_value'})
    hasDocumentType.text = hasDocumentType_content
    
    
    ## -----------------------------> hasGeneticStage
    if (hasGeneticStage_content == ''):
        pass
    else:
        hasGeneticStage = ET.SubElement(Manuscript, hasGeneticStageNS, attrib={'knoraType':'hlist_value'})
        hasGeneticStage.text = hasGeneticStage_content
        
        
    ## -----------------------------> hasOtherWritingTool
    if (otherWritingTool != ''):
        hasOtherWritingTool = ET.SubElement(Manuscript, hasOtherWritingToolNS, attrib={'knoraType':'richtext_value'})  # , 'mapping_id':'http://rdfh.ch/standoff/mappings/StandardMapping'
        ## take the content of hasOtherWritingTool + entities_declaration and transform it into xml, otherwise is string and Knora consider it as string
        entities_and_hasOtherWritingTool = ET.fromstring(entities_declaration + hasOtherWritingTool_content)
        hasOtherWritingTool.append(entities_and_hasOtherWritingTool)
        
    
    ## -----------------------------> hasPublicComment
    if (publicComment != ''):
        hasPublicComment = ET.SubElement(Manuscript, hasPublicCommentNS, attrib={'knoraType':'richtext_value'})  # , 'mapping_id':'http://rdfh.ch/standoff/mappings/StandardMapping'
        entities_and_hasPublicComment = ET.fromstring(entities_declaration + hasPublicComment_content)
        hasPublicComment.append(entities_and_hasPublicComment)
        
    
    ## -----------------------------> hasSupportInfo
    if (supportInfo != ''):
        hasSupportInfo = ET.SubElement(Manuscript, hasSupportInfoNS, attrib={'knoraType':'richtext_value'})  # , 'mapping_id':'http://rdfh.ch/standoff/mappings/StandardMapping'
        entities_and_hasSupportInfo = ET.fromstring(entities_declaration + hasSupportInfo_content)
        hasSupportInfo.append(entities_and_hasSupportInfo)
        
        
    ## -----------------------------> hasSupportType
    hasSupportType = ET.SubElement(Manuscript, hasSupportTypeNS, attrib={'knoraType':'hlist_value'})
    hasSupportType.text = hasSupportType_content
    
    
    ## -----------------------------> hasTranslatedAuthor
    if (translatedAuthor != '') and (hasTranslatedAuthor_content != ''):
        hasTranslatedAuthor = ET.SubElement(Manuscript, hasTranslatedAuthorNS)
        Author = ET.SubElement(hasTranslatedAuthor, AuthorNS, attrib={'knoraType':'link_value', 'linkType':'ref', 'target':hasTranslatedAuthor_content})
      
    
    ## -----------------------------> hasWritingColor
    if (hasWritingColor_content !=  ''):
        hasWritingColor = ET.SubElement(Manuscript, hasWritingColorNS, attrib={'knoraType':'hlist_value'})
        hasWritingColor.text = hasWritingColor_content
    
    
    ## -----------------------------> hasWritingTool
    if (hasWritingTool_content != ''):
        hasWritingTool = ET.SubElement(Manuscript, hasWritingToolNS, attrib={'knoraType':'hlist_value'})
        hasWritingTool.text = hasWritingTool_content
    
    
    ## -----------------------------> isPhotocopy
    isPhotocopy = ET.SubElement(Manuscript, isPhotocopyNS, attrib={'knoraType':'boolean_value'})
    isPhotocopy.text = isPhotocopy_content
    
    
    ## -----------------------------> manuscriptHasDateComputable
    if (date != '' and not date.startswith('0000#')):
        manuscriptHasDateComputable = ET.SubElement(Manuscript, manuscriptHasDateComputableNS, attrib={'knoraType':'date_value'})
        manuscriptHasDateComputable.text = manuscriptHasDateComputable_content
        
        
    ## -----------------------------> manuscriptHasDateEstablishedComputable
    if (datation != ''):
        manuscriptHasDateEstablishedComputable = ET.SubElement(Manuscript, manuscriptHasDateEstablishedComputableNS, attrib={'knoraType':'date_value'})
        manuscriptHasDateEstablishedComputable.text = manuscriptHasDateEstablishedComputable_content
    
    
    ## -----------------------------> manuscriptHasDateEstablishedList
    if (dateEstablishedList != '1'):
        manuscriptHasDateEstablishedList = ET.SubElement(Manuscript, manuscriptHasDateEstablishedListNS, attrib={'knoraType':'hlist_value'})
        manuscriptHasDateEstablishedList.text = manuscriptHasDateEstablishedList_content
    
    
    ## -----------------------------> manuscriptHasDateEstablishedReadable
    if (datation == '' and datation_comment == ''):
        pass
    else:
        manuscriptHasDateEstablishedReadable = ET.SubElement(Manuscript, manuscriptHasDateEstablishedReadableNS, attrib={'knoraType':'richtext_value'}) # NO MAPPING NEEDED
        entities_and_manuscriptHasDateEstablishedReadable = ET.fromstring(entities_declaration + manuscriptHasDateEstablishedReadable_content)
        manuscriptHasDateEstablishedReadable.append(entities_and_manuscriptHasDateEstablishedReadable)
 

    ## -----------------------------> manuscriptHasDateReadable
    if (date != ''):
        manuscriptHasDateReadable = ET.SubElement(Manuscript, manuscriptHasDateReadableNS, attrib={'knoraType':'richtext_value'})  # NO MAPPING NEEDED
        entities_and_manuscriptHasDateReadable = ET.fromstring(entities_declaration + manuscriptHasDateReadable_content)
        manuscriptHasDateReadable.append(entities_and_manuscriptHasDateReadable)
    
                
    ## -----------------------------> manuscriptHasEditorialSet
    manuscriptHasEditorialSet = ET.SubElement(Manuscript, manuscriptHasEditorialSetNS, attrib={'knoraType':'hlist_value'})
    manuscriptHasEditorialSet.text = manuscriptHasEditorialSet_content
    
    
    ## -----------------------------> manuscriptHasInternalComment
    if (internalComment != ''):
        manuscriptHasInternalComment = ET.SubElement(Manuscript, manuscriptHasInternalCommentNS, attrib={'knoraType':'richtext_value'})  # , 'mapping_id':'http://rdfh.ch/standoff/mappings/StandardMapping'
        entities_and_manuscriptHasInternalComment = ET.fromstring(entities_declaration + manuscriptHasInternalComment_content)
        manuscriptHasInternalComment.append(entities_and_manuscriptHasInternalComment)
    
    ## -----------------------------> manuscriptHasOldShelfmark
    if (oldShelfmark != ''):
        manuscriptHasOldShelfmark = ET.SubElement(Manuscript, manuscriptHasOldShelfmarkNS, attrib={'knoraType':'richtext_value'})  # NO MAPPING NEEDED
        entities_and_manuscriptHasOldShelfmark = ET.fromstring(entities_declaration + manuscriptHasOldShelfmark_content)
        manuscriptHasOldShelfmark.append(entities_and_manuscriptHasOldShelfmark)
     
    
    ## -----------------------------> manuscriptHasPublishedReference
    if (publishedRef != ''):
        manuscriptHasPublishedReference = ET.SubElement(Manuscript, manuscriptHasPublishedReferenceNS)
        Publication = ET.SubElement(manuscriptHasPublishedReference, PublicationNS, attrib={'knoraType':'link_value', 'linkType':'ref', 'target':publishedRef_content})

        
    ## -----------------------------> manuscriptHasShelfmark
    if (shelfmark != ''):
        manuscriptHasShelfmark = ET.SubElement(Manuscript, manuscriptHasShelfmarkNS, attrib={'knoraType':'richtext_value'}) # NO MAPPING NEEDED
        entities_and_manuscriptHasShelfmark = ET.fromstring(entities_declaration + manuscriptHasShelfmark_content)
        manuscriptHasShelfmark.append(entities_and_manuscriptHasShelfmark)
        
        
    ## -----------------------------> manuscriptHasTitle
    if (title != ''):
        manuscriptHasTitle = ET.SubElement(Manuscript, manuscriptHasTitleNS, attrib={'knoraType':'richtext_value'}) # NO MAPPING NEEDED
        entities_and_manuscriptHasTitle = ET.fromstring(entities_declaration + manuscriptHasTitle_content)
        manuscriptHasTitle.append(entities_and_manuscriptHasTitle)
        

    ## -----------------------------> manuscriptIsDigitized
    manuscriptIsDigitized = ET.SubElement(Manuscript, manuscriptIsDigitizedNS, attrib={'knoraType':'boolean_value'})
    manuscriptIsDigitized.text = manuscriptIsDigitized_content

    
    ## -----------------------------> manuscriptIsInArchive
    manuscriptIsInArchive = ET.SubElement(Manuscript, manuscriptIsInArchiveNS, attrib={'knoraType':'hlist_value'})
    manuscriptIsInArchive.text = manuscriptIsInArchive_content

     
    
    
    tree = ET.tostring(Manuscript, encoding="unicode")
    o.write('\n''\n'+ tree)

## WRITE END OF THE XML FILE
with o:  
    o.write('\n'+'</knoraXmlImport:resources>')

o.close


# In[8]:


###
### CREATE XML FOR SCANS
###


from xml.etree import ElementTree as ET
import re, csv
import glob
import os
from os import listdir

mydir = '/mnt/scanlettMounted/GustaveRoud/E_Scan/Scans_import/FondsArchive/'
# /mnt/scanlettMounted/GustaveRoud/E_Scan/Scans_complets/FondsArchive/
o = open('../OUTPUT_xml/images.xml', 'w')



###################################
## WRITE DECLARATIONS AND BEGINNING OF THE XML FILE -adding more line breaks for readibility '+'\n'+' ???-
###################################
o.write('<?xml version="1.0" encoding="UTF-8"?>'+'\n'+'<knoraXmlImport:resources xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://api.knora.org/ontology/knoraXmlImport/v1# ../p0112-roud-oeuvres-xml-schemas/p0112-roud-oeuvres.xsd" xmlns="http://api.knora.org/ontology/0112/roud-oeuvres/xml-import/v1#" xmlns:knoraXmlImport="http://api.knora.org/ontology/knoraXmlImport/v1#" xmlns:p0112-roud-oeuvres="http://api.knora.org/ontology/0112/roud-oeuvres/xml-import/v1#">'+'\n')


    
###################################
#### REGISTERING NAMESPACES
###################################
NS_ROUD = "http://api.knora.org/ontology/0112/roud-oeuvres/xml-import/v1#" 
NS_KNORAIMPORT = "http://api.knora.org/ontology/knoraXmlImport/v1#"
ET.register_namespace("p0112-roud-oeuvres", NS_ROUD)
ET.register_namespace("knoraXmlImport", NS_KNORAIMPORT)


###################################
## DEFINE ELEMENTS WITH NS
###################################
PageNS = ET.QName(NS_ROUD, "Page")
labelNS = ET.QName(NS_KNORAIMPORT, "label")
fileNS = ET.QName(NS_KNORAIMPORT, "file")
hasSeqnumNS = ET.QName(NS_ROUD, "hasSeqnum")
pageHasNameNS = ET.QName(NS_ROUD, "pageHasName")
pageIsPartOfManuscriptNS = ET.QName(NS_ROUD, "pageIsPartOfManuscript")
ManuscriptNS = ET.QName(NS_ROUD, "Manuscript")





###################################
## PREPARE CONTENT OF ELEMENTS AND ATTRIBUTES
###################################



dirs = os.listdir(mydir)
for eachDir in dirs:
    eachPath = mydir+eachDir+'/*.png'  ## attenzione *.tif or *.png
    allTif = glob.glob(eachPath)
    for eachTif in allTif:
        eachTif_splitted = os.path.split(eachTif)
        tifName = eachTif_splitted[1]
        tifHead = eachTif_splitted[0]
        tifCompletePath = eachTif
        
        
        ## -----------------------> Page/@id
        tifId = tifName
    
        ## -----------------------> file/@path
        filePath = tifCompletePath
        
        ## -----------------------> hasSeqnum
        seqnum = tifName.rsplit('_',1)[1].split('.',1)[0]
        
        ## -----------------------> pageHasName
        simpleName = tifName.rsplit('_',1)[0].rsplit('_',1)[1]
        if re.match(r'\d', simpleName):
            completeName = 'f. '+simpleName
        if re.match(r'p', simpleName):
            completeName = 'p. '+simpleName.split('p')[1]
        if re.match(r'annexe', simpleName):
            completeName = 'annexe '+simpleName.split('annexe')[1]
        if re.match(r'couv1', simpleName):
            completeName = 'annexe '+simpleName.split('annexe')[1]
            # TO BE ADDED WHEN COMPLETING IMAGES IMPORT !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            # if starts with couv
            # if starts with doc (a volte ha anche ff., a volte no)
            
        
        ## -----------------------> pageIsPartOfManuscript
        coteComplete = tifHead.rsplit('/',1)[1]
        fonds = coteComplete.rsplit('_',1)[0]  # first part
        fondsReadable = re.sub('_', ' ', fonds)
        cote = coteComplete.rsplit('_',1)[1]   # second part
        ms = cote[:2]
        numb = cote[2:3]
        let = cote[3:4]
        rest = cote[4:]
        coteAsInFiche = ms+' '+numb+' '+let+'/'+rest   # recreate because in naming scans whitespaces and slash have not been used
        
        # csv downloaded from sparql query (query saved in graphdb). First column: iri, second column: cote 
        # attention to delimiter for reading csv
        with open("../INPUT_data/fiche_iri_cote.csv", 'r') as csv_cote_id_correspondance:     
            cote_id_correspondance = csv.reader(csv_cote_id_correspondance, delimiter =',', doublequote=True)
            for row in cote_id_correspondance:
                if (coteAsInFiche == row[1]):
                    ficheTarget = row[0]
        
        #with open("../INPUT_data/fiche_cote-id_correspondance.csv", 'r') as csv_cote_id_correspondance:     # csv created from backup_fiches (with xsl in /transformationScripts) just to take easily the corresponding id for each shelfmark
         #   cote_id_correspondance = csv.reader(csv_cote_id_correspondance, delimiter =';', doublequote=True)
          #  for row in cote_id_correspondance:
           #     if (coteAsInFiche == row[1]):
            #        ficheTarget = row[0]
    

        ## -----------------------> label
        scanLabel = "page_"+fondsReadable+" "+coteAsInFiche+"___"+completeName+"___"+seqnum
        
    
    
        ###################################
        ## CREATE ELEMENTS AND ATTRIBUTES (AS PREVIOUSLY DEFINED WITH NS) AND ASSIGN THEM CONTENT
        ###################################


        Page = ET.Element(PageNS, attrib={'id':tifId}) 
        
        label = ET.SubElement(Page, labelNS)
        label.text = scanLabel
    
        file = ET.SubElement(Page, fileNS, attrib={'path':filePath, 'mimetype':'image/png'})   ## mimetype: png or tiff !!!
        
        hasSeqnum = ET.SubElement(Page, hasSeqnumNS, attrib={'knoraType':'int_value'})
        hasSeqnum.text = seqnum
        
        pageHasName = ET.SubElement(Page, pageHasNameNS, attrib={'knoraType':'richtext_value'})
        pageHasName.text = completeName
        
        pageIsPartOfManuscript = ET.SubElement(Page, pageIsPartOfManuscriptNS)
        Manuscript = ET.SubElement(pageIsPartOfManuscript, ManuscriptNS, attrib={'knoraType':'link_value', 'linkType':'iri', 'target':ficheTarget})

        
        




        tree = ET.tostring(Page, encoding="unicode")
        o.write('\n''\n'+ tree)

## WRITE END OF THE XML FILE
with o:  
    o.write('\n'+'</knoraXmlImport:resources>')

o.close

