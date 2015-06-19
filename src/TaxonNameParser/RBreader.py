from lxml import etree

import RBParaClassifier
from   XMLTreeBuilder import XMLFromRecord
import wordreader
import os
import SISDump
import csv

from getBits import *

def red_list_family(faname):

    # global root, currparent, taxonstack, taxonNo, wp, t, paras, indx, p, tname, tparsed, speciesrec, taxonel, currentparent, txel, np
    os.chdir(working_directory)
    root = etree.Element("Family")

    currparent = root
    # taxonstack = []
    taxonNo = 1000
    assessedBy = None
    famassessedBy = None

    wp = wordreader.wordreader("{0}{1}.doc".format(working_directory,faname))

    paras = [t[3] for t in wp.paras]

    if paras[1].startswith("assessed by "):
        famassessedBy = paras[1].split("assessed by ")[1].strip()

    for indx, p in enumerate(paras):

        # start by finding the paragraph with the assessment -- seems to be the most stable!

        if p.startswith(('CR ', 'EN ', 'VU ', 'DD')):

            # paragraph before is the species name; possibly assessed by
            tname = paras[indx - 1]
            tparsed = RBParaClassifier.paraDescMatcher.paraParse(tname, "A")
            if tparsed:

                taxonNo += 1
                #if tparsed.rank == "species":
                #    speciesrec = tparsed
                taxonel = etree.SubElement(currparent, "Taxon")

                XMLFromRecord(taxonel,str(taxonNo),'TaxonID')
                #taxonstack.append(currparent)
                #currentparent = taxonel
                # if tparsed.rank in ("variety", "subspecies"):
                # # tparsed.parentTaxon = currentparent
                #     tparsed.genus = speciesrec.genus
                #     tparsed.species = speciesrec.species
                tparsed.family = faname
                txel = XMLFromRecord(taxonel, tparsed, "TaxonName")
            if " assessed by " in tname:
                assessedBy = tname.split(" assessed by ")[1].strip()
            elif famassessedBy:
                assessedBy = famassessedBy
            else:
                pass

            # current p is the assessment
            if p.startswith('DD'):
                rlcategory = "DD"
                rlcriteria = None
            else:
                rlcategory, rlcriteria = p.split(None ,1)
                rlcriteria = rlcriteria.strip()

            XMLFromRecord(taxonel, assessedBy, "Assessors")
            XMLFromRecord(taxonel, rlcategory, "RLCategory")  # Add the assessment
            XMLFromRecord(taxonel, rlcriteria, "RLCriteria")



            XMLFromRecord(taxonel, 'terrestrial', "System")
            XMLFromRecord(taxonel, 'Afrotropical', "Realm")
            # Now do the rest of the paragraphs until a blank line is found; with luck this is consistent

            for np in paras[indx + 1:]:

                if np == '\r':
                    break

                np = np.strip()

                if np.startswith("Range: "):
                    rangetxt = np.replace("Range: ", "", 1)
                    rttxel = etree.SubElement(taxonel,"Range")
                    XMLFromRecord(rttxel, rangetxt, "RangeText")  # Add the range text
                    XMLFromRecord(rttxel, get_country_names(rangetxt),"Country")
                    if " endemic" in rangetxt:
                        XMLFromRecord(rttxel, "True", "Endemic")

                elif np.startswith("Habitat: "):
                    txel = XMLFromRecord(taxonel, np.replace("Habitat: ", "", 1), "Habitat")  # Add the range
                    XMLFromRecord(taxonel, getElevations(np))

                elif np.startswith("Threats: "):
                    txel = XMLFromRecord(taxonel, np.replace("Threats: ", "", 1), "Threats")

                elif np.startswith("Management suggestions: "):
                    txel = XMLFromRecord(taxonel, np.replace("Management suggestions: ", "", 1), "Management")

                elif any([(teststring in np) for teststring in ("AOO", "EOO", "assessed as", " CR ", " EN ", "occupancy")]):
                    txel = XMLFromRecord(taxonel, np, "Assessment_text")
                    txel = XMLFromRecord(taxonel, getAOOandEOO(np))

                else:
                    txel = XMLFromRecord(taxonel, np, "Description")
    return root


def writeassessments(mytree, csvwriter):
    root = mytree.getroot()
    for taxon in root.findall('.//Taxon'):
        print(taxon.find('TaxonName/family').text, taxon.find('TaxonName/genus').text,
              taxon.find('TaxonName/species').text,
              taxon.find('RLCategory').text, taxon.find('RLCriteria').text)
        csvwriter.writerow([taxon.find('TaxonName/family').text, taxon.find('TaxonName/genus').text,
                            taxon.find('TaxonName/species').text,
                            taxon.find('RLCategory').text, taxon.find('RLCriteria').text])
    pass


def processFamily(faname, csvwriter=None):
    treatment = red_list_family(faname)
    mytree = etree.ElementTree(treatment)
    mytree.write("XML/{0}.xml".format(faname), encoding="utf-8")
    print(fam, ' xml generated')
    # writeassessments(mytree, csvwriter)

    SISDump.SIS_dump(mytree, faname)
    # print(etree.tostring(treatment, encoding = str, pretty_print=True))


working_directory = 'T:\\Cameroon\\GGosline\\Cameroon Red Data Book\\Families\\'
if __name__ == "__main__":

    os.chdir(working_directory)
    # famlist = [os.path.splitext(f)[0] for f in os.listdir() if f.endswith('.doc')]
    famlist = ('GUTTIFERAE',)
    for fam in famlist:
        processFamily(fam)

        # with open('CameroonRDRatings.csv', 'w', encoding='utf-8') as csvf:
        #     csvwriter = csv.writer(csvf)
        #     for fam in famlist:
        #         processFamily(fam, csvwriter)
