import json
from operator import itemgetter  
import re
import sys

from Microsoft.Office.Interop.Word import *
import SortedCollection
from System import DateTime
import System
import clr


clr.AddReference("Microsoft.Office.Interop.Word")

# import win32com
# from win32com.client import constants as c
# from win32com import client 


class wordreader(object):

    """description of class"""
    def __init__(self, filename=None, filepath=None):
        from System.Runtime.InteropServices import Marshal
        self.wordApp = Marshal.GetActiveObject('Word.Application')
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

wp = wordreader(r"T:\Cameroon\FWTA\FWTAebook\Flora of West Tropical Africa - workng copy.docx")
rng = wp.doc.StoryRanges(1)

keyfind = rng.Find
keyfind.clear

tx = [[p.Range, p.Range.Start, p.Range.End, p.Range.Text, p.Style.NameLocal] for p in wp.doc.Paragraphs if p.Range.Text != '\r' and p.Style.NameLocal[0:7] == "Heading"]
# json.dump([t[1:4] for t in tx])

input = open('headers.txt', 'r')

th = json.load(input)
hdrs = SortedCollection.SortedCollection([[t[0:2], t[2][0:-1]] for t in th], key=itemgetter(0))
hdrs1 = SortedCollection.SortedCollection([[t[0:2], t[2][0:-1]] for t in th if t[3] == "Heading 1"], key=itemgetter(0))
hdrs2 = SortedCollection.SortedCollection([[t[0:2], t[2][0:-1]] for t in th if t[3] == "Heading 2"], key=itemgetter(0))
pass

