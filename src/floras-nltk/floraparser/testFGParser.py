__author__ = 'Geoge'

import sys

from collections import defaultdict
from floracorpus.reader import AbstractFloraCorpusReader, FloraCorpusReader
import FGParser
from nltk.parse import FeatureEarleyChartParser, FeatureIncrementalBottomUpLeftCornerChartParser, FeatureChartParser

trec = defaultdict(lambda: None)

description = 'Fruit orange, ovoid-3-gonous and acute when young, becoming 3-crested, eventually globose, 1·3–3 cm. in diam., smooth or with a few tubercles, 1–3-seeded'

trec['description'] = description
trdr = [trec]
ttaxa = AbstractFloraCorpusReader(reader=trdr)

ttrace = 4
of = sys.stdout
if __name__ == '__main__':
    if False:
        ttrace = 0
        ttaxa = FloraCorpusReader(db=r'..\resources\efloras.db3',
                                  query="Select * from Taxa where genus = 'Salacia' and species = 'erecta';", )
        of = open('testphrases.txt', 'w', encoding='utf-8')
    parser = FGParser.FGParser(parser=FeatureIncrementalBottomUpLeftCornerChartParser, trace=ttrace)
    for taxon in ttaxa.taxa:
        for sent in taxon.sentences:
            for i, phrase in enumerate(sent.phrases):
                trees = parser.parse(tk.lexwords for tk in phrase.tokens)
                if trees:
                    print('Success: ' + phrase.text, file=of)
                    print('No. of trees: %d' % len(trees), file=of)
                    if ttrace:
                        for treex in trees:
                            treex.draw()
                else:
                    print('Fail:    ' + phrase.text, file=of)
                    trees = parser.partialparses()
                    print('No. of trees: %d' % len(trees), file=of)
                    if ttrace:
                        for treex in trees:
                            treex.draw()

    of.close()

