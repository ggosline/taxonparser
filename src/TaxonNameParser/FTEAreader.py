import re

from lxml import etree  
from win32com import client 
import win32com
from win32com.client import constants as c

import FTEAParaClassifier, FTEADistClassifier


class wordreader(object):
    """description of class"""
    def __init__(self, filename=None, filepath=None):

        self.wordApp = win32com.client.Dispatch('Word.Application')
        self.wordApp.Visible = True
        if filename:
            self.filename = filename
            try:
                self.doc = self.wordApp.Documents(filename)
            except:
                self.doc = self.wordApp.Documents.Open(filename)
        else:
            self.doc = self.wordApp.Documents.Add()
            self.filename = ""

    def getwords (self):
        return [w.Text for w in self.doc.Words]

def XMLFromRecord(parent, tparsed, tag=None):
    """ parent is parent element in tree; tparsed is a simple string or a list or records (see recordtype.py)
        Create etree element with tag if tag is specified; attach to parent 
        create subelements from list of records; append as children """
    if tparsed:
        
        if type(tparsed).__name__ == "str":
            if tag:
                txel = etree.SubElement(parent, tag)
            else:
                txel = parent
            txel.text = tparsed
        elif type(tparsed).__name__ == "list":
            
            for pmem in tparsed:
                if tag:
                    txel = etree.SubElement(parent, tag)
                else:
                    txel = parent
                txflds = [f for f in pmem if f[1]]
                for fld in txflds:
                    el = etree.SubElement (txel, fld[0])
                    el.text = fld[1]
        else:
            if tag:
                txel = etree.SubElement(parent, tag)
            else:
                txel = parent
            txflds = [f for f in tparsed if f[1]]
            for fld in txflds:
                el = etree.SubElement (txel, fld[0])
                el.text = fld[1]
    return txel

root = etree.Element("Family")
currparent = root
taxonstack = []
taxonNo = 0

# wp = wordreader(r"E:\WTA\FWTA\test.docx")

wp = wordreader(r"T:\Cameroon\FTEA\...docx")

tx = [[p.Range, p.Range.Start, p.Range.End, p.Range.Text, p.Style.NameLocal] for p in wp.doc.Paragraphs if p.Range.Text != '\r']


for t in tx:

    if t[4] in ("Description", "Subspecies Citations", "Genus Heading"):
        tparsed = FTEAParaClassifier.paraDescMatcher.paraParse(t[3], "A")
        if tparsed:
            taxonNo += 1
            if tparsed.rank == "species":
                speciesrec = tparsed
            taxonel = etree.SubElement (currparent, "Taxon")
            taxonstack.append(currparent)
            currentparent = taxonel
            if tparsed.rank in ("variety", "subspecies"):
                # tparsed.parentTaxon = currentparent
                tparsed.genus = speciesrec.genus
                tparsed.species = speciesrec.species
            txel = XMLFromRecord(taxonel, tparsed, "TaxonName")
        else:
            txel = XMLFromRecord(taxonel, t[3], "Description")

    elif t[4] == "keys":

        pass
    elif t[4] in ("Distributions"):
        tparsed = FTEADistClassifier.paraDescMatcher.distMatch(t[3])
        if tparsed:
            if hasattr(tparsed[0], "country"):
                txel = XMLFromRecord(taxonel, tparsed, "distribution")
            else:
                txel = XMLFromRecord(taxonel, tparsed)
    elif t[4] in ("syn"):
        tparsed = FTEAParaClassifier.paraDescMatcher.paraParse(t[3], "S")
        if  tparsed.genus[1:2] == "." and tparsed.genus[0:1] == speciesrec.genus[0:1]:
            tparsed.genus = speciesrec.genus
        if tparsed:
            txel = XMLFromRecord(taxonel, tparsed, "SynonymName")
        else:
            txel = XMLFromRecord(taxonel, "PARSE FAILED: " + t[3], "SynonymName")
    else:
        pass


# print(etree.tostring(root, encoding = str, pretty_print=True))
tree = etree.ElementTree(root)
tree.write(r"T:\Cameroon\FWTA\FTEA\test.xml", encoding="utf-8")
