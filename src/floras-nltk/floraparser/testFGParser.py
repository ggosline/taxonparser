__author__ = 'Geoge'

import sys

from collections import defaultdict
from floracorpus.reader import AbstractFloraCorpusReader, FloraCorpusReader

from nltk.parse import FeatureEarleyChartParser, FeatureIncrementalBottomUpLeftCornerChartParser, FeatureChartParser
from nltk.parse import FeatureBottomUpChartParser, FeatureBottomUpLeftCornerChartParser
from floraparser.FGParser import FGParser, cleanparsetree
from floraparser.fltoken import FlToken

trec = defaultdict(lambda: None)

description = 'lobes oblong, 2.5–4 mm. long, 2 mm. wide, with an axial  line'

trec['description'] = description
trdr = [trec]
ttaxa = AbstractFloraCorpusReader(reader=trdr)

ttrace = 3
of = sys.stdout
if __name__ == '__main__':
    if False:
        ttrace = 0
        ttaxa = FloraCorpusReader(db=r'..\resources\efloras.db3',
                                  query="Select * from AllTaxa where flora_name = 'FTEA' and rank = 'species' and genus = 'Uncaria' and species = 'africana';", )
        of = open('testphrases.txt', 'w', encoding='utf-8')
    parser = FGParser(parser=FeatureBottomUpLeftCornerChartParser, trace=ttrace)
    for taxon in ttaxa.taxa:
        for sent in taxon.sentences:
            for i, phrase in enumerate(sent.phrases):
                trees = parser.parse(phrase.tokens)
                if trees:
                    print('Success: ' + phrase.text, file=of)
                    print('No. of trees: %d' % len(trees), file=of)
                    if ttrace:
                        for treex in trees:
                            cleanparsetree(treex)
                            treex.draw()
                            print(treex)
                else:
                    print('Fail:    ' + phrase.text, file=of)
                    trees = parser.partialparses()
                    print('No. of trees: %d' % len(trees), file=of)
                    if ttrace:
                        for treex in trees[0:40]:
                            # cleanparsetree(treex)
                            treex.draw()

    of.close()

