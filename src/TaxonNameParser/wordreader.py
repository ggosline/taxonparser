from lxml import etree  
from win32com import client 
import win32com
from win32com.client import constants as c

class wordreader(object):
    """description of class"""

    def __init__(self, filename=None, filepath=None) -> object:
        """
        :rtype : object
        """
        self.wordApp = win32com.client.Dispatch('Word.Application')
        if filename:
            self.filename = filename
            try:
                self.doc = self.wordApp.Documents(filename)
            except:
                self.doc = self.wordApp.Documents.Open(filename)
        else:
            self.doc = self.wordApp.Documents.Add()
            self.filename = ""
        paras = [[p.Range, p.Range.Start, p.Range.End, p.Range.Text, p.Style.NameLocal] for p in self.doc.Paragraphs]

    @property
    def paras(self):
        return [[p.Range, p.Range.Start, p.Range.End, p.Range.Text, p.Style.NameLocal] for p in self.doc.Paragraphs]

    @property
    def words (self):
        return [w.Text for w in self.doc.Words]

if __name__ == "__main__":
    wp = wordreader(r"T:\Cameroon\GGosline\Cameroon Red Data Book\DRACAENACEAE.doc")

    tx = wp.paras
    # taxa = [t for t in tx if t[4] == "accepted_centre"]
    for t in tx:
        if t[4] == "Taxon":
            print(t[3])
    
