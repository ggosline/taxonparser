__author__ = 'gg12kg'

from floracorpus.reader import FloraCorpusReader
from floraparser.fltoken import *
from nltk import ngrams, bigrams, trigrams

from collections import Counter
from pprint import pprint

SQLFlora = "Select * from Taxa where flora_name = '%(flora_name)s' and family = '%(family)s';"


class Parser():
    def __init__(self, flora_name, family):
        self.SQL = SQLFlora % {'flora_name': flora_name, 'family': family}
        self.rdr = FloraCorpusReader(query=self.SQL)
        pass


if __name__ == '__main__':

    tgcounter = Counter()

    ps = Parser('FZ', 'Celastraceae')
    for taxon in ps.rdr.taxa:
        for sentence in taxon.sentences:
            # for tg in trigrams([wd.text for wd in sentence.words]):
            # if not ',' in tg and 'than' in tg:
            # tgcounter[tg] += 1
            for tk in sentence.tokens:
                if tk.flPOS == 'UNK':
                    tgcounter[tk.text] += 1
    pprint(tgcounter.most_common(100))
    pass