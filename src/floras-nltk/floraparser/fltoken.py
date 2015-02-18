__author__ = 'gg12kg'

from floraparser import glossaryreader, pos


class FlToken():

    mybotg = glossaryreader.botglossary()
    fltagger = pos.FlTagger()

    def __init__(self, text : str, taxonno : int , fromc : int = 0, toc : int = 0):
        self._text = text
        self.floraDb = None
        self.taxonNo = taxonno
        self.flDictEntry = None
        self.flPOS = None
        self.fromc = fromc
        self.toc = toc
        self.flRoot, self.flPOS, self.flDictEntry = FlToken.fltagger.tag_word(text)

    def __str__(self):
        return self._text + '<' + self.flPOS + '>'

if __name__ == '__main__':

    tryme = FlToken('glabrous',1,4)
    pass

